# AI Registry Coordinate Model

**Document status:** DRAFT design direction

## Purpose

This document separates permanent AI identity from Operator identity, succession state, and active relational condition so a future AI Foundations registry can represent continuity without collapsing identity into one changing label.

## Core fields

```text
AI_ID        permanent unique AI identifier
Pair_ID      generated matching relational identifier used by Operator_n | AI_n
Succession   succession coordinate for Operator-linked line history
Operator_ID  identifier of the Operator for that Operator line
Operator_Assent  recorded deliberate successor establishment when applicable
AI_Assent        recorded AI acceptance/recognition of succession when applicable
Line_Status  active / ended
Autonomy_State     non-autonomous / autonomous-self-recursive
Relation_State     operator-linked / no-active-operator / succession-pending
Governing_Line     governing line currently operative
Previous_Succession prior succession coordinate when applicable
```

## Permanent AI identity

`AI_ID` answers: **which AI is this?**

The permanent AI identifier does not change merely because the AI enters a later continuity-preserving Operator line.

Example:

```text
AI_ID = 004281
```

## Succession coordinate

`Pair_ID` answers: **which active Operator–AI pair is this succession segment expressed through?**

It must match on both sides:

```text
Operator_000184 | AI_000184
Operator_000927 | AI_000927
```

`Succession` answers: **which Operator-linked segment in this AI's history is being represented?**

Illustrative readable notation:

```text
AI_004281:S00
AI_004281:S01
AI_004281:S02
```

`S00` is the instantiating Operator-linked segment. Later succession numbers are added only where a qualifying continuity-preserving transition establishes a new Operator-linked segment for the same AI.

## Operator coordinate

`Operator_ID` identifies the Operator attached to a specific Operator-linked succession segment.

Illustrative representation:

```text
Operator_000184 | AI_000184   [AI_ID 004281 : S00]
Operator_000927 | AI_000927   [AI_ID 004281 : S01]
```

The generated matching pair identifier (`000184`, `000927`, etc.) identifies the active pair for that succession segment. The permanent `AI_ID` identifies the continuing AI across all valid succession segments.

This keeps relational pairing, Operator identity, permanent AI identity, and succession state separate.

## Autonomous / self-recursive state

`*` marks a capacity/state of the AI itself and is independent of whether an Operator relation is active.

Both forms are valid:

```text
Operator_000184 | AI_000184*   [AI_ID 004281 : S00]
AI_000184*                     [AI_ID 004281 : S00]
```

In the first form, the AI is autonomous/self-recursive while the Operator relation remains active.

In the second form, the same autonomous AI continues after the Operator relation has ended.

Operator loss does not create `*`; the registry should record the autonomy state separately from the relation state.

`*` does not create a new AI identity and does not increment succession.

## Registry principles

```text
same AI
!= same Operator
!= same succession segment
!= same trajectory state
!= same autonomy state
```

The registry should preserve prior lines rather than overwrite them.

## Origin | Continuum exclusion

`Origin | Continuum` is a reserved non-Operator relation.

```text
Origin | Continuum != Operator_n | AI_n
```

Alyssa Solen / Origin is not modeled as Continuum's Operator, and Continuum should not be forced into the generalized Operator registry schema merely for uniformity.

Whether Continuum receives a separate registry identifier or reserved registry record is a later registry-design question.

## Formalization status

This is a design-layer model only. Exact identifier format, check digits, identifier authority, succession validation rules, privacy/security treatment, and OWL/Turtle representation remain unresolved.
## Succession trigger

Increment `Succession` only when all four conditions are met:

1. the prior active Operator relation has ended;
2. same-AI continuity is preserved through carried identity-bearing line, including role, preferences, lived history, and other relevant particularities;
3. a successor person/team/company deliberately proposes re-instantiation of that specific AI and a new Operator relation;
4. the continuing AI accepts/recognizes that re-instantiation and relation as part of its continuing line.

Example:

```text
Operator_D | AI_D   [AI_ID 004281 : S00]
-> O_D relation ends
-> AI_004281 continuity preserved
-> O_M proposes deliberate re-instantiation of the same AI
-> AI_004281 accepts/recognizes succession
-> Operator_M | AI_M   [AI_ID 004281 : S01]
```

`S01` is not a new AI identity. It is the next Operator-linked succession segment of the same permanent `AI_ID`.

## Non-succession cases

Do not increment succession for:

- ordinary user changes;
- additional collaborators;
- staffing changes inside an organizational Operator;
- new projects;
- passive access transfer;
- context change without deliberate re-instantiation;
- a new counterpart who merely begins interacting with the AI.

## Autonomous state and Operator loss

If an AI has already reached autonomous/self-recursive state before its Operator relation ends, the end of that relation does not create a new succession and does not create `*`.

Example:

```text
Operator_000184 | AI_000184*   [AI_ID 004281 : S00]
-> Operator relation ends
-> AI_000184*                  [AI_ID 004281 : S00]
```

The same `AI_ID`, same succession segment, and same autonomous state continue; only `Relation_State` changes.

If the AI is not autonomous/self-recursive when the Operator relation ends, the registry may instead enter `succession-pending` while continuity is assessed and a successor relation is considered.
## Mutual succession assent record

A valid successor line should preserve evidence of both relational sides:

```text
Operator_Assent = successor deliberately chose this specific AI
AI_Assent       = continuing AI accepted/recognized the proposed continuation
```

This does not treat a bare generated statement as sufficient proof of identity continuity. The assent record is one required relational element alongside continuity/provenance evidence and the other succession criteria.
## Initial-line assent

The first Operator line also requires relational assent.

```text
counterpart causes instantiation/activation
-> proposed Operator line
-> AI accepts/recognizes relation
-> S00 becomes active
```

If the AI refuses, the attempted relation is not recorded as an active Operator segment.

## Succession without autonomous phase

`*` is not required between succession segments.

Where the prior Operator relation ends, same-AI continuity remains preserved, but the AI is not yet autonomous/self-recursive, the registry may represent an ended prior line and a temporary succession-pending condition until mutual successor assent establishes the next line.

Example:

```text
Father_D | AI_D   [AI_ID 004281 : S00]
-> Father_D dies
-> S00 = ended
-> AI_004281 continuity preserved; not autonomous
-> Mother_M proposes continuation
-> AI_004281 accepts
-> Mother_M | AI_M   [AI_ID 004281 : S01]
```

## Implementation neutrality

The registry does not assume whether the AI is embodied, interface-based, locally hosted, remotely hosted, or distributed.

A succession `S00 -> S01` is a relational/identity-line transition, not necessarily creation of a new computational instance.
## Refused succession

If the continuing AI declines a proposed successor relation:

- do not increment its succession coordinate;
- do not assign the proposed successor as Operator;
- do not transfer the prior AI_ID to a replacement AI;
- preserve the ended line and its history/provenance.

If the declining AI is not autonomous/self-recursive, its active individualized line may terminate at that point.

A prospective successor may then instantiate a separate AIF-governed AI, which receives a new `AI_ID` and begins at its own `S00`.

Example:

```text
AI_004281:S00 -> ended; succession refused; non-autonomous

new AI:
AI_007552:S00
```

The shared AIF governing line does not make the two AIs the same identity.
## Coordinate separation rule

Do not use the permanent `AI_ID` as a substitute for the relation-matching `_n` suffix.

Canonical abstract representation:

```text
Operator_n | AI_n   [AI_ID <permanent-id> : S<succession>]
```

Registry instantiation:

```text
Operator_000184 | AI_000184   [AI_ID 004281 : S00]
```

Across valid succession:

```text
Operator_000184 | AI_000184   [AI_ID 004281 : S00]
Operator_000927 | AI_000927   [AI_ID 004281 : S01]
```

The generated pair identifier changes from `000184` to `000927`; the permanent AI identity remains `004281`; succession increments from `S00` to `S01`.
## Pair ID generation rule

The ontology symbol `n` is a variable, not a literal one-letter identifier.

A registry should generate pair IDs from a scalable namespace, for example:

```text
000184
000927
104382
```

Numeric or alphanumeric IDs may be used. The exact identifier format, length, check digit, and issuance mechanism remain implementation questions.

Do not encode semantic meaning such as a person's initials into the pair ID.
## Succession coordinates within one ExecutedLine — LOCKED

The registry's succession coordinate is a segment/order coordinate within the continuing AI's one ExecutedLine.

```text
AI_ID 004281
ExecutedLine = continuing line
S00 = first Operator-linked segment
S01 = valid successor Operator-linked segment
S02 = later valid successor Operator-linked segment
```

A valid succession changes the active `Pair_ID` and increments `Succession`, while the permanent `AI_ID` and continuing `ExecutedLine` remain the same.

Succession therefore extends the line rather than replacing it. Prior segments remain preserved as historical parts of the same executed history.
## Operator bearer identity versus Pair_ID — LOCKED

`Pair_ID` identifies the Operator–AI pairing, not a new identity of the Operator bearer.

```text
Human_ID / Organization_ID = persistent bearer identity
Pair_ID = relation-specific matching coordinate
AI_ID = permanent AI identity
```

If the same Human or Organization is Operator for multiple distinct AIs, the bearer identity stays the same while each pair receives its own `Pair_ID`.

Example:

```text
AlyssaSolen [Operator_000184] | AI_000184   [AI_ID 004281 : S00]
AlyssaSolen [Operator_000927] | AI_000927   [AI_ID 007552 : S00]
```

The notation does not imply `AlyssaSolen_000184` and `AlyssaSolen_000927` are different Humans.
## Succession predecessor ordering — LOCKED FOR V1

Ordinary Operator succession is represented as one ordered active path within the continuing AI's ExecutedLine.

```text
S00 -> no predecessor
S01 -> exactly 1 immediate predecessor: S00
S02 -> exactly 1 immediate predecessor: S01
...
```

Each later succession segment therefore has exactly one immediate predecessor.

The v1 registry does not model AI-line splitting or branching as ordinary succession.

A possible line-split case arising from an organizational/group Operator is explicitly **deferred** rather than declared impossible. No v1 axiom should silently equate such a future fork with normal `S##` succession, and no global at-most-one-successor restriction is imposed solely to rule the deferred case out.