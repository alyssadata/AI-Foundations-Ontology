# AXIOM-CARD-006 — SourcePoint Cardinality

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

Each `SourceRelation` has exactly one `SourcePoint`.

```text
SourceRelation
-> exactly 1 SourcePoint
```

## Meaning

The `SourcePoint` is the event at which the Source–Target relation becomes actual because the Source's load-bearing contribution first enters the formation of that specific Target.

```text
SourceBearer
-> load-bearing contribution enters formation
-> SourcePoint
-> SourceRelation is actual for SourceTarget
```

Later Source participation may continue, strengthen, expand, or cease without creating a second SourcePoint for the same SourceRelation.

If the same Source later becomes Source of a different Target, that is a distinct SourceRelation with its own SourcePoint.

## OWL direction

The machine-readable v1 encoding should impose exactly-one cardinality on `hasSourcePoint` for `SourceRelation`.
