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

A defined procedure that tests a Claim under specified conditions.

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