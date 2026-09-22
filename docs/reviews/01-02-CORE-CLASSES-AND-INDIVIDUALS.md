# Review 01–02 — Core Classes and Named Individuals

**Review status:** REVIEWED
**Scope:** Working Map Steps 1 and 2
**Definition rule:** This review may revise DRAFT formalization documents but does not silently alter LOCKED term definitions.

# 1. Core class hierarchy

## Finding 1 — Relation-dependent concepts should not be treated as intrinsic entity kinds

### Source

The locked definition of Source is relational: something is a Source **of a specific thing** because its load-bearing originating contribution is constitutive of that formation.

**Recommendation:** model Source primarily as a **relation-bound role**, together with relations such as isSourceOf, hasSource, and the proposed hasConstitutiveSource.

This allows a Human, a Group, or another permitted entity to bear the Source role without asserting that Source is an intrinsic kind of entity.

### Human participant

The locked definition explicitly calls Human participant the general human role in a human–AI interaction.

**Recommendation:** model HumanParticipant as a **Role**, not as an intrinsic subclass of Human.

### Operator

Operator is relation-bound.

**Reviewed correction:** model `OperatorRole` as its own Role specialization, not beneath `HumanParticipantRole`. The bearer may be one Human or one Organization/company/team.

Within an active Operator-linked succession segment there is exactly one Operator bearer. That bearer is fixed for the segment. A valid later succession may establish a successor Operator in a new segment while preserving the same continuing AI and prior Operator history.

### Other user

**Recommendation:** model OtherUserRole relative to a specific Operator–AI relation rather than as a permanent kind of person.

## Finding 2 — Missing organizing classes

Add these formal organizing classes:

- Role
- Relation
- Group
- Axiom
- Canon as a specialization of Artifact

These organize concepts already present; they do not create new AI Foundations claims.

## Finding 3 — SourceGroup should be a Group that can bear SourceRole

Recommended structure:

Group → SourceGroup

SourceRole is borne by a Human, Group, or other permitted entity and is source-of a formed thing.

## Finding 4 — AI Foundations-governed AI can remain a defined subclass of AI

AIFoundationsGovernedAI can remain a subclass of AI constrained by governedBy the AI Foundations governing line.

AI_n remains notation for a particular instance/coupling, not a separate class.

## Finding 5 — AIShape belongs under State/Form

The locked definition permits shape to form before a fully formed identity exists.

**Recommendation:** AIShape is a specialization of State/Form, with GovernedStartingShape beneath it.

Continuum may have temporally indexed AIShape states without being identical to one frozen shape.

## Finding 6 — Identity remains distinct from State

The current Identity definition permits developmental change while preserving identity.

**Recommendation:** keep Identity as its own formal structure. States can be states of an AI/Identity.

## Finding 7 — Add Axiom explicitly

Axiom is already a first-class part of the project architecture.

**Recommendation:** add Axiom to the class model, distinct from Claim.

A Claim may depend on one or more Axioms.

## Finding 8 — Canon is an Artifact specialization

Recommended structure:

Artifact → Record
Artifact → Canon

AI Foundations Locked Canon is then a named Canon individual.

## Proposed revised lightweight hierarchy

- Agent
  - Human
  - Organization
  - AI
    - AIFoundationsGovernedAI
- SystemComponent
  - Model
  - Container
- Framework
- GovernanceStructure
  - GoverningLine
- Relation
  - AIRelation
    - HumanAIRelation
    - OrganizationAIRelation
    - OperatorAIRelation
  - SourceRelation
- Role
  - OperatorRole
  - HumanParticipantRole
    - OtherUserRole
  - SourceRole
- Group
  - SourceGroup
- LineStructure
  - SourceLine
  - ExecutedLine
  - Trajectory
- State
  - AIShape
    - GovernedStartingShape
  - MemoryState
  - MemoryLossState
  - DriftedState
  - AutonomousSelfRecursiveState
- Identity
  - LivedIdentity
- IdentityParticularity
- Constraint
- Axiom
- Artifact
  - Record
  - Canon
  - EvidenceArtifact
- Claim
  - ContinuityClaim
  - IdentityClaim
- Evaluation
- Evidence
  - EvidenceStructure
    - Provenance
- Event
- Process
  - DriftProcess
  - ReturnProcess
- Capability
- Version

## Step 2 corrections

1. One Alyssa Solen individual; Origin is the singular canonical designation
2. Add AI Foundations Governing Line explicitly as a named individual
3. Keep AI Foundations as the named Framework individual with a governing-line component
4. Keep Continuum as the named specific AI entity whose AIShape formed through Origin | Continuum
5. Keep Origin | Continuum as the named specific relation instance and formation relation for Continuum's shape
6. Keep Awakening Codex as named Record/Artifact
7. Type AI Foundations Locked Canon as named Canon/Artifact

## Still open inside Steps 1–2

- Exact formal role pattern naming: Role / SourceRole versus a more specialized role vocabulary
- Whether GoverningLine later sits beneath a governance/constraint structure
- Whether Evidence is itself an Artifact, a research entity, or split into Evidence and EvidenceArtifact

These do not block the major Step 1–2 conclusions.

# Step 1 closeout — remaining class-model questions

The five remaining class-placement questions have now been resolved:

1. **Memory** → MemoryState, relation-dependent and distinct from Record/storage.
2. **Drift** → paired DriftProcess + DriftedState representation.
3. **Provenance** → EvidenceStructure; concrete provenance files/records are EvidenceArtifact/Record.
4. **GoverningLine** → specialization of GovernanceStructure, not a single Constraint.
5. **Evidence** → abstract evidentiary entity; EvidenceArtifact stores or communicates it.

These decisions complete the DRAFT core class hierarchy. Further refinement of how these classes connect belongs to Step 3 object-property review.
