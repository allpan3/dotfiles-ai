# Fact-finding delegation

The parent asks the user questions and manages the interview. Subagents investigate facts;
they do not make the user's design decisions. Give each child the question it must resolve,
the relevant context and repository path, and a brief that says to inspect only, change no
file, and modify no external state. Ask for findings with source locations and unresolved
questions. Continue questions that do not depend on the investigation.

## In T3

Use T3's `orchestrator_capabilities`, `delegate_task`, and `task_status` tools when available.
If the session is identified as T3 or exposes only part of that tool set, report the missing
tools instead of silently substituting native delegation.

Read `~/.agents/t3/models.md` and use its `grilling explorer` role. Resolve the model through
the target table and check its provider, model, and option IDs with `orchestrator_capabilities`.
If the sheet or role is missing, ask the user to configure it before dispatch. Follow the
sheet's routine-work selection, fallback, quota, and task replacement rules. Omit `target`
for `auto` or `inherit-parent`.

Start from the entry's configured reasoning level. Raise it one step, up to max, for the
hardest work; lower it one step for judgment and two or more steps for routine work. Use the
nearest supported level. Keep the selected model and change only supported reasoning and
speed options. Use fast mode only when the user requests it. If an adjusted entry is rejected,
retry once with the original entry and report it. Model availability failures follow the
shared sheet's fallbacks.

Use `delegate_task` with `role: "research"` and `mode: "async"`. Each call has its own
`clientRequestId`, stable across retries of that call. Keep the returned `taskId`. Include all
necessary context in the brief; a child does not inherit this conversation. Use absolute paths
for referenced files. When only pending children can advance the interview, yield for their
completion notifications instead of polling. Use `task_status` when a result is needed
mid-turn and to confirm a failed or cancelled child has stopped before replacing it.

## Outside T3

Use the host's normal subagent tools and model-selection rules. No T3 tools or model sheet
are required. If subagents are unavailable, inspect the facts directly and continue the same
interview. Do not ask the user to supply facts you can inspect yourself.
