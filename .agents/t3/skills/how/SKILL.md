---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
disable-model-invocation: true
---

# How

Explore the codebase to answer "how does X work?" questions. Produce architectural explanations at the level of a senior engineer onboarding onto a subsystem, enough to build a working mental model, not so much that it reads like annotated source code.

This workflow requires T3's `orchestrator_capabilities`, `delegate_task`, and `task_status` tools. If they are unavailable, report that this workflow needs T3 and stop. Do not substitute another delegation mechanism. Call `orchestrator_capabilities` before dispatch and resolve the configured roles against its available providers, models, and options.

Every spawn is a `delegate_task` child with `role: "research"` and a brief that says to inspect only and change no file. Explorers use the `how explorer` line in the model sheet, and every explainer uses the `how explainer` line. Set `target` from that line's entry. If a needed role is missing or empty, ask the user to configure it before dispatch. Leave `target` unset when the value is `auto` or `inherit-parent`. If a model is unavailable or out of quota, use its fallback in the shared model sheet and say so. Pick each subagent's reasoning level and fast or standard speed for the job using `references/delegation.md`, adapted from the Subagents section of **poteto-mode**.

## 1. Assess complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (a single module, a small utility, a narrow question such as "how does function X work"): no explorers. Spawn one explainer that explores and explains in one pass, built from `references/explainer-prompt.md` without the explorer-findings section. Go to step 4.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): go to step 2.

When in doubt, take the simple path.

## 2. Explore (complex only)

Decompose the question into 2 to 4 angles, each a distinct slice of the subsystem. Spawn all explorers in a single message, each with `references/explorer-prompt.md` and its angle filled in.

## 3. Synthesize (complex only)

Once all explorers have returned, spawn one explainer with `references/explainer-prompt.md` and every explorer's findings filled in.

## 4. Present

Present the explainer's output. Light edits for clarity or context from the conversation are fine. Do not substantially rewrite it.

## Output format

The explanation uses the sections defined in `references/explainer-prompt.md`, dropping any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.

## Models

Read the shared model sheet at `~/.agents/t3/models.md` each time this skill runs. Model assignments, routine-work selection, and fallback rules live there, not in this skill. Resolve model names through its target table before dispatch.

An entry is `<providerInstanceId>/<modelId>` plus `<optionId>=<value>` pairs, and it maps onto `delegate_task`'s `target`, with the provider instance as `providerInstanceId`, the model as `model`, and the pairs as `options`. It splits at its first `/`, so a model ID with its own `/`, such as OpenCode's `<provider>/<model>`, is written whole after it. Option IDs differ per provider, so take them from `orchestrator_capabilities`. `inherit-parent` or `auto` omits `target`.
