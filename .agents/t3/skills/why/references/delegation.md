# T3 research delegation

Read the shared model sheet before dispatch.

Use `mode: "async"` and `role: "research"` for `delegate_task`. Every brief must say
"inspect only, change no file, and modify no external state". Keep the tools needed
for source searches and citation checks available. Use an explicit `target` per
configured entry, except for `auto` or `inherit-parent`.

A child gets only its brief, never your context. Give each investigator the original
question, code anchor, assigned source, and applicable playbooks. Give the synthesizer
the original question, code anchor, all findings, skipped sources, and confidence
framework. Use absolute file paths for referenced instructions and name the repository
path. Inspect the current checkout; a new worktree would omit uncommitted edits.

Before each spawn, start from the role's configured reasoning level and pick
the reasoning level and speed the job needs. Raise it one step, up to max, for
the hardest or subtlest work. Lower it one step for judgment and two or more
steps for routine work. Use fast mode only when explicitly requested by the
user. Otherwise use standard speed. Change only the entry's reasoning and
speed options, and keep the family the role names. Use the option IDs and
values in `orchestrator_capabilities`. If the model has no value at that level,
or no speed option, use its nearest supported one. An `auto` or
`inherit-parent` entry stays on the parent model. If `delegate_task` rejects
the adjusted entry, do not try another adjusted entry. Use the role's original
entry and say so. If the model is unavailable or out of quota, use the shared
model sheet's fallbacks.

Every investigator and synthesizer is a `delegate_task` call so every child shows up
in T3. Give each call its own `clientRequestId`, stable across retries of that call,
and keep each returned `taskId`. A child's completion wakes this thread, so end the
turn instead of polling, and call `task_status` only when a result is needed mid-turn.
`task_cancel` stops a child, and `task_status` confirms it stopped. Wait for all
investigators before spawning the synthesizer. Do not present the final answer until
the synthesizer has completed.
