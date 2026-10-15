# Design diagrams that explain the mechanism

Paste the relevant snippet directly into the HTML starter's body. Adapt its content and geometry
to the explanation. The examples need no external libraries or build step.

## Select by the question

| Reader's question | Useful form | What to make explicit |
| --- | --- | --- |
| Who sends what, and in which order? | Sequence diagram | Actors, message direction, and time order |
| What overlaps, or determines latency? | Timing diagram | Start and end times, units, and dependencies |
| Where does data go or get stored? | Data-flow diagram | Operations on edges, storage, and boundaries |
| Where are components placed or connected? | Physical layout or circuit diagram | Placement, connectivity, and domain symbols |
| What changes between two designs? | Aligned before/after diagrams | Same positions and scale; changed parts marked |
| How do values differ or change over time? | Table, bars, or line plot | Units, baseline, and a scale suited to the claim |

A service diagram cannot establish timing without timing evidence. An illustrative layout does not
establish physical dimensions. Draw what the sources support and state assumptions that affect the
conclusion. For scientific plots intended for export or publication, use standard plotting tools.

## Build a figure

- Start with the claim, such as "A cache hit avoids a database request." Include only the actors,
  steps, or values needed to show why it holds. Put unrelated mechanisms in a separate figure.
- Label an edge with its operation, direction, and value when relevant. Use a boundary when a
  process, clock domain, or machine boundary explains a cost or constraint.
- For comparisons, preserve component positions and scales. Mark additions, removals, or changed
  states with text or line patterns as well as color. Distinguish a missing edge from an unknown one.
- Attach a duration to the interval it measures. Keep units in labels. State whether values are
  measured, calculated, or illustrative; do not invent numbers to make a figure look complete.
- Use `<figure>` and a claim-bearing `<figcaption>`. Give SVG an accessible title and description.
  Prefix IDs per figure so arrow markers and accessibility references do not collide.
- Use `var(--fg)`, `var(--muted)`, `var(--accent)`, and `var(--surface)` from the starter. A status
  must remain distinguishable without color. Do not assume a white background.
- Keep labels readable at the final display size. Wrap a wide SVG in a keyboard-focusable scroll
  region and retain its minimum width. Use `<tspan>` for deliberate line breaks; SVG text does not
  wrap automatically. Draw edges before nodes when their endpoints would otherwise cover labels.

## Example: a cache-hit sequence

Question: does the database participate in a cache hit? A sequence diagram answers this with calls
and their order. The example assumes the cache lookup succeeds; it makes no claim about misses or
freshness policy. The database lifeline remains visible so the absence of a call is explicit.

```html
<figure class="diagram">
  <div role="region" aria-label="Cache-hit sequence; scroll if needed" tabindex="0"
       style="overflow-x:auto">
    <svg viewBox="0 0 560 225" role="img" aria-labelledby="hit-title hit-description"
         style="display:block;width:100%;min-width:560px;color:var(--fg)">
      <title id="hit-title">A cache hit avoids a database request</title>
      <desc id="hit-description">The client reads a key from the cache. The cache returns the
        stored value. No message is sent to the database in this scenario.</desc>
      <defs><marker id="hit-arrow" viewBox="0 0 10 10" refX="9" refY="5"
        markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M0 0L10 5L0 10Z" fill="var(--accent)"/>
      </marker></defs>
      <g stroke="var(--muted)" stroke-dasharray="5 5">
        <path d="M70 48V188M260 48V188M460 48V188"/>
      </g>
      <g fill="currentColor" text-anchor="middle" font-size="16">
        <text x="70" y="30">Client</text><text x="260" y="30">Cache</text>
        <text x="460" y="30">Database</text>
        <text x="165" y="82">read(key)</text>
        <text x="165" y="142">return cached value</text>
        <text x="460" y="211">No request</text>
      </g>
      <g stroke="var(--accent)" stroke-width="2" marker-end="url(#hit-arrow)">
        <path d="M70 95H260"/><path d="M260 155H70"/>
      </g>
    </svg>
  </div>
  <figcaption>A successful cache lookup returns the value without contacting the database.</figcaption>
</figure>
```

## Example: serial and parallel reads

Question: why can overlapping independent work shorten completion time? Show both schedules on the
same time axis. These are illustrative 4 ms reads, with no shared-resource contention or scheduling
overhead. A dependency or shared bottleneck would change the result. Keep this assumption visible
when adapting the figure; do not present its idealized numbers as a benchmark.

```html
<figure class="diagram">
  <div role="region" aria-label="Read schedules; scroll if needed" tabindex="0"
       style="overflow-x:auto">
    <svg viewBox="0 0 640 305" role="img" aria-labelledby="reads-title reads-description"
         style="display:block;width:100%;min-width:640px;color:var(--fg)">
      <title id="reads-title">Independent reads can overlap</title>
      <desc id="reads-description">On a common illustrative scale, two serial 4 millisecond reads
        complete at 8 milliseconds. Parallel reads both start at zero and complete at 4 milliseconds.</desc>
      <g fill="none" stroke="var(--muted)" stroke-dasharray="4 5">
        <path d="M120 35V270M360 35V270M600 35V270"/>
      </g>
      <g stroke="var(--accent)" stroke-width="2" fill="var(--accent-soft)">
        <rect x="120" y="55" width="240" height="32"/>
        <rect x="360" y="95" width="240" height="32"/>
        <rect x="120" y="170" width="240" height="32"/>
        <rect x="120" y="210" width="240" height="32"/>
      </g>
      <g fill="currentColor" font-size="16">
        <text x="8" y="75">Serial</text><text x="8" y="190">Parallel</text>
        <text x="130" y="77">Read A: 4 ms</text><text x="370" y="117">Read B: 4 ms</text>
        <text x="130" y="192">Read A: 4 ms</text><text x="130" y="232">Read B: 4 ms</text>
        <text x="120" y="292" text-anchor="middle">0 ms</text>
        <text x="360" y="292" text-anchor="middle">4 ms</text>
        <text x="600" y="292" text-anchor="middle">8 ms</text>
      </g>
    </svg>
  </div>
  <figcaption>Illustrative independent reads finish at 8 ms serially or 4 ms in parallel,
    assuming no contention or scheduling overhead.</figcaption>
</figure>
```

## Add interaction when it answers a question

Read [the interaction examples](interactions.md) for process steps, before/after switching, or
parameter controls. Use a static figure when the reader needs to see all cases at once.

## Check the explanation

Compare the figure to its sources, not only to its caption. Follow one normal case and a relevant
boundary or failure case when the claim covers them. Confirm that direction, order, quantities,
and omissions support the claim. Then inspect normal and narrow widths in both themes. Check that
labels fit, arrowheads meet their intended endpoints, and comparisons retain a common scale.
