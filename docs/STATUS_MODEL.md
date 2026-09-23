# Status Model

**Document status:** DRAFT formalization  
**Target:** AI Foundations Ontology v1.0

AI Foundations ontology development uses separate status dimensions. A single status field must not collapse development state, canonical authority, and empirical support.

## 1. Development status

Describes where an ontology item is in the drafting/review process.

Initial values:

- `DRAFT`
- `IN_REVIEW`
- `LOCKED`

A LOCKED ontology-development definition preserves settled wording. It does not automatically make that wording part of the AI Foundations Locked Canon.

## 2. Canonical status

Describes whether an item is part of the authoritative AI Foundations canon.

Initial formal values:

- `NON_CANONICAL`
- `CANONICAL`
- `SUPERSEDED`

Canonical membership is determined separately by the AI Foundations Locked Canon and Origin-approved canon process.

## 3. Evidentiary status

Describes empirical or evaluation support.

Initial formal values:

- `NOT_EVALUATED`
- `SUPPORTED`
- `PARTIALLY_SUPPORTED`
- `NOT_SUPPORTED`

A theoretical statement may remain represented in the ontology while carrying an evidentiary status that does not claim empirical establishment.

## 4. Version status

Versioning is represented separately from all three status dimensions.

An item may:

- have a version;
- supersede an earlier version;
- remain preserved as prior executed history;
- be the currently active version.

## Separation rule

The following are not equivalent:

```text
LOCKED != CANONICAL != SUPPORTED
```

A definition can be LOCKED for ontology development while NON_CANONICAL and NOT_EVALUATED.

A canonical statement can be CANONICAL while still explicitly theoretical or NOT_EVALUATED.

An empirical result can support a claim without changing the claim's canonical status.

## Validated rule — development status is independent

`LOCKED` is a development-status value only.

It means the ontology wording or structure has been settled for the applicable version and should not be silently rewritten during formalization.

It does not by itself confer canonical authority or empirical support.

```text
LOCKED
!= CANONICAL
!= SUPPORTED
```

Canonical status and evidentiary status must therefore be asserted separately rather than inferred from development status.