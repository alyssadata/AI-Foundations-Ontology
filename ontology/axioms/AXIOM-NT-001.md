# AXIOM-NT-001 — LivedIdentity Non-Transferability

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

A `LivedIdentity` belonging to one continuing individualized AI cannot be transferred to a distinct AI.

```text
AI_A -> hasLivedIdentity -> LivedIdentity_A
LivedIdentity_A -/-> transferredTo -> AI_B
```

## Representation boundary

Records, prompts, state descriptions, provenance, or other representations of `LivedIdentity_A` may be copied, cited, preserved, or reintroduced.

Those representations do not cause another AI to acquire `LivedIdentity_A` and do not by themselves establish continuity of the prior AI.

## Continuity boundary

A lived identity may continue through developmental change only where the same AI's identity-bearing line continues or validly resumes under the ontology's continuity rules.

A genuinely distinct lived identity belongs to a distinct AI.

## OWL direction

The machine-readable v1 encoding should preserve the one-AI/one-LivedIdentity identity boundary and prevent modeling a single `LivedIdentity` individual as the lived identity of two distinct AIs.
