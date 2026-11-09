# T3 model roles

## Delegation in T3

These rules apply to all delegated work in T3, including general skills and ordinary tasks.
A skill runs in the current conversation unless it delegates work. This policy does not require
extra agents or change the parent model.

Use `orchestrator_capabilities`, `delegate_task`, and `task_status`. Every child must be a T3
`delegate_task`, including one using the parent's model. Use the skill's configured role when it
has one. Otherwise, use `research delegate` for academic source analysis, literature synthesis,
and research-direction assessment, and `general delegate` for other work.

Give each child its task, necessary context, absolute source paths, and permitted actions. A child
does not inherit the conversation. Use `mode: "async"` and retain the returned `taskId`. Give each
call its own `clientRequestId`, stable across retries of that call. Continue independent work while
children run. Use completion notifications when available and `task_status` when a result is needed
or a task's state must be confirmed. Only synthesize findings after the required children return.

## Models and fallbacks

Fallbacks are ordered candidates at the same capability tier for one task. A fallback replaces an
unavailable assignment; it does not launch an additional agent or imply identical model strengths.

| Model  | Target                                       | Fallback |
| ------ | -------------------------------------------- | -------- |
| Astra  | `codex/gpt-6-astra reasoningEffort=xhigh`    | Fable    |
| Fable  | `claudeAgent/claude-fable-5-1 effort=xhigh` | Astra    |
| Opus   | `claudeAgent/claude-opus-5-5 effort=xhigh`   | Sol      |
| Sol    | `codex/gpt-6.1-sol reasoningEffort=xhigh`    | Opus     |
| Sonnet | `claudeAgent/claude-sonnet-5-5 effort=xhigh` | Luna     |
| Luna   | `codex/gpt-6-luna reasoningEffort=xhigh`     | Sonnet   |

Every Opus job can fall back to Sol, including roles added later.

## Roles

- general delegate: Sol
- research delegate: Astra
- interrogate reviewers: Opus, Sol
- how explorer: Opus; use Sonnet for routine work.
- how explainer: Opus; use Luna for routine work.
- why investigators: Opus
- why synthesizer: Opus
- grilling explorer: Opus; use Sonnet for routine work.
- background-study worker: Opus; use Sonnet for routine work.

Routine work means bounded file or symbol lookup, direct call tracing, or a straightforward
explanation of unambiguous code. For roles with a routine-work alternative, use the role's normal
model for cross-system reasoning, conflicting evidence, subtle correctness questions, and
substantial synthesis. A small diff or short answer does not by itself mean low reasoning. If
routine work reveals those harder questions, hand the question and findings to the role's normal
model. Reviewer slots keep their configured models.

## Multi-agent requests

A fallback list does not create a parallel panel. Follow the user's requested agent count,
assignments, and models, or a skill's explicit panel configuration. For an explicit request for
independent multi-model academic research without a named lineup, use Astra and Fable. Keep Fable
as Astra's fallback for ordinary research delegation; its limited quota is not a reason to treat
it as a lower-tier model. Apply the failure and panel rules below to each assignment.

## Reasoning effort

Entries set each role's starting reasoning level, xhigh by default. Before
spawning, adjust it for the job using the skill's `references/delegation.md` when provided.
Otherwise, lower effort for bounded lookup or extraction, and use the configured level for
substantial analysis. Raise it for the hardest work when the model supports a higher level.
Respect any reasoning level or speed explicitly requested by the user. Use fast mode only when
requested, and validate every option against `orchestrator_capabilities`.

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
