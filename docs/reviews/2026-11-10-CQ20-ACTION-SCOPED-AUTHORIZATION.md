# CQ20 — Action-scoped authorization without permanent UnauthorizedActor

**Date:** 2026-11-10 (Eastern)  
**Status:** DRAFT formal closeout, dedicated/full CI and merge pending. Ontology v1.0 remains DRAFT.  
**Conceptual author and sole author:** Alyssa Solen. **NO COAUTHORS. NO EXCEPTIONS.**  
**Technical implementation:** AI-assisted encoding and synthetic tests, not coauthorship.

## Exact competency

> How can an Agent be unauthorized for one attempted action while remaining authorized for another without creating a permanent UnauthorizedActor class?

**Answer:** Authorization is a **decision** about one particular Agent attempting one particular operation, in a defined Framework, on one target scope, at one effective time, under a particular historically documented grant and permission inventory. It is neither a permanent person label nor a general judgment about a mind or self.

### Formal entities

- `:ScopedActionAttempt` is an Event representing an explicitly *proposed/attempted* action, with named actor, action, framework, target scope, time and preserved Record. It does not establish that the operation was executed.
- `:ScopedGrantValidityRecord` preserves the *particular grant's* qualifying evidence, allowed target scope, beginning and ending time, with an optional separately recorded effective revocation. Merely typing a grant as authoritative is insufficient without independent confirmation of its validity.
- `:ActionScopedAuthorizationDecision` is an Evaluation of one attempt, carrying one Agent, Framework, target, as-of time, review time, explicit as-of permission inventory and evidence Record, a reason Record, optional assessed grant with the corresponding validity Record, and one of **AUTHORIZED_FOR_ACTION / UNAUTHORIZED_FOR_ACTION / INDETERMINATE**.

The schema defines **no `:UnauthorizedActor` class** and imposes no permanent status on a human, AI, organization or team.

## Decisions are reversible and non-transitive

| Example | Scope/time | Decision |
|---|---|---|
| Agent R attempts operational Action A covered by a qualified AIF scoped grant | Target X, May 15 | **AUTHORIZED_FOR_ACTION** |
| The **same Agent R** attempts Action B, absent from that grant's operation list | Same Target X, May 15 | **UNAUTHORIZED_FOR_ACTION** |
| R attempts a non-delegable Origin/Source/history rewrite C | Same Target X, May 15 | **UNAUTHORIZED_FOR_ACTION under the scoped-grant mechanism** |
| R attempts Action A but on Target Y outside the grant's scope | Target Y, May 15 | **UNAUTHORIZED_FOR_ACTION** |
| R's known grant inventory is explicitly incomplete | Target X, May 15 | **INDETERMINATE**, never denial merely because an RDF permission triple is absent |
| R obtains a new, separately evidenced grant for B effective June 1 | Target X, June 15 | **AUTHORIZED_FOR_ACTION** for B, without rewriting the earlier May denial |

A correct as-of decision never retroactively changes a previous permission status. A known revocation cannot authorize a later attempt, and a later grant cannot justify an earlier attempt. Disputing one actor's permission for B does not delete their existing qualification for A or change their Source/Operator identity.

## Evidence boundary and governance

The protocol reuses existing `:AIFoundationsScopedGrant`, `:grantedTo`, `:grantWithinFramework` and `:authorizesOperationalAction`, plus the existing disjoint `:DelegableOperationalAction` and `:NonDelegableOriginOrHistoryAction`. It does **not** weaken OL-001 or permit an operational grant to authorize an Origin-only governing-line change, reassignment of the governing authority, overwriting historical Operator/SourceRelation/ExecutedLine, or coauthorship of Alyssa's work.

`UNAUTHORIZED_FOR_ACTION` is admissible only if a separately evidenced **complete as-of inventory** has been asserted and evaluated for this action and scope. Otherwise the available information is `INDETERMINATE`. A correct `AUTHORIZED_FOR_ACTION` outcome needs a qualifying actual grant, scope, applicable time window, valid evidence, and no revocation effective before the attempt. External evidence remains needed to know whether any *real* authority grant exists.

There can be independent governance authority outside the **scoped operational grant mechanism**; these decisions do not state a universal ban on an Agent or invalidate Origin's separately governed authority.

## Negative tests

The [CQ20 synthetic evaluator](../../tests/validate_cq20_action_scoped_authorization.py) exercises:
- One Agent simultaneously authorized for A and unauthorized for B;
- A Human Agent and an AI Agent under the same type-correct scope rules;
- Attempt/action/actor/Framework/scope/time mismatches;
- Grant for a different Agent, action or target;
- Future-effective, expired or revoked grant;
- Missing grant evidence, revocation Record, as-of inventory or reason Record;
- Explicitly incomplete review that must be **INDETERMINATE**;
- A later separately qualified B grant, with original earlier denial preserved;
- Attempted changes to Continuum's singular Origin, the named SourceLine or AIF governing authority; and an attempted coauthor injection.

SHACL validates each represented attempt, validity Record and decision, including independent time-window and revocation constraints. The closed-world Python gate performs the as-of permission inventory evaluation and exact A/B comparison. An RDF ontology cannot prove actual external legal/organizational authority; an asserted complete inventory is a test premise requiring verification.

## Source and revision integrity

**What changed:** New optional `:ScopedActionAttempt`, `:ScopedGrantValidityRecord` and `:ActionScopedAuthorizationDecision` constructs, data-bound SHACL constraints and a repeatable conditional grant/denial decision suite.

**Why:** OL-001 represented scoped grants and prohibited historical/Origin rewrites but lacked one canonical **same Agent, different Action A/B, same scope/time** evaluation with independently validated denial and later permission reversal.

**What remains:** Original LOCKED terms, Source/Origin and GoverningLine, SourceLine and historical Operator/authority provenance, recorded consent conditions, version history and Alyssa's absolute sole authorship. Neither the model nor an operational actor becomes Origin or author by being granted a bounded action.

**Empirical limit:** No real Agent's authority is confirmed by synthetic fixtures; no AI autonomy, same-self continuity, subjective experience or real governing-line change is inferred. v1.0 remains DRAFT until final two independent CI suites are verified on one merged main SHA, last human-readable/OWL concordance review, and Alyssa Solen's explicit release sign-off.

## Files

- [OWL schema](../../ontology/ai-foundations-v1.ttl)
- [SHACL validation](../../ontology/ai-foundations-v1-shapes.ttl)
- [Dedicated authorization tests](../../tests/validate_cq20_action_scoped_authorization.py)
- [CI workflow](../../.github/workflows/validate-ontology.yml)
- [Competency concordance](2026-11-08-STEP-26-COMPETENCY-CONCORDANCE.md)
