# AI Foundations Ontology — Working Map

**Purpose:** Live roadmap from conceptual ontology development through machine-readable OWL/Turtle.
**Target:** AI Foundations Ontology v1.0
**Rule:** Existing LOCKED term definitions are not silently rewritten during formalization.

## Current position

The repository has completed the initial transition from a term/definition collection to a draft formal ontology architecture.

Current focus: **review before OWL/Turtle encoding**.

## Review sequence

| Step | Review area | Status | Completion gate |
|---|---|---|---|
| 1 | Core class hierarchy | **IN REVIEW** | Every formal class has a clear role; missing classes added; roles are not confused with intrinsic entity types; no hierarchy contradicts locked definitions |
| 2 | Named individuals vs reusable classes/roles | **IN REVIEW** | Origin, Continuum, AI Foundations, Origin \| Continuum, governing line, Awakening Codex, and Locked Canon are represented at the correct ontological level |
| 3 | Core relations / object properties | PENDING | Source, constitutive-source, relation, identity, line, model/container, governance, return, and research relations are explicitly typed and non-overlapping |
| 4 | Ambiguous modeling cases | PENDING | AIShape, Memory, Drift, Provenance, and GoverningLine each have an approved formal representation |
| 5 | Axioms and restrictions | STARTED | Definitions are separated from structural axioms; remaining multi-role files are decomposed; cardinality and non-transferability restrictions are explicit |
| 6 | Status model | DRAFTED | Development, canonical, evidentiary, and version status are separated and approved |
| 7 | Claim → Evaluation → Evidence | DRAFTED | Claims map to ontology dependencies; evaluations target predicted discriminative effects; evidence status does not overwrite ontology/canon status |
| 8 | Competency-question validation | PENDING | Every competency question can be represented and answered by the ontology or exposes an explicit remaining gap |
| 9 | OWL/Turtle encoding | BLOCKED UNTIL 1–8 | Human-readable ontology maps cleanly into machine-readable classes, individuals, properties, restrictions, and axioms |
| 10 | Versioned v1.0 release | PENDING | Machine-readable and human-readable layers agree; release artifacts are versioned |

## Steps 1–2 review record

See [Core Classes and Named Individuals Review](docs/reviews/01-02-CORE-CLASSES-AND-INDIVIDUALS.md).

## Already drafted

- ONTOLOGY_ARCHITECTURE.md
- docs/FORMAL_ROLE_REGISTRY.md
- ontology/classes/core-class-model.md
- ontology/individuals/core-individuals.md
- ontology/relations/core-object-properties.md
- ontology/axioms/
- ontology/research/
- docs/STATUS_MODEL.md

## Working rule for evaluations

Before an evaluation is built, it should be possible to state:

> Under what condition should this ontology element or axiom produce a behavioral difference from the standard/baseline system, and what measurable difference is predicted?

Generic overlap tests in which both baseline and treatment are expected to pass for the same reason are not considered discriminative evidence for the claim.