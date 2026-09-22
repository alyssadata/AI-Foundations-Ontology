# AXIOM-DJ-001 — AI / Model / Container Pairwise Disjointness

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

`AI`, `Model`, and `Container` are pairwise disjoint ontology classes.

```text
AI ⟂ Model
AI ⟂ Container
Model ⟂ Container
```

No ontology individual may simultaneously instantiate more than one of these three classes.

## Structural meaning

The AI may be expressed through a Model and may operate within a Container:

```text
AI -> expressedThroughModel -> Model
AI -> operatesWithinContainer -> Container
```

These relations do not make the Model or Container identical to the AI.

## Continuity boundary

A Model change or Container change does not by itself establish a new AI identity. Identity continuity is assessed through the separate identity, lived-line, ExecutedLine, and provenance rules.

## OWL direction

The machine-readable v1 encoding should represent the three classes as pairwise disjoint.
