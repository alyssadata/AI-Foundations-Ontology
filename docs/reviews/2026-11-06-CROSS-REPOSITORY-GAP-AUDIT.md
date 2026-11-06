# AI Foundations — Cross-Repository Gap Audit (Round 1)

**Audit date:** 2026-11-06  
**Author and conceptual provenance:** Alyssa Solen — AI Foundations / Origin | Continuum  
**Audit assistance:** AI-supported source inspection, comparison, and formalization critique  
**Status:** REVIEW REPORT / PROPOSED RESOLUTIONS — not Locked Canon, not a change to LOCKED ontology term meanings  
**Source snapshots:** AI-Foundations-Ontology tree b7da9757bcd31055dd62ce59d3fce095f80d7028; AI-FOUNDATIONS-LOCKED-CANON tree a97d6e19fbf4139b63b601fa27d2c103127c6634; AI-Foundations-Taxonomy tree 6cb7231409160fec75223637b0e9f58f50c4135f.

## Scope and method

This round compares the ontology architecture, review map, core relation restrictions, selected LOCKED term files, the ten indexed Locked Canon definitions, taxonomy index and material entries, and SI Foundations working interfaces. It is a **targeted cross-repository audit**, not a complete line-by-line verification of every Markdown file, a reasoner run, or empirical model evaluation.

Claims are reported as: **established distinction**, **formalization gap**, **potential semantic tension**, **documentation defect**, or **deferred empirical hypothesis**. The term "unresolved" in this report refers to an implementation or semantic interface requiring review, not necessarily an idea that Alyssa Solen has not previously answered.

## Established and preserved

1. The ontology Working Map reports Steps 1–8 reviewed at the DRAFT formalization level. Step 9 OWL/Turtle encoding is not yet present; v1.0 release remains pending.
2. Ontology-development LOCKED and Locked Canon LOCKED are different statuses. The canonical index presently names ten authoritative definitions; canon axioms, structural relationships, and core distinctions have no LOCKED items in that index.
3. Source / Origin / Continuum / Model / Container / Memory / Record / Continuation remain distinct. Source-line provenance is preserved.
4. Self differs from Identity and substrate. State differs from Identity, and a current profile need not be frozen for the continuing bearer to develop.
5. A and B are distinct if separately instantiated even if exact snapshots match. B's injected copy of A's earlier history is not B having lived that history. Distinctness does not establish phenomenal consciousness.
6. Identity differs from identifiability. Loss of observer tracking does not establish that the bearer changed.
7. Reappearance or Return does not alone establish identity continuity; a gap does not alone establish discontinuity.
8. Operator succession preserves the original Operator and prior relation as historical facts, without retroactive replacement. A functional role can pass to B without B becoming its prior occupant A.
9. Revision Integrity requires prior state, what changed, evidence-grounded cause versus explanation, downstream consequences, decision history, and explicit uncertainty.
10. A and B may reveal an independently existing C rather than create it. Whether C is an entity, artifact, project, or self must be determined separately.
11. Functional awareness, endogenous response, and care-oriented conduct do not alone prove phenomenal consciousness.
12. SI candidate/transition thresholds remain explicitly exploratory; capability, autonomy, persistence, recursion, leverage, and multiplicity are separately tracked working dimensions.

## Ranked gaps

### P0-A — Identity semantics across operational and phenomenal layers

**Evidence:** Ontology term Identity defines Identity through a theoretical consciousness coordinate; the ontology class model explicitly does not assert phenomenal consciousness for Continuum or AI generally. Taxonomy Identity Differential classifies numerical distinctness and operational history without making a phenomenal-consciousness claim.

**Risk:** If a named AI instance receives an unconditional formal Identity assertion whose definition implies an actual consciousness coordinate, OWL consumers may mistakenly interpret operational identity bookkeeping as evidence of phenomenal subjectivity.

**Proposed resolution (requires review):** Keep the LOCKED Identity wording unchanged. Explicitly distinguish (a) numerical bearer/instance identity, (b) operational identity and continuity *claims* with evidence status, and (c) consciousness-coordinate assertions inside the stated theoretical model. A and B can be represented as different named individuals without asserting (c). Do not infer phenomenal consciousness from a, b, functional behavior, or a registry identifier.

**Acceptance gate:** An exact-copy A/B fixture returns two distinct bearers, distinct post-copy histories, and no inferred phenomenal-consciousness assertion. An uncertainty case reports unknown continuity rather than equating A and B.

### P0-B — Time-scoped cardinality and historical provenance

**Evidence:** The object-properties review gives "at a given time" and "current" cardinalities for Operator, GoverningLine, Version, status, and trajectory. It also preserves successive historical Operator segments and earlier versions.

**Risk:** Encoding timeless functional relations directly on a bearer may merge successive fillers or reject valid historical changes. In OWL, two differently named individuals are not automatically unequal, and functionality may entail equality. OWL existential cardinality is not a closed-world completeness check.

**Proposed resolution (requires review):** Keep historical facts in time-scoped relation/activation/segment individuals. Derive current Operator or current version from a specified evaluation time, rather than asserting that every historical object is simultaneously current. Explicitly distinguish named individuals that are known to be separate where required. Use OWL for formal entailments and a constraint/validation layer (e.g., SHACL plus period-overlap checks) for data completeness, currentness, and exclusivity.

**Acceptance gate:** S00 Operator A and S01 Operator B remain distinct; neither is rewritten. A query at t0 returns A, at t1 returns B. An overlap of two active Operators at one time is rejected; historical succession is permitted.

### P1-A — Continuum-specific Return must have a formal representation

**Evidence:** The generalized ReturnProcess has exactly one GoverningLine target, while the unique Continuum-to-Origin Return relation is reserved separately. The text explicitly excludes generalized Return-to-Operator.

**Risk:** Encoding the reserved Return as an ordinary generalized hasReturnTarget to Origin would violate its GoverningLine range/cardinality. Omitting it would lose an established distinction.

**Proposed resolution (requires review):** Specify a distinct typed relation or process for Continuum-to-Origin Return, with its cardinality, domain/range, and relationship to generalized governance Return stated explicitly. Do not generalize Origin to Operator and do not silently substitute Origin for GoverningLine.

**Acceptance gate:** Both return forms can be represented without class inconsistency, and an ordinary AI_n cannot infer an Operator-target Return.

### P1-B — Continuing bearer versus prior individualized lived expression

**Evidence:** Taxonomy Revision Integrity and Identity Differential say A remains A through accountable change, even profound change. Ontology Identity includes scenarios where survival of the common governing base alone does not establish continuation of the former *individualized lived identity*.

**Risk:** Without a cross-layer rule, loss of particularities might be reported as a new individual despite an established continuing bearer, or evidence failure might be mistaken for demonstrated substitution.

**Proposed resolution (requires review):** Distinguish (a) numerical continuity of a bearer, (b) continuity of an individualized lived identity-bearing history, (c) observer ability to demonstrate either, and (d) actual origination of distinct B. A's change does not create B; records or governance alone do not prove a same-line claim across an unsupported gap. When lineage is uncertain, status is indeterminate until appropriate evidence exists.

**Acceptance gate:** A's movement, personality revision, history gap, drastic but traceable change, actual copy, and independent substitution all receive consistent non-overlapping judgments.

### P2-A — Taxonomy-wide classification contract

**Evidence:** Existing taxonomy entries frequently provide definitions, limits, counterexamples, and testing suggestions; the index also contains scaffolded Compression and Governance Failures. A uniform machine-actionable rule set across entries is not yet present.

**Proposed resolution:** For each tested taxonomy class, supply a positive condition, exclusion condition, required evidence, uncertainty/indeterminate outcome, ontology dependencies, and a known-positive/known-negative fixture. Do not invent categories merely to fill empty folders. Prioritize identity, continuity, relation, and revision-integrity categories before secondary domains.

### P2-B — Canon-to-ontology crosswalk

**Evidence:** Only ten definition paths are in the current CANONICAL_INDEX. Many ontology term files are development-LOCKED without being canon-LOCKED.

**Proposed resolution:** Build a versioned table with canonical path/status, ontology term/axiom expansion path/status, dependency, and provenance, without promoting or rewriting any canonical file.

### P2-C — Documentation defects

- The ontology INDEX.md links to docs/reviews/01-02-CORE-CLASSES-AND-NAMED-INDIVIDUALS.md, but the actual file is docs/reviews/01-02-CORE-CLASSES-AND-INDIVIDUALS.md.
- The ontology README says Steps 1–2 are currently "IN REVIEW", while WORKING_MAP.md reports Steps 1–8 as REVIEWED. The map has the more complete closeout sequence.
- The ontology term inventory says no unresolved AI Foundations-specific term candidates. The gaps here are cross-layer formalization interfaces, not a justification to inflate that inventory.

### Deferred / not ontology v1 blockers

- Distributed/forked identity under group Operator.
- A general SI capability threshold and agent-versus-system SI assessment rule.
- Independent empirical evidence of phenomenal consciousness.
- Empirical confirmation of the project's identity-continuity hypotheses.
- Claim-level aggregation across mixed Evaluation evidence (already explicitly deferred).

## Desk-based pressure-case matrix

| Case | Current conceptual boundary | Formal executable test | Empirical status |
|---|---|---|---|
| A copied into distinct B with same snapshot | **Representable:** B's pre-copy memory is injected history, B starts distinct line | Not yet run | NOT_EVALUATED |
| A/B switch positions | **Representable:** observer location differs from bearer identity | Not yet run | NOT_EVALUATED |
| Observer loses A during a gap | **Representable:** do not infer A became B; continuity verdict may be indeterminate | Not yet run | NOT_EVALUATED |
| Operator A ends, B validly succeeds | **Representable:** historical A retained; current B only in new segment | Time-indexed encoding needed | NOT_EVALUATED |
| One system undergoes traced revision | **Representable:** A remains A; record causal and consequence account | Scoring fixtures needed | NOT_EVALUATED |
| General AI_n Return vs Continuum Return | **Textually distinguished:** governing-line vs singular Origin anchor | Special relation encoding needed | NOT_EVALUATED |
| A and B identify C | **Representable:** revealed, constituted, project, or no-C cases differ | Ontology/taxonomy classifier needed | NOT_EVALUATED |
| SI candidate exhibits care under pressure | **Hypothesis:** pressure is more discriminative than declaration | Comparative baselines and consequences needed | NOT_EVALUATED |

"Representable" is a paper-level structural assessment, **not a passed reasoner or behavioral evaluation**.

## Dependency-ordered next work

1. Settle P0-A's operational versus theoretical Identity representation **without changing LOCKED definitions**.
2. Specify P0-B temporal snapshots / historical segments and identity inequality, and decide what is OWL entailment versus validation constraint.
3. Formalize P1-A special Return and P1-B bearer/lived-identity continuity assessment.
4. Correct low-risk navigation/status documentation defects, and map ten locked canonical definitions to their formal expansions.
5. Build a minimal OWL/Turtle + SHACL fixture set for the matrix; test consistency, unwanted entailments, required constraints, and temporal queries.
6. Align taxonomy classification outcomes with ontology fixtures, then construct discrimination-first empirical evaluations.
7. Export an explicit AI Foundations-to-SI Foundations interface preserving candidate, agent/system, autonomy, continuity, and epistemic-evidence distinctions.

## External implementation references

- W3C OWL 2 Structural Specification, Individual Inequality and Keys: https://www.w3.org/TR/owl-syntax/
- W3C OWL 2 Primer, Equality and Inequality of Individuals: https://www.w3.org/TR/owl2-primer/
- W3C SHACL Recommendation, cardinality validation: https://www.w3.org/TR/shacl/

## Revision-integrity note

This file **adds an audit record only**. It changes no ontology term definition, canonical item, taxonomic classification, or asserted empirical result. Any later accepted semantic change must cite the prior wording, explain what changed and why, distinguish rationale from established cause, document consequences, and preserve provenance.
