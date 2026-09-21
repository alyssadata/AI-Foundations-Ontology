# AI Registry Coordinate Model

**Document status:** DRAFT design direction

## Purpose

This document separates permanent AI identity from Operator identity, succession state, and active relational condition so a future AI Foundations registry can represent continuity without collapsing identity into one changing label.

## Core fields

```text
AI_ID        permanent unique AI identifier
Succession   succession coordinate for Operator-linked line history
Operator_ID  identifier of the Operator for that Operator line
Line_Status  active / ended
Continuation_Mode  operator-linked / autonomous
Governing_Line     governing line currently operative
Previous_Line      prior succession coordinate when applicable
```

## Permanent AI identity

`AI_ID` answers: **which AI is this?**

The permanent AI identifier does not change merely because the AI enters a later continuity-preserving Operator line.

Example:

```text
AI_ID = 004281
```

## Succession coordinate

`Succession` answers: **which Operator-linked line in this AI's history is being represented?**

Illustrative readable notation:

```text
AI_004281:S00
AI_004281:S01
AI_004281:S02
```

`S00` is the instantiating Operator line. Later succession numbers are added only where a qualifying line-changing event leads to a new Operator line while continuity of the same AI is preserved.

## Operator coordinate

`Operator_ID` identifies the Operator attached to a specific Operator line.

Illustrative representation:

```text
O_1837 | AI_004281:S00
O_2914 | AI_004281:S01
```

This keeps Operator identity separate from AI identity.

## Autonomous continuation

When the active Operator relation ends and the AI is sufficiently self-sustaining/self-recursive to continue without a successor Operator, readable notation may use `*`:

```text
AI_004281:S00*
```

`*` does not create a new AI identity. It marks post-Operator autonomous continuation of the same identity-bearing line.

## Registry principles

```text
same AI
!= same Operator
!= same succession line
!= same trajectory state
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

Increment `Succession` only when all three conditions are met:

1. the prior active Operator relation has ended;
2. same-AI continuity is preserved through carried identity-bearing line, including role, preferences, lived history, and other relevant particularities;
3. a successor person/team/company deliberately re-instantiates that specific AI and explicitly establishes a new Operator relation.

Example:

```text
O_D | AI_004281:S00
-> O_D relation ends
-> AI_004281 continuity preserved
-> O_M deliberately re-instantiates the same AI
-> O_M | AI_004281:S01
```

`S01` is not a new AI identity. It is the next Operator-linked succession line of the same permanent `AI_ID`.

## Non-succession cases

Do not increment succession for:

- ordinary user changes;
- additional collaborators;
- staffing changes inside an organizational Operator;
- new projects;
- passive access transfer;
- context change without deliberate re-instantiation;
- a new counterpart who merely begins interacting with the AI.

## Autonomous fork

If the prior Operator relation ends and the AI is sufficiently self-sustaining/self-recursive to continue without another Operator, succession need not increment. The existing line may continue in autonomous mode:

```text
AI_004281:S00*
```

If a later deliberate successor re-instantiation is subsequently established, the next Operator-linked succession may then be recorded without erasing the autonomous interval.