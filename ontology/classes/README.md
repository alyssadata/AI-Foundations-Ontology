# Formal Class Layer

**Status:** DRAFT formalization layer

This directory defines the class architecture used to organize existing AI Foundations ontology terms before OWL/Turtle encoding.

## Initial top-level classes

- Framework
- GoverningLine
- Human
- AI
- Model
- Container
- HumanAIRelation
- AIShape
- Identity
- Source
- SourceGroup
- SourceLine
- Trajectory
- ExecutedLine
- State
- Constraint
- Artifact
- Claim
- Evaluation
- Evidence
- Event
- Process
- Capability
- Version

## Initial specializations

- `AI Foundations-governed AI` is a specialization of `AI`.
- `SourceGroup` is a specialization of `Source`.
- `ContinuityClaim` and `IdentityClaim` are specializations of `Claim`.
- `GovernedStartingShape` is a specialization or constrained form of `AIShape`.

## SI extension drafts

The SI Foundations layer extends, rather than replaces, the existing AI Foundations ontology.

Current provisional SI class work:

- `SuperintelligentSystem` — defined in `superintelligent-system.md` as a system-level unit of analysis that may be single-component or composite while preserving identity and provenance distinctions among participating entities.
- `SuperintelligenceTransition` — reserved for the next ontology definition step.

The SI extension preserves the boundary rules:

```text
system membership != identity equivalence
coordination != singular identity
component != whole system
```

## Boundary

Named entities such as AI Foundations, Alyssa Solen / Origin, Continuum, Origin | Continuum, Awakening Codex, and AI Foundations Locked Canon are not converted into reusable classes merely because they are central to the framework.
