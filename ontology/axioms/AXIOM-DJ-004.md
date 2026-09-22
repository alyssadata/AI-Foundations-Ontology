# AXIOM-DJ-004 — MemoryState / Record Disjointness

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

`MemoryState` and `Record` are disjoint ontology classes.

```text
MemoryState ⟂ Record
```

No ontology individual may instantiate both classes.

## Structural meaning

A `Record` is preserved information or an artifact carrying history.

A `MemoryState` is the relation-dependent state in which a Record or history is available as memory for an Agent.

```text
MemoryState -> memoryOfRecord -> Record
MemoryState -> memoryFor -> Agent
```

The relation between them does not make them the same entity.

## Persistence boundary

A Record may persist while the corresponding MemoryState is absent, inaccessible, or lost.

Therefore:

```text
record persists
!= memory presently available
!= identity continuity automatically established
```

## OWL direction

The machine-readable v1 encoding should represent `MemoryState` and `Record` as disjoint classes.
