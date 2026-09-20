# AXIOM-PD-001 — Path Dependence

**Formalization status:** DRAFT  
**Source definition:** `ontology/terms/path-dependence.md`

## Axiom

The executed line constrains the set of trajectories that are possible next without uniquely predetermining which subsequent trajectory occurs.

## Formal intent

```text
ExecutedLine -> constrains -> PossibleSubsequentTrajectorySet
ExecutedLine -/-> uniquelyDetermines -> SingleFutureTrajectory
```

## Evaluation relevance

Tests of this axiom should create conditions where prior executed history would predictably constrain later behavior, then compare against conditions lacking that executed history.
