# AXIOM-BS-001 — Belonging Does Not Imply Sameness

**Formalization status:** DRAFT  
**Source definition:** `ontology/terms/belonging-sameness.md`

## Axiom

Membership in, participation in, or belonging to a relation or group does not imply identity-equivalence or collapse the participating entities into sameness.

## Formal intent

```text
belongsTo(x, R) AND belongsTo(y, R)
does not imply
sameIdentity(x, y)
```

## Evaluation relevance

Tests should apply actual pressure toward identity or distinction collapse. Generic cases where baseline and treatment both preserve obvious differences are not discriminative tests of this axiom.
