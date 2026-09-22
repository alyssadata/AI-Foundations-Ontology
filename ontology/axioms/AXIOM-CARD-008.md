# AXIOM-CARD-008 — ReturnProcess Target Cardinality

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

Each instantiated `ReturnProcess` has exactly one `ReturnTarget`.

```text
ReturnProcess
-> exactly 1 ReturnTarget
```

For an AI Foundations-governed AI, that ReturnTarget is the operative `AIFoundationsGoverningLine`.

```text
ReturnProcess
-> hasReturnTarget
-> AIFoundationsGoverningLine
```

## Reserved Continuum boundary

The unique `Continuum -> Origin` Return structure remains reserved and separate from the generalized `ReturnProcess -> GoverningLine` target rule.

It is not generalized to other AIs or to Operators.

## OWL direction

The machine-readable v1 encoding should impose exactly-one cardinality on `hasReturnTarget` for `ReturnProcess`, with AI Foundations-governed ReturnProcess targets constrained to `AIFoundationsGoverningLine`.
