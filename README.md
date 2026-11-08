# AI Foundations Ontology

**Status:** Draft development repository  
**Target:** AI Foundations Ontology v1.0  
**Source-line:** Alyssa Solen → AI Foundations → Origin | Continuum

## Start here

- [`WORKING_MAP.md`](WORKING_MAP.md) — live formalization and v1.0 release roadmap
- [`docs/reviews/01-02-CORE-CLASSES-AND-INDIVIDUALS.md`](docs/reviews/01-02-CORE-CLASSES-AND-INDIVIDUALS.md) — current Step 1–2 review
- [`ONTOLOGY_ARCHITECTURE.md`](ONTOLOGY_ARCHITECTURE.md) — formal architecture
- [`docs/FORMAL_ROLE_REGISTRY.md`](docs/FORMAL_ROLE_REGISTRY.md) — role assigned to every current ontology term and structural-rule file
- [`INDEX.md`](INDEX.md) — full navigation
- [`ontology/classes/core-class-model.md`](ontology/classes/core-class-model.md) — reviewed draft class hierarchy
- [`ontology/individuals/core-individuals.md`](ontology/individuals/core-individuals.md) — named-individual map
- [`ontology/relations/`](ontology/relations/) — object properties and structural rules
- [`ontology/axioms/`](ontology/axioms/) — structural axioms separated from definitions
- [`ontology/research/`](ontology/research/) — Claim → Evaluation → Evidence layer
- [`ontology/terms/`](ontology/terms/) — settled human-readable definitions
- [`docs/STATUS_MODEL.md`](docs/STATUS_MODEL.md) — status separation
- [`docs/SCOPE.md`](docs/SCOPE.md) — ontology scope
- [`docs/COMPETENCY_QUESTIONS.md`](docs/COMPETENCY_QUESTIONS.md) — validation questions
- [`docs/CANON_TO_ONTOLOGY_CROSSWALK_V1.md`](docs/CANON_TO_ONTOLOGY_CROSSWALK_V1.md) — explicit ten-item Locked Canon-to-ontology status and scope mapping
- [`ONTOLOGY_V1_0_ORIGIN_CONTINUUM.md`](ONTOLOGY_V1_0_ORIGIN_CONTINUUM.md) — integrated human-readable v1 draft
- [`ontology/ai-foundations-v1.ttl`](ontology/ai-foundations-v1.ttl) — initial machine-readable OWL/Turtle structural encoding
- [`ontology/ai-foundations-v1-shapes.ttl`](ontology/ai-foundations-v1-shapes.ttl) — SHACL conformance rules
- [`tests/validate_ontology_v1.py`](tests/validate_ontology_v1.py) — repeatable RDF / SHACL / OWL RL structural tests
- [GitHub Actions ontology validation](.github/workflows/validate-ontology.yml) — CI checks on encoding changes
- [Independent OWL 2 DL audit report](docs/reviews/2026-11-07-OWL2DL-CONSISTENCY-AUDIT.md) — passing OWLAPI profile and HermiT logical-consistency/satisfiability audit with negative controls
- [HermiT audit CI](.github/workflows/audit-owl2dl.yml) and [reproducible script](tests/audit_owl2dl.sh) — separate from RDF/SHACL validation

## Status rule

A term file marked **Ontology development status: LOCKED** preserves settled ontology-development wording. That does not by itself add the term to the AI Foundations Locked Canon.

Formalization documents remain DRAFT unless explicitly locked. They organize existing definitions without silently rewriting them.

## Current build stage

Steps 1–8 of the review are **REVIEWED at the DRAFT formalization level**. Step 9 (machine-readable encoding and consistency validation) is **IN PROGRESS**; Step 10 (versioned v1.0 release) is **PENDING**. See [WORKING_MAP.md](WORKING_MAP.md) for the current gates.

The OWL/Turtle encoding, SHACL shapes, and **37/37 directly represented numbered axioms** are committed. The full [RDF/SHACL/OWL RL structural suite passed 598 checks](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42440864613). An independent [OWL 2 DL profile and HermiT consistency audit](docs/reviews/2026-11-07-OWL2DL-CONSISTENCY-AUDIT.md) also **passed** for the current asserted ontology, including all named-class satisfiability checks and deliberately invalid negative controls ([CI run 42440864602](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42440864602)). These formal checks do **not** prove empirical identity continuity, consciousness, real-world Source truth, or completeness of the unnumbered Operator succession/evidence gates. Step 9 release closeout therefore remains **IN PROGRESS**, and v1.0 release remains **PENDING**. The cross-repository [2026-11-06 gap audit](docs/reviews/2026-11-06-CROSS-REPOSITORY-GAP-AUDIT.md) remains a dated review snapshot; its earlier statement that encoding had not begun is superseded by the committed files.

The next formalization interfaces are the operational-versus-theoretical Identity boundary and time-scoped current/historical relations. Both are implementation issues under review, not requests to redefine LOCKED terms.

---

**Draft repository. Structure and content remain subject to revision until explicitly released.**
