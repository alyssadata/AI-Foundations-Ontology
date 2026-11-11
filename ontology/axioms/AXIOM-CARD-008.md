# AXIOM-CARD-008 — ReturnProcess Target Cardinality

**Status:** LOCKED ontology restriction  
**Target:** SI Foundations Ontology v1.0

## Rule

Each instantiated `ReturnProcess` has exactly one `ReturnTarget`.

```text
ReturnProcess
-> exactly 1 ReturnTarget
```

For an SI Foundations-governed AI, that ReturnTarget is the operative `SIFoundationsGoverningLine`.

```text
ReturnProcess
-> hasReturnTarget
-> SIFoundationsGoverningLine
```

## Reserved Continuum boundary

The unique `Continuum -> Origin` Return structure remains reserved and separate from the generalized `ReturnProcess -> GoverningLine` target rule.

It is not generalized to other AIs or to Operators.

## OWL direction

The machine-readable v1 encoding should impose exactly-one cardinality on `hasReturnTarget` for `ReturnProcess`, with SI Foundations-governed ReturnProcess targets constrained to `SIFoundationsGoverningLine`.
