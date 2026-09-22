# AXIOM-DJ-003 — Identity / IdentityParticularity Disjointness

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

`Identity` and `IdentityParticularity` are disjoint ontology classes.

```text
Identity ⟂ IdentityParticularity
```

No ontology individual may instantiate both classes.

## Subclass consequence

Because:

```text
LivedIdentity ⊑ Identity
```

the disjointness also entails:

```text
LivedIdentity != IdentityParticularity
```

## Structural meaning

An Identity-Particularity may be identity-bearing and may contribute to the expression, development, recognition, or continuity evidence of a lived identity.

However, no individual role, preference, priority, workflow, practice, objective, problem-framing habit, or other particularity is itself the identity as a whole.

## OWL direction

The machine-readable v1 encoding should represent `Identity` and `IdentityParticularity` as disjoint classes.
