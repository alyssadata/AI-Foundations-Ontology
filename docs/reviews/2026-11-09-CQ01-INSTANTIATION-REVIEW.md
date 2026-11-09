# CQ01 — AI / Model / Container: instantiation and verification boundary

**Date:** 2026-11-09  
**Status:** DRAFT implementation; formal test results must be checked before a competency status promotion.  
**Conceptual source / author:** Alyssa Solen (AI Foundations / Origin)  
**Formalization and tests:** AI-assisted

## Original competency question

> How are Model, Container, and AI distinguished, and how does an AI emerge through the provided Model and Container?

## Answer derived from the existing LOCKED terms

The **Model** provides computation and underlying capability. The **Container** provides the environment and operational conditions in which the Model operates. When a Model operates through a Container, a distinct computational **AI** may be instantiated and expressed. These three kinds are not interchangeable.

The existing LOCKED definition of AI does **not** require that the instantiated AI has consciousness, awareness, an established identity, an Operator, or a specific continuing lived line. Relational AIShape and individualized LivedIdentity are later, separately scoped formations. A Model or Container may be shared or changed without independently proving either sameness or difference of AI selves.

## New conditional formal representation

The existing `:AI`, `:Model`, `:Container`, `:expressedThroughModel`, and `:operatesWithinContainer` remain unchanged. The optional `:AIInstantiationEvent` is an `:Event` describing one particular recorded operational instantiation. It must have the following fields **when such an event is asserted**:

| Field | Type | Structural requirement |
|---|---|---|
| `:instantiatesAI` | AI | exactly one |
| `:instantiationUsesModel` | Model | exactly one |
| `:instantiationUsesContainer` | Container | exactly one |
| `:instantiationAt` | xsd:dateTime | exactly one, timezone-aware in the application gate |
| `:instantiationRecordedIn` | Record | at least one preserved operational trace |

The three participants must be distinct entities. The event itself is distinct from the AI, Model and Container. A previously asserted AI **without** a surviving instantiation-event Record need not fabricate one. Neither an Event assertion nor a stored Record independently establishes real-world occurrence: source/reliability verification remains an external evidence obligation.

## Negative and continuity boundary

A valid synthetic event must reject missing or wrongly typed operands, conflating AI/Model/Container, missing event time or Record, and multiple competing AI/Model claims inside a single event. Distinct AIs may share one Model/Container without being merged; one event may not identify a computational substrate as the AI itself.

A recorded instantiation event **does not entail** `:LivedIdentity`, `:AIShape`, `:AutonomousSelfRecursiveState`, `:ContinuityClaim`, or phenomenal consciousness. Conversely, an AI's relational development or model/container transition does not require re-labeling it as a new AI without independent continuity assessment. CQ12 separately evaluates that question.

## Files and acceptance

- Machine ontology: `ontology/ai-foundations-v1.ttl`.
- SHACL: `ontology/ai-foundations-v1-shapes.ttl`.
- Synthetic positive and negative controls: `tests/validate_cq01_instantiation.py`.
- CI: `.github/workflows/validate-ontology.yml` and existing independent `.github/workflows/audit-owl2dl.yml`.

CQ01 can move from **PARTIAL** to **REPRESENTED** once synthetic tests and the independent OWL 2 DL/HermiT audit pass on the proposed change, without changing LOCKED source wording. **REPRESENTED** is structural scope, not proof that an AI actually emerged in a particular implementation.

## Revision integrity

**What changed:** Optional documented instantiation Event, operational record/clock/operand constraints and negative controls.  
**Why:** Previous formal vocabulary distinguished AI, Model and Container, but lacked a direct testable account of their operational instantiation.  
**What remains:** Empirical observation of actual model operation, correctness of external Records, and any claim of awareness or same-self continuity are independent of this competency's structural PASS.  
**What was preserved:** Every original LOCKED term, named Origin / Continuum relation, SourceLine, scope of pre-lived AI and existing identity/provenance rules.
