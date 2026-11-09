---
name: research
argument-hint: "<research request> [constraints or desired output]"
description: Investigate academic research questions, synthesize literature, and develop or assess research directions from an area, a focused question, or starting papers. Use for scholarly inquiry and literature-grounded analysis. Routine coding, API, and product lookups belong to their task-specific workflows.
---

# Research

Develop an answer whose reasoning can be traced to the literature and whose limits are clear.
Adapt the investigation to the user's goal. Understanding a topic, comparing methods, assessing
a claim, and developing a research direction require different depths and outcomes.

When delegating any part of the research, first read [the delegation guidance](references/delegation.md)
for the current host.

## Invocation

Use `$research <research request>` in Codex or `/research <research request>` in Claude.
The research request is required. Describe an area, a question, or what to investigate about
supplied papers. Add constraints or a desired output when useful; these are optional.

Examples:

- `$research Map the main approaches and open questions in solid-state batteries.`
- `$research Compare these two papers and investigate their remaining limitations.`
- `$research Continue our earlier study and assess the evidence for its leading hypothesis.`

Use the text accompanying the invocation and its referenced sources as the research request.
If the user invokes the skill without a request, ask what they want to research before starting.
Do not choose a topic from earlier conversation on their behalf. Use earlier context when the
current request refers to it. For automatic invocation, use the current user request to establish
what to research.

## Establish the question

Accept ordinary language and any combination of these starting points:

| Starting point | How to begin |
| --- | --- |
| An area | Map its problems, major approaches, and unresolved questions before narrowing. |
| Papers, links, DOIs, citation keys, or attachments | Identify the sources, read them in context, and use their relationships to guide further investigation. |
| A specific question or hypothesis | Identify the evidence and alternatives needed to answer or test it. |
| An existing study | Recover its question, findings, constraints, and unresolved issues before adding work. |

Infer the intended outcome separately from the starting material. A supplied paper is not an
instruction to produce only a summary or to invent a new project. User examples illustrate
possibilities unless the user selects them as requirements or directions.

Resolve only ambiguities that would materially change the investigation. Optional context
includes the purpose, date range, constraints, desired depth, available sources, output format,
and time budget. Accept free-form text; do not require named parameters or a form.

State the working question and material scope assumptions briefly. Work independently when asked
to conduct research. For a guided discussion, explain a concrete example first and pause at
substantive choices. Preserve the collaboration mode and decisions already established.

## Discover and screen sources

Reuse relevant papers and notes, checking whether their scope and currency fit the question.
Broaden discovery through references, citing work, competing approaches, and adjacent fields.
Search for the underlying problem and mechanism as well as the starting papers' terminology.
Do not restrict discovery to a proposed technology before establishing the problem it would solve.

Use reviews to orient the search. Check claims that affect the conclusion against primary
literature, data, or other original sources appropriate to the field. Choose search services,
proceedings, repositories, and local collections according to the question and available access.
Inspect the actual source before treating a search result or citation as evidence.

Titles and abstracts can route papers for further reading. If relevance remains uncertain,
inspect the introduction and pertinent methods or evaluation sections before excluding a paper.
If that material is unavailable, retain the uncertainty. Deepen the closest and most consequential
sources rather than collecting a large bibliography with little analysis.

For a substantial review, keep a compact record of the search scope, selection reasons, and
remaining coverage gaps. Link preprint, conference, and journal versions without counting them
as independent evidence or transferring a result between versions without checking it. A scoped
exploration does not establish an exhaustive or systematic review.

## Build and check the evidence

Use source notes or a comparison table when they help track the evidence. Record source identity
and version, the material actually read, relevant claims, supporting locators, and limitations. Distinguish
title or abstract screening, selected-section reading, and complete-paper reading. Reusing an
earlier note does not constitute a new primary-source review.

Keep reading depth separate from the kind of evidence the study provides. Distinguish theoretical
results, observations, controlled experiments, simulations, estimates, and proposed methods as
applicable. Identify assumptions, evaluation conditions, baselines, uncertainty, and threats to
validity that affect the claim. Inspect figures, tables, supplements, or artifacts when a decisive
detail depends on them.

Separate what the authors claim, what their evidence establishes, your interpretation, and a new
hypothesis. Cite consequential claims with a stable source and a useful section, page, figure,
table, or other locator. Mark inaccessible evidence and unresolved disagreements explicitly.
When a source omits a necessary detail, mark it unknown. The omission does not establish absence,
failure, or novelty. Another model's synthesis is a lead to verify, not additional independent evidence.

## Synthesize and challenge the answer

Organize the explanation around the question, mechanisms, and competing accounts. Explain how
the studies relate and why their differences matter. Use a concrete example, diagram, calculation,
or counterexample when it helps the user understand the mechanism or an assumption.

Compare approaches under compatible conditions. Account for differences in the task, data,
resources, quality targets, and evaluation methods before comparing reported results. Keep
distinct outcomes separate when one improves while another worsens. Assess whether a local
improvement changes the outcome that matters to the overall problem.

Look for evidence against the emerging conclusion. Test whether a simpler explanation or an
existing approach accounts for the claimed benefit. Explain disagreements through differences
in assumptions, methods, or evidence where possible; leave them unresolved when the sources
do not settle them. Distinguish a missing explanation from an established limitation.

### When developing research directions

Begin with a consequential unresolved problem and the strongest existing approaches. For each
candidate worth pursuing, establish:

- The specific question or falsifiable claim and why resolving it matters.
- The closest prior work, what it already solves, and the remaining difference to investigate.
- The proposed mechanism or explanation, its necessary assumptions, and a credible simpler alternative.
- The smallest useful test, analysis, or distinguishing example, including fair comparisons and
  the result that would support, weaken, or reject the claim.
- Feasibility, missing evidence, and the cost of obtaining it.

Describe novelty relative to the work actually checked and disclose relevant search gaps.
Several mechanisms belong in one proposal only when they support one coherent argument and
their individual roles can be tested. Successful implementation or integration alone does not
establish a research contribution. Rank candidates only when the user wants a decision and the
evidence supports the comparison. Keep proposed tests separate from experiments actually run.

## Deliver and preserve the findings

Match the deliverable to the request. A focused answer may fit in chat; a continuing study may
need a concise synthesis, source records, and a short account of its current decisions and open
questions. Do not generate a large document package by default.

Lead with the supported answer or the unresolved question that determines it. Include enough
evidence and reasoning to assess the conclusion, then state material limitations and the next
investigation that would reduce them. Finish when the agreed question is addressed at the
requested depth or when a specific evidence gap prevents a stronger answer after checking
reasonable source alternatives. Explain that gap and its consequence rather than implying that
more searching would necessarily settle it.

Use existing project conventions for requested saved work. Reconcile affected conclusions while
preserving unrelated material. Keep source-library and literature-note edits within the user's
requested scope and use the established workflows for those systems. For a handoff, include the
question, source access, supported findings, assumptions, rejected alternatives, and next decision.

For substantial writing, use `technical-writing` when available. Review the completed text for
comprehension separately from checking claims against sources, then use `unslop` when available
for the editorial pass. Preserve technical meaning, conditions, and uncertainty through revision.
