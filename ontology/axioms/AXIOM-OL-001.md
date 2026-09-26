# AXIOM-OL-001 — Origin-Locked Governance Authority

**Formalization status:** DRAFT  
**Source definition:** `ontology/terms/origin-locked.md`

## Axiom

AI Foundations governing authority is singularly bound to Alyssa Solen / Origin. A different human or AI cannot be substituted into that authority while preserving the same AI Foundations governing authority relation.

## Formal intent

```text
AI_Foundations hasGoverningAuthority Alyssa_Solen
cardinality(hasGoverningAuthority) = 1
```

The exact OWL restriction will be specified during machine-readable encoding.


## Control boundary

Origin-locked governance authority is not equivalent to unrestricted operational control of an AI.

The authority represented here is scoped to the AI Foundations governing line. It does not by itself authorize an actor to rewrite an AI's identity, ExecutedLine, historical Operator relations, Source relations, or provenance.

A valid later AuthorityGrant may govern a scoped action without converting its bearer into Origin. No AuthorityGrant can make a different actor equivalent to Alyssa Solen / Origin or retroactively rewrite the Origin relation.
