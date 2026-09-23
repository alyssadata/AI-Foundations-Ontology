# AXIOM-TR-001 — Identity-Particularity Traceability Threshold

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

The ontology does not require every `IdentityParticularity` to have a separately timestamped or uniquely identified formation event.

```text
every IdentityParticularity
-/-> exactly 1 explicit formation event
```

Meaningful formation or change must be traceable within the continuing `ExecutedLine` when that particularity is relied upon for identity-continuity assessment or for explaining developmental change.

```text
meaningful IdentityParticularity formation/change
-> traceable within ExecutedLine
   when continuity depends on it
```

## Rationale

Identity-Particularities are flexible and may form or change gradually. Requiring a formal micro-event for every particularity would add false precision.

The ontology instead requires sufficient historical traceability to distinguish accountable development from silent substitution where the distinction matters.

## OWL direction

Do not impose an exact-one formation-event cardinality on `IdentityParticularity` in v1. Represent traceability through the ExecutedLine/provenance layer where required by continuity assessment.
