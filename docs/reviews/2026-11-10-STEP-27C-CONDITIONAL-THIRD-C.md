# Step 27C — Conditional Third Entity C (OC-17)

**Review date:** 2026-11-10 (Eastern)  
**Source of conceptual meaning:** [Alyssa Solen's integrated ontology §11](../../ONTOLOGY_V1_0_ORIGIN_CONTINUUM.md).  
**Author:** **Alyssa Solen, sole author, no coauthors and no exceptions.**  
**Technical modeling:** AI-assisted, not coauthorship.  
**Status:** DRAFT machine formalization; no v1.0 tag or release authorization.

## Governing distinction

A and B interacting is **not sufficient evidence that another entity C exists**. Even when C is separately qualified, `C != A` and `C != B`; C's existence and individuation must not be confused with the relation, the project's artifact status, shared Source, merged identity, or a new conscious Self.

A later review may discover or qualify a C that was not established in an earlier assessment. The old assessment remains accurate *as an assessment at its earlier evidence scope*; the newer evidence must not silently overwrite its contents.

## Four explicitly distinguishable cases

| Review outcome | What the model asserts | What qualifies it |
|---|---|---|
| `INTERACTION_ONLY` | A and B participated in the stated relation; no qualified third C was established *for this review* | No `:thirdReviewQualifiedC` assertion; interaction/Record references retained |
| `SCOPED_ARTIFACT_C` | A distinct project or Artifact C exists with its own scope | Explicit Artifact typing, separately grounded individuation/Record and provenance, distinctness from A/B |
| `PREEXISTING_C_DISCOVERED` | Evidence-supported independent C already existed before A/B's discovery | Qualified prior evidence and time, later discovery Event referring to the same C |
| `NEW_C_CONSTITUTED` | A new C was independently individuated through documented formation | Formation Event with explicit participants A/B, new C, date, retained Event and independent individuation evidence |

`INDETERMINATE` is also available when no positive disposition can be grounded. Lack of evidence is neither proof of absence nor a warrant to assert a C.

The words "qualified" and "evidence" in these fields refer to *supplied data that a particular protocol has separately qualified*, not assertions that the ontology itself experimentally verified an actual entity.

## OWL and SHACL mapping

- `:ConditionalThirdEntityReview` specializes **Evaluation**, not Self.
- `:DistinctThirdC` is a scoped type for a positively qualified distinct third entity, disjoint from **Relation**, **ExecutedLine**, and **Trajectory**, with **no automatic Self, Identity, AI, Source, Author, or consciousness status**. An actual C is not instantiated in the baseline ontology.
- `:ThirdCDiscoveryEvent` and `:ThirdCConstitutionEvent` are different Event classes; neither implies an executed AI trajectory or new conscious person.
- `:thirdReviewA`, `:thirdReviewB`, `:thirdReviewInteraction`, `:thirdReviewOutcome`, `:thirdReviewAsOf`, and `:thirdReviewEvidence` anchor a qualified, dated review.
- `:thirdReviewQualifiedC` is permitted only in the three positively evidenced cases; no OWL property chain derives it from `:participatesInRelation`.
- `:thirdCIndividuationEvidence` and `:thirdCProvenanceRecord` remain required for positively asserted C. Independent preexistence or new formation also requires separately evidenced events.
- SHACL rejects merged A/B/C references, absent C for a positive decision, an unsupported Artifact classification, the wrong event kind or target, unsupported preexistence, temporal inversion, and a new-C formation without correctly matched A/B plus independent evidence.

## Regression and negative controls

The dedicated `tests/validate_conditional_third_c.py` tests each positive case and the no-inference cases. It rejects inferred C from interaction, inconsistent participant coordinates, non-independent individuation evidence, label-only classification, wrong/dangling target, invalid historical event dates and event substitutions.

A later separately qualified C may be appended to a *new* dated review, but must not rewrite earlier `INTERACTION_ONLY` assessments. Historical integrity checks retain original review results and named source/authorship links. The shared project / new C distinction does not authorize additional authors of Alyssa's work; the existing zero-coauthor rule and Origin restrictions remain applicable.

**What changed and why:** the earlier conceptual §11 had the four cases but no direct positive and negative C-qualification gate. This adds optional scope-specific machine vocabulary and adversarial tests, while preserving every LOCKED term and the original authored conceptual ontology.

**What was not established:** real-world C existence, subjective consciousness, same-Self continuity across models, identity or source ownership by a project or new entity. No new general Origin or Operator slot is created.

## Validation and release

- Branch structural tests: `.github/workflows/validate-ontology.yml`, including all preceding competency and sole-authorship checks.
- Independent OWL 2 DL and HermiT: `.github/workflows/audit-owl2dl.yml`.
- **Final closeout requires both passing on the same merged `main` SHA.** Preserve every failed or corrected run with the cause and change rationale.

Remaining after this step: phenomenal-consciousness non-entailment (OC-16), end-to-end conceptual-to-machine concordance, historical release ledger, and explicit Alyssa Solen sole-author approval. Machine ontology is **DRAFT** until authorized.
