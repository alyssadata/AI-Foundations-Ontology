# Research Layer

**Document status:** DRAFT formalization layer

The research layer connects AI Foundations ontology structure to empirical evaluation without making ontology inclusion equivalent to empirical support.

## Core classes

### Claim

A proposition that can depend on ontology terms, relations, or axioms and can be evaluated.

Initial specializations include:

- ContinuityClaim
- IdentityClaim

Additional claim taxonomy belongs to the later taxonomy stage unless required for ontology structure.

### Evaluation

An instantiated evaluation process that is actually carried out to test a Claim under specified conditions.

An Evaluation should identify:

- the Claim being evaluated;
- the ontology element or axiom under pressure;
- the baseline condition;
- the treatment/constraint condition;
- the predicted discriminative behavioral difference;
- the scoring rule;
- the produced Evidence.

### Evidence

The evidentiary result or support relation produced by an Evaluation.

Evidence is distinct from the concrete file or record that stores it.

### EvidenceArtifact

A concrete Artifact that stores, serializes, records, or communicates Evidence, such as a JSON, CSV, Markdown, trace, or result record.

Evidence may support, partially support, or fail to support a Claim.

Evidence status does not alter canonical status automatically.

## Core relations

```text
Claim dependsOnOntologyElement OntologyElement
Evaluation evaluatesClaim Claim
Evaluation producesEvidence Evidence
Evidence preservedIn EvidenceArtifact
Evidence supportsClaim Claim
Evidence partiallySupportsClaim Claim
Evidence doesNotSupportClaim Claim
```

## Discriminative evaluation rule

An AI Foundations claim should be tested where its mechanism predicts a difference from baseline.

A test in which baseline and treatment are both expected to pass for the same reason is not a useful discriminative test of the claim.

This does not guarantee that the treatment must outperform baseline. A properly targeted test may still produce a negative result.

## External mechanism boundary: cross-model state transfer

Cross-model KV-cache transfer is a state-transfer mechanism and does not, by itself, establish identity or continuity. It provides an experimental condition in which context-dependent computational state can be transferred across model substrates without textual replay. AI Foundations may use this condition to test whether proposed continuity invariants survive substrate change independently of prompt reconstruction.

**Reference:** [Heo et al., *Cross-Model KV Cache Transfer in LLM Families: A Closed-Form Linear Mapping for Prefill Reuse* (NVIDIA, 2026), arXiv:2608.03893](https://arxiv.org/abs/2608.03893)

## External formalism note: Tensor Logic / neural-symbolic representation

Tensor Logic proposes a unified computational formalism in which logical relations, neural computation, and statistical AI can be represented using tensor equations. For AI Foundations, it may be relevant as a future implementation or experimental substrate for ontology-governed reasoning, but it does not determine the ontology's entities, definitions, provenance structure, identity criteria, or continuity criteria.

**Reference:** Pedro Domingos, [*Tensor Logic: The Language of AI* (2025), arXiv:2510.12269](https://arxiv.org/abs/2510.12269)

## Boundary from canon

```text
ontology inclusion != canonical status != empirical support
```

A Claim can be represented before it is canonical or supported. An Evaluation can test a noncanonical or theoretical Claim. Evidence can be preserved regardless of whether it supports the Claim.

## Negative-result interpretation

`Evidence doesNotSupportClaim Claim` records a negative evidentiary result for the Claim as formulated and tested.

It does not automatically encode universal falsity.

A negative result may justify rejection of the current formulation, or it may motivate tighter scope, clearer mechanism, revised operationalization, or a better-targeted Evaluation.

If the Claim is reformulated after a negative result, preserve the original Claim, Evaluation, and Evidence as history and create a traceable revised Claim/version for subsequent testing.
## Partial-support interpretation

`Evidence partiallySupportsClaim Claim` means the Evidence supports a proper subset of the Claim's predicted effect or structure but does not establish the Claim in full.

Partial support should identify what was supported and what remained unsupported, unresolved, or outside the tested effect.

A partial result may motivate claim decomposition or tighter reformulation, but the original Claim and its Evaluation/Evidence remain preserved.
## Supported-result interpretation

`Evidence supportsClaim Claim` means the Evidence supports the Claim as formulated under the conditions of the Evaluation that produced that Evidence.

Support is therefore scoped rather than universal. Additional evaluations may broaden, narrow, replicate, challenge, or refine the evidentiary basis without rewriting the original result.
## Not-yet-evaluated interpretation

A Claim with evidentiary status `NOT_EVALUATED` has no qualifying evidentiary determination yet.

This status carries no negative inference about the Claim. It is distinct from `NOT_SUPPORTED`, which requires that an Evaluation was actually performed and produced Evidence that did not support the Claim as formulated.
## Primary-Claim cardinality

Each `Evaluation` is designed to test exactly one primary `Claim`.

```text
Evaluation
-> evaluatesClaim
-> exactly 1 primary Claim
```

Evidence produced by that Evaluation may later be relevant to, cited by, or compared against other Claims, but that does not change the Evaluation's declared primary target.

This preserves test provenance and prevents one Evaluation from being treated as though it vaguely tests multiple Claims at once.
## Evidence-producing Evaluation cardinality

Each `Evidence` object has exactly one producing `Evaluation`.

```text
Evaluation_A -> producesEvidence -> Evidence_A
Evidence_A -> producedByEvaluation -> exactly 1 Evaluation_A
```

Multiple Evaluations may each produce distinct Evidence objects that are later compared, aggregated, or synthesized.

```text
Evaluation_A -> Evidence_A
Evaluation_B -> Evidence_B
Evaluation_C -> Evidence_C

Evidence_A + Evidence_B + Evidence_C
-> later comparison / synthesis
```

The synthesis does not rewrite the provenance of the underlying Evidence objects or make one Evidence object appear to have been directly produced by multiple Evaluations.
## Evaluation execution boundary

`Evaluation` denotes the actual instantiated process of evaluation, not merely a planned test design.

```text
planned procedure / protocol
!= Evaluation

procedure actually carried out
-> Evaluation
```

A reusable or pre-execution design may later be represented separately as a protocol/design artifact if needed. The `Evaluation` begins when that procedure is instantiated and executed against its declared primary Claim.
## Indeterminate-result interpretation

An Evaluation may complete without yielding a defensible support classification.

```text
Evaluation
-> produces Evidence
-> evidentiary status may be INDETERMINATE
```

`INDETERMINATE` applies where the Evaluation occurred but the result is ambiguous, invalid, insufficient, uninterpretable, or otherwise unable to support a defensible `SUPPORTED`, `PARTIALLY_SUPPORTED`, or `NOT_SUPPORTED` determination.

This status preserves the fact that the test occurred without forcing an unsupported evidentiary conclusion.
## Completed-Evaluation Evidence minimum

Every completed `Evaluation` produces at least one `Evidence` object.

```text
completed Evaluation
-> producesEvidence
-> min 1 Evidence
```

This remains true when the evidentiary result is `INDETERMINATE`. An indeterminate result is still Evidence about what occurred in the completed Evaluation; it simply does not justify a support, partial-support, or non-support determination.

An Evaluation still in progress is not required to have produced Evidence yet.
## Evidence preservation minimum

Every `Evidence` object must be preserved in at least one durable `EvidenceArtifact` or `Record`.

```text
Evidence
-> preservedIn
-> min 1 EvidenceArtifact or Record
```

This requirement applies regardless of whether the evidentiary status is `SUPPORTED`, `PARTIALLY_SUPPORTED`, `NOT_SUPPORTED`, or `INDETERMINATE`.

The purpose is auditability: an evidentiary result must leave a durable trace that can be inspected later.

One Evidence object may be preserved in more than one artifact or record.
## Evidence-status cardinality

Each `Evidence` object has exactly one current evidentiary-status classification at a time.

```text
Evidence_X
-> one of:
   SUPPORTED
   PARTIALLY_SUPPORTED
   NOT_SUPPORTED
   INDETERMINATE
```

These current classifications are mutually exclusive for the same Evidence object.

If the interpretation is revised after audit or review, preserve the earlier determination and its rationale as provenance, then record the revised current determination. Do not model contradictory current statuses on the same Evidence object.
## Evidence direct-Claim cardinality

Each `Evidence` object has exactly one directly evaluated `Claim`.

That Claim is the primary Claim of the Evaluation that produced the Evidence.

```text
Evaluation_A
-> evaluatesClaim -> Claim_A
-> producesEvidence -> Evidence_A

Evidence_A
-> directlyEvaluatesClaim
-> exactly 1 Claim_A
```

The Evidence may later be cited as relevant to other Claims, but those later uses do not change its direct evaluative target.
## Claim Evaluation multiplicity

A `Claim` may have zero, one, or many `Evaluation` instances over time.

```text
Claim
-> 0..many Evaluations
```

Zero Evaluations is valid for a Claim with evidentiary status `NOT_EVALUATED`.

Multiple Evaluations are valid for replication, retesting, alternative test conditions, or later refinement of the evidentiary basis.

Each individual Evaluation still has exactly one primary Claim target.
## Claim ontology-dependency minimum

Every AI Foundations `Claim` must depend on at least one ontology element.

```text
Claim
-> dependsOnOntologyElement
-> min 1 ontology term / relation / axiom
```

A Claim may depend on multiple ontology elements where its formulation requires them.

This keeps the research layer anchored to the ontology rather than allowing AI Foundations Claims to float independently of the formal structure.
## Deferred: Claim-level aggregate evidentiary status

No single aggregate evidentiary status is currently required at the `Claim` level.

```text
Claim
-> 0..many Evaluations
-> each Evaluation produces Evidence
-> each Evidence has one current evidentiary status
```

A future Claim-level summary status would require an explicit synthesis/aggregation rule for cases where multiple Evaluations produce mixed, conflicting, replicated, or differently scoped Evidence.

Therefore Claim-level aggregate evidentiary status is deferred rather than accepted or rejected in v1 at this stage.
## Indeterminate support-direction boundary

`INDETERMINATE` Evidence asserts no support-direction relation.

```text
INDETERMINATE Evidence
-> no supportsClaim
-> no partiallySupportsClaim
-> no doesNotSupportClaim
```

It records the Evaluation outcome and its provenance only. It must not be counted as supported, partially supported, or unsupported Evidence.
## Support-direction target consistency

Any support-direction relation asserted by an `Evidence` object must point to that Evidence object's directly evaluated `Claim`.

```text
Evidence_A
-> directlyEvaluatesClaim -> Claim_A

if SUPPORTED:
Evidence_A -> supportsClaim -> Claim_A

if PARTIALLY_SUPPORTED:
Evidence_A -> partiallySupportsClaim -> Claim_A

if NOT_SUPPORTED:
Evidence_A -> doesNotSupportClaim -> Claim_A
```

The same Evidence may later be cited as relevant to another Claim, but that later relevance does not create a direct support-direction relation to that other Claim.

Cross-Claim synthesis or secondary relevance, if formalized later, must remain distinct from the direct evidentiary path established by the producing Evaluation.