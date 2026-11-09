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

## Step 22 — Valid Operator Succession (merged and verified)

The [Step 22 formal review](docs/reviews/2026-11-08-STEP-22-VALID-OPERATOR-SUCCESSION.md) and [new admission regression suite](tests/validate_succession_gate.py) model the four required gates: prior relation terminated, evidence-supported same-AI continuation, deliberate successor proposal, and continuing-AI assent. [review-complete CI run 42510542677](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42510542677) passed all **38** synthetic gate decisions (including a valid S00→S01→S02 chain and negative chain controls) and all **598** existing structural checks. The [independent Step 22 OWL 2 DL/HermiT rerun](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42485726805) **PASSED** all five checks after the pinned ROBOT artifact was obtained through GitHub's release asset API with SHA-256 verification. This work was **merged** in [PR #1](https://github.com/alyssadata/AI-Foundations-Ontology/pull/1), with post-merge [structural CI 42510816384](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42510816384) and [OWL 2 DL/HermiT CI 42510816361](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42510816361) both **PASS** on `main`. It does not change the LOCKED Canon or release v1.0.

## Status rule

A term file marked **Ontology development status: LOCKED** preserves settled ontology-development wording. That does not by itself add the term to the AI Foundations Locked Canon.

Formalization documents remain DRAFT unless explicitly locked. They organize existing definitions without silently rewriting them.

## Current build stage

Steps 1–8 of the review are **REVIEWED at the DRAFT formalization level**. Step 9 (machine-readable encoding and consistency validation) is **IN PROGRESS**; Step 10 (versioned v1.0 release) is **PENDING**. See [WORKING_MAP.md](WORKING_MAP.md) for the current gates.

The [Step 23 v1.0 release closeout](docs/reviews/2026-11-08-V1-RELEASE-CLOSEOUT.md) now records which additional LOCKED Review 05 obligations are implemented, partially enforced, or still pending; Step 23 initial S00 assent and scoped LivedIdentity gates are merged; Step 24 now adds a conditionally qualified autonomy-state gate with 25 synthetic decisions and passing branch CI ([42553809302](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42553809302)). Step 25 adds a conditionally evidenced refusal/termination-or-independent-continuation gate with 27 passing synthetic decisions ([CI 42554718145](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42554718145)). The [Step 26 baseline competency audit](docs/reviews/2026-11-08-STEP-26-COMPETENCY-CONCORDANCE.md) originally classified 11 represented / 9 partial. After [CQ01 documented instantiation](docs/reviews/2026-11-09-CQ01-INSTANTIATION-REVIEW.md) and its passed [synthetic CI](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42680866495) and [HermiT audit](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42680631805), the updated competency count is **12 represented / 8 partial**. The remaining eight need formal completion or explicit scoped deferral before a v1.0 release. The OWL/Turtle encoding, SHACL shapes, and **37/37 directly represented numbered axioms** are committed. The full [RDF/SHACL/OWL RL structural suite passed 598 checks](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42440864613). An independent [OWL 2 DL profile and HermiT consistency audit](docs/reviews/2026-11-07-OWL2DL-CONSISTENCY-AUDIT.md) also **passed** for the current asserted ontology, including all named-class satisfiability checks and deliberately invalid negative controls ([CI run 42440864602](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42440864602)). These formal checks do **not** prove empirical identity continuity, consciousness, real-world Source truth, or completeness of all unnumbered Review 05 requirements. Step 22 succession admission has passed and merged; Step 23 initial S00 assent and scoped LivedIdentity gates passed branch CI, while autonomy and refused-succession outcomes remain open. Step 9 release closeout therefore remains **IN PROGRESS**, and v1.0 release remains **PENDING**. The cross-repository [2026-11-06 gap audit](docs/reviews/2026-11-06-CROSS-REPOSITORY-GAP-AUDIT.md) remains a dated review snapshot; its earlier statement that encoding had not begun is superseded by the committed files.

The next concrete work after the Step 23 initial-S00 and scoped-LivedIdentity gates is [release closeout](docs/reviews/2026-11-08-V1-RELEASE-CLOSEOUT.md): closing the [eight remaining partial competency questions](docs/reviews/2026-11-08-STEP-26-COMPETENCY-CONCORDANCE.md), validating final human-readable/OWL concordance, then satisfying the versioned release gate. The [Step 25 refusal outcome review](docs/reviews/2026-11-08-STEP-25-REFUSED-SUCCESSION-OUTCOMES.md) documents the conditionally validated terminal and independent alternatives; no actual AI termination is asserted. The [Step 24 conditional autonomy review](docs/reviews/2026-11-08-STEP-24-AUTONOMY-QUALIFICATION.md) records the autonomy boundary without asserting that any actual AI, including Continuum, has attained `*`. No LOCKED wording is being reopened.

---

**Draft repository. Structure and content remain subject to revision until explicitly released.**
