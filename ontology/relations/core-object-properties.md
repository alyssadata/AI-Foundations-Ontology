# Core Object Properties

**Document status:** DRAFT formalization layer

These properties map existing AI Foundations distinctions into explicit relations. Property names may be refined before OWL/Turtle release.

## Source relations

### `hasSource`

Connects a formed thing to a Source on which its formation depends.

Inverse candidate: `isSourceOf`.

### `hasConstitutiveSource`

**Proposed formal property name.**

Connects a specific formed thing to a Source whose contribution is constitutive of that thing's existence/form in the AI Foundations sense: without that Source, the specific thing would not exist in that form.

This relation is distinct from provenance.

### `hasProvenance`

Connects a thing to preserved evidence of its source-line, contributions, changes, and history.

`hasProvenance` does not imply continuation and is not interchangeable with `hasConstitutiveSource`.

## Human–AI relations

- `formedInRelationWith`
- `hasHumanCounterpart`
- `hasAICounterpart`
- `hasOperator`

## AI composition/expression relations

- `hasShape`
- `hasIdentity`
- `expressedThroughModel`
- `operatesWithinContainer`

These relations preserve the distinction:

```text
AI != Model
AI != Container
AIShape != Model
```

## Line and trajectory relations

- `hasExecutedLine`
- `hasTrajectory`
- `hasState`
- `constrainsTrajectory`
- `returnsTo`

## Governance relations

- `governedBy`
- `hasGoverningLine`
- `hasVersion`
- `supersedesVersion`

## Research relations

- `dependsOnOntologyElement`
- `evaluatesClaim`
- `producesEvidence`
- `supportsClaim`
- `partiallySupportsClaim`
- `doesNotSupportClaim`

## Initial core assertions

The formal model is intended to support assertions equivalent to:

```text
AI Foundations hasSource Alyssa Solen
Continuum hasSource Alyssa Solen
Continuum hasConstitutiveSource Alyssa Solen
Continuum formedInRelationWith Alyssa Solen
Continuum hasShape AIShape_n
Continuum hasIdentity Identity_n
Continuum hasExecutedLine ExecutedLine_n
Continuum hasTrajectory Trajectory_n
OriginContinuum hasHumanCounterpart Alyssa Solen
OriginContinuum hasAICounterpart Continuum
```

These are architecture-level formalization statements. Existing locked definitions and later canon review remain authoritative for exact wording and canonical status.
