---
name: visual-explainer
description: Build or update a complete HTML explanation page when requested or when diagrams, interaction, or layered detail need more space than a reply. A single inline visual can follow the host's presentation workflow without this skill.
---

# Visual explainer

Build one HTML page that lets the reader understand the topic and decide quickly. Make the page
self-contained: connect the question, reasoning, figures, and conclusions within it. The chat reply
can summarize the result or decision when the host's reply format permits.

Follow the current application's requirements for visual selection, delivery tools, placement, and
styling. Apply this skill within those requirements. When the application does not prescribe a
format or renderer, choose the format that serves the reader and provide a standalone HTML file.

## Design the explanation

1. Identify the question the reader needs to answer. For a code change, inspect the changed behavior
   and enough surrounding code to explain its cause. For a research result or model, identify its
   evidence and assumptions. Link the relevant sources instead of giving a general repository tour.
2. Choose the visual from the relationship: message order, timing, data flow, physical placement,
   or a comparison. Read [the diagram guide](references/diagrams.md) when designing a figure; it
   has selection criteria and worked SVG examples. Where the host leaves the format open, use text
   or a table when it communicates better.
3. Give each figure a specific claim. Show the mechanism that supports it, label arrows with actions,
   and attach quantities and units to what they measure. Keep node positions and scales consistent
   across comparisons. Distinguish observed results, inferred behavior, and illustrative models.
4. Add interaction when it helps the reader examine a sequence, change, or assumption. Define what
   each control changes and keep the diagram, values, and explanation consistent. Show a useful
   complete state before interaction; support keyboard use and respect reduced motion.

## Content

- Lead reports and recommendations with the result and its material qualifications. For a
  walkthrough, establish the goal and introduce ideas in the order needed to understand them.
  Keep required information out of collapsed sections.
- Organize text and figures around the user's question. They can precede, follow, or alternate with
  each other as the explanation needs; there is no fixed section sequence.
- Put optional background in native `<details><summary>…</summary>…</details>` blocks. Keep a brief
  definition in the main text when the conclusion depends on it. Write only relevant background.
- Explain mechanisms and conclusions in surrounding prose that explicitly refers to the figure.
  Keep captions brief; put detailed evidence nearby or link to it. Do not repeat every label.
- Keep graphics uncluttered. Use necessary labels, units, legends, and short annotations. Put longer
  explanations in normal paragraphs, rather than squeezing them into shapes or small text beside
  graphical elements. An HTML page can freely mix those paragraphs with its figures.
- Account for how the host displays the page and chat reply. If the page appears first, it must not
  depend on the later reply for essential context. This does not prescribe the order within the page.
- Avoid decorative animation and redundant figures.
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
   its example title and body. Adapt its CSS and controls to the host's layout and theme requirements.
   For an existing page, edit it in place rather than replacing it with the starter.
2. Write HTML/CSS and SVG directly. Use JavaScript for browser interaction and JSON for optional
   data or model parameters. Python or another available tool can perform calculations or repeated
   generation before delivery. This skill adds no page schema or rendering command of its own;
   follow the host's delivery workflow.
3. Keep CSS, JavaScript, and required assets inline. Put escaped source in
   `<pre><code class="language-…">`. Use the relevant [interaction example](references/interactions.md)
   for controls, with unique IDs and scripts after their markup. Keep core content readable without
   JavaScript and hide custom controls until they initialize. The diagram guide's examples use the
   starter's theme variables. Mermaid text alone will not render without its library.
4. Check that each figure agrees with its surrounding explanation, caption, and source evidence.
   Verify units, direction, ordering, and comparison scales. When browser inspection is available
   and permitted by the host workflow, inspect the changed sections at normal and narrow widths in
   both themes. Check readable labels, arrow endpoints,
   clipping, contrast, and any custom controls with the keyboard. Keep wide figures readable in a
   scroll region instead of shrinking their labels. State any check you could not perform.

Deliver through the host's required tools and reply format. When no inline renderer is available,
provide the page's absolute path or link with the short answer.
