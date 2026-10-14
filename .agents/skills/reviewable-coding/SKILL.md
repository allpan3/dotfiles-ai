---
name: reviewable-coding
description: Implement a substantial feature or refactor as a sequence of understandable steps, and give a review guide. Runs only when the user invokes it by name.
disable-model-invocation: true
---

# Reviewable coding

Implement the agreed change so that the user can understand its design and review how it
developed. Use the request and existing design notes to find the complete scope; a separate task
brief is not necessary.

## Steps

- Make one step for each behavior change or design decision. Keep mechanical edits, such as renames,
  moved code, or formatting, in separate steps. Do not make steps that are too small to understand
  alone, and do not add unrelated refactoring.
- When commits are in scope, make one commit for each step, so that the commits are understandable
  in sequence. Otherwise, describe the steps in the review guide. This skill does not authorize a
  commit or push.
- Reviewable steps do not require a pause after each step. Continue the agreed work between the
  checkpoints that the user requested.

## Review guide

- At the end, give a short review guide in the final answer, or in the existing task note when the
  work continues across sessions. Include what changed and why, the main concepts, a reading order,
  and the checks that ran.
- Link the relevant files or commits. Explain each step as it was at that commit, not only the final
  design.
- Use Markdown. Use `visual-explainer` when a diagram or interaction makes a step clearer.
