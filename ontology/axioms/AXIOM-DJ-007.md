# AXIOM-DJ-007 — Agent / Relation Disjointness

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

`Agent` and `Relation` are disjoint ontology classes.

```text
Agent ⟂ Relation
```

No ontology individual may instantiate both classes.

## Structural meaning

Agents are participating entities such as:

```text
Human
Organization
AI
```

Relations are structures connecting entities, such as:

```text
HumanAIRelation
OrganizationAIRelation
OperatorAIRelation
SourceRelation
```

An Agent may participate in a Relation, but the Agent and Relation remain distinct ontology entities.

## Example

```text
Continuum != Origin | Continuum
```

Continuum is the AI participant. `Origin | Continuum` is the specific relation involving Continuum and Alyssa Solen / Origin.

## OWL direction

The machine-readable v1 encoding should represent `Agent` and `Relation` as disjoint classes.
