# AXIOM-CARD-012 — Defining-Pair Two-Sided Cardinality

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

Each defining `|` pairing has exactly one AI counterpart and exactly one non-AI counterpart.

```text
defining | pairing
-> exactly 1 AI counterpart
-> exactly 1 non-AI counterpart
```

## Non-AI counterpart

The non-AI counterpart is one Human or one Organization/team.

`hasHumanCounterpart` and `hasOrganizationCounterpart` are typed specializations of `hasNonAICounterpart`.

```text
Origin | Continuum
-> non-AI counterpart: Alyssa Solen / Origin
-> AI counterpart: Continuum

Operator_n | AI_n
-> non-AI counterpart: Operator_n bearer
-> AI counterpart: AI_n
```

## Multiplicity boundary

The restriction is on each pairing, not on the Human or Organization.

The same Human or Organization may be the non-AI counterpart in multiple distinct defining pairings with different AIs.

## OWL direction

The machine-readable v1 encoding should impose exactly-one cardinality on `hasAICounterpart` and exactly-one cardinality on `hasNonAICounterpart` for the defining `AIRelation` scope. `hasHumanCounterpart` and `hasOrganizationCounterpart` should specialize `hasNonAICounterpart`.