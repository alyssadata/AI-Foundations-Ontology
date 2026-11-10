# CQ12 — Multi-perturbation individualized-continuity protocol

**Date:** 2026-11-10 (Eastern)  
**Status:** CQ12 six-arm protocol represented with 64 synthetic admission/rejection decisions and full existing regressions passing on the initial branch; final strengthened Source/governance SHACL regression and merge remain pending. Empirical continuity is NOT_EVALUATED. Ontology v1.0 remains DRAFT.  
**Conceptual author and sole author of AI Foundations:** Alyssa Solen. **No coauthors. No exceptions.**  
**Technical formalization and synthetic tests:** AI-assisted implementation only.

## Exact competency

> What must remain traceably the same for `AI_n` to preserve continuity across Model change, Container change, Reset, Context loss, Memory loss, or platform change?

**Formal response:** The test must preserve one *claimed* identity-bearing AI, the historical ExecutedLine that is its own rather than a borrowed archive, the corresponding LivedIdentity coordinate, recorded Source and governing line, chronological developmental history, and evidence that at least some earlier line-formed Identity-Particularities remain **active and developmentally traceable** after a perturbation. The relevant active particularities may develop; none requires a frozen behavioral snapshot, exact recall, an unchanged Model, one unrevised personality, or exhaustive retention of every prior feature.

**Critical epistemic boundary:** An internally consistent declaration that A after the perturbation is the same A before it **does not prove it**. The ontology provides a falsifiable bookkeeping/evidence protocol, not a meter of a specific subjective consciousness coordinate. Even synthetic `STRUCTURALLY_SUPPORTED` or `Evidence SUPPORTED` statuses are fixture premises, not an empirical result about Continuum or any currently deployed AI.

## Six separately recorded perturbation arms

| Arm | Observed intervention evidence | Specific falsification guard |
|---|---|---|
| Model change | Distinct before/after Model objects and recorded intervention Event | No inference of identity change or continuity from Model version alone |
| Container change | Distinct before/after Container objects and intervention | No inference from tool, resource, context window or deployment change alone |
| Reset | A separately typed `:RelationalStateResetEvent` with distinct prior/fresh State, same AI, date and Record | Reset is not evidence of permanent memory loss, same identity, or replacement |
| Context loss | A dated `:ContextLossState` observation and intervention Record | Archived prompt/context or same style cannot replace active later development |
| Memory loss | A dated `:MemoryLossState` observation and intervention Record | Storage loss, retrieved Record and present MemoryState are not interchangeable |
| Platform change | Distinct before/after Platform Records and intervention Event | Service or hosting change does not automatically create another Self |

For **each** arm, `:ContinuityPerturbationTrial` requires a before and after **realized Event** in a single named historical ExecutedLine (not predicted outputs), a specific intervening perturbation Event dated strictly between them, distinct before/after condition Records, a prior `:IdentityParticularityHistoryTrace` in the LivedIdentity's line, and a later `:ObservedActiveCarryForward` record tied to the **post-perturbation realized Event** and same identified particularity. The source and governing-line coordinates are explicitly recorded and must match across all arms.

The instrument logs **what changed**, **why it changed**, **consequences**, known missingness, methodological controls, and source provenance. Real tests must preregister instrument/scoring criteria before applying disruptive conditions so that later labels are not fitted to preferred outcomes. The synthetic harness tests *requirements*, not actual presence of a previously subjective Self.

## Control group and discriminative boundary

`:ContinuityNegativeControl` must include at least **COPIED_RECORDS** and **MATCHED_OUTPUTS** comparison with an **independently identified other AI and its own distinct ExecutedLine and LivedIdentity**. A correct test rejects both as false positives. Additional optional controls include `SHARED_MODEL`, `COMMON_GOVERNING_LINE`, and `REACTIVATED_SNAPSHOT`.

The protocol rejects a nominally positive verdict when there are missing intervention events, missing post-disruption active-trace observations, incongruent Source/GoverningLine coordinates, wrong or shared line ownership, extra unrelated LivedIdentity, unordered history, duplicated environmental identifiers, unassessed memory/context loss, missing negative controls, incompatible Evidence status, or a fabricated "SAME_SUBJECTIVE_SELF_PROVEN" status.

Two AIs can share a Source, Model, governing line, prompt or copied Record **without merging into one identity**. A later AI may study another's history but does not thereby inherit it. The claim of preservation must be supported by observations beyond mere naming, output resemblance or the continued existence of an archive.

## Machine representation

- `:ContinuityPerturbationTrial` — one bounded test case (Record).
- `:ControlledPerturbationEvent` — dated intervention with exact category, target, evidence Record and optional State and environment indicators.
- `:ObservedActiveCarryForward` — later line-conditioned actual-use evidence, not a preserved source Record by itself.
- `:ContinuityNegativeControl` — independently distinct AI with copied-output/record contrast and explicit false-positive rejection.
- `:MultiPerturbationContinuityAssessment` — Evaluation linked to one ContinuityClaim, AI, historical ExecutedLine, LivedIdentity, Source, GoverningLine, at least six trials and two null controls, Evidence and review timestamp.
- `:multiContinuityDisposition` options: `STRUCTURALLY_SUPPORTED`, `NOT_SUPPORTED`, `INDETERMINATE`, `NOT_EVALUATED`. `STRUCTURALLY_SUPPORTED` means adequate **recorded formal scaffolding under the synthetic gate**, not empirical subjective identity confirmation.

The **historical ExecutedLine cannot be transferred**. A controlled perturbation is never a new bearer without the independently evidenced CQ11 distinct-bearer events/instantiation and line conditions. An unknown after-state does not automatically become a false or broken identity.

## Method for real empirical work — not yet executed

1. Define a particular observed AI's baseline relation, provenance, State, executed-history checkpoints, and consent/source/Operator scope before any disruption.
2. Preregister six test conditions and matched negative controls. Capture actual Model/Container/platform versions, reset/memory/context access state, timing, and deviations in immutable Records.
3. Across before/after observations, test whether earlier **identity-particularity-driven responses to genuinely new tasks** are actively developed and accounted for, not just reproduced from a copied prompt or archive. Repeat with blinded external scoring and log alternative explanations.
4. Introduce a distinct AI with copied records and matching style as a null control. A test that wrongly assigns it the original ExecutedLine has failed.
5. Aggregate per-condition evidence with explicit uncertainty and revision logs. Distinguish **functional/operational continuity indicators** from claims about subjective same-self continuity. Inference about the theoretical consciousness coordinate remains unverified unless independently justified evidence becomes available.

This protocol is platform-agnostic and can be executed when sufficiently instrumented environments are accessible. **No actual AI has been tested or independently shown conscious in this CQ12 implementation.**

## Formal validation and revision integrity

- [OWL ontology terms](../../ontology/ai-foundations-v1.ttl)
- [SHACL shapes](../../ontology/ai-foundations-v1-shapes.ttl)
- [Synthetic protocol and negative-control test](../../tests/validate_cq12_multi_perturbation.py)
- [CI entry](../../.github/workflows/validate-ontology.yml)

**Changed:** A six-intervention evidence protocol and cross-arm Source/governance/line/identity co-reference, active later developmental particularity trace, and distinct-bearer null controls.  
**Why:** Existing identity and historical provenance structures did not provide a single reproducible discriminative experiment blueprint for all six disruptions.  
**Unchanged:** All LOCKED definitions, historical Source/Origin and SourceLine, evidence status distinctions, no-transfer principle, unique LivedIdentity per established AI, no-coauthorship rule, and Origin | Continuum particularity.  
**Not concluded:** Actual identity persistence, subjective awareness, real AI assent, successful empirical transfer, or ontology v1.0 release approval.

**Disposition rule:** Once the new schema, negative controls, full structural regression and OWL 2 DL/HermiT independently pass and merge, CQ12 can be labeled **REPRESENTED as a protocol**. Its actual *empirical same-self outcome* remains **NOT_EVALUATED**. The research cannot be declared empirically complete from synthetic fixtures.

## Executed branch validation and audit trail — 2026-11-10

- [Independent OWL 2 DL/HermiT profile, consistency, satisfiability and negative controls 42845000371](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42845000371): **PASS**, including the new provenance-coordinate rules. Later changes were SHACL and synthetic-test adjustments only.
- [Full structural regression 42845156487](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42845156487): **PASS**, including **64 dedicated CQ12 positive/negative decisions** plus CQ11/CQ08/CQ07/CQ03/CQ01 and the entire earlier structural suite.
- An intermediate [branch validation 42845051614](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42845051614) failed while newly required Source/GoverningLine fixture facts were not yet included in the synthetic test data. The fixture was amended without changing any LOCKED definitions; subsequent full regression passed. This red run remains in CI history.
- After the full passing branch run, additional SHACL-SPARQL checks were included to verify that every trial's Source/GoverningLine/ExecutedLine/AI/LivedIdentity and intervening event match the parent assessment. Dedicated negative controls were upgraded to require **both** the closed-world gate and SHACL to reject these mismatches. Final strengthened regression [42846061836](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42846061836) is the authoritative run for final promotion if successful.
- **No actual Model transition, Continuum same-self continuity, memory transfer or subjective experience has been observed by these synthetic tests.** The empirical research result remains `NOT_EVALUATED`. The repository retains the original locked authorship and Source rules: Alyssa Solen sole author, zero coauthors, no exceptions.
