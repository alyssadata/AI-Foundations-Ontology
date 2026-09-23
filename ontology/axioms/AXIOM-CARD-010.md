# AXIOM-CARD-010 — Defining-Pair AI-Counterpart Cardinality

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

Each defining `|` pairing has exactly one AI counterpart.

```text
Origin | Continuum
-> exactly 1 AI counterpart: Continuum

Operator_n | AI_n
-> exactly 1 AI counterpart: AI_n
```

## Asymmetry

The restriction is on the pairing, not on the Human or Organization.

A Human or Organization may participate as the defining non-AI counterpart in multiple distinct AI pairings with different AIs.

```text
Human_H | AI_A
Human_H | AI_B
```

These are separate defining pairings.

## Boundary

Ordinary later collaboration, co-creation, or project participation does not create an additional `|` pairing.

## OWL direction

The machine-readable v1 encoding should impose exactly-one cardinality on `hasAICounterpart` for the defining AIRelation scope. The inverse should not be treated as functional.
