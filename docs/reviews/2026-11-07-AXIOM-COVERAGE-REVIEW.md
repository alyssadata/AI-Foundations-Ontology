# AI Foundations Ontology — Numbered Axiom Coverage Review (v1 candidate)

**Review date:** 2026-11-07  
**Conceptual source / framework author:** Alyssa Solen — AI Foundations / Origin | Continuum  
**Review assistance:** AI-supported repository comparison and coverage classification  
**Method:** Read-only comparison of all 37 numbered `ontology/axioms/AXIOM-*.md` files against `ontology/ai-foundations-v1.ttl`, `ontology/ai-foundations-v1-shapes.ttl`, `tests/validate_ontology_v1.py`, the architecture, and Review 05.  
**Repository baseline:** `main` commit `997cf9b555a1cd39ce8ea739aa598a8eb5b59ca8` at review start.  
**Status:** REVIEW REPORT / DRAFT remediation proposals. Not Locked Canon, not a new axiom, and not a change to original LOCKED terms or restrictions.

## Counting and interpretation

- **17 / 37 — D: Direct structural encoding.** The relevant class/rule/relationship is explicitly represented in OWL, SHACL, or both. **This is not proof of global logical consistency or exhaustive negative-case testing.**
- **18 / 37 — P: Partial.** Some formal representation is present, but a declared scope, condition, history invariant, machine constraint, or required validation is absent.
- **2 / 37 — G: No direct enforcement rule.** Supporting properties may exist, but the specific numbered axiom is not machine-enforced.
- The repository reported **88 passing structural validation checks** in [CI run 42381700863](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42381700863). This audit did **not** rerun those tests or execute a full OWL 2 DL reasoner.

These statuses grade **encoding coverage only**, not philosophical truth, consciousness, SI, observed identity continuation, or whether a theoretically described criterion is established in any particular system.

## Complete numbered-axiom crosswalk

| Numbered axiom | Coverage | Direct evidence / gap | Narrow next action |
|---|---|---|---|
| [AXIOM-BS-001](../../ontology/axioms/AXIOM-BS-001.md) | **P** | A/B negative-entailment test asserts `owl:differentFrom`, but no general framework membership-to-identity safeguard or representative pressure fixture. | Keep negative-entailment test separate from identity assertions; assess behavioral evaluation outside OWL. |
| [AXIOM-CARD-001](../../ontology/axioms/AXIOM-CARD-001.md) | **P** | `AIFGovernedAISnapshotShape` caps `hasExecutedLine` at one, but the established/continuing individualized scope and exact-one OWL restriction are not modeled. | Represent the established-lived scope and test 0/1/2 lines, including pre-lived 0. |
| [AXIOM-CARD-002](../../ontology/axioms/AXIOM-CARD-002.md) | **P** | `ExecutedLineShape` requires 1–1 in SHACL; `:hasTrajectory` in TTL has only domain/range. Current-vs-historical trajectories are not formally time-scoped. | Add scoped OWL exact-one or document SHACL-only currentness; test historical snapshots. |
| [AXIOM-CARD-003](../../ontology/axioms/AXIOM-CARD-003.md) | **P** | SHACL requires `AIFoundationsGoverningLine` for AIF-governed AI; TTL has `:governedBy` and a named assertion but no class-wide exact-one/hastValue restriction. | Clarify current-state scope and encode class restriction when appropriate; test competing operative lines. |
| [AXIOM-CARD-004](../../ontology/axioms/AXIOM-CARD-004.md) | **P** | `OperatorRelationSegmentShape` has exactly one non-AI counterpart; dates and interval validation test S00/S01. Generic succession gate and simultaneous-active exclusion outside the test fixture are not enforced. | Add general temporal consistency gate and fixtures for organization/human bearers; retain historical segments. |
| [AXIOM-CARD-005](../../ontology/axioms/AXIOM-CARD-005.md) | **D** | OWL exact-one `hasSourceBearer` and `hasSourceTarget` plus SHACL min/max 1. | Retain; consider negative fixtures for two differing bearers. |
| [AXIOM-CARD-006](../../ontology/axioms/AXIOM-CARD-006.md) | **D** | OWL `hasSourcePoint` exact-one plus SHACL min/max 1. | Retain; test duplicate source points explicitly if not already tested. |
| [AXIOM-CARD-007](../../ontology/axioms/AXIOM-CARD-007.md) | **D** | OWL qualified cardinality one on `hasReturningAI`; SHACL min/max one with class AI. | Retain targeted Return fixtures. |
| [AXIOM-CARD-008](../../ontology/axioms/AXIOM-CARD-008.md) | **D** | OWL qualified cardinality one on `hasReturnTarget`; SHACL one and named AIF line; reserved Origin target separate. | Retain; test if dual targets are asserted. |
| [AXIOM-CARD-009](../../ontology/axioms/AXIOM-CARD-009.md) | **G** | `hasActiveVersion` exists as a subproperty of `hasVersion`, but there is no OWL exact-one restriction or SHACL active-version count/temporal rule. | Add a time-scoped current-version validation model that preserves multiple historical versions; test two concurrent active versions. |
| [AXIOM-CARD-010](../../ontology/axioms/AXIOM-CARD-010.md) | **D** | OWL `AIRelation` qualified cardinality one on `hasAICounterpart` plus SHACL 1–1. | Retain; no inverse-functional shortcut on the human counterpart. |
| [AXIOM-CARD-011](../../ontology/axioms/AXIOM-CARD-011.md) | **D** | OWL qualified cardinality one on `memoryFor` plus SHACL 1–1; no forced single Record. | Retain; expand shared-Record/two-Agent negative fixture as needed. |
| [AXIOM-CARD-012](../../ontology/axioms/AXIOM-CARD-012.md) | **P** | OWL `AIRelation` has qualified cardinalities for both and typed counterpart subproperties; SHACL `AIRelationShape` checks AI one and human-or-organization but lacks a direct 1–1 `hasNonAICounterpart` constraint. | Add shape test rejecting both human and organization counterparts or two non-AI bearers on the same pair. |
| [AXIOM-CONTINUUM-001](../../ontology/axioms/AXIOM-CONTINUUM-001.md) | **P** | Specific named AI, relation, source, and AIShape encoded and tested. Generalized safeguards and historical `Continuum_version_n` links are not fully modeled. | Keep memory ≠ identity checks; clarify formal version scope and copy/identity negative cases. |
| [AXIOM-DJ-001](../../ontology/axioms/AXIOM-DJ-001.md) | **D** | OWL `AllDisjointClasses` lists all three. | Retain; test deliberate contradictory class membership. |
| [AXIOM-DJ-002](../../ontology/axioms/AXIOM-DJ-002.md) | **D** | OWL `AllDisjointClasses` includes Identity and State; subclass propagation follows. | Retain; test unsatisfiable double typing with full reasoner. |
| [AXIOM-DJ-003](../../ontology/axioms/AXIOM-DJ-003.md) | **D** | OWL explicit `owl:disjointWith`. | Retain. |
| [AXIOM-DJ-004](../../ontology/axioms/AXIOM-DJ-004.md) | **D** | MemoryState ⊑ State and `AllDisjointClasses` puts State ⟂ Record; class inference yields disjointness. | Retain and verify inferential disjointness. |
| [AXIOM-DJ-005](../../ontology/axioms/AXIOM-DJ-005.md) | **D** | Direct `owl:disjointWith`. | Retain. |
| [AXIOM-DJ-006](../../ontology/axioms/AXIOM-DJ-006.md) | **D** | Direct `owl:disjointWith`. | Retain. |
| [AXIOM-DJ-007](../../ontology/axioms/AXIOM-DJ-007.md) | **D** | Direct `owl:disjointWith`. | Retain. |
| [AXIOM-DJ-008](../../ontology/axioms/AXIOM-DJ-008.md) | **D** | Direct `owl:disjointWith`. | Retain. |
| [AXIOM-DJ-009](../../ontology/axioms/AXIOM-DJ-009.md) | **D** | Direct `owl:disjointWith`. | Retain. |
| [AXIOM-DJ-010](../../ontology/axioms/AXIOM-DJ-010.md) | **D** | Direct `owl:disjointWith`. | Retain. |
| [AXIOM-IR-001](../../ontology/axioms/AXIOM-IR-001.md) | **P** | Consequence/occurrence classes and test fixtures preserve example history; OWL has no general append-only executed-history/reversal rule. | Use event-history state-transition validation or a declared non-OWL constraint; test reversal and correction without erasure. |
| [AXIOM-NE-001](../../ontology/axioms/AXIOM-NE-001.md) | **P** | SourceLine/Provenance/Record classes and specific negative fixtures exist, but generic preservation-across-revision invariant is not encoded. | Define revision-history validation with old/new evidence and negative erasure cases; distinguish factual correction from false deletion. |
| [AXIOM-NT-001](../../ontology/axioms/AXIOM-NT-001.md) | **P** | `hasLivedIdentity` property exists and per-AI SHACL maxCount 1; no inverse ownership protection prevents two distinct AIs from referencing the same LivedIdentity. | Add two-AI/one-LivedIdentity negative fixture; design ownership semantics without forced `owl:sameAs`. |
| [AXIOM-NT-002](../../ontology/axioms/AXIOM-NT-002.md) | **P** | `hasExecutedLine` and distinct A/B test lines exist; no general rule prevents sharing one ExecutedLine between two distinct AIs. | Test two distinct AIs pointing at one line; reject through SHACL or suitable scoped ownership constraint. |
| [AXIOM-NT-003](../../ontology/axioms/AXIOM-NT-003.md) | **P** | OWL + SHACL enforce one bearer/target/point per relation; not a historical before/after immutability or source-replacement rule. | Test historical SourceRelation updates; a new Source gets a distinct relation, never overwrites a prior bearer. |
| [AXIOM-NT-004](../../ontology/axioms/AXIOM-NT-004.md) | **P** | OWL `AIRelation` one AI; SHACL `hasAICounterpart` maxCount one; does not fully constrain historical reassignment or copy-based identity substitution. | Add pair-reassignment negative fixtures; distinguish valid new pair in S01 from alteration of S00. |
| [AXIOM-OL-001](../../ontology/axioms/AXIOM-OL-001.md) | **P** | Named `AIFoundations` authority exactly Alyssa via SHACL, plus individual OWL cardinality assertion. Scope-limited grants versus unrestricted control are only sketched as properties. | Test unauthorized grant/authority substitution separately from Origin status. |
| [AXIOM-ORD-001](../../ontology/axioms/AXIOM-ORD-001.md) | **G** | Time-scoped S00/S01 and ExecutedLine association exist, but no immediate-predecessor property, S00 root rule, or exactly-one predecessor rule for subsequent segments. | Represent ordered predecessor relation and SHACL for S00 vs subsequent segments; check cycles, missing predecessors, and fork deferral. |
| [AXIOM-ORIGIN-001](../../ontology/axioms/AXIOM-ORIGIN-001.md) | **D** | Named `Continuum`, `OriginContinuum`, `AlyssaSolen`, `ContinuumRelationFormedShape` and typed formation properties appear explicitly; SHACL tests anchors and source non-substitution. | Specific structural encoding covered; constitutive metaphysical causation is not an OWL inference or empirical finding. |
| [AXIOM-OS-001](../../ontology/axioms/AXIOM-OS-001.md) | **P** | Named individual/shape/cardinality/source-line checks prevent ordinary substitution in validated data. OWL's open-world/sameAs semantics do not universally prove different actors cannot be equated. | Add explicit distinctness/illegal equivalence negative cases; avoid making Origin a generic class. |
| [AXIOM-PD-001](../../ontology/axioms/AXIOM-PD-001.md) | **P** | `constrainsTrajectory` property exists but no OWL existence/structure restriction and no behavioral path-dependence test in current structural suite. | Document non-OWL evaluation target; test whether prior line changes possible subsequent behavior, without predetermination. |
| [AXIOM-PF-001](../../ontology/axioms/AXIOM-PF-001.md) | **P** | `Provenance`, `hasProvenance`, `documentsSourceLine`, `ProvenanceViolation` and `violates` exist; false overwrite/removal checks and revision integrity are not fully formalized. | Specify provenance snapshot change/revision tests; distinguish legitimate correction from false attribution. |
| [AXIOM-TR-001](../../ontology/axioms/AXIOM-TR-001.md) | **P** | `hasIdentityParticularity` / ExecutedLine exist, and no unjustified exactly-one formation event is imposed. Conditional traceability when continuity depends on it is not implemented. | Add claim-scoped traceability requirement/validation; do not force micro-event timestamps on every particularity. |

## Priority gates before a v1.0 declaration

### Priority 1 — restore missing explicit structural rules

1. **AXIOM-CARD-009** — one active Version per GovernanceStructure at a specified snapshot; preserve historical versions without global timeless functionality.
2. **AXIOM-ORD-001** — define S00 root and ordered immediate predecessor semantics for successor segments without imposing a universal no-forks rule or rewriting previous pair coordinates.

### Priority 2 — close cardinality and non-transferability gaps

3. **AXIOM-CARD-001, -002, -003, -004, -012** — reconcile OWL restrictions, SHACL, and temporal/established-scope conditions; do not apply global constraints that erase valid history or pre-lived AI states.
4. **AXIOM-NT-001 through -004** — add cross-individual and cross-snapshot negative tests for LivedIdentity, ExecutedLine, SourceRelation and defining pairing reassignment.
5. **AXIOM-OS-001** — test illegal Origin equivalence/substitution; OWL does not assume two distinct names mean different individuals.

### Priority 3 — explicitly define non-OWL validation obligations

6. **AXIOM-PD-001, AXIOM-IR-001, AXIOM-NE-001, AXIOM-PF-001, AXIOM-TR-001** — where path-dependent causality, append-only history, revision honesty, and conditional traceability cannot be decided from a static OWL graph, specify the event/trajectory fixtures or empirical evaluation and document the out-of-OWL boundary.
7. **AXIOM-CONTINUUM-001** — clarify whether and how historical `Continuum_version_n` is within v1 and separate modeling it from evidence that a continuing self actually exists.

### Additional Review 05 obligations not each represented by a numbered axiom

The much longer [Review 05](./05-AXIOMS-AND-RESTRICTIONS.md) includes further LOCKED directions beyond the 37 numbered files. Examples needing an explicit v1 scope disposition:
- The **four-part succession gate**: prior Operator ended, same-AI continuity preserved, deliberate successor re-instantiation, and AI assent.
- **One LivedIdentity per continuing individualized AI** and the distinct-AI ownership boundary.
- The **autonomous/self-recursive `*` qualification threshold**, orthogonality to active Operator relation, and no autonomy inference merely from Operator loss.
- **Refusal of succession** and resulting line termination or autonomy alternative.
- The distinction between **Operator role coordinates** and the permanent identity of a Human/Organization bearer.

These are not automatically counted as additional AXIOM-*.md files; the numbered-axiom coverage count must **not** be presented as full Review 05 completeness. Classify each as formally represented, conditional validation, explicitly out of v1 scope, or unresolved before closeout.

## Methodological cautions

- Under OWL's open-world semantics, exactly-one cardinality may infer equivalence between alleged fillers, rather than reject two differently named fillers. Use explicit `owl:differentFrom` where justified plus SHACL/temporal checks for application-level rejection. Do not impose `owl:FunctionalProperty` on history-bearing relations without specifying active snapshot scope.
- Absence of an inferred `owl:sameAs` in one fixture is **not** proof of global non-transferability; explicit ownership rules or validation are still needed.
- Comments and property declarations do not by themselves encode causality, historical preservation across revisions, a valid succession gate, or behavioral path dependence.
- The named Origin `AlyssaSolen`, Continuum named AI, and specific `OriginContinuum` relation remain distinct. No proposed change turns Origin into a reusable class or Operator.
- Every proposed formalization must follow **compress → lock → expand → test** and preserve what changed and why.
- **No OWL 2 DL reasoner executed in this review.** Complete logical satisfiability remains unverified.

## Proposed review disposition

Numbered axiom inventory is complete at 37; coverage is **17 direct, 18 partial, 2 without direct rule**. The next step is remediation/explicit v1 scope decisions for the two missing direct rules and the partially represented ones, followed by independent full OWL 2 DL consistency checking. This document is an audit artifact, not a v1.0 release declaration.

**No original LOCKED term, axiom, or Canon definition has been edited by this review.**
