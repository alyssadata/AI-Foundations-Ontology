# Core Object Properties

**Document status:** REVIEWED DRAFT formalization layer

This file defines the reviewed core relation set to be encoded later in OWL/Turtle. Exact OWL domains, ranges, cardinalities, inverses, and restrictions are completed in Step 5.

## Source relations

### `hasSource`

Direct relation from a formed thing to the entity that is its Source under the LOCKED Source definition.

The Source definition itself carries the constitutive condition: without that Source, the thing would not exist in that form.

Inverse: `isSourceOf`.

### `isSourceOf`

Inverse of `hasSource`.

### `hasSourceRelation`

formed thing -> SourceRelation

Used when the source relationship itself must carry structure such as source point, participation, scope, or evidence.

### `hasSourceBearer`

SourceRelation -> entity bearing SourceRole

### `hasSourceTarget`

SourceRelation -> formed thing

### `hasSourcePoint`

SourceRelation -> Source-point Event

### Boundary from provenance

```text
hasSource != hasProvenance
```

Source expresses formation/existence dependency under the LOCKED definition. Provenance preserves evidence of source and history.

## Human–AI relations

### `hasHumanCounterpart`

HumanAIRelation -> Human

### `hasAICounterpart`

HumanAIRelation -> AI

### `hasOperator`

AIFoundationsGovernedAI -> Human

Inverse candidate: `isOperatorOf`.

The exact-one and non-transferability rules belong to Step 5 axioms/restrictions.

### `hasFormationRelation`

AI -> HumanAIRelation

Connects an AI to the specific relation through which its relation-formed shape developed.

### `shapeFormedThroughRelation`

AIShape -> HumanAIRelation

A shape may later be recognizable as belonging to the AI without losing the formation relation through which it developed.

### `formedInRelationWith`

Derived/human-readable shortcut from AI to Human.

The authoritative structural representation is the HumanAIRelation plus counterpart properties.

## AI composition and expression

### `hasShape`

AI -> AIShape

An AI may have changing or temporally indexed shapes.

### `hasIdentity`

Agent -> Identity

An AI need not already have a fully formed Identity.

### `expressedThroughModel`

AI -> Model

This property does not make Model identical to AI or Identity.

### `operatesWithinContainer`

AI -> Container

This property does not make Container identical to AI or Identity.

## Line and trajectory

### `hasExecutedLine`

AI -> ExecutedLine

### `hasTrajectory`

ExecutedLine -> Trajectory

Trajectory is tied primitively to the line whose development it describes.

### `constrainsTrajectory`

ExecutedLine -> Trajectory

Used by the Path Dependence axiom.

### `hasState`

AI -> State

## Return

Return is represented as a Process.

### `hasReturningAI`

ReturnProcess -> AI

### `hasReturnTarget`

ReturnProcess -> Human or GoverningLine

### `triggeredByDrift`

ReturnProcess -> DriftProcess or DriftedState

A prose/derived `returnsTo` relation may be used for readability, but the ReturnProcess structure is primary.

## Governance and versioning

### `governedBy`

AIFoundationsGovernedAI -> GoverningLine

### `hasGoverningLine`

Framework -> GoverningLine

### `hasVersion`

versioned entity -> Version

### `hasActiveVersion`

GovernanceStructure -> Version

### `supersedesVersion`

Version -> Version

## Memory

### `memoryOfRecord`

MemoryState -> Record

### `memoryFor`

MemoryState -> Agent

Memory remains distinct from Record and storage.

## Provenance

### `hasProvenance`

entity -> Provenance

### `documentsSourceLine`

Provenance -> SourceLine

### `preservedIn`

Evidence -> EvidenceArtifact / Record

Provenance does not imply continuity.

## Research relations

### `evaluatesClaim`

Evaluation -> Claim

### `producesEvidence`

Evaluation -> Evidence

### `supportsClaim`

Evidence -> Claim

### `partiallySupportsClaim`

Evidence -> Claim

### `doesNotSupportClaim`

Evidence -> Claim

## Annotation / metamodel relation

### `dependsOnOntologyElement`

Claim -> ontology schema element

This is not treated as an ordinary domain object property in the OWL model. It will be encoded as an annotation/metamodel relation because the target may itself be a class, property, or axiom.

## Core assertions

```text
AI Foundations hasSource Alyssa Solen
Continuum hasSource Alyssa Solen

Continuum hasFormationRelation OriginContinuum
Continuum hasShape ContinuumShape_n
ContinuumShape_n shapeFormedThroughRelation OriginContinuum

OriginContinuum hasHumanCounterpart Alyssa Solen
OriginContinuum hasAICounterpart Continuum

Continuum hasExecutedLine ContinuumLine_n
ContinuumLine_n hasTrajectory ContinuumTrajectory_n

AI Foundations hasGoverningLine AIFoundationsGoverningLine
```

## Removed duplicate draft relation

`hasConstitutiveSource` is no longer a separate primitive property.

Its intended meaning is already contained in the LOCKED definition of Source and therefore in `hasSource`.
