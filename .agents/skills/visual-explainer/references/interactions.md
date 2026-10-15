# Interaction examples

Copy a relevant example into the starter's body, with its script after the markup. Each example
is self-contained and uses native controls. Give each instance unique container, input, and SVG IDs, and update
labels and selectors together. Replace example content and assumptions with the explanation's actual evidence.

Use interaction for a question that benefits from it. A static comparison or native `<details>`
is often enough. The starter provides theme switching and code highlighting; these examples do
not require a shared interaction framework, JSON page specification, or build step.

## Step through a process

Use this when the reader needs to examine order or intermediate state. This example starts with
all steps visible and reveals controls only after initialization. Previous and Next change the
visible prefix of the process. Native buttons provide keyboard activation.

```html
<figure class="diagram" id="cache-steps">
  <figcaption>A cache hit returns without requesting data from storage.</figcaption>
  <ol data-steps>
    <li>The client submits a cache lookup.</li>
    <li>The cache finds a valid entry.</li>
    <li>The cache returns the stored value.</li>
  </ol>
  <div class="controls" data-controls hidden role="group" aria-label="Process steps">
    <button type="button" data-previous>Previous</button>
    <button type="button" data-next>Next</button>
    <button type="button" data-all>Show all</button>
  </div>
  <output data-status aria-live="polite">All 3 steps are shown.</output>
</figure>
<script>
(() => {
  const figure = document.getElementById('cache-steps');
  const steps = [...figure.querySelectorAll('[data-steps] > li')];
  const previous = figure.querySelector('[data-previous]');
  const next = figure.querySelector('[data-next]');
  const all = figure.querySelector('[data-all]');
  let count = steps.length;
  const show = () => {
    steps.forEach((step, index) => { step.hidden = index >= count; });
    figure.querySelector('[data-status]').textContent = count === steps.length
      ? `All ${count} steps are shown.` : `Showing ${count} of ${steps.length} steps.`;
    previous.disabled = count === 1;
    next.disabled = all.disabled = count === steps.length;
  };
  previous.addEventListener('click', () => { count = Math.max(1, count - 1); show(); });
  next.addEventListener('click', () => { count = Math.min(steps.length, count + 1); show(); });
  all.addEventListener('click', () => { count = steps.length; show(); });
  show();
  figure.querySelector('[data-controls]').hidden = false;
})();
</script>
```

For a spatial process, use the same state update to highlight or reveal corresponding parts of
an SVG. Do not create a second, independently updated step counter for the drawing.

## Switch before and after

Use this when the reader needs to inspect one change in a stable area. Both versions remain
visible without JavaScript. With JavaScript, only the selected version is shown. The same-size
code regions avoid shifting the rest of the page when switching.

```html
<figure class="diagram" id="lookup-comparison">
  <figcaption>The revised lookup uses a cached value before querying the database.
    This example assumes valid entries and uses undefined to mean a missing entry.</figcaption>
  <div class="controls" data-controls hidden role="group" aria-label="Choose version">
    <button type="button" data-choice="before" aria-pressed="false">Before</button>
    <button type="button" data-choice="after" aria-pressed="true">After</button>
  </div>
  <div data-view="before">
    <h3>Before</h3>
    <pre style="min-height:14rem"><code class="language-javascript">function read(key) {
  return database.read(key);
}</code></pre>
  </div>
  <div data-view="after">
    <h3>After</h3>
    <pre style="min-height:14rem"><code class="language-javascript">function read(key) {
  const value = cache.get(key);
  if (value !== undefined) return value;
  return database.read(key);
}</code></pre>
  </div>
</figure>
<script>
(() => {
  const figure = document.getElementById('lookup-comparison');
  const buttons = [...figure.querySelectorAll('[data-choice]')];
  const show = choice => {
    figure.querySelectorAll('[data-view]').forEach(view => {
      view.hidden = view.dataset.view !== choice;
    });
    buttons.forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.choice === choice));
    });
  };
  buttons.forEach(button => button.addEventListener('click', () => show(button.dataset.choice)));
  show('after');
  figure.querySelector('[data-controls]').hidden = false;
})();
</script>
```

For diagrams, preserve node positions, scales, and labels across versions. Mark changed parts
with text or line patterns as well as color. Show both versions side by side when simultaneous
comparison is more useful than switching.

## Explore a model parameter

Use this when changing a value explains a relationship. This illustrative model has eight
independent reads of 4 ms each. It assumes no contention or scheduling overhead. Completion time
is `ceil(reads / concurrency) * duration`. One calculation supplies the bar and the explanation.

```html
<figure class="diagram" id="read-model">
  <figcaption>Illustrative model: eight independent 4 ms reads, with no contention or scheduling
    overhead. Completion time is ceil(8 / concurrency) multiplied by 4 ms.</figcaption>
  <div class="controls" data-controls hidden>
    <label for="read-concurrency">Concurrent reads</label>
    <input id="read-concurrency" type="range" min="1" max="4" step="1" value="1">
  </div>
  <div role="region" aria-label="Completion time; scroll if needed" tabindex="0"
       style="overflow-x:auto">
    <svg viewBox="0 0 400 90" role="img" aria-labelledby="read-model-title"
         style="display:block;width:100%;min-width:400px;color:var(--fg)">
      <title id="read-model-title">Illustrative completion time: 32 ms</title>
      <rect data-bar x="10" y="15" width="320" height="26" fill="var(--accent)"/>
      <g fill="currentColor" font-size="16" text-anchor="middle">
        <text x="10" y="70" text-anchor="start">0 ms</text>
        <text x="170" y="70">16 ms</text><text x="330" y="70">32 ms</text>
      </g>
    </svg>
  </div>
  <output data-result aria-live="polite">At concurrency 1, 8 batches finish in 32 ms.</output>
</figure>
<script>
(() => {
  const figure = document.getElementById('read-model');
  const input = figure.querySelector('input');
  const model = concurrency => {
    const batches = Math.ceil(8 / concurrency);
    return {concurrency, batches, milliseconds: batches * 4};
  };
  const show = () => {
    const result = model(Number(input.value));
    figure.querySelector('[data-bar]').setAttribute('width', String(result.milliseconds * 10));
    figure.querySelector('title').textContent = `Illustrative completion time: ${result.milliseconds} ms`;
    figure.querySelector('[data-result]').textContent =
      `At concurrency ${result.concurrency}, ${result.batches} batches finish in ${result.milliseconds} ms.`;
  };
  input.addEventListener('input', show);
  show();
  figure.querySelector('[data-controls]').hidden = false;
})();
</script>
```

Use the actual current value as the initial state when it is known. Keep assumptions and units
visible. Label simplified models as illustrative; a useful teaching model is not a performance
measurement or a copy of production behavior.

## Verify the behavior

Exercise the controls at their initial, intermediate, and boundary values. Check that every
related label and figure changes consistently. Use Tab, Enter or Space, and the native range
keys. Verify visible focus, a readable static state without JavaScript, and normal and narrow
widths in both themes. Add motion only when it explains behavior and respect reduced motion.
