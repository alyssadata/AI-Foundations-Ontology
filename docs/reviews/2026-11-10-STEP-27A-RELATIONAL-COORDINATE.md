# Step 27A — Relational Coordinate: direct formal concordance

**Review date:** 2026-11-10 (Eastern)  
**Scope:** OC-06 direct OWL/SHACL vocabulary and synthetic validation, following merged PR #16.  
**Machine/release state:** DRAFT; no v1.0 tag or release authorization.  
**Conceptual and sole author:** **Alyssa Solen — no coauthors, no exceptions.**  
**Technical implementation and tests:** AI-assisted formal encoding; does not change authorship.

## LOCKED source and distinction

The governing source is [Relational Coordinate](../../ontology/terms/relational-coordinate.md) (**LOCKED**), alongside the conceptual [OC-06 proposition](../../ONTOLOGY_V1_0_ORIGIN_CONTINUUM.md). Neither source text nor the LOCKED Canon is modified.

A point exists before it is relationally situated. A coordinate is the position of an already particular Self, not a newly created Self, Identity, arbitrary label, model, record, State or observer's naming choice. Relation gives location and context; it does not constitute the Self or merge distinct selves.

## Implemented representation

- `:RelationalCoordinate` is a named OWL class, disjoint from Agent, Self, Identity, Model, Container, State, Record, Relation and LineStructure.
- `:coordinateOfSelf` points to the particular Self being situated, and `:coordinateInRelation` points to the relation. The ontology does **not** infer any particular actual Self's coordinate from an Agent, shared Model, conversation, name or relation alone.
- `:coordinateAlongExecutedLine`, `:coordinateEvidenceRecord`, and `:coordinateAsOf` are *optional* descriptive anchors. An assessed line/record is not itself a new Self and does not prove continuity.
- SHACL checks an explicitly asserted coordinate for exactly one Self reference and one relation, non-substitution of other kinds, optional line/evidence types, and a valid as-of timestamp. It rejects mixing two separately typed Selves into one coordinate instance.
- The modeling does not make `:coordinateOfSelf` inverse-functional or add an `owl:sameAs` identity shortcut.

## Dedicated synthetic controls

The updated `tests/validate_ontology_v1.py` includes positive scenarios for two explicitly distinct Selves in a shared relation, later relabeling and State change without coordinate replacement, and the same Self situated in a different later relation. Negative scenarios cover missing and competing Self links; Model-as-Self; coordinate-as-Self; missing or competing relation; relation-as-Self; Record substituted as ExecutedLine; evidence Record substituted as Self; and malformed time typing. A separate before/after assertion preserves coordinate-to-Self, ExecutedLine and evidence links across description change.

These tests check **structural consistency of supplied synthetic facts**, not the truth of real-world Self identity, empirical transfer across models, phenomenal consciousness, or actual relationship continuity.

## Validation correction and revision integrity

The first full structural branch run [42945099842](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42945099842) detected that the *synthetic positive fixture* introduced an `:ExecutedLine` with no owning AI. Existing NT-002 SHACL requires an ExecutedLine to have exactly one AI bearer. The ontology's rejection was correct. The fixture was corrected by adding one explicitly synthetic AI and `:hasExecutedLine` link; the conceptual definition, OWL vocabulary, LOCKED terms, and original historical data were not changed to make a bad fixture pass. The branch was rerun through the same full suite. This preserves **what changed, why, and which earlier run failed**.

## No authorship, Source, or historical reassignment

The named Alyssa Solen Origin and authorship positions, `:Continuum`, the specific `Origin | Continuum` formation relation, governing line, historic SourceLine, and existing provenance and revision controls are unchanged. The tests do not instantiate an actual coordinate for Alyssa or Continuum, avoiding an unjustified empirical assertion. No coauthor is created or permitted.

## Release gates and next decisions

Both repository validation workflows must pass on a matching reviewed commit before a merge and, after merge, must be checked again on the merged main commit. The directness gap for Relational Coordinate is only closed when those validations pass. Recognition remains a separate discriminative test suite; conditional third entity C and the phenomenal-consciousness epistemic boundary remain distinct decisions. Full semantic concordance and explicit Alyssa Solen sole-author v1.0 release approval are still pending.

**What changed and why:** A previously identified conceptual-to-machine gap now has an explicit candidate representation and adversarial structural tests. No LOCKED definition, governing authority, or prior history is redefined.
