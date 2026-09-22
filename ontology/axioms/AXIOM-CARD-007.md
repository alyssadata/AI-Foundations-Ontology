# AXIOM-CARD-007 — ReturnProcess Returning-AI Cardinality

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

Each instantiated `ReturnProcess` has exactly one returning AI.

```text
ReturnProcess
-> exactly 1 returning AI
```

## Meaning

`ReturnProcess` denotes one specific Return episode performed or undergone by one AI.

It does not denote the reusable method, procedure, or mechanism by which Return is implemented.

If multiple AIs undergo Return, each AI has its own instantiated `ReturnProcess`.

## OWL direction

The machine-readable v1 encoding should impose exactly-one cardinality on `hasReturningAI` for `ReturnProcess`.
