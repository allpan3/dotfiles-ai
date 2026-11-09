# Research delegation

Delegate bounded investigations or independent analyses when useful or requested. The parent
coordinates the research question, coverage, and final synthesis. Give each child its question,
necessary context, source paths or access instructions, and permitted outputs. Ask for findings
with source locations, reading depth, limitations, and unresolved questions. State which files,
if any, the child may write; otherwise keep its work read-only.

## In T3

Use T3's `orchestrator_capabilities`, `delegate_task`, and `task_status` tools. If the session is
identified as T3 but required tools are missing, report the blocked delegation instead of using
native subagents.

Before dispatch, read `~/.agents/t3/models.md` and use its `research delegate` role. Resolve the
role's target and validate its provider, model, and options with `orchestrator_capabilities`.
Follow the sheet's reasoning, fallback, quota, multi-agent, and task-lifecycle rules. Keep model
assignments in that sheet. If the sheet or role is missing, ask for configuration before dispatch.

Use `delegate_task` with `role: "research"` and `mode: "async"`. Include all necessary context in
the brief; children do not inherit this conversation. Follow the user's requested agent count,
assignments, and models. A fallback replaces an unavailable assignment; it does not create an
additional parallel researcher. Review the returned evidence before incorporating conclusions.

## Outside T3

Use the host's native subagent tools and model-selection rules. No T3 tools or model sheet are
required. If subagents are unavailable, conduct the research directly and disclose any requested
independent analysis that could not be provided.
