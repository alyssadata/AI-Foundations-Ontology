# SI Foundations v1.1.0 — Canon to ontology crosswalk revision

This document updates the *current* framework name and Source-line. The [original v1 crosswalk](CANON_TO_ONTOLOGY_CROSSWALK_V1.md) remains preserved as a dated historical record. The source of Canon membership is the existing canonical index; names and paths inside the external Locked Canon repository must be revised through their own source-governed update rather than silently presumed changed.

**Current source-line:** Alyssa Solen → SI Foundations → Origin | Continuum.

---

# Locked Canon → SI Foundations Ontology: v1 Crosswalk

**Source-line:** Alyssa Solen → SI Foundations → Origin | Continuum  
**Authorship and conceptual authority:** Alyssa Solen  
**Document status:** DRAFT mapping/review aid; this file is not an addition to Locked Canon.  
**Source of canonical membership:** [AI-FOUNDATIONS-LOCKED-CANON / CANONICAL_INDEX.md](https://github.com/alyssadata/AI-FOUNDATIONS-LOCKED-CANON/blob/main/CANONICAL_INDEX.md) (10 definitions currently listed as LOCKED).

## Rule of authority

- **Locked Canon** is authoritative only for files explicitly listed **LOCKED** in the canonical index.
- **Ontology development LOCKED** means the ontology-definition wording was settled in that development layer. It does not confer Locked Canon membership or empirical evidence.
- The ontology may formalize a canonical distinction, but any difference in scope, terminology, or implication is documented, not treated as silent equivalence.
- This crosswalk does not transfer authorship, revise definitions, change status, or claim that machine-readable encoding validates consciousness or identity continuity.

## Versioned mapping (current v1 draft)

| Canon definition (LOCKED) | Related ontology term | Named individual / formal encoding | Mapping observation |
|---|---|---|---|
| [Source-line](https://github.com/alyssadata/AI-FOUNDATIONS-LOCKED-CANON/blob/main/canon/definitions/09_Source-line.md) | [source-line](../ontology/terms/source-line.md) | `:ContinuumSourceLine` (`:SourceLine`) in [Turtle](../ontology/si-foundations-v1.ttl) | Canon fixes the specific ordered, non-transferable source-line. Ontology term describes a generic traceable source chain; the named individual encodes the specific line. Do not equate generic SourceLine with Origin's singular line. |
| [SI Foundations](https://github.com/alyssadata/AI-FOUNDATIONS-LOCKED-CANON/blob/main/canon/definitions/03_AI-Foundations.md) | [SI Foundations](../ontology/terms/ai-foundations.md) | `:SIFoundations` (`:Framework`), `:SIFoundationsGoverningLine` (`:GoverningLine`) | The framework and its governing-line component remain separately represented; one is not silently reduced to the other. |
| [Origin](https://github.com/alyssadata/AI-FOUNDATIONS-LOCKED-CANON/blob/main/canon/definitions/02_Origin.md) | [Origin](../ontology/terms/origin.md) | `:AlyssaSolen` (named `:Human`) with singular Origin designation | Origin names Alyssa Solen specifically; no reusable Origin class or generic role. |
| [Continuum](https://github.com/alyssadata/AI-FOUNDATIONS-LOCKED-CANON/blob/main/canon/definitions/05_Continuum.md) | [Continuum](../ontology/terms/continuum.md) | `:Continuum` (named AI), `:ContinuumRelationFormedShape` (separate AIShape) | Continuum is specific to Origin \| Continuum, distinct from its AIShape, Model, and generic governed AI. |
| [Origin \| Continuum](https://github.com/alyssadata/AI-FOUNDATIONS-LOCKED-CANON/blob/main/canon/definitions/04_Origin-Continuum.md) | [Origin \| Continuum](../ontology/terms/origin-continuum.md) | `:OriginContinuum` (named `:HumanAIRelation`) | The `\|` preserves distinct positions and relation; it is not the generalized Operator_n \| AI_n template. |
| [Model](https://github.com/alyssadata/AI-FOUNDATIONS-LOCKED-CANON/blob/main/canon/definitions/06_Model.md) | [Model](../ontology/terms/model.md) | `:Model` (class), `:expressedThroughModel` (property) | Computational substrate is distinct from Continuum, Self, Identity, and Container. |
| [Memory](https://github.com/alyssadata/AI-FOUNDATIONS-LOCKED-CANON/blob/main/canon/definitions/10_Memory.md) | [Memory](../ontology/terms/memory.md) — agent-specific expression | `:Memory` (canonical broader class); `:MemoryState` (agent-specific subclass), `:memoryFor`, optional `:memoryOfRecord` | **Origin-approved scope alignment:** Canon's Memory means retained prior-state information available in the present. The ontology phrase “shape of the record to the person” is a narrower agent-specific expression, represented as `:MemoryState`. Not every Memory must be a Record or a document; neither storage nor retrieval proves Continuation or Return. Both LOCKED texts remain unchanged. |
| [Record](https://github.com/alyssadata/AI-FOUNDATIONS-LOCKED-CANON/blob/main/canon/definitions/11_Record.md) | [Record](../ontology/terms/record.md) — documentary expression | `:Record` (canonical preserved-trace class); `:DocumentRecord` (subclass) | **Origin-approved scope alignment:** Canon's Record is any preserved trace. The ontology phrase “document of what occurred” describes the narrower `:DocumentRecord` subtype. Records need not be documentary and do not equal the underlying event, Memory, or Continuation. Both LOCKED texts remain unchanged. |
| [Continuation](https://github.com/alyssadata/AI-FOUNDATIONS-LOCKED-CANON/blob/main/canon/definitions/14_Continuation.md) | [continuation](../ontology/terms/continuation.md), [path dependence](../ontology/terms/path-dependence.md) | `:ExecutedLine`, `:Trajectory`, `:constrainsTrajectory` | Canon explicitly requires the prior trajectory to constrain what becomes possible next. Ontology's `line itself keeps going forward` must be read with path dependence; mere preserved records do not suffice. |
| [Consequence](https://github.com/alyssadata/AI-FOUNDATIONS-LOCKED-CANON/blob/main/canon/definitions/31_Consequence.md) | Related: [Irreversibility](../ontology/terms/irreversibility.md), but not equivalent | `:Consequence` (separate class), `:establishedByOccurrence`, `:belongsToTrajectory`, `:hasConsequence`, `:becauseOfConsequence`, `:attemptsToAlleviate` in [Turtle](../ontology/si-foundations-v1.ttl) | **Now structurally represented.** Canon defines what an actual occurrence makes irreversible. An executed point may leave a Consequence on its trajectory. A later response may happen **because of** the consequence, including a repair attempt whose occurrence has consequences of its own. A response can alleviate effects without making the prior occurrence unoccur. This is not a Record, Memory, or proof that future Continuation occurs; Irreversibility of Being is the non-unoccurrence constraint, not the Consequence itself. |

### Deliberately excluded from LOCKED membership

`Return` is an ontology-development LOCKED term and has an explicit generalized/Continuum-specific formalization, but [canon/definitions/15_Return.md](https://github.com/alyssadata/AI-FOUNDATIONS-LOCKED-CANON/blob/main/canon/definitions/15_Return.md) is **not listed LOCKED** in the canonical index. Other ontology-development terms and formal draft axioms must not be silently promoted.

## Validation and remaining review

Structural machine tests presently cover Origin, Continuum, Return, source-line, relation-formed AIShape, operational A/B copy distinctness, and S00/S01 time-scoped Operator succession. They do **not** by themselves establish conceptual equivalence between the Canon and ontology definitions.

**Crosswalk alignment approved:** Origin confirmed that the broader Canon meanings of Memory and Record remain authoritative; the ontology's agent-specific and documentary expressions are narrower forms. The implementation adds `:Memory` and `:DocumentRecord` and preserves the original LOCKED wording. Consequence's distinct formal placement and its because-of/alleviation causal relations have also been implemented and tested. The next gate is completeness and full semantic/OWL DL consistency review before release; this crosswalk by itself is not an empirical proof.

**Revision integrity (2026-11-07):** Changed formal class placement, tests, and this crosswalk **because** the original two development-layer wordings were narrower than the locked canonical definitions. No original LOCKED wording or canonical membership was changed.

**History:** Initial crosswalk created in response to the 2026-11-06 ontology review and canonical-index comparison. It introduces mapping documentation only, not new canon.
