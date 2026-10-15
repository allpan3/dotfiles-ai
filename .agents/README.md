# Shared AI Setup

Maintain plain skills here and run `~/.agents/setup-agents.sh` to make them available to Claude Code and
Codex. No plugin installation is needed.

## Layout

- `skills/` contains general skills for regular and T3 sessions.
- `t3/skills/` contains T3-only skills. It is currently empty of skills.
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

Use `/unslop` in Claude or `$unslop` in Codex, and similarly for the other names. Automatic use
depends on the task matching the skill's description. T3-only skills must check for the required T3
tools before performing orchestration.

## Attribution

`unslop` is adapted from
[Cursor's pstack](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md). Its
[MIT license](skills/unslop/LICENSE) is included with the skill.

`visual-explainer` builds on Geoffrey Litt's
[`explain-diff-html` skill](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524#file-explain-diff-html-md).
Its renderer workflow is inspired by
[Ankit's explain-diff implementation](https://gist.github.com/ankitg12/8e808d387799de4e9839bc393f8e6405).
