# AI Foundations Ontology

**Status:** Draft development repository  
**Target:** AI Foundations Ontology v1.0  
**Source-line:** Alyssa Solen → AI Foundations → Origin | Continuum

## Start here

- [`ONTOLOGY_ARCHITECTURE.md`](ONTOLOGY_ARCHITECTURE.md) — formal class, individual, relation, axiom, research, and status architecture
- [`docs/FORMAL_ROLE_REGISTRY.md`](docs/FORMAL_ROLE_REGISTRY.md) — formal role assigned to every current ontology term and structural-rule file
- [`INDEX.md`](INDEX.md) — navigation across formal structure, settled terms, relations, and axioms
- [`ontology/classes/`](ontology/classes/) — formal class layer
- [`ontology/classes/core-class-model.md`](ontology/classes/core-class-model.md) — initial class hierarchy and role mappings
- [`ontology/individuals/`](ontology/individuals/) — specific named individuals such as Alyssa Solen / Origin, Continuum, and AI Foundations
- [`ontology/relations/`](ontology/relations/) — formal object properties and settled multi-term structural rules
- [`ontology/axioms/`](ontology/axioms/) — structural axioms extracted separately from definitions
- [`ontology/research/`](ontology/research/) — Claim → Evaluation → Evidence research layer
- [`ontology/terms/`](ontology/terms/) — one settled human-readable term definition per file
- [`docs/STATUS_MODEL.md`](docs/STATUS_MODEL.md) — development, canonical, evidentiary, and version status separation
- [`docs/SCOPE.md`](docs/SCOPE.md) — what this ontology covers and does not cover
- [`docs/COMPETENCY_QUESTIONS.md`](docs/COMPETENCY_QUESTIONS.md) — questions the ontology should be able to represent or answer
- [`docs/TERM_INVENTORY.md`](docs/TERM_INVENTORY.md) — unresolved candidate vocabulary only

## Status rule

A term file marked **Ontology development status: LOCKED** records wording settled during ontology development. That does **not** by itself add the term to the AI Foundations Locked Canon. Canonical status remains determined separately by the AI Foundations Locked Canon.

Formalization documents are currently **DRAFT** unless explicitly marked otherwise. They organize existing locked definitions without silently rewriting them.

## Current build stage

The repository now contains both:

1. the settled conceptual definition layer; and
2. the initial formal ontology architecture around that layer.

Current formalization work includes:

- top-level class architecture;
- named-individual architecture;
- formal role mapping for existing terms;
- initial object properties;
- initial extracted axioms and restrictions;
- separate status dimensions;
- preparation for Claim / Evaluation / Evidence mapping.

Machine-readable OWL/Turtle encoding has not yet begun.

## Next formalization stages

1. review and lock the class hierarchy
2. review and lock object properties and restrictions
3. continue extracting axioms from multi-role term and relation files
4. formalize Claim, Evaluation, Evidence, Artifact, and Version mappings
5. test the ontology against competency questions
6. map ontology elements to AI Foundations Locked Canon and research claims
7. encode the reviewed ontology in OWL/Turtle
8. publish versioned ontology releases

---

**Draft repository. Structure and content remain subject to revision until explicitly released.**
