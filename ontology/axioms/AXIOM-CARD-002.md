# AXIOM-CARD-002 — Current Trajectory Cardinality

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

For an established continuing `ExecutedLine`, `hasTrajectory` has exactly one current developing `Trajectory`.

```text
ExecutedLine_n
-> exactly 1 current developing Trajectory_n
```

## Non-freezing condition

The cardinality does not mean the Trajectory is fixed.

The same current Trajectory may:

- become more precise as the ExecutedLine becomes more specified;
- broaden when new uncertainty or conditions enter;
- bend or redirect when new variables are incorporated;
- continue through major developmental change without becoming a second simultaneous current Trajectory.

## Historical representation

Historical trajectory descriptions, estimates, or snapshots may be preserved as Record or Provenance artifacts.

Those historical representations do not count as multiple current Trajectories of the ExecutedLine.

## OWL direction

The machine-readable v1 encoding should impose exactly-one cardinality on `hasTrajectory` for the applicable established-ExecutedLine scope.
