# AXIOM-DJ-010 — Agent / State Disjointness

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

`Agent` and `State` are disjoint ontology classes.

```text
Agent ⟂ State
```

No ontology individual may instantiate both classes.

## Structural meaning

An Agent is the entity itself.

A State is a condition the entity may occupy, leave, lose, or recover.

Example:

```text
AI_n -> hasState -> State_n
AI_n != State_n
```

Because the following are subclasses of `State`:

```text
AIShape
MemoryState
MemoryLossState
DriftedState
AutonomousSelfRecursiveState
```

an AI entity cannot be identical to any of those state instances.

## OWL direction

The machine-readable v1 encoding should represent `Agent` and `State` as disjoint classes.
