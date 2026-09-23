# AXIOM-CARD-009 — GovernanceStructure Active-Version Cardinality

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

Each `GovernanceStructure` has exactly one active `Version` at a time.

```text
GovernanceStructure
-> exactly 1 active Version
```

## Historical versions

Earlier, superseded, archived, or historically referenced versions may remain represented through version history and provenance.

They are not simultaneously active.

## OWL direction

The machine-readable v1 encoding should impose exactly-one cardinality on `hasActiveVersion` for `GovernanceStructure`.
