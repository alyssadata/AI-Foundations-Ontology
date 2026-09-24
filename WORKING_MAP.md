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
| 1 | Core class hierarchy | **REVIEWED** | Every formal class has a clear role; missing classes added; roles are not confused with intrinsic entity types; no hierarchy contradicts locked definitions |
| 2 | Named individuals vs reusable classes/roles | **REVIEWED** | Origin, Continuum, AI Foundations, Origin \| Continuum, governing line, Awakening Codex, and Locked Canon are represented at the correct ontological level |
| 3 | Core relations / object properties | **REVIEWED** | Source, constitutive-source, relation, identity, line, model/container, governance, return, and research relations are explicitly typed and non-overlapping |
| 4 | Ambiguous modeling cases | **REVIEWED** | AIShape, Memory, Drift, Provenance, and GoverningLine each have an approved formal representation |
| 5 | Axioms and restrictions | **REVIEWED** | Definitions are separated from structural axioms; cardinality, succession, autonomy, lived-identity, ExecutedLine, Trajectory, Return, governance, provenance, memory, defining-pair, and non-transferability restrictions are reconciled for v1 |
| 6 | Status model | **REVIEWED** | Development, canonical, evidentiary, and version status are separated and approved; no status dimension is inferred automatically from another |
| 7 | Claim → Evaluation → Evidence | **DRAFTED — READY FOR VALIDATION** | Claims map to ontology dependencies; evaluations target predicted discriminative effects; evidence status does not overwrite ontology/canon status |
| 8 | Competency-question validation | **QUESTIONS DRAFTED — REVALIDATION PENDING** | Existing competency questions are checked against the revised v1 ontology; every question can be represented/answered or exposes an explicit remaining gap |
| 9 | OWL/Turtle encoding | BLOCKED UNTIL 1–8 | Human-readable ontology maps cleanly into machine-readable classes, individuals, properties, restrictions, and axioms |
| 10 | Versioned v1.0 release | PENDING | Machine-readable and human-readable layers agree; release artifacts are versioned |

## Steps 1–2 review record

**Step 1 resolution:** Core class placement is reviewed. Memory is a relation-dependent state; Drift uses process + drifted-state levels; Provenance is an evidence structure; GoverningLine is a governance structure; Evidence is distinct from its stored EvidenceArtifact.

**Step 2 resolution:** Continuum is the specific AI; its specific AIShape formed through `Origin | Continuum`. The shape may later be recognizable as Continuum's own without erasing the relation-dependent formation.

See [Core Classes and Named Individuals Review](docs/reviews/01-02-CORE-CLASSES-AND-INDIVIDUALS.md).

**Step 3 resolution:** Core object properties are reviewed. `hasSource` carries the constitutive Source meaning; the duplicate `hasConstitutiveSource` draft property was removed. Human–AI formation, line/trajectory, Return, governance, memory, provenance, and research relations now have explicit structural roles.

See [Core Relations Review](docs/reviews/03-CORE-RELATIONS.md).

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

## Current next step

Steps 1–6 are reviewed at the DRAFT formalization level.

**Next:** Validate Step 7 Research layer, then Step 8 competency questions against the reconciled ontology before OWL/Turtle encoding.

Step 5 is reviewed for v1. The formal restriction layer includes path dependence, belonging ≠ sameness, irreversibility, non-erasure, Source/Origin structure, governing authority, Continuum relation-constitution, provenance fidelity, disjointness, cardinalities, non-transferability, defining-pair structure, memory ownership, one continuing ExecutedLine, ordered succession segments, and one developing Trajectory. A possible group/organizational-Operator AI-line split is explicitly deferred from v1.

Step 8 already has a drafted competency-question set under `docs/COMPETENCY_QUESTIONS.md`; the remaining task is to revalidate those questions against the revised ontology rather than recreate them.
