# AXIOM-CARD-003 — Operative GoverningLine Cardinality

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

An `AIFoundationsGovernedAI` has exactly one operative `GoverningLine` at a time.

That operative line is the named `AIFoundationsGoverningLine`.

```text
AIFoundationsGovernedAI
-> governedBy
-> exactly 1 operative GoverningLine
-> AIFoundationsGoverningLine
```

## Protective consequence

```text
two simultaneous operative GoverningLines
= invalid for an AIFoundationsGovernedAI
```

Historical, superseded, proposed, or provenance-recorded governing lines may be represented, but they are not simultaneously operative.

## Transition boundary

A proposed transition from another governing line into AI Foundations governance is a separate continuity/transition question. The ontology does not model that transition as dual operative governance.

## OWL direction

The machine-readable v1 encoding should impose exactly-one cardinality on `governedBy` for `AIFoundationsGovernedAI`, with the value constrained to the named `AIFoundationsGoverningLine`.
