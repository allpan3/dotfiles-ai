---
name: interrogate
description:
  'Use for "interrogate", "adversarial review", "multi-model review", "challenge this",
  "stress test this code", "find blind spots", or "tear this apart". Multiple LLM reviewers
  challenge changes from independent angles.'
disable-model-invocation: true
---

# Interrogate

Spawn one reviewer per configured model to adversarially review code changes. The adversarial signal
comes from model diversity, not assigned personas. The deliverable is a synthesized verdict. Do NOT
auto-apply changes.

## T3 capability check

This workflow requires T3's `orchestrator_capabilities`, `delegate_task`, and `task_status` tools.
If they are unavailable, report that this workflow needs T3 and stop. Do not substitute another
delegation mechanism. Call `orchestrator_capabilities` before dispatch and resolve the configured
panel against its available providers, models, and options.

## Step 1, Scope

Identify what to review from context:

- If the user points at specific files or a diff, use that.
- If on a feature branch, run `git diff main...HEAD` (or the appropriate base branch) for the full
  changeset.
- If the user's message references recent work, gather the relevant files.

Package the diff or file contents with any surrounding context files the reviewers need to
understand the code.

## Step 2, Intent

Before spawning reviewers, state the intent in one clear paragraph from the user's message, commit
messages, the PR description if one exists, and the code. If you're unsure about the intent, ask the
user before proceeding.

## Step 3, Spawn Reviewers

Launch all reviewers in a single response with `delegate_task`, one per entry on the
`interrogate reviewers` line in the model sheet, labeled Reviewer A, B, and so on to match the entry
count. If the sheet or that line is missing or empty, ask the user to configure the panel before
dispatch. There is no fallback panel embedded in this skill.

Each reviewer gets `role: "review"`, a brief that says to inspect only and change no file, and
`target` set from its configured entry. Omit `target` for an `auto` or `inherit-parent` entry, so
that reviewer runs on the parent model.

If a model is unavailable or out of quota, use its fallback in the shared model sheet and say so.
Follow the sheet's panel rules if this would duplicate an existing reviewer.

Read `references/reviewer-prompt.md` and fill in the same template for every reviewer with the
stated intent, the diff or file contents, the rubric from `references/rubric.md`, and the
code-quality lens from `references/code-quality-review.md`. Pick each subagent's reasoning level and
fast or standard speed for the job, using `references/delegation.md`, which contains the relevant T3
dispatch guidance from **poteto-mode**.

## Step 4, Synthesize

As results come back, build a unified picture. Parse every reviewer's findings. Merge findings that
describe the same issue differently, and note which models raised each one. Findings two or more
models raised independently are the highest signal. Read a lone model's finding, but weight it
accordingly. Note disagreements. If one model flags something and another explicitly says the
opposite, that is context for the verdict.

## Step 5, Lead Judgment

You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator. Read
`references/lead-judgment.md` for the full framework. Put every finding in one of four buckets, with
the model(s) that raised it and a one-line rationale.

- **Act on**. Real issues affecting correctness, security, or maintainability given the actual
  goals. They would block a real PR.
- **Consider**. Legitimate, but you're not sure they outweigh the cost of addressing them now. Worth
  the user's attention.
- **Noted**. Technically valid but not actionable. Context-dependent, premature optimization, or
  low-impact at this stage.
- **Dismissed**. Wrong, nitpicky, or missing context, with a brief reason.

## Output Format

### Intent

> [The stated intent paragraph from Step 2]

### Reviewers

- Reviewer [label]: [model name], [N findings] (one bullet per reviewer)

### Act On

[Each: description, which models raised it, why it matters.]

### Consider

[Each: description, which models raised it, the tradeoff.]

### Noted

[Brief list.]

### Dismissed

[Each with a brief rationale.]

### Agreement Map

[Where models agreed and diverged, and what that pattern tells us.]

## Models

Read the shared model sheet at `~/.agents/t3/models.md`. Resolve model names through
its target table and follow its selection, fallback, and panel rules.

An entry is `<providerInstanceId>/<modelId>` plus `<optionId>=<value>` pairs, and it maps onto
`delegate_task`'s `target`, with the provider instance as `providerInstanceId`, the model as
`model`, and the pairs as `options`. It splits at its first `/`, so a model ID with its own `/`,
such as OpenCode's `<provider>/<model>`, is written whole after it. Option IDs differ per provider,
so take them from `orchestrator_capabilities`. `inherit-parent` or `auto` omits `target`.

Read the `interrogate reviewers` role line each time this skill runs. The sheet determines the
panel's size and membership; adding providers to T3 does not automatically add reviewers to the
panel.
