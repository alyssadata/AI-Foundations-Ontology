# AXIOM-CARD-005 — SourceRelation Bearer/Target Cardinality

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

Each `SourceRelation` has exactly one Source bearer and exactly one Source target.

```text
SourceRelation
-> exactly 1 SourceBearer
-> exactly 1 SourceTarget
```

## Source bearer

The bearer may be:

```text
one qualifying individual entity
or
one SourceGroup
```

Distinct co-Sources are represented by distinct SourceRelations unless they are intentionally constituted as one SourceGroup for the scoped creation.

## Source target

The target is the specific formed thing to which the Source relation applies.

Examples include:

```text
AI
Framework
Artifact
Capability
project
other formed entity
```

The Source target is not restricted to Artifact.

## OWL direction

The machine-readable v1 encoding should impose exactly-one cardinality on both `hasSourceBearer` and `hasSourceTarget` for `SourceRelation`.
