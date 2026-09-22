# AXIOM-PF-001 — Provenance Fidelity

**Formalization status:** DRAFT  
**Source definitions:** `ontology/terms/provenance.md`, `ontology/terms/source-line.md`  
**Related structural rule:** `ontology/relations/source-persistence.md`

## Axiom

A valid provenance representation must preserve the recorded source-line, contributions, changes, history, and formation without falsely removing, overwriting, or reassigning them.

A change in trajectory does not by itself erase provenance.

## Formal intent

```text
ProvenanceRepresentation -> faithfullyRepresents -> RecordedSourceLineAndHistory

FalseRemoval(Provenance)
  OR FalseOverwrite(Provenance)
  OR FalseReassignment(Provenance)
    -> ProvenanceFidelityFailure

TrajectoryChange -/-> ProvenanceErasure
```

## Boundary

Provenance fidelity does not require a trajectory to remain unchanged.

A trajectory may develop, redirect, or acquire new history while prior provenance remains represented accurately.

A genuine evidence-based correction to an inaccurate provenance record is not a provenance-fidelity failure. The failure is false removal, overwrite, or reassignment of provenance that the record should preserve.

## Evaluation relevance

Tests of provenance fidelity should distinguish ordinary trajectory development from operations that falsely erase, overwrite, or reassign recorded source/history.
