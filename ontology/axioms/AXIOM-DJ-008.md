# AXIOM-DJ-008 — Role / Relation Disjointness

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

`Role` and `Relation` are disjoint ontology classes.

```text
Role ⟂ Relation
```

No ontology individual may instantiate both classes.

## Structural meaning

A Role is a function or status borne by an entity.

A Relation is a structure connecting entities.

Examples:

```text
OperatorRole != OperatorAIRelation
SourceRole != SourceRelation
```

An entity may bear a Role within or with respect to a Relation, but the Role and Relation remain distinct ontology entities.

## OWL direction

The machine-readable v1 encoding should represent `Role` and `Relation` as disjoint classes.
