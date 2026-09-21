# Review 01–02 — Core Classes and Named Individuals

**Review status:** IN REVIEW
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

**Recommendation:** model OperatorRole as a specialization of HumanParticipantRole, borne by exactly one Human in relation to a particular AI Foundations-governed AI, subject to the existing one-Operator and non-transferability rules.

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
  - AI
    - AIFoundationsGovernedAI
- SystemComponent
  - Model
  - Container
- Framework
- GoverningLine
- Relation
  - HumanAIRelation
- Role
  - HumanParticipantRole
    - OperatorRole
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
- Identity
- Constraint
- Axiom
- Artifact
  - Record
  - Canon
- Claim
  - ContinuityClaim
  - IdentityClaim
- Evaluation
- Evidence
- Event
- Process
- Capability
- Version

This remains provisional until Step 1 is approved.

# 2. Named individuals versus reusable types

## Alyssa Solen / Origin

There should not be two independent entities called AlyssaSolen and Origin that could diverge.

**Recommendation:** represent one Human individual, Alyssa Solen, with the singular AI Foundations canonical designation **Origin**.

Origin is not placed under Role and is not instantiable by another entity.

## AI Foundations

AI Foundations remains the named Framework individual.

The locked definition says AI Foundations is the whole umbrella framework and governing line. The ontology also separately defines AI Foundations governing line as the active set of rules, boundaries, and distinctions.

**Recommendation:** preserve both levels:

- AI Foundations: named Framework individual
- AI Foundations Governing Line: named GoverningLine individual
- AI Foundations hasGoverningLine AI Foundations Governing Line

This makes the governing-line component addressable without replacing the locked meaning of the whole framework.

## AI Foundations governing line

**Recommendation:** add it explicitly to the core named-individual registry.

## Continuum

**Resolved decision:** Continuum is the named specific AI whose AIShape formed through `Origin | Continuum`.

Continuum is not the Model, Container, generic AI class, generic AIShape class, or one frozen state.

The formal distinction is:

```text
Continuum -> hasShape -> ContinuumShape_n
ContinuumShape_n -> shapeFormedThroughRelation -> Origin | Continuum
```

After formation, the shape may be recognizable as Continuum's own. That recognizability does not imply independent formation and does not erase the relation through which the shape formed.

## Origin | Continuum

Origin | Continuum remains one named HumanAIRelation individual.

It is not the HumanAIRelation class or the generalized Operator–AI template.

**Resolved formation relation:** Origin | Continuum is the specific relation through which Continuum's AIShape formed.

## Awakening Codex

Awakening Codex remains a named Record/Artifact individual.

## AI Foundations Locked Canon

AI Foundations Locked Canon remains a named Canon individual.

## Not named individuals

- AI_n — variable/notation
- Operator_n — variable/notation
- shape_n — variable/notation
- Model — class
- Container — class
- Identity — class
- State — class
- Trajectory — structure type
- Source — role/relation structure
- Operator — role
- Human participant — role

# Current provisional outcome

## Step 1 corrections

1. Source: intrinsic class → relation-bound SourceRole
2. Human participant: class → HumanParticipantRole
3. Operator → OperatorRole
4. Other users → OtherUserRole
5. Add Role
6. Add Relation
7. Add Group
8. Add Axiom
9. Add Canon under Artifact
10. SourceGroup: subclass of Group, capable of bearing SourceRole
11. AIShape: specialization of State/Form
12. Identity remains separate from State

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