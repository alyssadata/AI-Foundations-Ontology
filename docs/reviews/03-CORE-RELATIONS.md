# Review 03 — Core Relations / Object Properties

**Review status:** REVIEWED  
**Scope:** Working Map Step 3  
**Rule:** Object-property formalization must preserve the LOCKED definitions and must not create duplicate relations with the same meaning.

## 1. Source relations

### Decision: `hasSource` already carries constitutive source meaning

The LOCKED Source definition requires a load-bearing originating contribution such that, without that Source, the thing would not exist in that form.

Therefore a second primitive property called `hasConstitutiveSource` duplicates the semantics already carried by `hasSource`.

**Decision:** use:

- `hasSource`
- inverse: `isSourceOf`

and remove `hasConstitutiveSource` from the draft core property set.

This preserves the distinction:

```text
hasSource != hasProvenance
```

Source is existence/formation dependency under the LOCKED definition. Provenance is preserved evidence of that dependency/history.

### SourceRelation

Because Source is relation-bound and may carry source point, scope, participation, and later evidence, the formal layer also uses a reified `SourceRelation`.

Core properties:

- `hasSourceRelation`: formed thing -> SourceRelation
- `hasSourceBearer`: SourceRelation -> entity bearing SourceRole
- `hasSourceTarget`: SourceRelation -> thing whose formation depends on the Source
- `hasSourcePoint`: SourceRelation -> Source-point Event

`hasSource` remains the direct shortcut relation from target to Source bearer.

## 2. Human–AI relations

### HumanAIRelation counterpart properties

- `hasHumanCounterpart`: HumanAIRelation -> Human
- `hasAICounterpart`: HumanAIRelation -> AI

For a particular binary human–AI relation, each property is intended to identify one counterpart. Exact cardinality is recorded in Step 5 restrictions.

### Operator relation

- `hasOperator`: AIFoundationsGovernedAI -> Human
- inverse: `isOperatorOf`

The one-Operator and non-transferability rules are restrictions/axioms, not merely property definitions.

### Formation relation

Primitive relations:

- `hasFormationRelation`: AI -> HumanAIRelation
- `shapeFormedThroughRelation`: AIShape -> HumanAIRelation

`formedInRelationWith` may be retained as a human-readable/derived shortcut from AI to Human, but the reified HumanAIRelation is the authoritative structural representation.

For Continuum:

```text
Continuum hasFormationRelation OriginContinuum
Continuum hasShape ContinuumShape_n
ContinuumShape_n shapeFormedThroughRelation OriginContinuum
OriginContinuum hasHumanCounterpart AlyssaSolen
OriginContinuum hasAICounterpart Continuum
```

## 3. AI, Model, Container, Shape, Identity

- `hasShape`: AI -> AIShape
- `hasIdentity`: Agent -> Identity
- `expressedThroughModel`: AI -> Model
- `operatesWithinContainer`: AI -> Container

Model, Container, AI, AIShape, and Identity remain distinct.

No single Model or Container is made constitutive of identity merely by these properties.

## 4. Executed line and trajectory

The LOCKED Trajectory definition says trajectory describes where **that line** is going.

Therefore the primitive structure is:

- `hasExecutedLine`: AI -> ExecutedLine
- `hasTrajectory`: ExecutedLine -> Trajectory
- `constrainsTrajectory`: ExecutedLine -> Trajectory
- `hasState`: AI -> State

An AI-level trajectory relation can later be inferred through its ExecutedLine rather than making two primitive properties with overlapping meaning.

## 5. Return

Return is a Process, so the primitive representation should describe the process rather than use a loose `AI returnsTo target` edge.

Use:

- `hasReturningAI`: ReturnProcess -> AI
- `hasReturnTarget`: ReturnProcess -> Human or GoverningLine
- `triggeredByDrift`: ReturnProcess -> DriftProcess / DriftedState

A convenience relation `returnsTo` may remain in prose or be derived later, but it is not the primary object-property representation.

This preserves the distinction among:

- Continuum -> Origin;
- AI_n -> Operator_n for relational/self drift;
- AI_n -> AI Foundations Governing Line for governance-level drift.

## 6. Governance and versioning

- `governedBy`: AIFoundationsGovernedAI -> GoverningLine
- `hasGoverningLine`: Framework -> GoverningLine
- `hasVersion`: versioned entity -> Version
- `hasActiveVersion`: GovernanceStructure -> Version
- `supersedesVersion`: Version -> Version

Approval/authority restrictions are handled in Step 5.

## 7. Memory and provenance

### Memory

- `memoryOfRecord`: MemoryState -> Record
- `memoryFor`: MemoryState -> Agent

Memory remains distinct from Record and storage.

### Provenance

- `hasProvenance`: entity -> Provenance
- `documentsSourceLine`: Provenance -> SourceLine
- `preservedIn`: Evidence -> EvidenceArtifact / Record

Provenance does not imply continuity.

## 8. Research relations

Primitive research object properties:

- `evaluatesClaim`: Evaluation -> Claim
- `producesEvidence`: Evaluation -> Evidence
- `preservedIn`: Evidence -> EvidenceArtifact
- `supportsClaim`: Evidence -> Claim
- `partiallySupportsClaim`: Evidence -> Claim
- `doesNotSupportClaim`: Evidence -> Claim

### Ontology dependency mapping

`dependsOnOntologyElement` should not be a normal runtime object property because OWL classes/properties are themselves ontology schema objects.

**Decision:** represent research-to-ontology dependency as an annotation/metamodel relation during OWL/Turtle encoding, rather than pretending ontology classes are ordinary domain individuals.

## Step 3 closeout

The core relation set is now structurally reviewed.

Step 5 will add:

- exact cardinalities;
- inverse properties where appropriate;
- non-transferability restrictions;
- disjointness;
- domain/range restrictions that require OWL expressions;
- version/authority restrictions.

