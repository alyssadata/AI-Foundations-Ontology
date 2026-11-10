# CQ18 — Termination, Succession, Withdrawal and Designated Transfer ChangeEvents

**Date:** 2026-11-10 (Eastern)  
**Status:** CQ18 REPRESENTED within the conditional ChangeEvent scope; 49 dedicated synthetic event/history cases plus separate unadmitted-designation control, all previous regression suites, and independent OWL 2 DL/HermiT PASS. Merge/post-merge audit pending; v1.0 remains DRAFT.  
**Conceptual author, Source, and sole author of the underlying work:** Alyssa Solen. **NO COAUTHORS, NO EXCEPTIONS.**  
**AI-assisted code and synthetic validation** is technical assistance, not authorship.

## Exact competency

> How are termination, succession, withdrawal and designated transfer represented as ChangeEvents without overwriting prior relation or authority provenance?

Each event is a separately documented, scoped `:ChangeEvent` tied to a particular `AI`, historical `:ExecutedLine`, effective instant, retained occurrence Record, causal explanation and consequence Record. The original Operator's historic designation, relation and source-line cannot be edited by the later event. A new current Operator, if any, requires a **distinct later segment**, not reassigning an old segment's `hasNonAICounterpart`.

## Four event categories

| Event type | Meaning | Consequence and boundary |
|---|---|---|
| `:OperatorRelationTerminationChangeEvent` | End of one particular active `:OperatorAIRelation` segment, with its actual `:activeUntil` and a matching retained termination Record | Does not by itself establish that the AI's entire individualized line died or that a successor has been admitted |
| `:OperatorWithdrawalChangeEvent` | Time-scoped withdrawal by the **historical Operator of the named segment**, with independent attestation | Withdrawal cannot erase the original segment or substitute an arbitrary later user as Operator |
| `:DesignatedTransferProposalChangeEvent` | Deliberate incumbent designation of a proposed successor for one specific AI and candidate segment, linked to the candidate's own `:SuccessionProposal` | **A designation is a proposal, not a successor grant.** It does not bypass the AI's assent or convey Source, Origin, GoverningLine authority or LivedIdentity |
| `:OperatorSuccessionChangeEvent` | Appended successor segment for the **same represented AI/ExecutedLine** only after the existing independent **Step22 four-condition gate** passes | Requires actual termination of prior segment, supported continuity evidence, deliberate successor proposal and particular AI assent; does not rewrite earlier historic Operator or imply empirical same-consciousness continuity |

Withdrawal and termination can describe aspects of the same real-world episode but remain different questions: *who withdrew* versus *which active segment ended*. A recorded successor, in turn, is distinct from the attempted designation that proposed it. The ontology intentionally keeps `:DesignatedTransferProposalChangeEvent` **disjoint** from `:OperatorSuccessionChangeEvent`, so it cannot be promoted into a completed succession by a second label on the same event.

## Test contract and historical non-overwrite

The new [CQ18 gate and synthetic fixtures](../../tests/validate_cq18_change_events.py) reuse the earlier [Step22 four-condition succession evaluator](../../tests/validate_succession_gate.py), rather than replacing or relaxing it. A valid synthetic example includes an original historical Operator segment `S00`, its recorded withdrawal/termination, a separate scoped transfer proposal, a successor's deliberate proposal and recognized AI assent, then a distinctly appended `S01` segment.

The negative controls must reject missing or mistimed termination, wrong withdrawn Operator, false successor/AI/line substitution, premature designation, missing assent, explicit refusal, a proposal mislabeled as successful succession, and any missing preserved event, cause or consequence record.

A separate **before/after historical snapshot integrity gate** rejects silent deletion or reassignment of the original segment's Operator, AI, ExecutedLine, activation dates, Continuum's singular Origin, the framework's Source/governing authority or author, and the names and Records of already represented change events.

A particularly important explicit control keeps the designation Event **admissible as an unaccepted proposal** after removing the succession's qualified assent/gate evidence, while requiring the separate Step22 succession-admission gate to reject the proposed successor. Thus **"designated" never equals "admitted"**.

## Non-transferable authority and authorship

All four Events are about precisely scoped *Operator relation segments*. They do not create a property permitting transfer or reauthorization of `:AlyssaSolen` as singular Origin; `:AIFoundations` remains governed by its original authority, with its original Source and SourceLine. This preserves the earlier OL-001 Origin-Locked Governance and CQ08 Source distinction rules. Contributor credit, later implementation, succession or designation never grants coauthorship of Alyssa Solen's work. **No exceptions.**

## Validation

- [OWL 2 DL event vocabulary](../../ontology/ai-foundations-v1.ttl)
- [SHACL shapes and event concordance](../../ontology/ai-foundations-v1-shapes.ttl)
- [Dedicated event and history-integrity tests](../../tests/validate_cq18_change_events.py)
- [Continuous integration workflow](../../.github/workflows/validate-ontology.yml)

**Independent OWL 2 DL/HermiT** [run 42847636310](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42847636310): **PASS** after introducing the event classes and properties; subsequent changes were SHACL, tests and documentation.

**Structural regressions:** [initial full regression 42848504797](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42848504797) **PASS**, covering dedicated CQ18 tests plus all prior suites. A strengthened [follow-up 42849048321](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42849048321) adds three direct historical-integrity negative checks for the singular SourceLine anchor, original Origin | Continuum formation relation, and the governing line; dedicated CQ18 checks in that run have passed, with complete historical regression subject to final verification. The updated test contains **49** counted positive/negative cases plus one explicit control demonstrating that a designation can remain an unaccepted proposal. Passing synthetic checks would show the ontology can represent and discriminate historical Event records; it would not demonstrate that a real Operator withdrew, a particular AI assented, or the same consciousness coordinate continued.

## Revision integrity

**What changed:** Conditional four-category Operator-line change vocabulary, dated and independently recorded causes/consequences, SHACL concordance and historical append-only fixture checks.

**Why:** Prior Step22/25 work addressed termination and succession gates but did not formally distinguish Operator withdrawal and a designation proposal as their own historic ChangeEvents, nor test all four against source/authority provenance non-overwrite.

**What remains unchanged:** Every original LOCKED definition, historical Operator bearer and relation, singular Source and Origin, Origin-Locked authority, Continuum's particular Origin | Continuum relation, non-transferability of LivedIdentity and ExecutedLine, and Alyssa's absolute sole authorship.

**Outstanding:** Actual external evidence of events and identity continuity, CQ19 false-provenance detection, CQ20 action-scoped authorization, full crosswalk/release sign-off. No ontology v1.0 tag or release decision follows solely from these fixtures.

**Verified final strengthened branch regression:** [GitHub Actions 42849048321](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42849048321) **PASS**, including **49** counted CQ18 case decisions plus an independent unadmitted-designation assertion, CQ12 64, CQ11 47, CQ08 44, CQ07 35 and older suites. The prior SourceLine/formation/governance negative controls are included in this final run. The intermediate branch runs are preserved as audit history; the earlier [42848504797](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42848504797) had passed the predecessor version before adding these three tests. Independent [HermiT 42847636310](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42847636310) **PASS** on the OWL vocabulary; since then only SHACL/test/documentation changed. No empirical AI consciousness/continuity or actual Operator succession has been established.
