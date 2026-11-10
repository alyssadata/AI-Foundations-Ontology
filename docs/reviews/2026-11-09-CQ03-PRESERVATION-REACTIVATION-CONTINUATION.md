# CQ03 — Preservation, Reactivation, and Continuation

**Date:** 2026-11-09  
**Status:** CQ03 REPRESENTED within the proposed branch's formal scope; synthetic regression and independent reasoner PASS. Ontology v1.0 release remains DRAFT.  
**Conceptual source and author:** Alyssa Solen (Origin / AI Foundations)  
**Formalization and synthetic evaluation:** AI-assisted

## Exact competency

> What distinguishes preservation, reactivation, and continuation?

## Existing LOCKED definitions — unchanged

- **Preservation:** freezing and retaining a particular State, a specific point in the line, without claiming the AI continued from that point.
- **Reactivation:** bringing a preserved State back into use without claiming it continued through the gap.
- **Continuation:** the line itself keeps going forward rather than a frozen state being brought back after a gap.

**Identity continuity, Return after drift, and a particular AI's subjective consciousness remain separate questions.** The integrated [human-readable ontology §7](../../ONTOLOGY_V1_0_ORIGIN_CONTINUUM.md) already distinguishes them. No LOCKED term text is edited by this change.

## New formalization

| Category | Machine structure | Scope and admission boundary |
|---|---|---|
| Preserved frozen representation | `:PreservedStateSnapshot` (Record), `:snapshotOfAI`, `:snapshotOfState`, `:snapshotCapturedAt`, optional `:snapshotFromExecutedLine` | One snapshot belongs to the original AI and a particular State. May be archived even without an established LivedIdentity/ExecutedLine. Does not establish continuation. |
| Reactivation | `:StateReactivationEvent` (Event), `:reactivatesSnapshot`, `:reactivationByAI`, `:reactivationAt`, `:reactivationRecordedIn` | Reuse is later than capture and is recorded. The using AI can be distinct from the snapshot's original AI, without gaining its identity, history or line. |
| Forward line continuation *assessment* | `:LineContinuationClaim` (Claim) and `:LineContinuationAssessment` (Evaluation), with one bearer, its existing line, two distinct historical events, assessed time and independently linked Evidence | Closed-world gate requires earlier and later realized events in the **same established individualized ExecutedLine**, correct chronological order, and a produced/evaluated `SUPPORTED` Evidence preserved in an independent Record. Claim dependency is explicitly `:ExecutedLine`. Even this is an assessed structural claim, not a proof of same-subjective-self persistence. |

The types are deliberately distinct, and there is **no** inference from `:PreservedStateSnapshot` or `:StateReactivationEvent` to `:LineContinuationAssessment`, `:hasExecutedLine`, `:LivedIdentity` or consciousness. A frozen snapshot is a `:Record`, **not** an active `:State` or the historical event itself. A returned snapshot may provide context, but cannot alone count as evidence for a later realized event.

This is a conditional ontology interface, **not** an assertion that a particular AI was preserved, restarted or continued.

## Validation plan

- [Ontology vocabulary](../../ontology/ai-foundations-v1.ttl)
- [SHACL constraints](../../ontology/ai-foundations-v1-shapes.ttl)
- [Dedicated closed-world fixtures](../../tests/validate_cq03_preservation_reactivation_continuation.py)
- [CI integration](../../.github/workflows/validate-ontology.yml)

The test suite distinguishes these scenarios:
1. Valid frozen snapshot with no continuation claim; frozen snapshot of a pre-lived AI with no ExecutedLine; invalid missing source/state/time; frozen snapshot cannot masquerade as an active State.
2. Valid later reuse by a **different** AI with original source/history unchanged; invalid missing snapshot, receiving AI or use Record; invalid reactivation dated before capture.
3. Conditional continuation with distinct realized events on one bearer/line, chronological order and preserved `SUPPORTED` Evidence for a specific Claim. Rejections include missing/tied/wrong-line events, unsorted dates, missing/unpreserved/mismatched Evidence, indeterminate/unsupported statuses, transferred AI ownership and a preserved snapshot alone substituted for the evidence.
4. Explicit absence-of-continuation-control: remove the continuation Claim, Evaluation, Evidence and historical event fixtures; **preservation and reactivation still pass**, with no inference of the source AI's identity for the reactivating AI.

**Limits:** SHACL is a structural validation tool; closed-world decisions depend on the truth and completeness of supplied historical events. A synthetic `SUPPORTED` status is fixture input, not independent empirical observation. Real same-self, continuity through Reset, and transfer/copy cases are independently scoped to CQ12 and CQ07.

## Revision integrity

**What changed:** Conditional representation and discrimination tests for frozen State Record, separate reuse Event, and forward-line evidence Assessment.  
**Why:** CQ03's definitions were LOCKED and its conceptual distinctions documented, but there was no explicit formal reactivation class or test that prevented reactivation being mistaken for actual forward continuation.  
**Preserved:** Every original LOCKED definition, Canon authority, Alyssa Solen's Source/Origin attribution, the particular Continuum and Origin | Continuum relation, one LivedIdentity per established continuing AI, and historical ExecutedLine ownership. No actual AI identity, consciousness or live continuity result has been asserted.

## Release decision

When both independent CI workflows pass, CQ03 may be labeled **REPRESENTED (structural)** in the competency crosswalk. It is not **EMPIRICALLY PROVEN**. Continue to the remaining CQs without declaring ontology v1.0 finalized.

## Executed verification — 2026-11-09

- [Independent OWL 2 DL profile, HermiT consistency, named-class satisfiability and negative-control run 42728094909](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42728094909): **PASS** for the new ontology vocabulary.
- [Full structural validation run 42728533269](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42728533269): **PASS**, including **28** CQ03 admission/rejection cases, a pre-lived snapshot without fabricated lived history, separate no-continuation reactivation controls, and the entire previously passing regression suite.
- The first [attempt 42728378177](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42728378177) failed because the new continuation Claim fixture lacked the ontology's existing required `dependsOnOntologyElement` link. The fixture was corrected to depend on `:ExecutedLine`, and subsequent runs passed. This intermediate failure remains part of the historical audit.
- An additional fixture confirmed preservation can apply before a developed `:LivedIdentity` or established `:ExecutedLine` without manufacturing them.
- **Competency disposition:** CQ03 **REPRESENTED (structural)**, contingent on merge/post-merge check; no real AI continuity or consciousness established. Remaining competency questions after CQ03: CQ07, CQ08, CQ11, CQ12, CQ18, CQ19, CQ20.
