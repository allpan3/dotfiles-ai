# Shared AI Setup

Maintain plain skills here and run `~/.agents/setup-agents.sh` to make them available to Claude Code and
Codex. No plugin installation is needed.

## Layout

- `skills/` contains general skills for regular and T3 sessions.
- `t3/skills/` contains T3-only skills.
- `t3/models.md` assigns models to T3 roles, including the review panel.
- `setup-agents.sh` creates T3 homes and links skills and shared instructions.

Skills can be grouped in nested folders. Each skill folder must have a unique name across both
collections. Keep its scripts, references, license, and agent metadata beside `SKILL.md`. Do not
nest one skill inside another. The linker skips hidden folders, directory symlinks, and
`node_modules`.

## Install and update

The `ai` vcsh repository owns the active skills, shared instructions, Claude settings, and
instruction links in your home directory. The myrepos `ai` entry clones it alongside the other
dotfiles and runs `~/.agents/setup-agents.sh` after cloning or a successful update. No separate
development checkout is needed.

```sh
mr -d "$HOME/.config/vcsh/repo.d/ai.git" update
```

Edit files directly under `~/.agents`. Run `~/.agents/setup-agents.sh` after adding, removing, renaming,
or regrouping skills. Use `vcsh ai -C "$HOME"` for Git commands and stage explicit paths. Keep
credentials, Codex configuration, T3 settings, caches, and generated skill links untracked.

| Location               | Skills                                                 |
| ---------------------- | ------------------------------------------------------ |
| `~/.agents/skills/`    | General source files, read directly by all Codex homes |
| `~/.claude/skills/`    | General skills                                         |
| `~/.claude-t3/skills/` | General and T3-only skills        |
| `~/.codex-t3/skills/`  | T3-only skills                    |

T3 Codex also reads the general skills in `~/.agents/skills`, so the linker does not duplicate them
in `~/.codex-t3/skills`. Regular Codex gets no T3-only links. Configure T3's Claude home as
`~/.claude-t3` and T3's Codex home as `~/.codex-t3`.

Setup creates both T3 homes and their skills directories. It links:

- `~/.claude-t3/CLAUDE.md` and `~/.codex-t3/AGENTS.md` to `~/.agents/AGENTS.md`.
- `~/.claude-t3/settings.json` to `~/.claude/settings.json`.

Claude settings are shared, so changes through either home affect both.
Skills are discovered separately through the skill directories. Plugin
registrations are shared through settings, but plugin installation files and
caches remain specific to each home. Setup does not install plugins.

Existing files and links to other targets are preserved with a yellow warning
on stderr. A missing source or failed link also produces a warning. Setup
attempts the remaining links, then exits with an error. Correct links remain
silent. T3 application settings, Codex configuration, credentials, and runtime
state remain unchanged. Shared instructions and portable Claude settings are
tracked by `ai`.

Repeated runs leave correct links untouched. It replaces files, folders, or links whose names match
maintained skills. It removes stale links pointing into the two source collections under `~/.agents`
and preserves unrelated entries, including downloaded skills. It rejects duplicate names, shared regular/T3 homes, and
overlapping destinations before replacing links. If one destination fails, it attempts the others
and exits with an error.

Existing links expose content edits immediately. A running agent session may need its skills
reloaded or its session restarted.

## Invocation

| Skill               | Invocation            |
| ------------------- | --------------------- |
| `unslop`            | Automatic or explicit |
| `visual-explainer`  | Automatic or explicit |
| `reviewable-coding` | Explicit only         |
| `interrogate` | Explicit only, in T3 |
| `how` | Explicit only, in T3 |
| `why` | Explicit only, in T3 |

Use `/unslop` in Claude or `$unslop` in Codex, and similarly for the other names. Automatic use
depends on the task matching the skill's description. T3-only skills must check for the required T3
tools before performing orchestration.

Invoke `interrogate` explicitly with `/interrogate` in Claude or `$interrogate`
in Codex for adversarial or multi-model code review.
It reads the `interrogate reviewers` line directly from `~/.agents/t3/models.md`
on each invocation.
That line controls the independent reviewer slots. The shared model table
provides ordered fallbacks; every Opus job can fall back to Sol. A fallback
that duplicates an existing panel model is reported as reduced diversity,
not counted as another independent review.

Invoke `how` explicitly with `/how` in Claude or `$how` in Codex for codebase
explanations. It reads the `how explorer` and `how explainer` assignments from
`~/.agents/t3/models.md`. Routine exploration uses Sonnet, and straightforward
explanation uses Luna. More demanding work uses Opus with Sol as fallback.
T3 capabilities and actual task results determine which targets can run.

Invoke `why` explicitly with `/why` in Claude or `$why` in Codex to investigate
why code was designed or changed. It reads the `why investigators` and
`why synthesizer` assignments from `~/.agents/t3/models.md`. Both use Opus,
with Sol as fallback. It searches available evidence categories in parallel
and separates documented reasons from inferences and unresolved questions.

## Attribution

- `unslop` is adapted from
  [Cursor's pstack](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md).
- `visual-explainer` builds on
  [Geoffrey Litt's explain-diff-html](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524#file-explain-diff-html-md),
  [Ankit's implementation](https://gist.github.com/ankitg12/8e808d387799de4e9839bc393f8e6405),
  and [Nico Bailon's visual-explainer](https://github.com/nicobailon/visual-explainer).
- `interrogate` is adapted from
  [chhoumann/t3-pstack](https://github.com/chhoumann/t3-pstack/tree/main/plugins/pstack/skills/interrogate).

- `how` is adapted from
  [chhoumann/t3-pstack](https://github.com/chhoumann/t3-pstack/tree/main/plugins/pstack/skills/how).
  Its description, exploration workflow, and two prompt templates are unchanged.
  Local changes provide T3 capability checks, shared model assignments, explicit-only
  Codex metadata, and standalone delegation guidance. Its [MIT license](t3/skills/how/LICENSE)
  is included.

- `why` is adapted from
  [chhoumann/t3-pstack](https://github.com/chhoumann/t3-pstack/tree/main/plugins/pstack/skills/why).
  Its description, investigation workflow, and upstream reference files are unchanged.
  Local changes provide T3 capability checks, shared model assignments, explicit-only
  Codex metadata, and standalone delegation guidance. Its [MIT license](t3/skills/why/LICENSE)
  is included.
