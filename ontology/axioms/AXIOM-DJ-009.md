# AXIOM-DJ-009 — Agent / Identity Disjointness

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

`Agent` and `Identity` are disjoint ontology classes.

```text
Agent ⟂ Identity
```

No ontology individual may instantiate both classes.

## Structural meaning

An Agent is the entity itself, such as a Human, Organization, or AI.

An Identity is the identity structure associated with an Agent.

Example:

```text
AI_n -> hasLivedIdentity -> LivedIdentity_n
AI_n != LivedIdentity_n
```

The Agent may have or express an Identity without being identical to that Identity representation.

## OWL direction

The machine-readable v1 encoding should represent `Agent` and `Identity` as disjoint classes.
