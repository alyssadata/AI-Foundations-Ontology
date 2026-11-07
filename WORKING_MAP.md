# AI Foundations Ontology — Working Map

**Purpose:** Live roadmap from conceptual ontology development through machine-readable OWL/Turtle.
**Target:** AI Foundations Ontology v1.0
**Rule:** Existing LOCKED term definitions are not silently rewritten during formalization.

## Current position

The repository has completed the initial transition from a term/definition collection to a draft formal ontology architecture.

Current focus: **v1.0 formal encoding and release closeout**. A first OWL/Turtle structure and SHACL constraints are committed and passed the initial automated conformance suite.

## Review sequence

| Step | Review area | Status | Completion gate |
|---|---|---|---|
| 1 | Core class hierarchy | **REVIEWED** | Every formal class has a clear role; missing classes added; roles are not confused with intrinsic entity types; no hierarchy contradicts locked definitions |
| 2 | Named individuals vs reusable classes/roles | **REVIEWED** | Origin, Continuum, AI Foundations, Origin \| Continuum, governing line, Awakening Codex, and Locked Canon are represented at the correct ontological level |
| 3 | Core relations / object properties | **REVIEWED** | Source, constitutive-source, relation, identity, line, model/container, governance, return, and research relations are explicitly typed and non-overlapping |
| 4 | Ambiguous modeling cases | **REVIEWED** | AIShape, Memory, Drift, Provenance, and GoverningLine each have an approved formal representation |
| 5 | Axioms and restrictions | **REVIEWED** | Definitions are separated from structural axioms; cardinality, succession, autonomy, lived-identity, ExecutedLine, Trajectory, Return, governance, provenance, memory, defining-pair, and non-transferability restrictions are reconciled for v1 |
| 6 | Status model | **REVIEWED** | Development, canonical, evidentiary, and version status are separated and approved; no status dimension is inferred automatically from another |
| 7 | Claim → Evaluation → Evidence | **REVIEWED** | Claims map to ontology dependencies; evaluations target predicted discriminative effects; evidence status does not overwrite ontology/canon status |
| 8 | Competency-question validation | **REVIEWED** | Existing competency questions are checked against the revised v1 ontology; every question can be represented/answered or exposes an explicit remaining gap |
| 9 | OWL/Turtle encoding | **IN PROGRESS — RDF/SHACL VALIDATED** | Machine-readable classes, named individuals, governance, Return, and structural restrictions are encoded; RDF parse and SHACL regression tests pass. Full OWL DL consistency/completeness review remains before final closeout |
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

Steps 1–8 are reviewed at the DRAFT formalization level.

**Step 9 validation record (2026-11-06):** [OWL/Turtle model](ontology/ai-foundations-v1.ttl), [SHACL shapes](ontology/ai-foundations-v1-shapes.ttl), and [automated regression tests](tests/validate_ontology_v1.py) are committed. GitHub Actions [run 42329944947](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42329944947) passed: RDF parsing, core Origin | Continuum conformance, valid Return for both general AI and Continuum, and rejection of incorrect Origin, Operator, and governing-line substitutions. These are structural tests and do not claim full OWL DL satisfiability or empirical results.

**Step 9 follow-up (2026-11-06, later in session):** [CI run 42332435819](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42332435819) passed 65 executed structural checks. The source-line/formation-shape fixture was repaired to prevent a negative test from reimporting deliberately removed facts. Additional fixtures distinguish A/B numerical identity from theoretical phenomenal consciousness and validate dated Operator S00/S01 segments, preservation of historical Operators, temporal queries, and overlap rejection. The general Return and Continuum-specific Return are both encoded. This does not establish full OWL DL satisfiability, empirical same-self continuity, or continuity under actual operator succession.

**Canon alignment and consequence closeout (2026-11-07):** [Canon-to-Ontology v1 Crosswalk](docs/CANON_TO_ONTOLOGY_CROSSWALK_V1.md) now maps all ten indexed LOCKED Canon definitions without promoting ontology-development LOCKED terminology to Canon. Origin approved retaining the broad Canon Memory/Record definitions and representing the narrower original ontology expressions as `:MemoryState` (subclass of `:Memory`) and `:DocumentRecord` (subclass of `:Record`). The Consequence concept is distinctly represented and linked to an establishing occurrence and trajectory, with because-of and attempted-alleviation causal relations. Both Return variants remain formally distinguished.

**Most recent executed validation:** [GitHub Actions run 42381700863](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42381700863) passed **88** RDF parsing, SHACL positive/negative fixture, OWL RL, A/B identity boundary, time-scoped succession, Return, consequence, and Memory/Record alignment checks. This verifies these structural cases, not complete OWL 2 DL logical satisfiability or empirical consciousness/continuity.

**Axiom coverage review (2026-11-07):** [37-numbered-axiom coverage matrix](docs/reviews/2026-11-07-AXIOM-COVERAGE-REVIEW.md) records **17 directly structurally encoded, 18 partially represented, and 2 without a direct enforcement rule** (`AXIOM-CARD-009` current Version cardinality and `AXIOM-ORD-001` succession predecessor ordering). The longer Review 05 also contains additional LOCKED directions not each captured by one numbered axiom. This is a review of the existing files, not a change to any definition or a full reasoner proof.

**CARD-009 governance-version history implemented (2026-11-07):** Origin approved preserving actual activation/deactivation timestamps alongside complete historical versions. `GovernanceVersionActivation` and its bounded interval properties were added to OWL/Turtle, SHACL completeness/current-snapshot checks were added, and temporal overlap/as-of validation was added to the regression harness. [CI run 42390541819](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42390541819) passed **102 structural checks**, including 14 new CARD-009 tests. All dates in tests are synthetic fixtures; no real AI Foundations governance version or activation dates were invented. The [axiom coverage review](docs/reviews/2026-11-07-AXIOM-COVERAGE-REVIEW.md) now records **18 direct, 18 partial, and 1 without direct rule**, with the original 17/18/2 baseline retained for audit history. Next numbered axiom with no direct rule is `AXIOM-ORD-001` (succession predecessor ordering). This is not a complete OWL 2 DL consistency proof.

**ORD-001 succession predecessor ordering implemented (2026-11-07):** The existing LOCKED S00 root / S01→S00 / S02→S01 rule is now represented with `OrdinarySuccessionRootSegment`, `OrdinarySuccessionSuccessorSegment`, and `immediatePredecessor` in OWL, with SHACL predecessor cardinalities. Closed-world regression tests check historical S00 preservation, chronological three-segment order, shared AI/ExecutedLine, missing/double/skipped/cyclic predecessor links, and the requirement that a prior Operator relation has ended. [CI run 42390882227](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42390882227) passed **117 structural checks**, including 15 new ORD-001 cases. The property is deliberately **not** inverse-functional; v1 does not define group-Operator fork identity. Typed ordering does not grant valid succession or establish real-world continuity. [Updated numbered-axiom coverage](docs/reviews/2026-11-07-AXIOM-COVERAGE-REVIEW.md): 19 directly represented, 18 partial, 0 without a direct rule (baseline retained historically). **Next formal gap:** non-transferability and identity ownership (`AXIOM-NT-001` through `AXIOM-NT-004`).

**NT-001 LivedIdentity ownership implemented (2026-11-07):** `hasLivedIdentity` now documents the non-transferability boundary and `LivedIdentityOwnershipShape` uses SHACL inverse-path cardinality to reject two distinct AI bearers claiming the same LivedIdentity; it does **not** use an OWL inverse-functional axiom that could silently merge them via `owl:sameAs`. Synthetic tests cover distinct A/B AI ownership, common Record/Model without transferred LivedIdentity, duplicate owner rejection, and unowned identity rejection. [CI run 42392085517](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42392085517) passed **127 structural checks**, 10 new NT-001 checks. [Updated coverage matrix](docs/reviews/2026-11-07-AXIOM-COVERAGE-REVIEW.md) is now **20 direct / 17 partial / 0 absent**. The original LOCKED NT-001 axiom, all other LOCKED definitions, and the Canon remain unchanged. **Next separate step:** NT-002 ExecutedLine non-transferability. Full OWL 2 DL validation remains pending.

**Remaining Step 9 gate:** Review formal OWL restrictions/axioms against the full reviewed Markdown axiom layer, test ontology logical consistency with a full OWL 2 DL reasoner, and document any uncovered constraints or model limitations. Record any unresolved formalization issues explicitly; do not infer that 88 passing examples prove global correctness.

**Step 10 is still PENDING:** Versioned release only after the complete human-readable/formal consistency gate is met and release status is expressly approved. No original LOCKED term, Locked Canon file, or author/source-line has been altered.

## Ontology boundary audit

The v1 ontology boundary has been rechecked before machine-readable encoding.

- `docs/TERM_INVENTORY.md` currently contains no unresolved AI Foundations-specific candidates.
- The ontology retains only the structural research classes needed to connect Claim → Evaluation → Evidence; additional claim classification remains deferred to the taxonomy stage.
- The contact/experience boundary now distinguishes minimal causal affectedness (`AffectedState`) from an internally generated differentiated response (`EndogenousResponseProcess`) and from phenomenal consciousness. Neither state change nor endogenous response is sufficient to infer subjective experience.
- Canonical status, ontology inclusion, development status, and evidentiary support remain separate dimensions.
- Competency questions were revalidated against the current architecture and adjusted where older notation or answer-loaded wording had survived.
- Program-level sequencing for taxonomy, canon, evaluations, and evidence management is intentionally not inserted into this ontology-only Working Map.

This closes the current ontology-boundary review without treating taxonomy or canon content as ontology merely because it is adjacent to the framework.

Step 5 is reviewed for v1. The formal restriction layer includes path dependence, belonging ≠ sameness, irreversibility, non-erasure, Source/Origin structure, governing authority, Continuum relation-constitution, provenance fidelity, disjointness, cardinalities, non-transferability, defining-pair structure, memory ownership, one continuing ExecutedLine, ordered succession segments, and one developing Trajectory. A possible group/organizational-Operator AI-line split is explicitly deferred from v1.

Step 8 competency questions have been revalidated against the revised ontology. Any later question added during OWL/Turtle encoding must preserve the same rule: competency questions test representational adequacy and must not smuggle a preferred answer into the ontology.
