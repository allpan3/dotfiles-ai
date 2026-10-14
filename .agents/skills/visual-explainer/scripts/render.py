#!/usr/bin/env python3
"""Render a visual-explainer JSON content spec as one self-contained HTML file

Usage:
    python3 render.py SPEC.json [-o OUTPUT.html] [--check] [--force]

The renderer writes /tmp/YYYY-MM-DD-explanation-<slug>.html by default and
chooses a numbered suffix instead of overwriting an existing file

Spec schema:
{
  "title": "Readable page title",
  "subtitle": "Optional context such as a project or question",
  "slug": "optional-output-slug",
  "sections": [
    {"id": "answer", "heading": "Answer", "html": "<p>Raw HTML...</p>"}
  ],
  "quiz": [
    {
      "question": "Question text",
      "options": [
        {"text": "Answer text", "correct": true, "feedback": "Why"},
        {"text": "Another answer", "correct": false, "feedback": "Why not"}
      ]
    }
  ]
}

Section HTML supports ordinary semantic HTML plus these presentation classes:
  .callout, .callout.warning, .diagram, .flow, .box, .box.fail, .arrow,
  .badge, .badge.new, .badge.changed

Use <pre><code class="language-python">escaped source</code></pre> for code
blocks. The embedded highlighter recognizes common language names and gives
diff blocks semantic line colors. The page has dependency-free light and dark
themes, an accessible persistent toggle, responsive styles, and quiz behavior
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
import random
import re
import tempfile
from pathlib import Path
from typing import Any


THEME_STORAGE_KEY = "visual-explainer-theme"
ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")

CSS = r"""
:root,
html[data-theme="light"] {
  color-scheme: light;
  --bg: #f7f8fc;
  --surface: #ffffff;
  --surface-2: #eef2f8;
  --fg: #172033;
  --muted: #5d687a;
  --accent: #9a3f12;
  --accent-strong: #75300e;
  --accent-soft: #fff0e5;
  --border: #ccd4e0;
  --shadow: 0 12px 30px rgba(28, 39, 58, 0.12);
  --code-bg: #f2f4f8;
  --code-fg: #1f2937;
  --code-border: #c9d1dc;
  --tok-keyword: #7c2d92;
  --tok-string: #0f6b3d;
  --tok-number: #9a3412;
  --tok-comment: #626d80;
  --tok-type: #075985;
  --tok-function: #1d4ed8;
  --tok-property: #8a3b12;
  --tok-operator: #9f1239;
  --tok-literal: #6d28d9;
  --diff-add-bg: #e9f8ef;
  --diff-add-fg: #126b38;
  --diff-del-bg: #ffeded;
  --diff-del-fg: #a11a2a;
  --diff-head-bg: #e8f3ff;
  --diff-head-fg: #135fa7;
  --success-bg: #eaf8ef;
  --success-fg: #17663a;
  --danger-bg: #ffeded;
  --danger-fg: #9a2030;
  --warning-bg: #fff6db;
  --warning-fg: #6f4c00;
}

html[data-theme="dark"] {
  color-scheme: dark;
  --bg: #0d1119;
  --surface: #151b26;
  --surface-2: #1d2533;
  --fg: #e8edf5;
  --muted: #a5b0c0;
  --accent: #ff9f68;
  --accent-strong: #ffc09a;
  --accent-soft: #382317;
  --border: #344052;
  --shadow: 0 14px 34px rgba(0, 0, 0, 0.38);
  --code-bg: #0b1018;
  --code-fg: #dce6f2;
  --code-border: #39475a;
  --tok-keyword: #e39ff6;
  --tok-string: #8fdaa9;
  --tok-number: #ffad7a;
  --tok-comment: #8d9aad;
  --tok-type: #7dd3fc;
  --tok-function: #8ab4ff;
  --tok-property: #ffc078;
  --tok-operator: #ff8dac;
  --tok-literal: #c6a7ff;
  --diff-add-bg: #123322;
  --diff-add-fg: #91e6af;
  --diff-del-bg: #3a1820;
  --diff-del-fg: #ff9cac;
  --diff-head-bg: #142d47;
  --diff-head-fg: #8ecaff;
  --success-bg: #153524;
  --success-fg: #9ae5b6;
  --danger-bg: #3b1820;
  --danger-fg: #ffa1af;
  --warning-bg: #3a3018;
  --warning-fg: #f6d883;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--fg);
  font-family: Georgia, "Times New Roman", serif;
  line-height: 1.68;
}
.page {
  width: min(920px, calc(100% - 2rem));
  margin: 0 auto;
  padding: 3.5rem 0 7rem;
}
h1, h2, h3 { line-height: 1.24; text-wrap: balance; }
h1 {
  margin: 0;
  padding-bottom: .7rem;
  border-bottom: 3px solid var(--accent);
  font-size: clamp(2rem, 5vw, 3.25rem);
}
h2 {
  margin: 3.4rem 0 1rem;
  color: var(--accent-strong);
  font-size: clamp(1.45rem, 3vw, 2rem);
  scroll-margin-top: 1rem;
}
h3 { margin-top: 2rem; font-size: 1.17rem; }
a { color: var(--accent-strong); text-underline-offset: .16em; }
.subtitle { margin: .65rem 0 0; color: var(--muted); font-size: 1.02rem; }
.theme-toggle {
  position: fixed;
  z-index: 20;
  top: 1rem;
  right: 1rem;
  display: inline-flex;
  align-items: center;
  gap: .5rem;
  min-height: 2.65rem;
  padding: .55rem .85rem;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: var(--surface);
  color: var(--fg);
  box-shadow: var(--shadow);
  font: 600 .86rem/1 system-ui, sans-serif;
  cursor: pointer;
}
.theme-toggle:hover { border-color: var(--accent); }
.theme-toggle:focus-visible,
.quiz-option:focus-visible,
summary:focus-visible,
a:focus-visible { outline: 3px solid var(--accent); outline-offset: 3px; }
.toc {
  margin: 2rem 0;
  padding: 1.2rem 1.45rem;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--surface);
  box-shadow: var(--shadow);
}
.toc strong { font-family: system-ui, sans-serif; }
.toc ul { margin: .55rem 0 0; padding-left: 1.3rem; }
.toc li + li { margin-top: .18rem; }
:not(pre) > code {
  padding: .12rem .34rem;
  border: 1px solid var(--code-border);
  border-radius: 4px;
  background: var(--code-bg);
  color: var(--code-fg);
  font: .9em/1.4 ui-monospace, "SFMono-Regular", Consolas, monospace;
}
pre {
  margin: 1.35rem 0;
  padding: 1.1rem 1.25rem;
  overflow-x: auto;
  border: 1px solid var(--code-border);
  border-radius: 10px;
  background: var(--code-bg);
  color: var(--code-fg);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .04);
  white-space: pre;
  tab-size: 2;
  font: .87rem/1.58 ui-monospace, "SFMono-Regular", Consolas, monospace;
}
pre code { display: block; min-width: max-content; color: inherit; font: inherit; }
.tok-keyword { color: var(--tok-keyword); font-weight: 650; }
.tok-string { color: var(--tok-string); }
.tok-number { color: var(--tok-number); }
.tok-comment { color: var(--tok-comment); font-style: italic; }
.tok-type { color: var(--tok-type); }
.tok-function { color: var(--tok-function); }
.tok-property { color: var(--tok-property); }
.tok-operator { color: var(--tok-operator); }
.tok-literal { color: var(--tok-literal); font-weight: 600; }
.tok-punctuation { color: var(--muted); }
.diff-line { display: inline-block; width: 100%; min-width: max-content; padding: 0 .3rem; }
.diff-add { background: var(--diff-add-bg); color: var(--diff-add-fg); }
.diff-del { background: var(--diff-del-bg); color: var(--diff-del-fg); }
.diff-head { background: var(--diff-head-bg); color: var(--diff-head-fg); font-weight: 650; }
.callout {
  margin: 1.4rem 0;
  padding: 1rem 1.2rem;
  border-left: 4px solid var(--accent);
  border-radius: 0 8px 8px 0;
  background: var(--accent-soft);
}
.callout.warning { border-color: var(--warning-fg); background: var(--warning-bg); color: var(--warning-fg); }
.diagram {
  margin: 1.4rem 0;
  padding: 1.25rem;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--surface);
  box-shadow: var(--shadow);
  font-family: system-ui, sans-serif;
}
.flow { display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: .75rem; }
.box {
  min-width: 130px;
  padding: .68rem 1rem;
  border: 2px solid var(--accent);
  border-radius: 9px;
  background: var(--accent-soft);
  text-align: center;
}
.box.fail { border-color: var(--danger-fg); background: var(--danger-bg); color: var(--danger-fg); }
.arrow { color: var(--muted); font-size: 1.45rem; }
details {
  margin: 1.2rem 0;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: var(--surface);
}
summary { padding: .7rem 1rem; cursor: pointer; font: 600 .95rem/1.45 system-ui, sans-serif; }
details[open] > summary { border-bottom: 1px solid var(--border); }
details > :not(summary) { margin-inline: 1rem; }
table { width: 100%; margin: 1.3rem 0; border-collapse: collapse; font-size: .93rem; }
th, td { padding: .62rem .75rem; border: 1px solid var(--border); text-align: left; vertical-align: top; }
th { background: var(--surface-2); font-family: system-ui, sans-serif; }
.badge {
  display: inline-block;
  padding: .16rem .52rem;
  border-radius: 999px;
  background: var(--surface-2);
  color: var(--fg);
  font: 700 .72rem/1.45 system-ui, sans-serif;
}
.badge.new { background: var(--success-bg); color: var(--success-fg); }
.badge.changed { background: var(--warning-bg); color: var(--warning-fg); }
.quiz-card {
  margin: 1.25rem 0;
  padding: 1.25rem 1.4rem;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--surface);
  box-shadow: var(--shadow);
}
.quiz-question { margin-top: 0; }
.quiz-option {
  display: block;
  width: 100%;
  margin: .5rem 0;
  padding: .72rem .9rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--surface-2);
  color: var(--fg);
  text-align: left;
  font: .95rem/1.45 system-ui, sans-serif;
  cursor: pointer;
}
.quiz-option:hover { border-color: var(--accent); }
.quiz-option[aria-pressed="true"][data-correct="true"] { border-color: var(--success-fg); background: var(--success-bg); }
.quiz-option[aria-pressed="true"][data-correct="false"] { border-color: var(--danger-fg); background: var(--danger-bg); }
.feedback { display: none; margin-top: .7rem; padding: .7rem .9rem; border-radius: 8px; font: .9rem/1.5 system-ui, sans-serif; }
.feedback.correct { display: block; background: var(--success-bg); color: var(--success-fg); }
.feedback.incorrect { display: block; background: var(--danger-bg); color: var(--danger-fg); }
.footer { margin-top: 4rem; padding-top: 1.2rem; border-top: 1px solid var(--border); color: var(--muted); font-size: .85rem; }
@media (max-width: 680px) {
  .page { width: min(100% - 1.25rem, 920px); padding-top: 4.5rem; }
  .theme-toggle { top: .65rem; right: .65rem; }
  .flow { flex-direction: column; }
  .arrow { transform: rotate(90deg); }
  table { display: block; overflow-x: auto; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
}
"""

THEME_BOOTSTRAP_JS = rf"""
(() => {{
  const key = {json.dumps(THEME_STORAGE_KEY)};
  let saved = null;
  try {{ saved = localStorage.getItem(key); }} catch (_) {{}}
  const systemDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = saved === 'light' || saved === 'dark' ? saved : (systemDark ? 'dark' : 'light');
  document.documentElement.dataset.theme = theme;
  document.documentElement.style.colorScheme = theme;
}})();
"""

INTERACTION_JS = rf"""
(() => {{
  'use strict';

  const root = document.documentElement;
  const toggle = document.getElementById('theme-toggle');
  const toggleLabel = document.getElementById('theme-label');
  const themeMeta = document.getElementById('theme-color');
  const themeKey = {json.dumps(THEME_STORAGE_KEY)};
  const media = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

  const storedTheme = () => {{
    try {{ return localStorage.getItem(themeKey); }} catch (_) {{ return null; }}
  }};

  const saveTheme = theme => {{
    try {{ localStorage.setItem(themeKey, theme); }} catch (_) {{}}
  }};

  const updateThemeControls = theme => {{
    const dark = theme === 'dark';
    toggle.setAttribute('aria-label', dark ? 'Switch to light appearance' : 'Switch to dark appearance');
    toggleLabel.textContent = dark ? 'Light' : 'Dark';
    const background = getComputedStyle(root).getPropertyValue('--bg').trim();
    if (background) themeMeta.setAttribute('content', background);
  }};

  const applyTheme = (theme, persist) => {{
    root.dataset.theme = theme;
    root.style.colorScheme = theme;
    if (persist) saveTheme(theme);
    updateThemeControls(theme);
  }};

  updateThemeControls(root.dataset.theme || 'light');
  toggle.addEventListener('click', () => {{
    applyTheme(root.dataset.theme === 'dark' ? 'light' : 'dark', true);
  }});

  if (media && typeof media.addEventListener === 'function') {{
    media.addEventListener('change', event => {{
      if (!storedTheme()) applyTheme(event.matches ? 'dark' : 'light', false);
    }});
  }}

  const keywordSets = {{
    python: 'and as assert async await break class continue def del elif else except False finally for from global if import in is lambda None nonlocal not or pass raise return True try while with yield match case'.split(' '),
    javascript: 'async await break case catch class const continue debugger default delete do else export extends finally for from function get if import in instanceof let new of return set static super switch this throw try typeof var void while with yield'.split(' '),
    typescript: 'abstract any as asserts async await bigint boolean break case catch class const constructor continue declare default delete do else enum export extends finally for from function get if implements import in infer instanceof interface is keyof let module namespace never new number object of override private protected public readonly require return set static string super switch symbol this throw try type typeof undefined unique unknown var void while with yield'.split(' '),
    shell: 'case do done elif else esac export fi for function if in local readonly return select then time until while'.split(' '),
    sql: 'add all alter and as asc begin between by case check column commit constraint create database default delete desc distinct drop else end exists foreign from full grant group having in index inner insert into is join key left like limit not null on or order outer primary references right rollback select set table then union unique update values view when where'.split(' '),
    rust: 'as async await break const continue crate dyn else enum extern false fn for if impl in let loop match mod move mut pub ref return self Self static struct super trait true type unsafe use where while'.split(' '),
    go: 'break case chan const continue default defer else fallthrough for func go goto if import interface map package range return select struct switch type var'.split(' '),
    java: 'abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while'.split(' '),
    c: 'auto break case char const continue default do double else enum extern float for goto if inline int long register restrict return short signed sizeof static struct switch typedef union unsigned void volatile while'.split(' '),
    cpp: 'alignas alignof and asm auto bitand bitor bool break case catch char class compl concept const consteval constexpr constinit const_cast continue co_await co_return co_yield decltype default delete do double dynamic_cast else enum explicit export extern false float for friend goto if inline int long mutable namespace new noexcept not nullptr operator or private protected public register reinterpret_cast requires return short signed sizeof static static_assert static_cast struct switch template this thread_local throw true try typedef typeid typename union unsigned using virtual void volatile wchar_t while xor'.split(' '),
    css: 'important inherit initial revert unset'.split(' '),
  }};
  const literals = new Set('true false null none undefined nan infinity yes no'.split(' '));
  const aliases = {{
    js: 'javascript', jsx: 'javascript', mjs: 'javascript', cjs: 'javascript',
    ts: 'typescript', tsx: 'typescript', py: 'python', bash: 'shell', sh: 'shell',
    zsh: 'shell', yml: 'yaml', html: 'markup', xml: 'markup', htm: 'markup',
    cs: 'c', csharp: 'c', h: 'c', cc: 'cpp', cxx: 'cpp',
  }};

  const appendToken = (fragment, text, className) => {{
    if (!text) return;
    if (!className) {{
      fragment.append(document.createTextNode(text));
      return;
    }}
    const span = document.createElement('span');
    span.className = className;
    span.textContent = text;
    fragment.append(span);
  }};

  const languageFor = code => {{
    const className = Array.from(code.classList).find(name => name.startsWith('language-'));
    const raw = className ? className.slice('language-'.length).toLowerCase() : 'text';
    return aliases[raw] || raw;
  }};

  const nextNonSpace = (source, index) => {{
    while (index < source.length && /\s/.test(source[index])) index += 1;
    return source[index] || '';
  }};

  const previousNonSpace = (source, index) => {{
    index -= 1;
    while (index >= 0 && /\s/.test(source[index])) index -= 1;
    return source[index] || '';
  }};

  const quotedEnd = (source, start, delimiter) => {{
    let index = start + delimiter.length;
    while (index < source.length) {{
      if (source[index] === '\\') {{ index += 2; continue; }}
      if (source.startsWith(delimiter, index)) return index + delimiter.length;
      index += 1;
    }}
    return source.length;
  }};

  const commentMarkers = language => {{
    if (['python', 'shell', 'yaml', 'ruby', 'toml'].includes(language)) return ['#'];
    if (language === 'sql') return ['--'];
    return ['//'];
  }};

  const highlightDiff = (code, source) => {{
    const fragment = document.createDocumentFragment();
    const lines = source.split('\n');
    lines.forEach((line, index) => {{
      const span = document.createElement('span');
      span.className = 'diff-line';
      if (/^(diff |index |@@|--- |\+\+\+ )/.test(line)) span.classList.add('diff-head');
      else if (line.startsWith('+')) span.classList.add('diff-add');
      else if (line.startsWith('-')) span.classList.add('diff-del');
      span.textContent = line;
      fragment.append(span);
      if (index < lines.length - 1) fragment.append(document.createTextNode('\n'));
    }});
    code.replaceChildren(fragment);
  }};

  const highlightCode = code => {{
    if (code.dataset.highlighted === 'true') return;
    const source = code.textContent || '';
    const language = languageFor(code);
    code.dataset.highlighted = 'true';
    if (language === 'diff' || language === 'patch') {{
      highlightDiff(code, source);
      return;
    }}
    if (['text', 'plaintext', 'none'].includes(language)) return;

    const keywordList = keywordSets[language] || (language === 'json' ? [] : null);
    if (!keywordList) return;
    const keywords = new Set(keywordList);
    const fragment = document.createDocumentFragment();
    let index = 0;
    while (index < source.length) {{
      const ch = source[index];

      if (/\s/.test(ch)) {{
        let end = index + 1;
        while (end < source.length && /\s/.test(source[end])) end += 1;
        appendToken(fragment, source.slice(index, end), '');
        index = end;
        continue;
      }}

      if (source.startsWith('<!--', index)) {{
        const close = source.indexOf('-->', index + 4);
        const end = close === -1 ? source.length : close + 3;
        appendToken(fragment, source.slice(index, end), 'tok-comment');
        index = end;
        continue;
      }}

      if (source.startsWith('/*', index)) {{
        const close = source.indexOf('*/', index + 2);
        const end = close === -1 ? source.length : close + 2;
        appendToken(fragment, source.slice(index, end), 'tok-comment');
        index = end;
        continue;
      }}

      const marker = commentMarkers(language).find(item => source.startsWith(item, index));
      if (marker) {{
        const close = source.indexOf('\n', index + marker.length);
        const end = close === -1 ? source.length : close;
        appendToken(fragment, source.slice(index, end), 'tok-comment');
        index = end;
        continue;
      }}

      const triple = language === 'python' && (source.startsWith("'''", index) || source.startsWith('\x22\x22\x22', index));
      if (triple || ch === "'" || ch === '"' || ch === '`') {{
        const delimiter = triple ? source.slice(index, index + 3) : ch;
        const end = quotedEnd(source, index, delimiter);
        const className = nextNonSpace(source, end) === ':' ? 'tok-property' : 'tok-string';
        appendToken(fragment, source.slice(index, end), className);
        index = end;
        continue;
      }}

      const number = source.slice(index).match(/^(?:0[xX][0-9a-fA-F]+|0[bB][01]+|\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)/);
      if (number) {{
        appendToken(fragment, number[0], 'tok-number');
        index += number[0].length;
        continue;
      }}

      const identifier = source.slice(index).match(/^[A-Za-z_$][\w$-]*/);
      if (identifier) {{
        const word = identifier[0];
        const lower = word.toLowerCase();
        const after = nextNonSpace(source, index + word.length);
        const before = previousNonSpace(source, index);
        let className = '';
        if (keywords.has(word) || keywords.has(lower)) className = 'tok-keyword';
        else if (literals.has(lower)) className = 'tok-literal';
        else if (before === '.' || after === ':') className = 'tok-property';
        else if (after === '(') className = 'tok-function';
        else if (/^[A-Z]/.test(word)) className = 'tok-type';
        appendToken(fragment, word, className);
        index += word.length;
        continue;
      }}

      const operator = source.slice(index).match(/^(?:===|!==|=>|==|!=|<=|>=|&&|\|\||\+\+|--|::|->|\?\?|\?\.|[+\-*\/%=&|!<>?:~^]+)/);
      if (operator) {{
        appendToken(fragment, operator[0], 'tok-operator');
        index += operator[0].length;
        continue;
      }}

      appendToken(fragment, ch, /[()[\]{{}},.;]/.test(ch) ? 'tok-punctuation' : '');
      index += 1;
    }}
    code.replaceChildren(fragment);
  }};

  document.querySelectorAll('pre code').forEach(highlightCode);

  document.querySelectorAll('.quiz-card').forEach(card => {{
    const feedback = card.querySelector('.feedback');
    card.querySelectorAll('.quiz-option').forEach(option => {{
      option.addEventListener('click', () => {{
        card.querySelectorAll('.quiz-option').forEach(item => item.setAttribute('aria-pressed', 'false'));
        option.setAttribute('aria-pressed', 'true');
        const correct = option.dataset.correct === 'true';
        feedback.className = 'feedback ' + (correct ? 'correct' : 'incorrect');
        feedback.textContent = (correct ? 'Correct — ' : 'Not quite — ') + option.dataset.feedback;
      }});
    }});
  }});
}})();
"""


# Report malformed renderer specifications
class SpecError(ValueError):
    """Raised when a content spec is incomplete or malformed"""


# Convert arbitrary text into a safe filename slug
def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "explanation"


# Require a non-empty string field from a mapping
def required_text(mapping: dict[str, Any], key: str, context: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SpecError(f"{context}.{key} must be a non-empty string")
    return value


# Validate and normalize the renderer content spec
def validate_spec(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise SpecError("spec must be a JSON object")

    title = required_text(raw, "title", "spec")
    subtitle = raw.get("subtitle", "")
    if not isinstance(subtitle, str):
        raise SpecError("spec.subtitle must be a string")

    slug_value = raw.get("slug", "")
    if slug_value is not None and not isinstance(slug_value, str):
        raise SpecError("spec.slug must be a string")
    slug = slugify(slug_value or title)

    sections_raw = raw.get("sections")
    if not isinstance(sections_raw, list) or not sections_raw:
        raise SpecError("spec.sections must be a non-empty array")

    sections: list[dict[str, str]] = []
    section_ids: set[str] = set()
    for index, section in enumerate(sections_raw):
        context = f"spec.sections[{index}]"
        if not isinstance(section, dict):
            raise SpecError(f"{context} must be an object")
        section_id = required_text(section, "id", context)
        if not ID_PATTERN.fullmatch(section_id):
            raise SpecError(f"{context}.id must match {ID_PATTERN.pattern}")
        if section_id in section_ids or section_id == "quiz":
            raise SpecError(f"{context}.id must be unique and cannot be 'quiz'")
        section_ids.add(section_id)
        sections.append(
            {
                "id": section_id,
                "heading": required_text(section, "heading", context),
                "html": required_text(section, "html", context),
            }
        )

    quiz_raw = raw.get("quiz", [])
    if not isinstance(quiz_raw, list):
        raise SpecError("spec.quiz must be an array")

    quiz: list[dict[str, Any]] = []
    for question_index, question in enumerate(quiz_raw):
        context = f"spec.quiz[{question_index}]"
        if not isinstance(question, dict):
            raise SpecError(f"{context} must be an object")
        question_text = required_text(question, "question", context)
        options_raw = question.get("options")
        if not isinstance(options_raw, list) or len(options_raw) < 2:
            raise SpecError(f"{context}.options must contain at least two options")

        options: list[dict[str, Any]] = []
        correct_count = 0
        for option_index, option in enumerate(options_raw):
            option_context = f"{context}.options[{option_index}]"
            if not isinstance(option, dict):
                raise SpecError(f"{option_context} must be an object")
            correct = option.get("correct")
            if not isinstance(correct, bool):
                raise SpecError(f"{option_context}.correct must be true or false")
            correct_count += int(correct)
            feedback = option.get("feedback", "Review the explanation above")
            if not isinstance(feedback, str) or not feedback.strip():
                raise SpecError(f"{option_context}.feedback must be a non-empty string")
            options.append(
                {
                    "text": required_text(option, "text", option_context),
                    "correct": correct,
                    "feedback": feedback,
                }
            )
        if correct_count != 1:
            raise SpecError(f"{context} must contain exactly one correct option")
        quiz.append({"question": question_text, "options": options})

    return {
        "title": title,
        "subtitle": subtitle,
        "slug": slug,
        "sections": sections,
        "quiz": quiz,
    }


# Shuffle answer positions reproducibly from the question text
def ordered_options(question: str, options: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = list(options)
    seed = int.from_bytes(hashlib.sha256(question.encode("utf-8")).digest()[:8], "big")
    random.Random(seed).shuffle(result)
    return result


# Render one quiz question with escaped text and accessible controls
def render_quiz_card(question: dict[str, Any], index: int) -> str:
    option_html = []
    for option in ordered_options(question["question"], question["options"]):
        option_html.append(
            '<button class="quiz-option" type="button" aria-pressed="false" '
            f'data-correct="{str(option["correct"]).lower()}" '
            f'data-feedback="{html.escape(option["feedback"], quote=True)}">'
            f'{html.escape(option["text"])}</button>'
        )
    return (
        '<div class="quiz-card">\n'
        f'<p class="quiz-question"><strong>{index}. {html.escape(question["question"])}</strong></p>\n'
        + "\n".join(option_html)
        + '\n<div class="feedback" role="status" aria-live="polite"></div>\n</div>'
    )


# Render the complete self-contained page
def render_page(spec: dict[str, Any]) -> str:
    toc = [
        f'<li><a href="#{html.escape(section["id"], quote=True)}-heading">{html.escape(section["heading"])}</a></li>'
        for section in spec["sections"]
    ]
    if spec["quiz"]:
        toc.append('<li><a href="#quiz-heading">Quiz</a></li>')
    # Short pages skip the contents box so the answer stays near the top
    toc_html = (
        '<nav class="toc" aria-label="Table of contents">\n<strong>Contents</strong>\n<ul>\n'
        + "".join(toc)
        + "\n</ul>\n</nav>"
        if len(toc) >= 3
        else ""
    )

    sections = "\n\n".join(
        f'<section aria-labelledby="{html.escape(section["id"], quote=True)}-heading">\n'
        f'<h2 id="{html.escape(section["id"], quote=True)}-heading">{html.escape(section["heading"])}</h2>\n'
        f'{section["html"]}\n</section>'
        for section in spec["sections"]
    )

    quiz = ""
    if spec["quiz"]:
        cards = "\n\n".join(
            render_quiz_card(question, index)
            for index, question in enumerate(spec["quiz"], start=1)
        )
        quiz = f'<section aria-labelledby="quiz-heading">\n<h2 id="quiz-heading">Quiz</h2>\n{cards}\n</section>'

    subtitle = (
        f'<p class="subtitle">{html.escape(spec["subtitle"])}</p>'
        if spec["subtitle"]
        else ""
    )
    generated = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" id="theme-color" content="#f7f8fc">
<title>{html.escape(spec["title"])}</title>
<script>{THEME_BOOTSTRAP_JS}</script>
<style>{CSS}</style>
</head>
<body>
<button class="theme-toggle" id="theme-toggle" type="button" aria-label="Switch to dark appearance">
  <span aria-hidden="true">◐</span><span id="theme-label">Dark</span>
</button>
<main class="page">
<header>
<h1>{html.escape(spec["title"])}</h1>
{subtitle}
</header>
{toc_html}
{sections}
{quiz}
<footer class="footer">Generated {html.escape(generated)}</footer>
</main>
<script>{INTERACTION_JS}</script>
</body>
</html>
"""


# Choose a non-clobbering filename when no explicit output is requested
def default_output_path(slug: str) -> Path:
    date_prefix = dt.date.today().isoformat()
    base = Path("/tmp") / f"{date_prefix}-explanation-{slug}.html"
    if not base.exists():
        return base
    for suffix in range(2, 1000):
        candidate = base.with_name(f"{base.stem}-{suffix}{base.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError("unable to choose an unused output filename")


# Write the page atomically after enforcing overwrite policy
def write_output(path: Path, content: str, force: bool) -> None:
    if path.suffix.lower() != ".html":
        raise ValueError("output path must end in .html")
    if path.exists() and not force:
        raise FileExistsError(f"output already exists: {path} (use --force to replace it)")
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        handle.write(content)
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


# Parse arguments, validate the spec, and render the requested output
def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("spec", type=Path, help="JSON content spec")
    parser.add_argument("-o", "--output", type=Path, help="explicit output HTML path")
    parser.add_argument("--check", action="store_true", help="validate the spec without rendering")
    parser.add_argument("--force", action="store_true", help="replace an existing explicit output")
    args = parser.parse_args()

    try:
        raw = json.loads(args.spec.read_text(encoding="utf-8"))
        spec = validate_spec(raw)
        if args.check:
            print("Spec valid")
            return 0
        output = args.output.expanduser() if args.output else default_output_path(spec["slug"])
        write_output(output, render_page(spec), args.force)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))

    print(output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
