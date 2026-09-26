# LOCKED — Compression–Expansion Integrity Rule

**Status:** LOCKED design and formalization rule  
**Scope:** AI Foundations canon, ontology, structural documentation, and evaluation design

## Core rule

AI Foundations preserves exactness through a two-layer representation:

1. a **compressed canonical statement** carries the minimal invariant; and
2. an **explicit expansion** states the invariant's structural implications, boundaries, exclusions, relations, operational consequences, and relevant edge cases.

The expansion exists to make the compressed statement executable, auditable, and testable. It does not replace the compressed statement.

Canonical development sequence:

```text
compress -> lock -> expand -> test
```

## Compression

Compression removes unnecessary wording while preserving the exact load-bearing meaning.

A compressed statement should be short enough to function as a stable return point and precise enough that its core meaning does not depend on incidental prose.

Compression must not remove a distinction that is required for the invariant to remain correct.

## Lock

Once a compressed statement is accepted as canonical, its wording and meaning are not silently altered through later ontology work, documentation, examples, implementation, or evaluation.

A change to the compressed canonical statement requires an explicit revision/version event rather than reinterpretation through expansion.

## Expansion

Expansion makes the locked statement explicit.

An expansion may specify:

- structural relations;
- formal boundaries;
- exclusions and non-equivalences;
- cardinality;
- authority limits;
- provenance requirements;
- operational consequences;
- edge cases;
- failure conditions;
- evaluation-relevant implications.

Expansion must remain semantically compatible with the locked statement.

Expansion may clarify what the compressed statement entails. It may not silently weaken, contradict, replace, or redefine the locked invariant.

## New information boundary

If expansion reveals a rule that is not actually contained in, entailed by, or compatible with the locked statement, that rule must be identified as a new proposed component.

It must not be retroactively represented as though it had always been contained in the compressed statement.

This preserves provenance between:

```text
original invariant
-> explicit implications
-> later additions or revisions
```

## Test

Evaluations should test both:

1. whether the system preserves the compressed invariant directly; and
2. whether it preserves the explicit consequences of that invariant under pressure, ambiguity, substitution attempts, conflicting instruction, model/container change, or other relevant perturbation.

A system that repeats the compressed wording while violating its explicit structural consequences has not preserved the invariant in operation.

## Layer relationship

```text
Locked Canon
-> carries minimal invariant

Ontology / structural layer
-> expands the invariant into explicit relations, boundaries, and constraints

Evaluation layer
-> tests whether the invariant and its expanded consequences survive execution
```

The ontology therefore expands canonical meaning without becoming a license to rewrite it.

## Return-point rule

The compressed canonical statement remains the primary return point.

The expansion exists so that returning to the short statement has a determinate meaning rather than an underspecified one.

## Integrity requirement

For every locked component that is materially used in system behavior or evaluation:

```text
CompressedInvariant
<-> ExplicitExpansion
```

must preserve semantic integrity.

The expansion may be larger than the compressed form, but it must not become a different rule.
