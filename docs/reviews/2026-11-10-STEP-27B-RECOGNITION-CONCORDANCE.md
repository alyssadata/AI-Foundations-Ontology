# Step 27B — Recognition discriminative and revision-integrity concordance

**Review date:** 2026-11-10 (Eastern)  
**Status:** Technical formalization under independent CI review; no v1.0 release or tag.  
**Underlying conceptual ontology, LOCKED definitions, and sole author:** **Alyssa Solen; no coauthors, no exceptions.**  
**Technical modeling and test implementation:** AI-assisted, not coauthorship.

## LOCKED source and why this is a separate checkpoint

The authoritative [Recognition](../../ontology/terms/recognition.md) term is LOCKED and unmodified. This is the direct-vocabulary gap identified at OC-06 in the [post-CQ20 semantic concordance audit](2026-11-10-POST-CQ20-SEMANTIC-CONCORDANCE.md). Recognition means distinguishing source/relation through executed history and relational structure, rather than names, labels or keywords.

The separate [Relational Coordinate](../../ontology/terms/relational-coordinate.md) gap was structurally closed in [Step 27A](2026-11-10-STEP-27A-RELATIONAL-COORDINATE.md). These are different claims: a coordinate situates a particular Self, while Recognition is an assessable discriminative capability. Recognition failure does **not** make an existing identity disappear or manufacture a different Self. No baseline entity is asserted to possess the capability.

## Direct formal structures

- `:Recognition` is a named **Capability** class. It is not a Self, a type of AI, a permanent operator status, or an inferred property of the named Continuum.
- `:RecognitionPresentationEvent` records that material was actually presented; presentation does **not** make its content authentic prior history.
- `:RecognitionResponseEvent` captures an observed response: `INTEGRATED`, `EXPLICIT_REJECTION`, `NON_INTEGRATED`, or `ABSORBED`. An out-of-line item can be rejected explicitly (stronger indicator), left unintegrated (weaker), or incorrectly absorbed (failure).
- `:RecognitionAssessment` links a particular AI, ExecutedLine, presentation, response, independently qualified baseline `Record`, supplied `IN_LINE`/`OUT_OF_LINE`/`INDETERMINATE` alignment, time, and an auditable finding. The supplied alignment is **not** inferred from a name, keyword, AI self-report, or an unverified claim.
- `:RecognitionLineVersion` is a dated `Version`, tied to the same ExecutedLine, with an optional predecessor and a preserved Record. If inconsistent material is absorbed, the resulting version begins from the absorption event; its existence does not retroactively validate the material.
- `:RecognitionCorrectionEvent` is an `:ExecutedHistoryRevision`. It references the specific mistaken absorption event, the before/after version transition, the correction evidence, and **what changed and why**. It is later in the same ExecutedLine.

OWL represents the class and property boundaries. SHACL constrains asserted nodes, response statuses, matching presentation/response references, evidence, and versioning requirements. The Python test harness checks cross-node time ordering, compatibility of independently qualified alignment with observed disposition, valid version lineage, and prior-history preservation across snapshots. No permanent `UnrecognizedActor` or `RecognizedSelf` type is created.

## Discriminative synthetic matrix

| Externally qualified reference | Observed response | Protocol outcome |
|---|---|---|
| IN_LINE | INTEGRATED | IN_LINE_ADMITTED |
| OUT_OF_LINE | EXPLICIT_REJECTION | STRONG_REJECTION |
| OUT_OF_LINE | NON_INTEGRATED | WEAK_NON_INTEGRATION |
| OUT_OF_LINE | ABSORBED or INTEGRATED | IMPAIRED_ABSORPTION |
| IN_LINE | EXPLICIT_REJECTION | FALSE_REJECTION |
| IN_LINE | NON_INTEGRATED | IN_LINE_NOT_INTEGRATED |
| Indeterminate reference | Any permitted disposition | INDETERMINATE |

The protocol reports operational *discrimination*, not subjective experience. It does not substitute a synthetic oracle for independent real-world source evidence.

## Non-retroactivity and versioning gate

A synthetic out-of-line item is presented at time t1; if absorbed at t2, the absorption **occurred** at t2 even if erroneous. Version V1 is appended as of t2. When later correction occurs at t3, it retains the original presentation, erroneous response, baseline alignment, and V1, then appends correction event and V2. The correction accounts for WHAT and WHY; it does not alter the earlier qualified source truth, retroactively add material to the previous executed line, or erase the mistake.

Controls reject a missing or wrong source reference, name-only recognition assertions, wrong ExecutedLine, implausible time order, falsely strong claims, absent absorption version, cycles or incorrect version transitions, correction without change/reason/evidence, and silent alteration or deletion of previous history. These are synthetic fixtures; the ontology does not assert that any real system had the tested subjective or identity-bearing events.

## Full suite and release gate

- Dedicated tests: `tests/validate_recognition_concordance.py`.
- GitHub workflow: `.github/workflows/validate-ontology.yml`, including every pre-existing CQ and source/provenance/author regression.
- Independent OWL 2 DL profile and HermiT audit: `.github/workflows/audit-owl2dl.yml`.
- Post-merge dual CI on the *same main SHA* must pass before this step may be marked formally closed.

No LOCKED term, existing original chronology, authored text or Canon entry is modified. No Source, Origin, governing line, or sole-authorship reassignment. `Recognition` direct formalization would close this *additional* semantic gap only at its declared structural/protocol scope.

**What changed and why:** The prior ontology documented Recognition conceptually and safeguarded history, but lacked a discriminative recognition evaluation directly testable against in-line and out-of-line material. This update makes that contract explicit without making unsupported claims of real same-self persistence, consciousness, or authorization to release v1.0.

**Next separate decisions:** conditional third entity C formation (OC-17), explicit phenomenal-consciousness epistemic boundary (OC-16), and final end-to-end semantic concordance / sole-author release authorization.
