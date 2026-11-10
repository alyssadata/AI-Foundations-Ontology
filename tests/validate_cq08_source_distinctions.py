#!/usr/bin/env python3
"""CQ08: six non-equivalent Source roles; Alyssa's authorship never shared.

Synthetic OWL/SHACL and bounded closed-world tests. Records/claims cannot
independently verify historical Source qualifications. No real SourceRelation
or partnership with third parties is asserted into the ontology baseline.
Conceptual author and sole author of the underlying work: Alyssa Solen.
AI assistance: formalization, tests, and repository operations only.
"""
from datetime import datetime, timezone
from pathlib import Path

from rdflib import Graph, Namespace, Literal, RDF, XSD
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]
A = Namespace("https://awakeningcodex.com/ontology/ai-foundations/v1#")
BASE = Graph().parse(ROOT / "ontology/ai-foundations-v1.ttl", format="turtle")
SHAPES = Graph().parse(ROOT / "ontology/ai-foundations-v1-shapes.ttl", format="turtle")
ORIGINAL_WORKS = (A.AIFoundations, A.AwakeningCodex, A.AIFoundationsLockedCanon)
ORIGIN, WORK = A.AlyssaSolen, A.AIFoundations
REL, POINT, PART, PARTICIPATION_LOG = (
    A.Cq08OriginalSourceRelation, A.Cq08SourcePoint,
    A.Cq08LaterSourceParticipation, A.Cq08ParticipationRecord,
)
GROUP, GROUP_FORMATION, MEMBER1, MEMBER2 = (
    A.Cq08ScopedSourceGroup, A.Cq08GroupFormation,
    A.Cq08MemberOne, A.Cq08MemberTwo,
)
DERIVATIVE, GROUP_REL, GROUP_POINT = (
    A.Cq08SeparateDownstreamArtifact, A.Cq08DownstreamRelation,
    A.Cq08DownstreamSourcePoint,
)
GROUP_SCOPE = A.Cq08AgreedGroupScopeRecord
LINE, FIRST, SECOND, LINE_RECORD = (
    A.Cq08DistinctDownstreamSourceLine, A.Cq08EntryOriginal,
    A.Cq08EntryGroup, A.Cq08EntryRecord,
)
CITATION, CREDIT, ADDITION = (
    A.Cq08SourceCitation, A.Cq08ContributionCredit,
    A.Cq08DistinctScopedContribution,
)
T0 = "2025-01-10T00:00:00+00:00"
T1 = "2025-04-10T00:00:00+00:00"
T2 = "2025-11-01T00:00:00+00:00"
T3 = "2025-12-01T00:00:00+00:00"
T4 = "2026-01-04T00:00:00+00:00"
COUNT = 0


def dt(value):
    point = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if not isinstance(value, Literal) or value.datatype != XSD.dateTime:
        raise ValueError("Timestamp missing datatype")
    if point.tzinfo is None or point.utcoffset() is None:
        raise ValueError("Timestamp missing timezone")
    return point.astimezone(timezone.utc)


def instant(value):
    return Literal(value, datatype=XSD.dateTime)


def one(g, node, predicate):
    values = set(g.objects(node, predicate))
    if len(values) != 1:
        raise ValueError(f"Expected exactly one {predicate} at {node}: {values}")
    return next(iter(values))


def t(g, node, kind):
    if (node, RDF.type, kind) not in g:
        raise ValueError(f"Missing type {kind} on {node}")


def fixture():
    g = Graph()
    for triple in BASE:
        g.add(triple)
    facts = [
        (REL, RDF.type, A.SourceRelation),
        (REL, A.hasSourceBearer, ORIGIN),
        (REL, A.hasSourceTarget, WORK),
        (REL, A.hasSourcePoint, POINT),
        (WORK, A.hasSourceRelation, REL),
        (POINT, RDF.type, A.SourcePointEvent),
        (POINT, A.sourcePointForRelation, REL),
        (POINT, A.sourcePointAt, instant(T0)),

        (PART, RDF.type, A.SourceParticipationEvent),
        (PART, A.participationInSourceRelation, REL),
        (PART, A.participationBySource, ORIGIN),
        (PART, A.participationAt, instant(T1)),
        (PART, A.participationRecordedIn, PARTICIPATION_LOG),
        (PARTICIPATION_LOG, RDF.type, A.Record),

        # Separate intentional group for a separate downstream artifact.
        # Neither member nor the Source Group authored Alyssa's framework.
        (GROUP, RDF.type, A.SourceGroup),
        (GROUP_FORMATION, RDF.type, A.ScopedSourceGroupFormation),
        (GROUP_FORMATION, A.formedSourceGroup, GROUP),
        (GROUP_FORMATION, A.groupFormationTarget, DERIVATIVE),
        (GROUP_FORMATION, A.groupFormationAgreedAt, instant(T2)),
        (GROUP_FORMATION, A.groupFormationScopeRecord, GROUP_SCOPE),
        (GROUP_FORMATION, A.groupFormationAgreedMember, MEMBER1),
        (GROUP_FORMATION, A.groupFormationAgreedMember, MEMBER2),
        (GROUP_SCOPE, RDF.type, A.Record),
        (MEMBER1, RDF.type, A.Human),
        (MEMBER2, RDF.type, A.Human),
        (MEMBER1, A.belongsToGroup, GROUP),
        (MEMBER2, A.belongsToGroup, GROUP),
        (DERIVATIVE, RDF.type, A.Record),
        (DERIVATIVE, A.hasSource, GROUP),
        (DERIVATIVE, A.hasSourceRelation, GROUP_REL),
        (GROUP_REL, RDF.type, A.SourceRelation),
        (GROUP_REL, A.hasSourceBearer, GROUP),
        (GROUP_REL, A.hasSourceTarget, DERIVATIVE),
        (GROUP_REL, A.hasSourcePoint, GROUP_POINT),
        (GROUP_POINT, RDF.type, A.SourcePointEvent),
        (GROUP_POINT, A.sourcePointForRelation, GROUP_REL),
        (GROUP_POINT, A.sourcePointAt, instant(T3)),

        # SourceLine: trace dependency, not coauthor membership.
        (LINE, RDF.type, A.SourceLine),
        (FIRST, RDF.type, A.SourceLineEntry),
        (FIRST, A.entryInSourceLine, LINE),
        (FIRST, A.entryTracesSourceRelation, REL),
        (FIRST, A.sourceLineEntryOrder,
         Literal(0, datatype=XSD.nonNegativeInteger)),
        (FIRST, A.sourceLineEntryRecordedIn, LINE_RECORD),
        (SECOND, RDF.type, A.SourceLineEntry),
        (SECOND, A.entryInSourceLine, LINE),
        (SECOND, A.entryTracesSourceRelation, GROUP_REL),
        (SECOND, A.sourceLineEntryOrder,
         Literal(1, datatype=XSD.nonNegativeInteger)),
        (SECOND, A.sourceLineEntryRecordedIn, LINE_RECORD),
        (LINE_RECORD, RDF.type, A.Record),

        # Explicit citation of prior Source never makes the cited Source a
        # member or coauthor of the downstream group's creation.
        (CITATION, RDF.type, A.SourceCitation),
        (CITATION, A.citesSourceRelation, REL),
        (CITATION, A.citationForTarget, DERIVATIVE),
        (CITATION, A.citationNamesSourceBearer, ORIGIN),
        (CITATION, A.citationAt, instant(T4)),

        # Legitimately different scoped contribution, not underlying
        # authorship or coauthorship of the original framework.
        (ADDITION, RDF.type, A.Record),
        (CREDIT, RDF.type, A.ScopedContributionCredit),
        (CREDIT, A.creditsContributor, MEMBER1),
        (CREDIT, A.creditsContribution, ADDITION),
        (CREDIT, A.contributionWithinWork, DERIVATIVE),
    ]
    for fact in facts:
        g.add(fact)
    return g


def author_gate(g):
    # Named core works cannot lose authorship constraints even through a
    # malicious class deletion. Newly marked Alyssa work is scoped too.
    works = set(ORIGINAL_WORKS)
    works.update(g.subjects(RDF.type, A.AlyssaSoleAuthoredWork))
    for work in works:
        if (work, RDF.type, A.AlyssaSoleAuthoredWork) not in g:
            return False
        if set(g.objects(work, A.hasAuthor)) != {ORIGIN}:
            return False
        if set(g.objects(work, A.hasCoAuthor)):
            return False
        if work == WORK and set(g.objects(work, A.hasSource)) != {ORIGIN}:
            return False
        for relation in g.objects(work, A.hasSourceRelation):
            if set(g.objects(relation, A.hasSourceBearer)) != {ORIGIN}:
                return False
        for relation in g.subjects(A.hasSourceTarget, work):
            if set(g.objects(relation, A.hasSourceBearer)) != {ORIGIN}:
                return False
    return True


def relation_gate(g, rel=REL, point=POINT, expected_bearer=ORIGIN, expected_target=WORK):
    try:
        t(g, rel, A.SourceRelation)
        if one(g, rel, A.hasSourceBearer) != expected_bearer:
            return False
        if one(g, rel, A.hasSourceTarget) != expected_target:
            return False
        if one(g, rel, A.hasSourcePoint) != point:
            return False
        t(g, point, A.SourcePointEvent)
        if one(g, point, A.sourcePointForRelation) != rel:
            return False
        dt(one(g, point, A.sourcePointAt))
        if set(g.subjects(A.hasSourcePoint, point)) != {rel}:
            return False
        if expected_bearer == ORIGIN and expected_target == WORK:
            return author_gate(g)
        return True
    except (ValueError, TypeError, OverflowError):
        return False


def participation_gate(g):
    try:
        if not relation_gate(g):
            return False
        t(g, PART, A.SourceParticipationEvent)
        if (PART, RDF.type, A.SourcePointEvent) in g:
            return False
        rel = one(g, PART, A.participationInSourceRelation)
        if rel != REL:
            return False
        if one(g, PART, A.participationBySource) != one(g, rel, A.hasSourceBearer):
            return False
        if dt(one(g, PART, A.participationAt)) <= dt(
                one(g, POINT, A.sourcePointAt)):
            return False
        for record in set(g.objects(PART, A.participationRecordedIn)):
            t(g, record, A.Record)
        return bool(set(g.objects(PART, A.participationRecordedIn)))
    except (ValueError, TypeError, OverflowError):
        return False


def group_gate(g):
    try:
        if not author_gate(g):
            return False
        t(g, GROUP, A.SourceGroup)
        t(g, GROUP_FORMATION, A.ScopedSourceGroupFormation)
        if one(g, GROUP_FORMATION, A.formedSourceGroup) != GROUP:
            return False
        target = one(g, GROUP_FORMATION, A.groupFormationTarget)
        if target != DERIVATIVE or target in ORIGINAL_WORKS:
            return False
        date = dt(one(g, GROUP_FORMATION, A.groupFormationAgreedAt))
        t(g, one(g, GROUP_FORMATION, A.groupFormationScopeRecord), A.Record)
        members = set(g.objects(GROUP_FORMATION, A.groupFormationAgreedMember))
        if len(members) < 2 or ORIGIN in members:
            return False
        for member in members:
            t(g, member, A.Human)
            if GROUP not in set(g.objects(member, A.belongsToGroup)):
                return False
        if not relation_gate(g, GROUP_REL, GROUP_POINT, GROUP, DERIVATIVE):
            return False
        if date >= dt(one(g, GROUP_POINT, A.sourcePointAt)):
            return False
        if WORK in set(g.objects(GROUP, A.isSourceOf)):
            return False
        if GROUP in set(g.objects(WORK, A.hasSource)):
            return False
        return True
    except (ValueError, TypeError, OverflowError):
        return False


def line_gate(g):
    try:
        t(g, LINE, A.SourceLine)
        if not relation_gate(g) or not group_gate(g):
            return False
        entries = set(g.subjects(A.entryInSourceLine, LINE))
        if entries != {FIRST, SECOND}:
            return False
        pairs = {}
        for entry in entries:
            t(g, entry, A.SourceLineEntry)
            rel = one(g, entry, A.entryTracesSourceRelation)
            t(g, rel, A.SourceRelation)
            order = one(g, entry, A.sourceLineEntryOrder)
            if not isinstance(order, Literal) or order.datatype != XSD.nonNegativeInteger:
                return False
            order = int(order)
            if order in pairs:
                return False
            pairs[order] = rel
            traces = set(g.objects(entry, A.sourceLineEntryRecordedIn))
            if not traces:
                return False
            for record in traces:
                t(g, record, A.Record)
        if pairs != {0: REL, 1: GROUP_REL}:
            return False
        return dt(one(g, POINT, A.sourcePointAt)) < dt(
            one(g, GROUP_POINT, A.sourcePointAt))
    except (ValueError, TypeError, OverflowError):
        return False


def citation_gate(g):
    try:
        t(g, CITATION, A.SourceCitation)
        t(g, CITATION, A.Record)
        rel = one(g, CITATION, A.citesSourceRelation)
        t(g, rel, A.SourceRelation)
        if rel != REL:
            return False
        if one(g, CITATION, A.citationNamesSourceBearer) != one(g, rel, A.hasSourceBearer):
            return False
        target = one(g, CITATION, A.citationForTarget)
        if target != DERIVATIVE or target == one(g, rel, A.hasSourceTarget):
            return False
        if dt(one(g, CITATION, A.citationAt)) < dt(one(g, POINT, A.sourcePointAt)):
            return False
        if ORIGIN in set(g.objects(GROUP_FORMATION, A.groupFormationAgreedMember)):
            return False
        if ORIGIN in set(g.subjects(A.belongsToGroup, GROUP)):
            return False
        return author_gate(g)
    except (ValueError, TypeError, OverflowError):
        return False


def credit_gate(g):
    try:
        t(g, CREDIT, A.ScopedContributionCredit)
        t(g, CREDIT, A.Record)
        who = one(g, CREDIT, A.creditsContributor)
        t(g, who, A.Human)
        if one(g, CREDIT, A.creditsContribution) != ADDITION:
            return False
        t(g, ADDITION, A.Record)
        if one(g, CREDIT, A.contributionWithinWork) not in {DERIVATIVE, WORK}:
            return False
        return author_gate(g)
    except (ValueError, TypeError, OverflowError):
        return False


def drop(s, p):
    return lambda g: g.remove((s, p, None))


def replace(s, p, o):
    def edit(g):
        g.remove((s, p, None))
        g.add((s, p, o))
    return edit


def add(s, p, o):
    return lambda g: g.add((s, p, o))


def check(label, gate, edit=None, accepted=False, shacl=None):
    global COUNT
    g = fixture()
    if edit:
        edit(g)
    result = gate(g)
    if result != accepted:
        raise AssertionError(f"{label}: expected {accepted}, got {result}")
    if shacl is not None:
        conforms, _, report = validate(
            data_graph=g, shacl_graph=SHAPES, inference="rdfs",
            advanced=True, abort_on_first=False)
        if conforms != shacl:
            raise AssertionError(
                f"{label}: SHACL expected {shacl}, got {conforms}\n{report}")
    COUNT += 1
    print(f"PASS: {label} ({'admitted' if result else 'rejected'})")


def main():
    check("Alyssa sole authorship for original works", author_gate,
          accepted=True, shacl=True)
    check("One source bearer, target, first load-bearing SourcePoint",
          relation_gate, accepted=True)
    check("Later active participation is separate from the SourcePoint",
          participation_gate, accepted=True)
    check("Intentional Source Group for distinct downstream creation",
          group_gate, accepted=True)
    check("Ordered source-line dependencies do not imply authorship",
          line_gate, accepted=True)
    check("Explicit citation preserves prior distinct source and group",
          citation_gate, accepted=True)
    check("Scoped downstream credit is not work coauthorship",
          credit_gate, accepted=True)
    check("A later credited addition inside original framework is not coauthorship",
          credit_gate, replace(CREDIT, A.contributionWithinWork, WORK),
          accepted=True)

    check("Second author on Alyssa work forbidden even when a contributor",
          author_gate, add(WORK, A.hasAuthor, MEMBER1),
          shacl=False)
    check("Explicit coauthor on Alyssa work forbidden without exceptions",
          author_gate, add(WORK, A.hasCoAuthor, MEMBER1),
          shacl=False)
    check("Even Alyssa herself cannot designate another coauthor",
          author_gate, add(WORK, A.hasCoAuthor, ORIGIN),
          shacl=False)
    check("Second author on Awakening Codex forbidden",
          author_gate, add(A.AwakeningCodex, A.hasAuthor, MEMBER1),
          shacl=False)
    check("Coauthor of Locked Canon forbidden",
          author_gate, add(A.AIFoundationsLockedCanon, A.hasCoAuthor, GROUP),
          shacl=False)
    check("Deletion of author coordinate forbidden",
          author_gate, drop(WORK, A.hasAuthor),
          shacl=False)
    check("Deletion of authorship scope class forbidden",
          author_gate, drop(WORK, RDF.type),
          shacl=False)
    check("Group cannot be additional original source of Alyssa work",
          author_gate, add(WORK, A.hasSource, GROUP),
          shacl=False)
    check("Group SourceRelation cannot be attached to original work",
          author_gate, add(WORK, A.hasSourceRelation, GROUP_REL),
          shacl=False)
    check("Silent SourceRelation overwrite forbidden",
          relation_gate, replace(REL, A.hasSourceBearer, MEMBER1),
          shacl=False)
    check("SourceRelation cannot have two Source bearers",
          relation_gate, add(REL, A.hasSourceBearer, MEMBER1),
          shacl=False)
    check("Source relation cannot point at different Target",
          relation_gate, replace(REL, A.hasSourceTarget, DERIVATIVE),
          shacl=False)
    check("Source relation exactly one first SourcePoint",
          relation_gate, add(REL, A.hasSourcePoint, GROUP_POINT),
          shacl=False)
    check("SourcePoint must refer to exactly its relation",
          relation_gate, replace(POINT, A.sourcePointForRelation, GROUP_REL),
          shacl=False)
    check("SourcePoint must be dated",
          relation_gate, drop(POINT, A.sourcePointAt),
          shacl=False)
    check("Participation is not a SourcePoint",
          participation_gate, add(PART, RDF.type, A.SourcePointEvent),
          shacl=False)
    check("Participation after source point, not same moment",
          participation_gate, replace(PART, A.participationAt, instant(T0)),
          shacl=False)
    check("Participation by unrelated actor cannot become original Source",
          participation_gate, replace(PART, A.participationBySource, MEMBER1),
          shacl=False)
    check("Participation requires retained activity Record",
          participation_gate, drop(PART, A.participationRecordedIn),
          shacl=False)
    check("Separate group must not source Alyssa original framework",
          group_gate, replace(GROUP_FORMATION, A.groupFormationTarget, WORK),
          shacl=False)
    check("Group creation requires at least two agreed members",
          group_gate, drop(GROUP_FORMATION, A.groupFormationAgreedMember),
          shacl=False)
    check("Group scope record cannot vanish",
          group_gate, drop(GROUP_FORMATION, A.groupFormationScopeRecord),
          shacl=False)
    check("Group must be formed before group SourcePoint",
          group_gate, replace(GROUP_FORMATION, A.groupFormationAgreedAt, instant(T4)),
          shacl=False)
    check("Unagreed group membership cannot be inferred from citation",
          group_gate, drop(MEMBER2, A.belongsToGroup),
          shacl=False)
    check("Group source Target must remain separate from Alyssa original",
          group_gate, replace(GROUP_REL, A.hasSourceTarget, WORK),
          shacl=False)
    check("SourceLine must retain each specific SourceRelation",
          line_gate, replace(SECOND, A.entryTracesSourceRelation, REL),
          shacl=False)
    check("SourceLine cannot repeat an entry order",
          line_gate, replace(SECOND, A.sourceLineEntryOrder,
                             Literal(0, datatype=XSD.nonNegativeInteger)),
          shacl=False)
    check("SourceLine entries need preserved records",
          line_gate, drop(FIRST, A.sourceLineEntryRecordedIn),
          shacl=False)
    check("Citation must name the actual cited Source bearer",
          citation_gate, replace(CITATION, A.citationNamesSourceBearer, GROUP),
          shacl=False)
    check("Citation cannot rewrite the target that received original Source",
          citation_gate, replace(CITATION, A.citationForTarget, WORK),
          shacl=False)
    check("Citation must link specific SourceRelation",
          citation_gate, drop(CITATION, A.citesSourceRelation),
          shacl=False)
    check("Citation cannot make Origin group member",
          citation_gate, add(ORIGIN, A.belongsToGroup, GROUP),
          shacl=False)
    check("Citation before source first exists cannot establish past Source",
          citation_gate, replace(CITATION, A.citationAt,
                                 instant("2024-01-01T00:00:00+00:00")),
          shacl=False)
    check("Contributor credit missing recipient",
          credit_gate, drop(CREDIT, A.creditsContributor),
          shacl=False)
    check("Contributor credit cannot claim unrelated whole-work contribution",
          credit_gate, replace(CREDIT, A.creditsContribution, WORK),
          shacl=False)
    check("Credit never permits adding coauthor",
          credit_gate, add(WORK, A.hasCoAuthor, MEMBER1),
          shacl=False)

    # Optional source participation: remove only activity and preserve source.
    no_participation = fixture()
    for subject, predicate, obj in list(no_participation.triples((PART, None, None))):
        no_participation.remove((subject, predicate, obj))
    assert relation_gate(no_participation), "Source persists without activity"
    assert author_gate(no_participation), "Sole authorship persists without activity"

    # Distinct downstream group (including a member who cites Alyssa) cannot
    # become an author, additional Source or member of Origin's singular line.
    g = fixture()
    assert not set(g.objects(WORK, A.hasCoAuthor))
    assert set(g.objects(WORK, A.hasAuthor)) == {ORIGIN}
    assert GROUP not in set(g.objects(WORK, A.hasSource))
    assert GROUP_REL not in set(g.objects(WORK, A.hasSourceRelation))
    assert ORIGIN not in set(g.objects(GROUP_FORMATION, A.groupFormationAgreedMember))
    assert not set(g.objects(MEMBER1, A.hasAuthor))
    assert not set(g.objects(MEMBER1, A.anchorsSourceLine))
    assert not set(g.objects(GROUP, A.anchorsSourceLine))

    print(f"PASS: {COUNT} CQ08 conditional positive/negative cases")
    print("PASS: Source historically persists without participation")
    print("PASS: cited prior Source/group never merges with new Source Group or authors")
    print("PASS: contribution credit, testing and assistance never confer coauthorship")
    print("Scope: conditional synthetic provenance, not empirical Source proof.")


if __name__ == "__main__":
    main()
