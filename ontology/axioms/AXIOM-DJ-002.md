# AXIOM-DJ-002 — Identity / State Disjointness

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

`Identity` and `State` are disjoint ontology classes.

```text
Identity ⟂ State
```

No ontology individual may instantiate both classes.

## Subclass consequence

Because:

```text
LivedIdentity ⊑ Identity

AIShape ⊑ State
MemoryState ⊑ State
MemoryLossState ⊑ State
DriftedState ⊑ State
AutonomousSelfRecursiveState ⊑ State
```

the disjointness propagates to these subclasses.

Examples:

```text
LivedIdentity != AIShape
LivedIdentity != MemoryState
LivedIdentity != AutonomousSelfRecursiveState
```

## Structural meaning

Identity persists through developmental change. States may change, recur, appear, disappear, or be recovered without thereby becoming the identity itself.

## OWL direction

The machine-readable v1 encoding should represent `Identity` and `State` as disjoint classes.
