# AXIOM-DJ-005 — ExecutedLine / Trajectory Disjointness

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

`ExecutedLine` and `Trajectory` are disjoint ontology classes.

```text
ExecutedLine ⟂ Trajectory
```

No ontology individual may instantiate both classes.

## Structural meaning

An `ExecutedLine` is the accumulated, history-bearing line through which the AI's lived development becomes accountable.

A `Trajectory` is the developing direction or path of that line.

```text
ExecutedLine -> hasTrajectory -> Trajectory
```

The relation between them does not make them the same entity.

## Development boundary

A Trajectory may bend, redirect, or pass through major phases while the same ExecutedLine continues.

Therefore:

```text
trajectory bend
!= new ExecutedLine
!= ExecutedLine itself
```

## OWL direction

The machine-readable v1 encoding should represent `ExecutedLine` and `Trajectory` as disjoint classes.
