# AXIOM-DJ-006 — Agent / Role Disjointness

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

`Agent` and `Role` are disjoint ontology classes.

```text
Agent ⟂ Role
```

No ontology individual may instantiate both classes.

## Structural meaning

Agents are entities such as:

```text
Human
Organization
AI
```

Roles are relation- or context-bound functions/statuses such as:

```text
OperatorRole
SourceRole
HumanParticipantRole
OtherUserRole
```

An Agent may bear a Role, but the bearer and the Role are not the same ontology entity.

## Example

```text
Organization_n -> bears -> OperatorRole
Organization_n != OperatorRole
```

## OWL direction

The machine-readable v1 encoding should represent `Agent` and `Role` as disjoint classes.
