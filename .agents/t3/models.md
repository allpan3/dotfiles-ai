# T3 model roles

## Models and fallbacks

Fallbacks are ordered candidates for one task, not additional agents.

| Model  | Target                                       | Fallback |
| ------ | -------------------------------------------- | -------- |
| Opus   | `claudeAgent/claude-opus-5-5 effort=xhigh`   | Sol      |
| Sol    | `codex/gpt-6.1-sol reasoningEffort=xhigh`    | Opus     |
| Sonnet | `claudeAgent/claude-sonnet-5-5 effort=xhigh` | Luna     |
| Luna   | `codex/gpt-6-luna reasoningEffort=xhigh`     | Sonnet   |

Every Opus job can fall back to Sol, including roles added later.

## Roles

- interrogate reviewers: Opus, Sol
- how explorer: Opus; use Sonnet for routine work.
- how explainer: Opus; use Luna for routine work.
- why investigators: Opus
- why synthesizer: Opus
- grilling explorer: Opus; use Sonnet for routine work.
- research worker: Opus; use Sonnet for routine work.

Routine work means bounded file or symbol lookup, direct call tracing, or a straightforward
explanation of unambiguous code. Use Opus for cross-system reasoning, conflicting evidence, subtle
correctness questions, and substantial synthesis. A small diff or short answer does not by itself
mean low reasoning. If routine work reveals those harder questions, hand the question and findings
to the role's normal model. Reviewer slots keep their configured models.

## Reasoning effort

Entries set each role's starting reasoning level, xhigh by default. Before
spawning, adjust it for the job using the skill's `references/delegation.md`.
Respect any reasoning level or speed explicitly requested by the user.

## Selection and failure handling

Resolve names through the table and validate each target and its options with
`orchestrator_capabilities`. The catalog does not guarantee remaining quota. Use only supported
options for the selected provider and model.

If a model is unavailable or its task fails because of quota or provider
availability, try the next candidate for the original choice. Try each candidate at most once per
task; do not recursively expand fallback lists. For a confirmed provider-wide quota failure, skip
other candidates on that provider for this run. Do not treat a task's difficulty or an ordinary
code/test failure as a quota failure. Report model switches and exhausted candidates.

Before replacing an accepted task, confirm it has failed or stopped through T3 task status. A queued
task, a slow task, or a wait timeout is not a failure. If an adjusted reasoning/speed option is
rejected, do not try another adjusted entry. Retry once with the role's original entry and say so.
Do not retry the same provider for a confirmed quota failure. Use a new delegation request ID for a
replacement task.

Panel entries run independently. If a fallback would duplicate a model already running or completed
in the panel, use that existing review and report the missing independent reviewer. Do not count it
twice or claim model diversity. If no candidates remain, report the unavailable role or incomplete
panel.
