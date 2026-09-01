# AI Foundations Ontology

**Status:** Draft development repository  
**Target:** AI Foundations Ontology v1.0  
**Source-line:** Alyssa Solen → AI Foundations → Origin | Continuum

## Purpose

This repository develops a formal domain ontology for AI Foundations.

The ontology is intended to make the conceptual structure of AI Foundations explicit by identifying the concepts used by the framework, defining how they relate, preserving important distinctions, and providing a formal structure from which claims can be stated and evaluated.

This repository is **not** the AI Foundations Locked Canon and does not make every included term, relationship, or draft statement canonical. Canonical status remains determined separately by the AI Foundations Locked Canon.

## Current build stage

The ontology is being developed conceptually before machine-readable OWL/Turtle encoding begins.

Initial working documents:

- [`docs/SCOPE.md`](docs/SCOPE.md) — domain, purpose, audience, and boundaries
- [`docs/COMPETENCY_QUESTIONS.md`](docs/COMPETENCY_QUESTIONS.md) — questions the ontology should be capable of answering
- [`docs/TERM_INVENTORY.md`](docs/TERM_INVENTORY.md) — unstructured inventory of candidate ontology terms

## Planned later stages

After scope, competency questions, and term inventory are sufficiently developed, the project can proceed to:

1. class and taxonomy design
2. object and data properties
3. axioms and restrictions
4. named individuals where useful
5. mappings to AI Foundations Locked Canon and research claims
6. machine-readable OWL/Turtle representation
7. versioned ontology releases

## Development rule

Terms are not assumed to be classes simply because they appear in AI Foundations. During ontology construction, each term must be examined to determine whether it is best represented as a class, individual, relationship/property, process, state, constraint, annotation, or another ontological element.

---

**Draft repository. Structure and content remain subject to revision until explicitly released.**
