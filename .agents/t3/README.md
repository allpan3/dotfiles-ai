T3-only skills live in `skills/`, each in its own folder with a `SKILL.md`.

`interrogate` uses T3 delegation for independent multi-model code review.
Invoke it explicitly with `/interrogate` in Claude or `$interrogate` in Codex.
Model assignments live in `~/.agents/t3/models.md`, shared with future
T3 skills alongside routine-work selection and ordered fallbacks. Run `~/.agents/setup-agents.sh`
after adding or removing skills.

`how` uses T3 research delegates to explain a codebase or subsystem.
Invoke it explicitly with `/how` in Claude or `$how` in Codex. Its model roles
are `how explorer` and `how explainer`.

`why` uses T3 research delegates to investigate design rationale and history.
Invoke it explicitly with `/why` in Claude or `$why` in Codex. Its model roles
are `why investigators` and `why synthesizer`.
