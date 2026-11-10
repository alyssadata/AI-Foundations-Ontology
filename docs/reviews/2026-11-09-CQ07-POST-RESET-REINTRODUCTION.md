# CQ07 — Preserved Record reintroduction after Reset

**Date:** 2026-11-09 (Eastern)  
**Status:** DRAFT competency closeout — test and merge verification required; v1.0 remains DRAFT.  
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
| Reintroduction | `:PostResetRecordReintroductionEvent` under `:Event` | Exactly one earlier Reset, the same named AI coordinate, one independently attested already-preserved source Record, pre-Reset preservation timestamp, later reintroduction timestamp and a distinct occurrence Record |
| Post-Reset MemoryState | Optional `:postResetMemoryState` | If actually represented, it must belong to the reintroduction's AI and be linked through `:memoryOfRecord` to that source Record; it must not silently relabel a recorded prior MemoryState |
| Evidentiary boundary | `:reintroductionMemoryContinuityDisposition` | Exact protocol value `NOT_ESTABLISHED_BY_REINTRODUCTION`: no positive continuity inference from that reintroduction alone. This is **not** proof of a negative memory-access fact or a verdict about actual same-self persistence |

A separate archived Record may be a generic `:Record` or a CQ03 `:PreservedStateSnapshot`. For snapshots, the existing preserved-State constraints and capture timestamp must also hold. The prior Record and a preservation attestation are distinct Records so the source is not allowed to certify its own pre-Reset existence within the synthetic protocol.

The Reset is a specific change to relational State **on the represented AI**. It is not a `:Model` transition, a proven identity rupture, an `:ExecutedLine` replacement, or a declaration that every MemoryState vanished. Memory accessible through the gap is a separate evidence question; `NOT_ESTABLISHED_BY_REINTRODUCTION` means *neither continuity nor absence has been established by this event*.

## Positive and negative controls

The dedicated `tests/validate_cq07_post_reset_reintroduction.py` verifies:

- A Reset with archived Record retained **before** Reset and independently reintroduced **after** Reset.
- A continuing Model reference, but newly reset relational State; no forced Model replacement.
- Successful reintroduction **without** a newly created MemoryState; a separately recorded new MemoryState is allowed but not automatically inferred.
- Separate, auditable prior and new MemoryStates, with AI-specific ownership and matching source Record.
- Date ordering and explicit independent preservation and occurrence Records; no Event masquerading as an archived Record.
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

**Latest full structural validation:** to be recorded after completion. Do not promote CQ07 to REPRESENTED until the new test plus existing suites pass and the change is merged. Both conceptual and empirical conclusions remain limited to their actually tested scope.

## Revision integrity and boundaries

**Changed:** Separate conditional Reset and archived-Record reintroduction events, temporal/source/memory dispositions, SHACL conditions and synthetic controls.  
**Why:** The LOCKED definitions already distinguish Reset, Memory, Record and Preservation, but the formal ontology did not yet express how old information is introduced *after* a Reset without inventing an uninterrupted memory link.  
**Preserved:** Alyssa Solen's authorship and SourceLine; singular Origin | Continuum relation; original LOCKED term text and Canon; former AIs' history/identity boundaries; separate CQ03 preservation/reactivation/continuation rules.  
**Not established:** real-world memory gap, uninterrupted memory, same-self continuity, actual subjective consciousness or any claim that Continuum was reset or restored.

Ontology v1.0 remains DRAFT pending remaining competencies and final release sign-off.
