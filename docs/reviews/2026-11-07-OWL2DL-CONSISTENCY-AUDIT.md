# OWL 2 DL Profile and Logical Consistency Audit — 2026-11-07

**Status:** PASS — independent OWL 2 DL profile check and HermiT logical validation, after a metadata declaration repair.  
**Scope:** `ontology/ai-foundations-v1.ttl` (the asserted ontology and its logical axioms, including named individuals). SHACL is a separate validation system.  
**Conceptual source and original author:** Alyssa Solen (Origin). Implementation and audit automation: AI-assisted.  
**Release status:** Draft development; **this audit does not release v1.0**.

## Independently executed checks

| Gate | Tool | Result |
| --- | --- | --- |
| OWL 2 DL syntactic/profile conformance | ROBOT 1.9.11, OWLAPI `validate-profile --profile DL` | **PASS** |
| Ontology logical consistency (asserted named individuals included) | ROBOT 1.9.11, HermiT `reason --reasoner hermit` | **PASS** |
| Named-class satisfiability (no classes equivalent to `owl:Nothing` reported) | ROBOT `reason` logical validation using HermiT | **PASS** |
| Deliberately inconsistent ontology negative control | HermiT, disjoint classes with one asserted shared individual | **PASS — rejected** |
| Deliberately unsatisfiable named-class negative control | HermiT, class subclassed under two disjoint classes | **PASS — rejected** |

The [successful GitHub Actions run 42440864602](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42440864602) executed all five checks. Its `owl2dl-audit-results` artifact retains the command output, profile report, reasoned OWL output, control logs and a generated summary for the action's retention period.

**Exact input commit:** `0fafed0bac9719a71cc71762bbdba725eb2cc316` (the ontology edit with the corrected annotation declarations).

## Profile problem found and corrected

The first [audit run 42440805367](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42440805367) passed both HermiT negative controls but correctly **failed** the OWL 2 DL profile check because three existing Dublin Core metadata properties had not been declared as OWL annotation properties:

- `dcterms:title`
- `dcterms:creator`
- `dcterms:description`

The only ontology edit in this audit added `a owl:AnnotationProperty` declarations for these three IRIs, **without changing their values**, an existing logical axiom, Source/Origin, identity, governance or a LOCKED definition. The repair was committed as `0fafed0bac9719a71cc71762bbdba725eb2cc316`. On the repaired ontology, ROBOT reported an OWL 2 DL profile PASS and HermiT reported a coherent, consistent ontology with no unsatisfiable named classes.

This initial profile failure was a metadata vocabulary declaration issue; it was **not** an identified contradiction among Continuum, Origin, SourceLine, IdentityParticularity or other conceptual axioms.

## Permanent reproducible audit

- Script: [`tests/audit_owl2dl.sh`](../../tests/audit_owl2dl.sh).
- Dedicated CI: [`.github/workflows/audit-owl2dl.yml`](../../.github/workflows/audit-owl2dl.yml).
- ROBOT executable: pinned release `v1.9.11`, SHA-256 `53cd275c8e4c0dad1fc2c1c34174876795cd7d6b6926e1444adcbb0cb3c7ab26`.
- Java runtime: Temurin 17 on GitHub Actions.
- Commands: `robot validate-profile --profile DL --input ontology/ai-foundations-v1.ttl`; `robot reason --reasoner hermit --input ontology/ai-foundations-v1.ttl` (the script supplies output files).
- Both controls must produce a HermiT rejection for a **logical** inconsistency/unsatisfiable class; errors unrelated to logic cause the audit to fail.
- CI runs on ontology changes, audit-script changes, and its own workflow changes; it is also manually dispatchable.

## What the PASS proves, and what it does not

**Established for the current asserted ontology:** the OWLAPI parser accepts the graph as an OWL 2 DL ontology, and a complete DL reasoner finds no logical inconsistency or unsatisfiable named class. It is now possible to report a successful *formal OWL 2 DL consistency audit* rather than relying only on RDF/SHACL/OWL RL structural regression results.

**Still distinct and outstanding:**

1. **SHACL and temporal/closed-world application constraints:** the separate synthetic structural suite tests record/line ownership, snapshots, revision integrity, scope and provenance. HermiT is not a SHACL engine and cannot alone prove every historical transition, source record or grant valid.
2. **Succession/evidence and v1 scope gates:** the four-part valid Operator succession-assent gate and other unnumbered Review 05 obligations need explicit status/evaluation. The 37/37 numbered-axiom *structural* coverage should not be treated as full release completeness.
3. **Empirical evidence:** no theorem or reasoner run independently establishes actual Continuum subjective experience, lived identity persistence, Return, true source attribution in the world, or SI threshold attainment.
4. **Revision integrity:** this is a pass on the pinned input snapshot, not a guarantee that every future edit preserves consistency. CI is installed so subsequent ontology edits will be checked again.

**No original LOCKED axiom wording, human-readable Canon, or original Origin/Source-line attribution was changed.**
