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
- `INDETERMINATE`

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
## Validated canonical status semantics

`SUPERSEDED` means an item was canonical historically but has been replaced by a later canonical version or statement.

```text
CANONICAL
-> later canonical replacement
-> SUPERSEDED
```

A superseded item remains preserved as canonical history and provenance. It is no longer the current operative canonical statement, but it does not become `NON_CANONICAL` merely because a later canonical version replaced it.

Therefore:

```text
SUPERSEDED
!= NON_CANONICAL
```
## Validated evidentiary semantics — `NOT_SUPPORTED`

`NOT_SUPPORTED` means an Evaluation was performed and the resulting Evidence did not support the Claim as currently formulated under the tested conditions.

```text
Claim formulation
+ Evaluation under specified conditions
+ Evidence does not support Claim
-> NOT_SUPPORTED
```

`NOT_SUPPORTED` does not by itself mean the Claim has been universally disproven or is necessarily false in every possible condition.

A `NOT_SUPPORTED` result may indicate, for example:

- the Claim is false;
- the Claim is too broad;
- the Claim is underspecified;
- the operational formulation is weak or mismatched;
- the Evaluation conditions did not adequately test the intended mechanism;
- the Claim may need tighter formulation before retesting.

Any revised Claim should be represented as a revised formulation/version rather than silently rewriting the evaluated Claim after the fact.
## Validated evidentiary semantics — `PARTIALLY_SUPPORTED`

`PARTIALLY_SUPPORTED` means the Evaluation produced Evidence supporting a proper subset of the Claim's predicted effect or structure, but not the Claim in full as formulated.

```text
Claim predicts A + B + C
Evidence supports A + B
Evidence does not establish C
-> PARTIALLY_SUPPORTED
```

The unsupported portion must remain explicit. Partial support must not be collapsed into `SUPPORTED` merely because some predicted behavior was observed.

A partially supported Claim may later be tightened, decomposed, or reformulated for more precise testing, while preserving the original Claim, Evaluation, and Evidence.
## Validated evidentiary semantics — `SUPPORTED`

`SUPPORTED` means the Claim, as formulated, received evidentiary support under the specified Evaluation conditions.

```text
Claim formulation
+ Evaluation under specified conditions
+ supporting Evidence
-> SUPPORTED
```

`SUPPORTED` does not mean the Claim has been universally proven true across all possible conditions, populations, implementations, or future evaluations.

The scope of support is bounded by the Claim formulation, Evaluation design, tested conditions, and produced Evidence.
## Validated evidentiary semantics — `NOT_EVALUATED`

`NOT_EVALUATED` means no qualifying Evaluation has yet produced an evidentiary result for the Claim.

```text
Claim
+ no qualifying evidentiary result yet
-> NOT_EVALUATED
```

`NOT_EVALUATED` does not imply that the Claim is weak, unsupported, false, or unlikely to be supported.

It records only that no evidentiary determination has yet been made.
## Validated version-status separation

Version state is independent of development, canonical, and evidentiary status.

```text
Version_2 supersedes Version_1
Version_1 remains preserved
Version_2 may be the active version
```

Being the active version means that version is currently operative for the applicable structure.

It does not by itself imply:

```text
ACTIVE VERSION = CANONICAL
ACTIVE VERSION = SUPPORTED
```

Canonical authority and evidentiary support must remain separately asserted.

## Step 6 closeout

The Status Model is reviewed for v1.

The four independent dimensions are:

1. development status;
2. canonical status;
3. evidentiary status;
4. version status.

No one dimension should be inferred automatically from another.
## Validated evidentiary semantics — `INDETERMINATE`

`INDETERMINATE` means an Evaluation was actually performed, but the resulting output does not permit a defensible determination of support, partial support, or non-support for the Claim.

```text
Evaluation performed
+ output/result exists
+ evidentiary interpretation is ambiguous, invalid, insufficient, or otherwise non-decisive
-> INDETERMINATE
```

`INDETERMINATE` is distinct from `NOT_EVALUATED` because an Evaluation did occur.

It is also distinct from `NOT_SUPPORTED` because the result does not justify a negative evidentiary judgment against the Claim.

The reason for indeterminacy should remain traceable with the Evaluation and its Evidence.