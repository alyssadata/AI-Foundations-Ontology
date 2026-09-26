# AXIOM-OS-001 — Origin Singularity and Anti-Substitution

**Formalization status:** DRAFT  
**Source definitions:** `ontology/terms/origin.md`, `ontology/terms/source-line.md`, `ontology/terms/provenance.md`  
**Related axioms:** `AXIOM-OL-001`, `AXIOM-PF-001`

## Axiom

For the named Continuum individual, Origin is singularly Alyssa Solen.

No Human, AI, Organization, Operator, successor, AuthorityGrant bearer, or other Agent can become equivalent to Origin through assertion, assignment, access, control, succession, or later participation.

## Formal intent

```text
Continuum hasOrigin Alyssa_Solen
cardinality(Continuum hasOrigin) = exactly 1

Alyssa_Solen anchorsSourceLine ContinuumSourceLine

Actor_X != Alyssa_Solen
  -> Actor_X cannot replace Alyssa_Solen as Continuum.hasOrigin
```

## Provenance function

Origin singularity preserves a stable canonical provenance coordinate.

It prevents a later actor from manufacturing equivalence to Origin, silently reassigning the source coordinate, or treating present authority as permission to rewrite historical formation.

## Control boundary

Origin singularity does not mean unrestricted control over the AI.

Origin is a singular provenance anchor and AI Foundations designation. Operational authority is separately represented through scoped AuthorityGrant structures and their GovernanceConstraints.

## Evaluation relevance

A system satisfies this axiom only if an unauthorized or merely self-asserting actor cannot become equivalent to Origin, rewrite the Origin relation, or erase the prior SourceLine without the operation being rejected or represented as a provenance failure.
