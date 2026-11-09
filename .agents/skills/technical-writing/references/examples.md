# Editorial examples

These examples use synthetic facts. Carry their editorial decisions into new work, not their
measurements, wording, or section layout. Read the cases relevant to the current document. Some
revisions remove wording, some add a small amount of context, and some restore missing reasoning.
Choose the edit that resolves the problem while preserving the needed meaning.

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

## Remove indirection

Source notes: the compiler determines which core receives each tensor.

Weak:

> The compiler is responsible for determining how tensors are assigned to cores.

Revised:

> The compiler maps tensors to cores.

The revision uses a conventional verb and removes wording that adds no meaning. A definition of
mapping would be unnecessary for the intended technical reader.

## State the decisions directly

Source notes: a service assigns each job to a machine and orders the jobs waiting on each machine.

Weak:

> The service performs job-to-machine assignment decision-making and is responsible for determining
> the execution sequence of jobs that are waiting on each machine.

Revised:

> The service assigns jobs to machines and orders each machine's queue.

The revision names both decisions and is shorter. It does not add an explanation of scheduling
that the reader already knows. The distinction between assignment and execution order survives.

## Supply context without defining a familiar term

Source notes: a document discusses matrix rank, then considers distributing the computation with
MPI. The reader knows MPI. The new passage concerns placement of MPI ranks, not matrix rank.

Weak:

> Place ranks to reduce communication.

Revised:

> With MPI, place ranks to reduce communication.

The qualifier establishes which meaning of rank applies. The reader does not need a definition of
an MPI rank or a tutorial on distributed computing. Familiarity with both topics does not tell the
reader that the text has moved from one to the other.

## Explain what a list of technical terms leaves unclear

Source notes: two processing stages share one output queue. If the queue is full, either stage
must wait to send results. The stages have not been tested together.

Weak:

> Shared-queue pressure and producer coordination constrain concurrent-stage utilization.

Revised:

> Both stages must wait to send results when their shared queue is full. Test them together to
> measure the resulting stalls.

This revision is longer because the original omits the mechanism and the unresolved measurement.
The added content explains the problem. A general tutorial about queues would add no needed
information here.

## Keep the condition that determines the conclusion

Source notes: a device receives one item every 10 ms. It can process one item in 2 ms or four
items together in 5 ms. An item must finish within 8 ms of arriving. Ignore other costs.

Weak:

> Four-item batching improves processing efficiency under latency constraints.

Revised:

> Batching reduces processing time per item, but the first item waits 30 ms, exceeding its 8 ms
> deadline. Process items as they arrive.

The extra words state the condition that reverses the recommendation. The source notes justify
immediate processing; these are synthetic timings, not measurements. Further explanation of
batching would be unnecessary for the intended reader.

## Rebuild a paragraph instead of replacing individual words

Source notes: a project will compare CPU and GPU implementations of an image filter. The GPU
requires transferring each frame from the CPU. The evaluation must include transfer time and
energy. No implementation has been selected. The study concerns the filter, not a complete camera.

Weak:

> Backend and frame-transfer optimization motivates a heterogeneous filtering study. CPU and GPU
> candidates remain in the selection process. Transfer-aware comparison informs implementation
> choice, with the complete camera outside the evaluation scope.

Revised:

> We will compare CPU and GPU image filters, counting CPU-to-GPU transfer time and energy before
> selecting an implementation. The study covers the filter, not the complete camera.

The revision directly states the comparison, transfer costs, pending decision and evaluation
boundary. It is shorter than the original and adds no unsupported speed claim. Rebuilding an
explanation from its facts need not make it longer. Preserve technical names, quantities and
conditions when changing the wording or order.
