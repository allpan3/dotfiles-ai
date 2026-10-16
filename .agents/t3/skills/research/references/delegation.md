# T3 research delegation

This workflow requires `orchestrator_capabilities`, `delegate_task`, and `task_status`.
If they are unavailable, report that this workflow needs T3 and stop. Read
`~/.agents/t3/models.md`, select the `research worker` role, and validate its target
and options with `orchestrator_capabilities`. Follow the sheet's routine-work selection,
model fallbacks, quota handling, and replacement rules. Ask for configuration if the
sheet or role is missing. Omit `target` for `auto` or `inherit-parent`.

Start from the role's configured reasoning level. Raise it one step, up to max, for
the hardest work; lower it one step for judgment and two or more steps for routine work.
Use the nearest supported level. Keep the selected model and change only supported
reasoning and speed options. Use fast mode only when the user requests it. If an adjusted
entry is rejected, retry once with the original entry and report it. Availability failures
follow the shared sheet's fallbacks.

Launch one `delegate_task` with `role: "research"` and `mode: "async"`. Include the
question, relevant context, repository path, and the three research instructions from
`SKILL.md` in its brief. A child does not inherit this conversation. Choose the findings
path using the repository's convention and include its absolute path in the brief.
Limit writes to that note; preserve unrelated content in an existing note. Do not modify
implementation files or external state. Ask the child to return the note path and any
unresolved questions.

Give the call a unique `clientRequestId`, stable across retries, and keep its `taskId`.
Continue independent work while it runs. If only the research is pending, yield for its
completion notification instead of polling. Use `task_status` when a result is needed
mid-turn and to confirm a failed or cancelled task has stopped before replacement.
When it completes, read the note, check that its claims cite primary sources, and return
the note link with the answer and any material gaps. Do not report completion before the
note exists.
