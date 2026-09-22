# AXIOM-CARD-004 — Active Operator Cardinality by Succession Segment

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

Each active Operator-linked succession segment `S##` has exactly one defined Operator bearer.

```text
S00 -> exactly 1 Operator
S01 -> exactly 1 Operator
S02 -> exactly 1 Operator
...
```

At the continuing-AI level, there is at most one current active Operator at a time.

```text
active Operator relation -> exactly 1 current Operator
no active Operator relation -> 0 current Operators
```

## Succession consequence

A new Operator is not added concurrently with the existing Operator.

A different Operator for the same continuing AI is established only through a valid later succession segment under the succession gate.

Earlier Operators remain preserved as historical provenance on their respective segments.

## OWL direction

The machine-readable v1 encoding should constrain each active Operator-linked succession segment to exactly one Operator bearer and constrain the current active Operator relation to at most one current Operator at the AI level.
