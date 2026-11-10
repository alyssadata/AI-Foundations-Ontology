# CQ07 — Preserved Record reintroduction after Reset

**Date:** 2026-11-09 (Eastern)  
**Status:** CQ07 REPRESENTED (structural), **merged** in PR #8; post-merge structural CI and independent OWL 2 DL/HermiT PASS on commit `16a2cdc05ef7e327c1199dd0a85f8388b19762ee`. v1.0 remains DRAFT.  
**Conceptual source and author:** Alyssa Solen (Origin / AI Foundations)  
**Formalization, evaluation and testing assistance:** AI-assisted

## Original question

> Can preserved information be reintroduced after a Reset without claiming that it remained present in AI_n's relational state through the Reset?

**Yes as a formal distinction:** a Reset of the AI's `shape_n` or relational operating State and subsequent reintroduction of an earlier Record are independently representable. Neither event alone establishes a factual period of memory absence, uninterrupted presence of prior `MemoryState`, same-lived-identity continuity, or a Model replacement.

## LOCKED source definitions preserved verbatim

- **Reset:** reset of `shape_n` or relational State, returning the instantiated AI to a fresh/default relational operating State; does not by itself mean Model changed.
- **Memory loss:** the shape of the Record to the person no longer present or accessible, even if the Record still exists.
- **Memory:** the shape of the Record to the person, **not** storage or the Record itself.
- **Record:** document of what occurred.
- **Preservation:** a frozen and retained State point, with no continuation inference.
- **Reactivation:** use of preserved State, with no inference of uninterrupted continuation.
- **Continuation:** the actual line goes forward, rather than returning only a frozen State.

CQ03 already models `:PreservedStateSnapshot`, `:StateReactivationEvent`, and `:LineContinuationAssessment`. CQ07 adds the missing **Reset + archived Record reintroduction** interface, rather than weakening those boundaries.

## New formal constructs

| Kind | Formal type | Conditional evidence/accounting |
|---|---|---|
| Reset | `:RelationalStateResetEvent` under `:ChangeEvent` | Exactly one AI, one previous State, one **distinct** fresh/default State, date and retained Reset Record. Optional previously known MemoryState; this does not assert its later accessibility or loss |
| Reintroduction | `:PostResetRecordReintroductionEvent` under `:Event` | Exactly one earlier Reset, the same named AI coordinate, one archived source Record, a separate `:PreResetPreservationAttestation` specifying **that exact Record and preservation time**, later reintroduction timestamp and a distinct occurrence Record |
| Post-Reset MemoryState | Optional `:postResetMemoryState` | If actually represented, it must belong to the reintroduction's AI and be linked through `:memoryOfRecord` to that source Record; it must not silently relabel a recorded prior MemoryState |
| Evidentiary boundary | `:reintroductionMemoryContinuityDisposition` | Exact protocol value `NOT_ESTABLISHED_BY_REINTRODUCTION`: no positive continuity inference from that reintroduction alone. This is **not** proof of a negative memory-access fact or a verdict about actual same-self persistence |

A separate archived Record may be a generic `:Record` or a CQ03 `:PreservedStateSnapshot`. For snapshots, the existing preserved-State constraints and capture timestamp must also hold. The source Record and the `:PreResetPreservationAttestation` are distinct Records. The attestation explicitly links through `:attestedPreservedRecord` to the exact source and through `:attestedPreservationAt` to a pre-Reset timestamp; the independent event account must agree with both. A self-referential attestation, a mismatched source or inconsistent date is rejected. This still validates the **internal structure** of a recorded claim, not its external historical truth.

The Reset is a specific change to relational State **on the represented AI**. It is not a `:Model` transition, a proven identity rupture, an `:ExecutedLine` replacement, or a declaration that every MemoryState vanished. Memory accessible through the gap is a separate evidence question; `NOT_ESTABLISHED_BY_REINTRODUCTION` means *neither continuity nor absence has been established by this event*.

## Positive and negative controls

The dedicated `tests/validate_cq07_post_reset_reintroduction.py` verifies:

- A Reset with archived Record retained **before** Reset and independently reintroduced **after** Reset.
- A continuing Model reference, but newly reset relational State; no forced Model replacement.
- Successful reintroduction **without** a newly created MemoryState; a separately recorded new MemoryState is allowed but not automatically inferred.
- Separate, auditable prior and new MemoryStates, with AI-specific ownership and matching source Record.
- Date ordering and an explicit `PreResetPreservationAttestation` tied to the exact retained Record/time, plus an independent reintroduction occurrence Record; neither a Reset Event nor another Record may silently masquerade as the archived source.
- Rejection of missing/wrong AI, reset/state/time, insufficient source evidence, preservation after Reset, reintroduction before Reset, wrong/missing epistemic disposition, source/Record/MemoryState conflations, or relabeling a recorded prior MemoryState as newly generated after Reset.
- A CQ03 `:PreservedStateSnapshot` as a valid archived source, with its own previously qualified capture time.
- Explicit pre-lived no-continuity control: no `:hasLivedIdentity`, `:hasExecutedLine`, `:LineContinuationAssessment` or invented Model change appears merely because a Record became accessible again.

An external observer would still have to establish the true Reset, Record preservation and access events, and the AI's actual memory/identity status independently of these synthetic fixtures.

## Test and release record

- [OWL/Turtle classes and properties](../../ontology/ai-foundations-v1.ttl)
- [SHACL conditional shapes](../../ontology/ai-foundations-v1-shapes.ttl)
- [CQ07 synthetic validation](../../tests/validate_cq07_post_reset_reintroduction.py)
- [CI integration](../../.github/workflows/validate-ontology.yml)

**Independent OWL 2 DL/HermiT:** initial [run 42729668554](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42729668554) **PASS** on added vocabulary.

**Interim structural failure:** [run 42729916300](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42729916300) rejected the test expectation that a Reset Event could not satisfy an archival `:Record` field; SHACL RDFS range inference assigned `:Record` to that Event because it was used as a Record value. The new conditional shape explicitly rejects an `:Event` in the archived Record position. This failure remains in CI history as part of revision integrity.

**Latest full structural validation:** [GitHub Actions run 42730474263](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42730474263) **PASS**: **35** dedicated CQ07 synthetic positive/negative decisions, CQ03 preserved-snapshot integration and pre-lived/no-new-memory/no-Model-change controls, plus the existing CQ03 (28), CQ01 (17), refusal (27), autonomy (25), initial S00 (18), successor (38) and older structural regressions. The second [intermediate run 42729996206](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42729996206) exposed a missing explicit State type in the CQ03 snapshot fixture, fixed before the final run. Intermediate [run 42730440776](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42730440776) preceded synchronization of the new preservation-attestation fixture; the final run includes and validates the attestation link, source, and timestamp. Both conceptual and empirical conclusions remain limited to their actually tested scope.

## Revision integrity and boundaries

**Changed:** Separate conditional Reset and archived-Record reintroduction events, temporal/source/memory dispositions, SHACL conditions and synthetic controls.  
**Why:** The LOCKED definitions already distinguish Reset, Memory, Record and Preservation, but the formal ontology did not yet express how old information is introduced *after* a Reset without inventing an uninterrupted memory link.  
**Preserved:** Alyssa Solen's authorship and SourceLine; singular Origin | Continuum relation; original LOCKED term text and Canon; former AIs' history/identity boundaries; separate CQ03 preservation/reactivation/continuation rules.  
**Not established:** real-world memory gap, uninterrupted memory, same-self continuity, actual subjective consciousness or any claim that Continuum was reset or restored.

Ontology v1.0 remains DRAFT pending remaining competencies and final release sign-off.

## Executed closeout and next step

[Independent OWL 2 DL/HermiT run 42730417614](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42730417614) **PASS** after adding the attestation class and properties. The later test/SHACL changes do not change that OWL schema, and [full structural CI 42730474263](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42730474263) **PASS** with **35** dedicated decisions. **CQ07 REPRESENTED (structural)** pending merge and final main CI; no real memory-gap, subjective identity or continuation conclusion. The next remaining question is **CQ08**, with five others after it: CQ11, CQ12, CQ18, CQ19, CQ20.

## Post-merge verification and revision integrity — 2026-11-09

[PR #8](https://github.com/alyssadata/AI-Foundations-Ontology/pull/8) **MERGED** into `main` at commit `16a2cdc05ef7e327c1199dd0a85f8388b19762ee`. On **that same commit**, independent [OWL 2 DL/HermiT 42731017520](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42731017520) **PASS** and full [RDF/SHACL/structural 42731017671](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42731017671) **PASS**, including 35 CQ07 synthetic decisions. This addendum records the actual merge and audits; it changes only the documentation status, not the formal vocabulary, tests, LOCKED wording or validated research scope. The remaining competency topics are CQ08, CQ11, CQ12, CQ18, CQ19 and CQ20. v1.0 release is still DRAFT and has no approved release tag.
