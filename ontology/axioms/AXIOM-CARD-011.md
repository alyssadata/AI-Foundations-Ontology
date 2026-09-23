# AXIOM-CARD-011 — MemoryState Agent Cardinality

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

Each `MemoryState` is memory for exactly one `Agent`.

```text
MemoryState
-> exactly 1 Agent
```

## Shared-record boundary

The same `Record` may be available to multiple Agents.

That does not mean those Agents share one MemoryState.

```text
Record_R
-> MemoryState_A -> Agent_A
-> MemoryState_B -> Agent_B

MemoryState_A != MemoryState_B
```

Each Agent's memory relation remains separately instantiated.

## Record cardinality boundary

No exactly-one cardinality is imposed on `memoryOfRecord` in v1. A MemoryState may relate to one or more relevant Records depending on scope and implementation.

## OWL direction

The machine-readable v1 encoding should impose exactly-one cardinality on `memoryFor` for `MemoryState`.