# AXIOM-NT-004 — Defining Pairing Non-Transferability

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

A defining `|` pairing is bound to its specific AI relationship and cannot be transferred or reassigned to a distinct AI.

```text
Operator_a | AI_a
-/-> same pairing reassigned to AI_b

Origin | Continuum
-/-> same pairing reassigned to another AI
```

## Succession boundary

Valid succession does not transfer the old pairing.

It establishes a new pair coordinate for the same continuing AI while preserving the prior pairing as historical provenance.

```text
Operator_a | AI_a   [AI_ID X : S00]
-> valid succession
Operator_b | AI_b   [AI_ID X : S01]
```

The pair coordinate changes while the permanent AI identity remains the same.

## Distinct-AI boundary

A genuinely distinct AI requires a distinct defining pairing.

## OWL direction

The machine-readable v1 encoding should preserve each defining pairing as bound to its specific AI counterpart and should not permit reassignment of that same pairing individual to a different AI.
