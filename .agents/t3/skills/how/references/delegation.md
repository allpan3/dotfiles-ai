# T3 research delegation

Adapted from the Subagents section of t3-pstack's `poteto-mode` for a standalone
research skill. Read the shared model sheet before dispatch.

Use `mode: "async"` for `delegate_task`. A read-only child gets "inspect only,
change no file" in its brief. Use an explicit `target` per configured entry,
except for `auto` or `inherit-parent`. Give each explorer its assigned angle and the original question. Give the
explainer the original question and, for complex work, all explorer findings.
Use absolute file paths when using pointers.
A child gets only its brief, never your context. Inspect the current code in
the shared checkout; a new worktree would omit uncommitted edits.

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

Every explorer and explainer is a `delegate_task` call, including reviewers in the parent's
model family, so every child shows up in T3. Give each call its own
`clientRequestId`, stable across retries of that call, and keep each returned
`taskId`. A child's completion wakes this thread, so end the turn instead of
polling, and call `task_status` only when a result is needed mid-turn.
`task_cancel` stops a child, and `task_status` confirms it stopped. Wait for all explorers before spawning the synthesizing explainer. Do not
present the final explanation until its explainer has completed.
