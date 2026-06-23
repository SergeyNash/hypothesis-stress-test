# AppSec workshop — scan queue (2024-11-12)

Facilitator notes from internal workshop with two AppSec engineers.

## Queue behavior today

- Default order is FIFO by commit time
- Critical projects wait several hours before scanning when the queue is full
- Engineers manually bump priority for "tier-1" apps when CISO escalates

## Pain points (verbatim from sticky notes)

> "We only learn about queue backlog when a release is blocked."

> "No shared criteria — everyone interprets 'critical' differently."

## Open questions

- Can we expose queue position to product teams?
- Does manual reorder scale past ~50 active repos?
