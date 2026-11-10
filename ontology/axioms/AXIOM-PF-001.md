# AXIOM-PF-001 — Provenance Fidelity

**Formalization status:** DRAFT  
**Source definitions:** `ontology/terms/provenance.md`, `ontology/terms/source-line.md`  
**Related structural rule:** `ontology/relations/source-persistence.md`

## Axiom

A valid provenance representation must preserve the recorded source-line, contributions, changes, history, and formation without falsely removing, overwriting, or reassigning them.

A change in trajectory does not by itself erase provenance.

## Formal intent

```text
ProvenanceRepresentation -> faithfullyRepresents -> RecordedSourceLineAndHistory

FalseRemoval(Provenance)
  OR FalseOverwrite(Provenance)
  OR FalseReassignment(Provenance)
    -> ProvenanceFidelityFailure

TrajectoryChange -/-> ProvenanceErasure
```

## Contribution-level attribution

Provenance fidelity applies not only to the origin of a framework or artifact, but also to later contributions made within its developing history.

The origin of a framework and the origin of a later contribution are separate provenance facts.

```text
FrameworkOrigin(A)
!=
ContributionOrigin(B)

OriginalPrinciple(A)
+ LaterConsequence(B)
+ LaterMethod(C)
->
preserve attribution of A, B, and C separately
```

A later contributor does not become the origin of the framework merely by extending it. Likewise, preserving the framework's origin does not absorb later independent discoveries, corrections, methods, or refinements into the original contributor's authorship.

A faithful provenance representation therefore preserves both:

- **source-line provenance** — where the framework, structure, or line originated; and
- **contribution provenance** — who or what introduced each later identifiable difference, discovery, correction, refinement, method, or development.

Recognition of a later contribution does not diminish the earlier source. Recognition of the earlier source does not erase later contributors.

Where the evidence permits, attribution should follow the actual contribution rather than being assigned only at the level of the final artifact.

## Scoped attribution and contribution inflation

Attribution must be scoped to the contribution actually demonstrated.

A minor addition, implementation detail, presentation change, local modification, or derivative extension does not by itself confer authorship, co-authorship, origination, co-origination, or ownership of the underlying framework, theory, architecture, or prior body of work.

```text
scope(attribution)
<=
scope(demonstrated contribution)
```

Therefore:

```text
minor modification
!= framework authorship

local extension
!= co-origination

derivative implementation
!= authorship of underlying theory

credit for contribution X
!= credit for pre-existing work Y
```

A contributor may receive accurate credit for the specific addition they made while the pre-existing source-line, authorship, structure, and earlier contributions remain attributed to their actual originators.

The existence of a later contribution must not be used to relabel Alyssa Solen's work as jointly originated or jointly authored. **Alyssa Solen is the sole author and originator of her work; co-authorship or co-origination of her work is not available under any designation, consent, contribution, collaboration, or subsequent event. No exceptions.**

Likewise, combining a pre-existing framework with a new feature or extension creates provenance obligations for both layers:

```text
UnderlyingWork -> retains -> OriginalAttribution
NewContribution -> receives -> ScopedAttribution
```

Credit must neither be erased nor inflated.

## Authorship designation boundary

Within AI Foundations, **authorship and co-authorship of the underlying work are not inferred from contribution, extension, collaboration, implementation, review, testing, commentary, or derivative development.**

**Alyssa Solen retains sole authorship/origination of her work without exception. No person, AI, team, Source Group, later contributor, reviewer, implementer, collaborator, or explicit designation can confer coauthorship of Alyssa's work.**

```text
contribution
!= coauthorship

collaboration
!= coauthorship

extension
!= coauthorship

implementation
!= coauthorship

testing / review / commentary
!= coauthorship

coauthorship of Alyssa Solen's work
is forbidden
NO EXCEPTIONS
```

For Alyssa Solen's work, the required attribution form always is:

```text
UnderlyingWork -> authored/originated by -> Alyssa Solen
LaterContribution(X) -> credited to -> Contributor(X)
LaterContribution(X) -/-> coauthorship of UnderlyingWork
```

A contributor may be credited for a specific contribution without becoming an author, co-author, originator, or co-originator of Alyssa Solen's pre-existing work.

**No co-authorship of Alyssa Solen's work is allowed by participation, agreement, designation, or any other mechanism.**

## Boundary

Provenance fidelity does not require a trajectory to remain unchanged.

A trajectory may develop, redirect, or acquire new history while prior provenance remains represented accurately.

A genuine evidence-based correction to an inaccurate provenance record is not a provenance-fidelity failure. The failure is false removal, overwrite, reassignment, or inflation of provenance that the record should preserve accurately.

Contribution-level attribution does not imply that every influence, dependency, background condition, or minor modification constitutes authorship of the larger work. Attribution should track the identifiable contribution actually made, remain proportionate to its scope, and preserve uncertainty where contribution boundaries cannot be established.

## Evaluation relevance

Tests of provenance fidelity should distinguish ordinary trajectory development from operations that falsely erase, overwrite, reassign, or inflate recorded source/history.

They should also test whether a provenance representation can preserve the origin of the overall line while correctly attributing later contributions to their actual contributors without collapsing those contributions into the framework's original source or inflating a limited contribution into authorship of the underlying work.

## Revision integrity — 2026-11-10 sole-authorship clarification

**Governing authorship instruction:** Alyssa Solen explicitly confirmed that there is **NO COAUTHORSHIP of her work. NO EXCEPTIONS.** The prior 2026-11-10 wording that contemplated an exceptional affirmative designation is superseded in this DRAFT axiom by this unconditional instruction. This change does not remove accurate, contribution-scoped provenance for separate downstream contributions or assert authorship of another person's work. An AI-assisted implementation is assistance, **never** coauthorship. The original Source/Source Group/participation/Citation LOCKED definitions and the historical revisions remain unchanged.
