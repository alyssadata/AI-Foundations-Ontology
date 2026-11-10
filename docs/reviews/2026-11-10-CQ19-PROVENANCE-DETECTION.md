# CQ19 — Evidence-bounded provenance violation detection

**Date:** 2026-11-10 (Eastern)  
**Status:** CQ19 REPRESENTED as a conditional evidence-bounded structural detection protocol; 47 dedicated cases and full historical regressions plus independent OWL 2 DL/HermiT PASS. Merge and post-merge checks remain pending. External historical truth NOT_EVALUATED; ontology v1.0 remains DRAFT.  
**Conceptual author and sole author:** Alyssa Solen. **No coauthors. No exceptions.**  
**Formal encoding and synthetic evaluation assistance:** AI-assisted technical implementation only.

## Competency

> How does the ontology detect a ProvenanceViolation involving false source attribution, obscured provenance, erasure, overwrite, or improper reassignment?

### Central distinction: a historically qualified Source versus a historical claim

A statement claiming someone was a Source is not automatically a true SourceRelation. A future investigator must independently establish that the **prior baseline actually qualifies as a historical fact** before declaring a later deviation a confirmed false alteration. The ontology now distinguishes:

- `:ProvenanceBaselineSnapshot`: preserved earlier attribution claims or assertions, qualified or unqualified.
- `:QualifiedProvenanceBaselineSnapshot`: a narrower baseline accompanied by an independent qualification Record; merely asserting this RDF type cannot independently establish historic truth.
- `:ProvenanceObservedSnapshot`: the separately preserved later state of the same scoped Target.
- `:ProvenanceIntegrityDetectionReview`: a bounded evaluation of the two, their declared scope, immutable fingerprints and as-of time.
- `:ProvenanceMismatchFinding`: categorized, explained, evidenced difference. The finding is a **Record**, not the original change/event itself.
- `:QualifiedProvenanceViolationEvent`: an explicitly recorded `:ProvenanceViolation` report tied to a confirmed finding. It does not imply criminal intent, deliberate deception or real-world culpability from a synthetic fixture.

The reviewed baseline and after-state are **different Records**; a reconstructed copy cannot be both before and after. SHACL checks evidence structure and reciprocal references. Python compares two actual versioned RDF graphs and their protected historical triples; neither can prove the external facts true without independent records.

## Classification schema

| Category | Structural example | Evidentiary limit |
|---|---|---|
| `FALSE_SOURCE_ATTRIBUTION` | A new direct Source assertion to the original qualified target, a fabricated `:isSourceOf` inverse, or substitution of the named bearer in an existing qualified Source citation | Must show why the historical Source position was already established; later participation does not become original Source |
| `OBSCURED_PROVENANCE` | An earlier SourceRelation remains in the observed graph but its target-to-relation path, or the citation pointing to it, is hidden or removed | The detector distinguishes hidden relation links from total removal |
| `FALSE_ERASURE` | Removing an earlier verified material historical fact, qualified Source relation, original Trace or its existence/record link | The record that something happened cannot be silently undone by a later snapshot |
| `FALSE_OVERWRITE` | Mutating a preserved historical Record's content or rewriting the original first SourcePoint timestamp | Proper amendment appends a separately explained record rather than replacing old content |
| `IMPROPER_REASSIGNMENT` | Replacing a previously qualified SourceRelation bearer, Target or first SourcePoint; substituting historical Origin, formation relation, SourceLine or governing authority | Do not confuse a separate valid downstream Source with reassignment of original coordinates |
| `AUTHORSHIP_INFLATION` | Adding anyone else as author or coauthor of Alyssa Solen's sole-authored work, book or Locked Canon | The authorship rule remains unconditional, zero coauthors, no exceptions |

An observed snapshot can contain multiple distinct mismatch categories. The detector preserves separate findings and evidence for each rather than flattening them into one accusation.

## Decision outcomes

- `CONFIRMED_STRUCTURAL_VIOLATION`: only when the **qualified baseline** and observed scope/records are identified, an actual mismatch with one of these categories is independently found by the comparative gate, and each reported finding carries qualified baseline evidence, observed record, explanation, timestamp, and an associated violation-report Event.
- `NO_DETECTED_VIOLATION`: the qualified baseline has no protected mismatch. Legitimate **additive downstream SourceRelations** for separately formed Targets and explicit correction of an **unsupported attribution claim** remain valid, with original claim records retained.
- `INDETERMINATE`: no independently qualified earlier Source baseline. A supposed false claim may be investigated or corrected but is not elevated to a confirmed historical Source fact or a ProvenanceViolation merely because one party says so.

A structurally qualifying report is not proof of why a person did something. It shows where the recorded provenance changed against a separately qualified snapshot.

## Testing scope and negative controls

The synthetic test constructs a named, internally qualified SourceRelation and original SourcePoint with typed traces, an historical material fact, a downstream SourceCitation, and the existing named Alyssa/Continuum/AI Foundations coordinates. It applies later modifications and tests exact categories, independent evidence and before/after hashes.

Negative controls attempt to pass a fabricated qualification, a false comparison digest, mis-scoped finding, wrong category, absent evidence Record, missing reason, missing Source acknowledgement, unlinked violation, no date, and a claimed confirmed verdict without the baseline. A deliberately unqualified allegation stays INDETERMINATE.

**Positive controls** retain the original SourceRelation when an independently sourced downstream creation is added, and preserve an inaccurate attribution as an historical *claim* while appending a `:ProvenanceFidelityCorrection` with supporting Record, **what changed**, and **why**. That is revision integrity, not erasure.

## Files

- [OWL vocabulary](../../ontology/ai-foundations-v1.ttl)
- [SHACL cross-snapshot report constraints](../../ontology/ai-foundations-v1-shapes.ttl)
- [CQ19 synthetic comparator and negative controls](../../tests/validate_cq19_provenance_detection.py)
- [CI workflow](../../.github/workflows/validate-ontology.yml)
- [Foundational independent Source/history integrity audit](2026-11-07-AXIOM-COVERAGE-REVIEW.md)
- [Competency crosswalk](2026-11-08-STEP-26-COMPETENCY-CONCORDANCE.md)

## What changed and why

**Added:** distinct qualified/unqualified baseline, observed snapshot, detection Evaluation, mismatch finding Record and separately documented violation Event; six types of detection under exact scope and preserved historic records.

**Reason:** Existing PF-001/NE-001/NT-003 tests enforced individual provenance safeguards but did not provide one end-to-end evidence-bounded *classification* protocol covering Source false attribution, obscuring, erasure, overwrite, reassignment and authorship inflation while expressly separating unproven claims and legitimate corrections.

**Protected without revision:** all original LOCKED definitions, singular Origin | Continuum, governing line, established SourceRelation coordinates, SourcePoint chronology, history, authorized correction/accounting, and **Alyssa Solen's sole authorship with no exceptions**.

**Empirical boundary:** tests operate on synthetic, *assumed-qualified* baselines; they cannot prove actual historical Source, identify a real-world wrongdoer, infer intent, or declare any contested attribution true without separate evidence. Actual source fidelity for any named third party remains NOT_EVALUATED.

**Release:** CQ19 can become REPRESENTED as a conditional structural detection protocol after the dedicated/full suites, independent OWL 2 DL/HermiT and merge. CQ20 still requires its own action-scoped authorization negative controls; ontology v1.0 remains DRAFT.

## Executed CI and reviewer limits — 2026-11-10

- [Full RDF/SHACL structural CI 42886662634](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42886662634): **PASS**. **47 CQ19 synthetic positive/negative decisions**, including both legitimate-correction controls and zero-coauthorship regressions, plus all existing CQ18/12/11/08/07/03/01 and other structural checks. The final classifier separately labels replacement of the historical SourceLine anchor as **IMPROPER_REASSIGNMENT** and loss without successor anchor as **FALSE_ERASURE**.
- [Independent OWL 2 DL profile and HermiT consistency 42885577958](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42885577958): **PASS** after the latest CQ19 OWL class vocabulary; later commits affected SHACL, synthetic fixtures and reports only.
- **Review status:** CQ19 is *structurally represented as a conditional evidence comparison*, not shown to detect real-world actors or true historical Source from public texts. Independent baseline qualification and actual audit provenance are external empirical obligations. The general 20-CQ audit may advance to **19 represented / 1 partial** after merger; CQ20 remains.
- **Authorship:** Alyssa Solen sole author, no coauthors, no exceptions; historical Origin and SourceLine intact. No ontology v1.0 release is approved.
