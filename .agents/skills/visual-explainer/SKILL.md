---
name: visual-explainer
description: Build or update an HTML explanation page with diagrams, code views, and collapsible background. Use when the user asks for a page, explainer, walkthrough, or visual explanation, or when a process, system, comparison, or code change needs a diagram or layered background that chat cannot show well. Not for a single diagram or table that fits in the reply.
---

# Visual explainer

Build one HTML page that lets the reader understand the topic and decide quickly. Keep the short
answer, its reason, and any decision in chat; put the detail on the page.

## Content

- Put the result, any decision or next action, material risks, and unresolved requirements first.
  Do not put them in collapsed sections.
- Organize the sections around the user's question. There is no fixed section sequence.
- Put optional background in native `<details><summary>…</summary>…</details>` blocks. Keep a brief
  definition in the main text when the conclusion depends on it. Write only background that is
  relevant to the current question.
- Use a diagram for a relationship or flow. Add a control only when changing a value, step, or
  option shows behavior. Use text or a table when it is sufficient.
- For a code change, link the relevant files or commits and read enough source to explain the
  behavior. Do not give a general repository tour.
- Avoid decorative animation and a figure for every fact.
- Add a quiz only when the user asks for one.

## Location and format

- Keep one page per topic. On follow-up, update the relevant section and keep the path and anchors
  stable.
- Save the page where the user or the project instructions say. Otherwise, use the session's
  scratch directory if the client names one; if not, omit `-o` and the renderer writes a new file
  under `/tmp`. Keep review pages outside production documentation unless the user asks to include
  them.
- Make each explanation in one format. If the user asks for a native page, such as a Claude
  artifact or a ChatGPT Page, and that tool accepts an HTML file, publish the rendered file with
  it. Do not make a second page with the same content. Local file links do not work on a published
  page; link files and commits by web URL.

## Render

Run the renderer by its full path, `python3 <skill-dir>/scripts/render.py`, where `<skill-dir>` is
the directory that contains this `SKILL.md`. A path relative to the project directory does not work.

1. Run `python3 <skill-dir>/scripts/render.py --help` when you need the JSON schema or the
   presentation classes.
2. Write the JSON spec. Put escaped source in `<pre><code class="language-…">`. For a diagram, use
   the renderer classes (`.diagram`, `.flow`, `.box`, `.arrow`) or inline SVG that uses
   `currentColor` or page variables such as `var(--accent)`. The page loads no external scripts,
   so Mermaid and chart-library code do not render.
3. Render with `python3 <skill-dir>/scripts/render.py <spec.json> -o <page.html>`. To update this
   task's page, use the same path with `--force`, and keep the spec beside the page.
4. If a browser tool can open the page, check the new or changed sections at a narrow width. Check
   keyboard operation only for custom controls that you added.

Reply with the short answer and the page's absolute path or link. State any check that you could
not do.
