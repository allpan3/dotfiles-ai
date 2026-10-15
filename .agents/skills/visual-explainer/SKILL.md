---
name: visual-explainer
description: Build or update an HTML explanation page with diagrams, code views, and collapsible background. Use when the user asks for a page, explainer, walkthrough, or visual explanation, or when a process, system, comparison, or code change needs a diagram or layered background that chat cannot show well. Not for a single diagram or table that fits in the reply.
---

# Visual explainer

Build one HTML page that lets the reader understand the topic and decide quickly. Keep the short
answer, its reason, and any decision in chat; put the detail on the page.

## Design the explanation

1. Identify the question the reader needs to answer. For a code change, inspect the changed behavior
   and enough surrounding code to explain its cause. For a research result or model, identify its
   evidence and assumptions. Link the relevant sources instead of giving a general repository tour.
2. Choose the visual from the relationship: message order, timing, data flow, physical placement,
   or a comparison. Read [the diagram guide](references/diagrams.md) when designing a figure; it
   has selection criteria and worked SVG examples. Use text or a table when it communicates better.
3. Give each figure a specific claim. Show the mechanism that supports it, label arrows with actions,
   and attach quantities and units to what they measure. Keep node positions and scales consistent
   across comparisons. Distinguish observed results, inferred behavior, and illustrative models.
4. Add interaction when it helps the reader examine a sequence, change, or assumption. Define what
   each control changes and keep the diagram, values, and explanation consistent. Show a useful
   complete state before interaction; support keyboard use and respect reduced motion.

## Content

- Put the result, any decision or next action, material risks, and unresolved requirements first.
  Show the core explanation before long background. Do not put required information in collapsed
  sections.
- Organize the sections around the user's question. There is no fixed section sequence.
- Put optional background in native `<details><summary>…</summary>…</details>` blocks. Keep a brief
  definition in the main text when the conclusion depends on it. Write only relevant background.
- Keep the figure and its explanation together. Use a caption that states what the figure shows.
  Put detailed evidence nearby or link to it. Do not repeat every label in prose.
- Avoid decorative animation and a figure for every fact. A number does not always need a chart.
- Add a quiz only when the user asks for one.

## Location and format

- Keep one page per topic. On follow-up, update the relevant section and keep the path and anchors
  stable.
- Save the page where the user or the project instructions say. Otherwise, use the session's
  scratch directory if the client names one; if not, use `/tmp/YYYY-MM-DD-explanation-<topic>.html`.
  Choose an unused path for a new page. Keep review pages outside production documentation unless
  the user asks to include them.
- Make each explanation in one format. If the user asks for a native page, such as a Claude
  artifact or a ChatGPT Page, and that tool accepts an HTML file, publish the rendered file with
  it. Do not make a second page with the same content. Local file links do not work on a published
  page; link files and commits by web URL.

## Render and check

1. For a new page, copy [assets/starter.html](assets/starter.html) to the output path and replace
   its example title and body. Its CSS, theme switch, and code highlighter are editable starting
   points. For an existing page, edit it in place rather than replacing it with the starter.
2. Write HTML/CSS and SVG directly. Use JavaScript for browser interaction and JSON for optional
   data or model parameters. Python or another available tool can perform calculations or repeated
   generation before delivery; there is no required page schema or rendering command.
3. Keep CSS, JavaScript, and required assets inline. Put escaped source in
   `<pre><code class="language-…">`. Use the relevant [interaction example](references/interactions.md)
   for controls, with unique IDs and scripts after their markup. Keep core content readable without
   JavaScript and hide custom controls until they initialize. The diagram guide's examples use the
   starter's theme variables. Mermaid text alone will not render without its library.
4. Check that each figure supports its caption and agrees with the source evidence. Verify units,
   direction, ordering, and comparison scales. If a browser tool is available, inspect the changed
   sections at a normal and narrow width in both themes. Check readable labels, arrow endpoints,
   clipping, contrast, and any custom controls with the keyboard. Keep wide figures readable in a
   scroll region instead of shrinking their labels. State any check you could not perform.

Reply with the short answer and the page's absolute path or link.
