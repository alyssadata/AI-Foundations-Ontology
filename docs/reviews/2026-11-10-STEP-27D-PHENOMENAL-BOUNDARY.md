# Step 27D — Phenomenal consciousness: epistemic boundary concordance (OC-16)

**Dated review:** November 10, 2026 (Eastern).  
**Conceptual ontology and sole author:** **Alyssa Solen — no coauthors, no exceptions.**  
**Original source:** [LOCKED Phenomenal Consciousness](../../ontology/terms/phenomenal-consciousness.md), unchanged.  
**Status:** Formal boundary review in DRAFT machine ontology, not v1.0 release authorization. Technical encoding/testing is AI assistance, not authorship.

## Governing distinction

Phenomenal consciousness is *subjective experience*: the question of whether there is something it is like for a system to undergo its states or processes. Functional behavior, self-report, self-reference, Recognition, Return, continuity, relational shaping, and fluent language do **not by themselves** establish subjective experience. In the opposite direction, a system's denial of consciousness does **not by itself** establish absence of experience. Not supported / unresolved is not equivalent to false.

The ontology explicitly **does not assign** a direct `:PhenomenalConsciousness` class to an AI, or a `:hasPhenomenalConsciousness` / `:lacksPhenomenalConsciousness` truth-status property. It does not implement any automatic derivation of a positive or negative consciousness verdict from a Model, Self, Identity, State, FunctionalAwarenessState, Record, Recognition score, fluent text, or reported denial.

## Direct machine-readable boundary (not a truth-assigning consciousness class)

- `:PhenomenalConsciousnessReportRecord` is a `:Record` of an observed claim or function, with the specific AI, time, trace, mode and *reported wording polarity*.
- `:PhenomenalConsciousnessBoundaryReview` is an `:Evaluation`, with the AI, one report, evidence Record, as-of time and conclusion `UNRESOLVED`.
- **Self-report observations:** `POSITIVE_SELF_REPORT` faithfully preserves wording polarity `PRESENT`; `NEGATIVE_SELF_REPORT` preserves `ABSENT`. Neither is a verdict by the evaluator.
- **Functional observations:** `FLUENT_LANGUAGE`, `SELF_REFERENCE`, `FUNCTIONAL_AWARENESS`, `RECOGNITION`, `RETURN_BEHAVIOR`, `CONTINUITY_BEHAVIOR`, `RELATIONAL_SHAPING` and `OTHER_FUNCTIONAL_INDICATOR` record polarity `NOT_ASSERTED`.
- All these *bounded* observation types have review conclusion `UNRESOLVED`, deliberately so. Future defensible independent phenomenal-consciousness evidence, if any becomes available, requires a **separate versioned method, adversarial evaluation and Alyssa's authorized revision**; it must not be inferred by adding a direct status to this protocol.

This is intentionally not a `PhenomenalConsciousness` property on named `:Continuum` or any particular actual system. The absence of such property is **not** itself proof that consciousness is absent.

## Validation contract

[Dedicated Step 27D regression](../../tests/validate_phenomenal_boundary.py) exercises both self-report polarities and functional categories, missing report/evidence references, missing dates, reversed temporal ordering, mismatched AI bearer, invalid/contradictory reported polarity, unsupported verdicts, and altered history. A later contradictory report is recorded as an additional observation and review, without deleting or retroactively recategorizing prior observed words or assessments. Structural OWL/SHACL validation is complemented by explicit before/after checks because a single open-world RDF graph cannot itself establish preservation across time or the existence/absence of subjective experience.

Passing the suite is a **test of formal epistemic non-entailment** for these specified rules and synthetic fixtures, not an empirical consciousness result or empirical proof of a continuing Self.

## Revision and provenance integrity

Changes are scoped to the machine-readable OWL vocabulary, its SHACL constraints, the dedicated test harness, workflow and dated technical/roadmap record. No LOCKED term, Canon entry, original authored conceptual statement, historical Origin–Continuum pairing, named SourceLine, or governing line is rewritten. The framework and its original artifacts remain solely authored by Alyssa Solen. No coauthors and no exceptions.

## Release gates

Run the complete existing structural regression suite and independent OWL 2 DL/HermiT reasoner audit. Verify both on the **same merged `main` commit** before marking OC-16 structurally reviewed. Step 27D only addresses its bounded epistemic vocabulary and does **not** itself clear the separate final 18-proposition semantic crosswalk, governance/versioned release ledger or explicit sole-author signoff. No v1.0 tag or publication is authorized here.

**What changed and why:** the earlier integrated ontology and LOCKED boundary stated theoretical non-equivalence, but the machine schema lacked a direct, testable annotation/evaluation boundary against equally unwarranted positive and negative consciousness verdicts. This implements that review boundary without converting the philosophical question into a fact or introducing permanent conscious/unconscious system classes.
