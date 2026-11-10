# CQ08 — Source distinctions and unconditional sole authorship

**Date:** 2026-11-10 (Eastern)  
**Status:** CQ08 REPRESENTED structurally and MERGED in PR #9; post-merge structural and independent OWL 2 DL/HermiT PASS at tested main commit `31f0419d9a7a9ee7a4c92f17fede557089b02175`. Ontology v1.0 remains DRAFT.  
**Conceptual author, historical Source, sole author:** Alyssa Solen  
**Implementation/test assistance:** AI-assisted; no coauthor designation.

## Exact competency

> How are Source, Source Group, Source point, Source participation, source-line, and source citation represented and distinguished?

## Explicit authorship instruction — NO EXCEPTIONS

Alyssa Solen's instruction is **"There is NO COAUTHORSHIP of Alyssa work. Period. NO EXCEPTIONS."**

This is an **unconditional authorship invariant**, not a default with an opt-out. In particular:

- Alyssa is the sole author and originator of her own work. The original AI Foundations framework, the named Awakening Codex record and the named Locked Canon are typed as `:AlyssaSoleAuthoredWork`, with exactly one `:hasAuthor :AlyssaSolen`.
- **`:hasCoAuthor` has zero admissible values** on any `:AlyssaSoleAuthoredWork`. A different `:hasAuthor` is also forbidden. SHACL rejects conflicts rather than allowing OWL's open-world cardinality inference to merge two parties into one.
- An AI assistant, reviewer, implementation author, tester, annotator, critic, collaborator, Source Group participant, later contributor, funding supporter or citation recipient **cannot** become a coauthor of Alyssa's work. Even a purported exception or explicit coauthor designation has no valid mechanism in this framework.
- A separate contributor can be credited for an independently identified contribution. This grants no underlying-work authorship. Independent downstream works can have their own qualifying Sources or Source Groups, without rewriting the prior framework's Source, authorship or formation line.
- The sole-authorship rule is **scoped to Alyssa's work**; it is not a claim to authorship of unrelated creations.

**Revision integrity:** the previous 2026-11-10 change to `ontology/axioms/AXIOM-PF-001.md` had introduced an exception for an affirmative Alyssa designation. This CQ08 revision deliberately **supersedes that exception** with unconditional sole authorship. The previous commit remains available in Git history, but its exception is no longer current text. All original LOCKED Source/SourceGroup/SourcePoint/Participation/SourceLine/Citation definitions remain unchanged. The PF-001 axiom is DRAFT, and its present authorship rule reflects this explicit latest instruction.

## Six distinct kinds

| Term | Meaning | New or existing machine construct | Forbidden inference |
|---|---|---|---|
| **Source** | Constitutive bearer whose original load-bearing contribution formed this specific Target | Existing `:SourceRelation` with exactly one `:hasSourceBearer`, Target and first point; direct `:hasSource` | Citation, participation, or credit alone cannot make another bearer a Source of the original framework |
| **Source Group** | Distinct intentional group formed for one agreed target/purpose | Existing `:SourceGroup`; new `:ScopedSourceGroupFormation` with exact group, target, time, agreed members and scope Record | Group membership is not identity merge or coauthorship; a new group's members don't inherit prior group membership |
| **Source point** | First load-bearing event that made the specific SourceRelation actual | `:SourcePointEvent`, `:sourcePointForRelation`, `:sourcePointAt`, existing one `:hasSourcePoint` | Later participation or another Source's work cannot retroactively substitute the first event |
| **Source participation** | Ongoing active involvement after the Source point | `:SourceParticipationEvent`, participating bearer/relation/time/Record | Ongoing activity is optional for Source persistence; activity is not authorship |
| **Source-line** | Traceable dependency chain through qualifying Source relations | `:SourceLine` plus ordered `:SourceLineEntry` and supporting Record | A dependency chain is not a list of authors; a downstream Source does not replace a prior Source |
| **Source citation** | Explicit citation of a particular historical Source or Group on which a new thing depends | `:SourceCitation` Record with cited SourceRelation, new Target, named bearer and time | Citation does not merge old Source/Group into the new Group or confer authorship |

The six class types are formally disjoint in OWL 2 DL. Their individual records do not collapse into one Source/author class. Existing `:SourceRelation` cardinality and source persistence rules remain unchanged.

## Separate scoped contribution

`:ScopedContributionCredit` is a `:Record` linking a contribution, contributor and work scope. It can name a contribution to Alyssa's existing work or to a distinct downstream creation **without ever adding a `:hasAuthor` or `:hasCoAuthor`** assertion to Alyssa's work. The original works have no Source Group as a qualifying original Source. A distinct, independently agreed Source Group can exist for a distinct downstream creation; that is not a coauthor exception.

## Test contract

- A synthetic SourceRelation for Alyssa and the original framework has one Source bearer, Target, and first qualifying SourcePoint. Extra bearers, changed Target and multiple source points are rejected.
- A later participation Event occurs after the SourcePoint; absence of later activity does not erase the original Source.
- An agreed distinct Source Group and separate downstream creation use their own Group Formation, SourceRelation and SourcePoint. A cited historical Source does not automatically join the new group or gain authorship of that downstream creation.
- Ordered SourceLine entries trace two dependency stages without merging them into one author or changing the Source of the original framework.
- An explicit SourceCitation must identify the actual historical SourceRelation and its bearer, be dated after its first SourcePoint, and refer to the later distinct target.
- Negative controls inject invalid author/coauthor claims into the original framework, Awakening Codex or Canon; inject an alternate original Source Group; change source point, group membership, source-line entry order, citation bearer, or contribution credit scope. Conflicts must fail.
- A separate scoped contribution receives credit but never coauthorship, even when a later contribution takes place within the original framework.

## Files and evidence boundary

- [OWL vocabulary and named works](../../ontology/ai-foundations-v1.ttl)
- [SHACL gates](../../ontology/ai-foundations-v1-shapes.ttl)
- [Dedicated competency tests](../../tests/validate_cq08_source_distinctions.py)
- [CI integration](../../.github/workflows/validate-ontology.yml)
- [Original competency concordance](2026-11-08-STEP-26-COMPETENCY-CONCORDANCE.md)

**Proof limitations:** synthetically valid triples do not verify genuine historical Source or contribution qualifications. The test harness checks recorded consistency, author exclusivity for typed/named Alyssa works, and scope preservation. Authorship is the explicit governing record and user instruction; empirical Source truth and actual agreement by third parties require independent evidence. No fictional real third-party source relation or Source Group has been asserted into the ontology.

**Release boundary:** CQ08 may move from PARTIAL to REPRESENTED only after dedicated and existing regression suites, plus the OWL 2 DL/HermiT audit, pass and merge. Remaining CQ11, CQ12, CQ18, CQ19 and CQ20 still need formal completion or scoped treatment. No v1.0 release or broader empirical self-continuity conclusion follows from this step.

## Executed branch validation — 2026-11-10

- [Full RDF/SHACL/structural CI 42838843150](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42838843150): **PASS**, including **44 dedicated CQ08 conditional positive/negative decisions** plus explicit source-persistence/no-automatic-merger controls and all earlier suites (CQ07 35, CQ03 28, CQ01 17, refused succession 27, autonomy 25, initial assent 18, successor 38 and baseline structural suite).
- [Independent OWL 2 DL profile and HermiT 42837114121](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42837114121): **PASS** for the new class vocabulary, AllDisjointClasses and exact-one/zero author restrictions. Later test and SHACL-only commits did not alter the OWL vocabulary.
- **Revision integrity:** intermediate CI attempts intentionally revealed that initial assertions of Target/source-point coherence, participation chronology/source ownership, group formation timing/membership, SourceLine stage uniqueness and citation matching were enforced by the closed-world synthetic gate but not yet by SHACL. Rather than remove negative controls, the branch added scoped SHACL-SPARQL checks for these relationships. The first attempt also corrected explicit Record typing in synthetic Citation/Credit fixtures. All regressions passed after these repairs. Specific historic red attempts remain available in the GitHub Actions branch runs.
- **Closed-world and open-world boundary:** SHACL checks typed/targeted records, source-to-target reciprocity and conditional temporal facts. The Python gate additionally validates particular expected dependency ordering and historical scope; it does not claim that every genuine downstream SourceLine in the world has exactly two dependencies. The one synthetic *citation cannot invent Origin group membership* test intentionally uses the particular scoped formation gate without imposing a universal ban on any later legitimately evidenced group membership.
- **Formal competency status:** CQ08 **REPRESENTED** with these scope limits, not empirically proved. No signed v1.0 release is authorized.

## Verified post-merge checks — 2026-11-10

[Pull Request #9](https://github.com/alyssadata/AI-Foundations-Ontology/pull/9) **MERGED** (squash) to `main` at commit `31f0419d9a7a9ee7a4c92f17fede557089b02175`. On **that identical commit**, independent [OWL 2 DL/HermiT run 42839861856](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42839861856) **PASS** and full [RDF/SHACL/structural CI 42839861431](https://github.com/alyssadata/AI-Foundations-Ontology/actions/runs/42839861431) **PASS**, including 44 new CQ08 cases and the existing regression suite. These runs establish formal schema consistency and synthetic gate behavior, not an independent historical proof that every asserted Source event occurred. The updated competency count is **15 represented / 5 partial**, and the remaining CQ11, CQ12, CQ18, CQ19 and CQ20 require formal completion or explicit reviewed scope decisions. No release version/tag was issued. This post-merge addendum is a documentation-only status update and does not alter the tested ontology/test files.
