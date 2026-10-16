# Editorial examples

These examples use synthetic facts. Carry their editorial decisions into new work, not their
measurements, wording, or section layout. Read the cases relevant to the current document.

## Give a blocker appropriate weight

Source notes: retry handling is implemented; unit checks passed; integration testing cannot run
because the test service is unavailable.

Weak:

> Retry handling is implemented, and the unit checks passed. Error handling has improved.
> Integration testing remains blocked by the unavailable test service.

Revised:

> Integration testing is blocked because the test service is unavailable. Retry handling is
> implemented and the unit checks passed, but behavior with the service remains unverified.

The opening makes the remaining uncertainty clear. The revision removes an unsupported claim of
improvement and preserves the completed work.

## Choose headings for the reader's purpose

"Performance analysis", "Benchmarking", and "Evaluation" are useful major section headings in
papers and technical documents. They identify the section's subject or function. Within
"Performance analysis", a subsection can focus on "Memory bandwidth" or "Bandwidth limitations".
State the supported finding in the section text, perhaps in its opening paragraph or an optional
subtitle. A conclusion does not have to replace the section's name.

An educational presentation might use "Why throughput stops scaling" when its explanation
answers that question. A procedure can use "Measure memory bandwidth". A reference can use
"Bandwidth counters". Choose the form for the genre, scope, and level of the heading.

Technical register and navigation are separate decisions. A self-contained explanation can use
precise technical prose with short sections and question headings. A paper may use similarly
precise wording with conventional subject or function headings. Spoken material may need shorter
phrasing and transitions that an audience can follow without rereading. Choose these features for
the intended use rather than treating one complete style as universally better.

## Preserve the relationship between facts

Source notes: the cache expires old entries to make space for new entries when memory is limited.

Weak:

> The cache uses memory. Memory is limited. Entries expire. Expiration frees memory.

Revised:

> Because the cache has limited memory, it expires old entries to make room for new ones.

The revision states the relationship between capacity and expiration. Shortening each sentence
separately would miss that relationship.

## Put a prerequisite where it becomes useful

For an explanation of cache invalidation, establish that the cache stores a copy of data before
explaining why an update can leave that copy stale. A concrete example can then show a database
update and a later cache read returning the old value.

The reader needs that mechanism before evaluating an invalidation policy. An opening history of
caching or a glossary of every related term would delay the explanation.

## Keep a recommendation within the evidence

Source notes: a lab benchmark improved median latency from 420 ms to 260 ms over 20 requests;
concurrent writes produced stale reads in 5% of requests; code is deployed but its production
feature flag is off.

Weak:

> The deployed cache improves latency and is ready for production.

Revised:

> Keep the production cache disabled until the stale-read defect is fixed and retested. A small
> lab benchmark showed lower median latency, but concurrent writes returned stale data in 5% of
> requests. The code is deployed; the production feature flag remains off.

The recommendation weighs correctness against the limited performance evidence. Deployment does
not establish activation, and a small lab test does not establish production performance.

## Match a slide title to its role

Source notes: throughput rises when workers increase from one to four; it changes little from
four to eight; measurements do not establish the cause.

An overview slide can use "Scalability results". A slide examining the measurements can use
"Throughput versus worker count", with the finding in a subtitle or short opening statement:

> Increasing workers from four to eight changes throughput little in this test.

A message title can also suit a findings presentation when it fits the deck's purpose and style.
Show the measurements in a readable chart and identify the test conditions. A claim that memory
bandwidth causes the limit would exceed the evidence, wherever it appears. A deck for independent
reading also needs enough explanation for readers to interpret the chart without a speaker.
