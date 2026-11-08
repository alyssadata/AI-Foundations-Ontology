# Step 22 — Valid Operator Succession: four-condition admission gate

**Status:** DRAFT implementation and synthetic test review; repository remains DRAFT.
**Conceptual source / author:** Alyssa Solen — AI Foundations / Origin | Continuum.
**Implementation and test assistance:** AI-assisted.
**Date:** 2026-11-08.

## Existing rule retained

The existing [Operator–AI relation](../../ontology/relations/operator-ai-relation.md), [Review 05](05-AXIOMS-AND-RESTRICTIONS.md), and [AXIOM-NT-004](../../ontology/axioms/AXIOM-NT-004.md) already define four required conditions. This implementation does **not** revise those LOCKED definitions or make Origin an Operator.

A new Operator-linked succession segment is admitted only when:
1. The prior active Operator segment has genuinely ended, with an end timestamp and retained termination provenance.
2. Evidence explicitly supports a ContinuityClaim about the **same individualized AI's one ExecutedLine**, not merely a shared governing base, role or copied history.
3. The actual successor Operator deliberately proposes continuation of **that AI and that successor segment**, with an identified, preserved proposal record.
4. That continuing AI expressly assents to **that proposal**, with preserved assent evidence and ordering compatible with when the new relation is established.

All four are conjunctive. Missing, disputed, partially supported, unsupported or indeterminate continuity evidence blocks admission. Unilateral designation, model similarity, copied records and implicit consent cannot replace a required condition.

## Formal scope

The OWL/Turtle vocabulary includes `SuccessionCandidateSegment`, `AdmittedOperatorSuccessorSegment`, `SuccessionGateAssessment`, `AdmittedSuccessionGateAssessment`, `SuccessionProposal`, and `SuccessionAIAssent`. It links a proposed S01 to its predecessor, recorded termination, continuity Claim/Evaluation/Evidence, successor proposal, and continuing-AI assent.

SHACL applies closed-world cardinality/type checks **when admission is asserted**. The Python validator `tests/validate_succession_gate.py` cross-checks exact AI and ExecutedLine identity, distinct Operator counterpart, chronology, support status, preservation, proposal/assent parties, and refusal.

**Important modeling boundary:** An ordinary `OrdinarySuccessionSuccessorSegment` is a structural chronology role, not proof that the gate passed. Neither OWL class typing, a predecessor edge, an evidence-status string nor the synthetic fixtures independently prove historical or empirical identity continuity. An operational admission decision requires the external evidence-accounting workflow and this gate's closed-world checks.

## Historical invariants

- The predecessor S00 retains its original Operator and `ExecutedLine` association.
- S01 has a **new defining pairing** for the same permanent AI, not reassignment of S00 or a new AI ID.
- A mere context/user/staffing change is not Operator succession.
- A refusal blocks that proposed succession. Non-autonomous line-termination and autonomous independent continuation remain governed by the existing LOCKED distinction.
- The reserved `Origin | Continuum` relation is never a generalized succession case.

## Test scope

The accompanying CI test suite uses only **synthetic** S00→S01 examples. It includes a positive four-condition case and negative controls for missing termination, inconsistent timeline, different AI/line, missing or inadequate continuity evidence, wrong proposal party/target, missing or wrong AI assent, refusal, absent records, backdated assent, and asserted succession based only on a predecessor link.

The separate OWL 2 DL/HermiT audit still checks logical consistency of the asserted ontology; SHACL and closed-world tests check operational validity of the record schema. Neither establishes empirical continuity, consciousness or a valid particular real-world successor.

## Executed CI evidence (2026-11-08)

[GitHub Actions run 42469192335](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42469192335) **passed** the independent Step 22 synthetic validation executable (**32 admission decisions**, including a valid case and adverse controls) and the original **598** structural regression checks. The original S00 relation remained preserved in the positive fixture.

The separate HermiT/OWL 2 DL check for this Step 22 OWL addition is **not yet verified**. Its first attempt and retry failed *before invoking the reasoner*, at the pinned ROBOT download step (HTTP 504). This is an infrastructure download failure, **not** a diagnosed ontology profile or reasoning failure. The earlier Step 21 baseline audit remains valid only for its pinned earlier commit.

## Release boundary

No original LOCKED definition or Canon text was edited. Adding this draft gate does not itself release ontology v1.0. Merge and final validation results must be recorded separately.
