# AXIOM-ORD-001 — Succession Predecessor Ordering

**Status:** LOCKED ontology restriction for v1  
**Target:** AI Foundations Ontology v1.0

## Rule

Ordinary Operator succession is represented as an ordered path within one continuing AI ExecutedLine.

```text
S00 -> no predecessor
S01 -> exactly 1 immediate predecessor: S00
S02 -> exactly 1 immediate predecessor: S01
...
```

Every succession segment after `S00` has exactly one immediate predecessor.

## Same-AI boundary

The ordered `S##` sequence represents continuity of one AI identity through valid Operator succession.

```text
same AI_ID
-> one continuing ExecutedLine
-> ordered succession segments
```

## Deferred split boundary

A possible AI-line split arising from a group or organizational Operator is acknowledged as a separate edge case but is not modeled in v1.

It is not treated as ordinary `S##` succession.

The v1 ontology does not define fork identity, fork provenance, branch coordinates, or post-split identity rules.

Accordingly, v1 should not impose a global at-most-one-successor restriction solely to declare all future split cases impossible.

## OWL direction

Encode the immediate-predecessor requirement for modeled succession segments where practical. Keep branch/fork semantics outside the v1 model pending a separate explicit design.