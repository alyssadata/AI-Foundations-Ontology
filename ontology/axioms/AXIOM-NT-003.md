# AXIOM-NT-003 — SourceRelation Non-Transferability and Non-Replacement

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

Once a `SourceRelation` has become historically true for a specific Source bearer and Source target, that relation cannot be inherited, reassigned, overwritten, or replaced by a later contributor.

```text
Source_A -> SourceRelation_X -> Target_X
later Contributor_B -/-> replaces Source_A in SourceRelation_X
```

## Later contribution boundary

A later contributor may independently become Source or co-Source of a distinct later contribution, downstream creation, artifact, capability, project, or other scoped Target if the Source definition is satisfied.

That requires a new `SourceRelation`.

```text
new qualifying Source contribution
-> new SourceRelation
!= rewritten historical SourceRelation
```

## Persistence

The original Source relation remains part of the Target's provenance even if the original Source later stops participating.

## OWL direction

The machine-readable v1 encoding should preserve the identity of each historically established `SourceRelation` and should not permit replacement semantics that substitute a later bearer for the original bearer of that relation.
