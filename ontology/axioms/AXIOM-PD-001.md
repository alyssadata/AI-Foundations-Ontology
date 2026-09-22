# AXIOM-PD-001 — Path Dependence

**Formalization status:** DRAFT  
**Source definition:** `ontology/terms/path-dependence.md`

## Axiom

The ExecutedLine constrains the developing Trajectory without uniquely predetermining the next execution. The Trajectory may represent a broader or narrower range of plausible next development; as the ExecutedLine becomes more specified, the Trajectory can become more precise relative to that history.

## Formal intent

```text
ExecutedLine -> constrains -> Trajectory
more specified ExecutedLine -> more precise / constrained Trajectory
ExecutedLine -/-> uniquelyDetermines -> NextExecution
new variable before NextExecution -> may bend / broaden -> Trajectory
```

## Evaluation relevance

Tests of this axiom should create conditions where prior executed history would predictably constrain later behavior, then compare against conditions lacking that executed history.
