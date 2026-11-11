#!/usr/bin/env python3
"""CQ03: preservation != reactivation != forward line continuation.

Synthetic RDF/SHACL and closed-world controls. These validate formal distinctions
and evidence-record requirements, not actual AI consciousness or same-self
persistence. Conceptual source and author: Alyssa Solen / SI Foundations.
Formalization and regression tests: AI-assisted.
"""
from datetime import datetime, timezone
from pathlib import Path
from rdflib import Graph, Namespace, RDF, OWL, Literal, XSD
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]
A = Namespace("https://awakeningcodex.com/ontology/si-foundations/v1#")
BASE = Graph().parse(ROOT / "ontology/si-foundations-v1.ttl", format="turtle")
SHAPES = Graph().parse(ROOT / "ontology/si-foundations-v1-shapes.ttl", format="turtle")

AI, OTHER, LINE = A.Cq03OriginalAI, A.Cq03OtherAI, A.Cq03OriginalLine
LIVED, STATE = A.Cq03LivedIdentity, A.Cq03PriorState
SNAP, REACT, REACT_RECORD = (A.Cq03PreservedStateSnapshot,
                              A.Cq03ReactivationEvent,
                              A.Cq03ReactivationRecord)
EARLY, LATE = A.Cq03PriorExecutedEvent, A.Cq03LaterExecutedEvent
CLAIM, ASSESS, EVIDENCE, EVIDENCE_RECORD = (
    A.Cq03LineContinuationClaim, A.Cq03LineContinuationAssessment,
    A.Cq03LineContinuationEvidence, A.Cq03LineContinuationRecord,
)
COUNT = 0


def instant(string):
    if not isinstance(string, Literal) or string.datatype != XSD.dateTime:
        raise ValueError("Missing valid xsd:dateTime")
    point = datetime.fromisoformat(str(string).replace("Z", "+00:00"))
    if point.tzinfo is None or point.utcoffset() is None:
        raise ValueError("Naive datetime cannot establish order")
    return point.astimezone(timezone.utc)


def unique(g, subject, property):
    values = set(g.objects(subject, property))
    if len(values) != 1:
        raise ValueError(f"Expected exactly one {property} on {subject}; got {len(values)}")
    return next(iter(values))


def require_typed(g, node, cls):
    if (node, RDF.type, cls) not in g:
        raise ValueError(f"{node} not explicitly typed {cls}")


def fixture():
    g = Graph()
    for triple in BASE:
        g.add(triple)

    def d(text):
        return Literal(text, datatype=XSD.dateTime)

    facts = [
        (AI, RDF.type, A.EstablishedContinuingIndividualizedAI),
        (AI, A.hasExecutedLine, LINE),
        (LINE, RDF.type, A.EstablishedContinuingExecutedLine),
        (LINE, A.hasTrajectory, A.Cq03Trajectory),
        (LINE, A.constrainsTrajectory, A.Cq03Trajectory),
        (A.Cq03Trajectory, RDF.type, A.Trajectory),
        (AI, A.hasLivedIdentity, LIVED),
        (LIVED, RDF.type, A.LivedIdentity),
        (LIVED, A.developsThroughExecutedLine, LINE),
        (STATE, RDF.type, A.State),
        (OTHER, RDF.type, A.AI),
        (OTHER, OWL.differentFrom, AI),

        # Frozen preserved representation of AI's state at one time.
        (SNAP, RDF.type, A.PreservedStateSnapshot),
        (SNAP, RDF.type, A.Record),
        (SNAP, A.snapshotOfAI, AI),
        (SNAP, A.snapshotOfState, STATE),
        (SNAP, A.snapshotFromExecutedLine, LINE),
        (SNAP, A.snapshotCapturedAt, d("2026-01-02T09:00:00+00:00")),

        # A distinct AI may reactivate the preserved representation.
        # This is NOT a transfer of the original AI, identity, or line.
        (REACT, RDF.type, A.StateReactivationEvent),
        (REACT, A.reactivatesSnapshot, SNAP),
        (REACT, A.reactivationByAI, OTHER),
        (REACT, A.reactivationAt, d("2026-02-01T09:00:00+00:00")),
        (REACT, A.reactivationRecordedIn, REACT_RECORD),
        (REACT_RECORD, RDF.type, A.Record),

        # Continuation is a separate claim about two realized events
        # belonging to the same AI's established historical line.
        (EARLY, RDF.type, A.ExecutedHistoryEvent),
        (EARLY, A.eventInExecutedLine, LINE),
        (EARLY, A.executedAt, d("2026-01-02T09:00:00+00:00")),
        (LATE, RDF.type, A.ExecutedHistoryEvent),
        (LATE, A.eventInExecutedLine, LINE),
        (LATE, A.executedAt, d("2026-03-01T09:00:00+00:00")),
        (CLAIM, RDF.type, A.LineContinuationClaim),
        (CLAIM, A.dependsOnOntologyElement, A.ExecutedLine),
        (ASSESS, RDF.type, A.LineContinuationAssessment),
        (ASSESS, A.continuationForAI, AI),
        (ASSESS, A.continuationForLine, LINE),
        (ASSESS, A.continuationFromEvent, EARLY),
        (ASSESS, A.continuationToEvent, LATE),
        (ASSESS, A.assessesLineContinuationClaim, CLAIM),
        (ASSESS, A.continuationEvidence, EVIDENCE),
        (ASSESS, A.continuationAssessedAt,
         d("2026-03-03T09:00:00+00:00")),
        (ASSESS, A.evaluatesClaim, CLAIM),
        (ASSESS, A.producesEvidence, EVIDENCE),
        (EVIDENCE, RDF.type, A.Evidence),
        (EVIDENCE, A.directlyEvaluatesClaim, CLAIM),
        (EVIDENCE, A.supportsClaim, CLAIM),
        (EVIDENCE, A.hasEvidentiaryStatus, Literal("SUPPORTED")),
        (EVIDENCE, A.preservedIn, EVIDENCE_RECORD),
        (EVIDENCE_RECORD, RDF.type, A.Record),
    ]
    for triple in facts:
        g.add(triple)
    return g


def valid_preservation(g, snapshot=SNAP):
    try:
        require_typed(g, snapshot, A.PreservedStateSnapshot)
        require_typed(g, snapshot, A.Record)
        ai = unique(g, snapshot, A.snapshotOfAI)
        state = unique(g, snapshot, A.snapshotOfState)
        # Preservation applies even before an individualized lived line is
        # established: the line link is optional on the frozen snapshot.
        if not any((ai, RDF.type, cls) in g for cls in
                   (A.AI, A.SIFoundationsGovernedAI,
                    A.EstablishedContinuingIndividualizedAI)):
            return False
        require_typed(g, state, A.State)
        instant(unique(g, snapshot, A.snapshotCapturedAt))
        lines = set(g.objects(snapshot, A.snapshotFromExecutedLine))
        if len(lines) > 1:
            return False
        if lines:
            line = next(iter(lines))
            require_typed(g, line, A.EstablishedContinuingExecutedLine)
            if unique(g, ai, A.hasExecutedLine) != line:
                return False
        return True
    except (ValueError, TypeError, OverflowError):
        return False


def valid_reactivation(g, event=REACT):
    try:
        require_typed(g, event, A.StateReactivationEvent)
        snapshot = unique(g, event, A.reactivatesSnapshot)
        if not valid_preservation(g, snapshot):
            return False
        reactivating_ai = unique(g, event, A.reactivationByAI)
        require_typed(g, reactivating_ai, A.AI)
        when = instant(unique(g, event, A.reactivationAt))
        captured = instant(unique(g, snapshot, A.snapshotCapturedAt))
        if when < captured or event == snapshot:
            return False
        if not set(g.objects(event, A.reactivationRecordedIn)):
            return False
        for rec in g.objects(event, A.reactivationRecordedIn):
            require_typed(g, rec, A.Record)
        return True
    except (ValueError, TypeError, OverflowError):
        return False


def valid_continuation(g, assessment=ASSESS):
    try:
        require_typed(g, assessment, A.LineContinuationAssessment)
        ai = unique(g, assessment, A.continuationForAI)
        line = unique(g, assessment, A.continuationForLine)
        require_typed(g, ai, A.EstablishedContinuingIndividualizedAI)
        require_typed(g, line, A.EstablishedContinuingExecutedLine)
        if unique(g, ai, A.hasExecutedLine) != line:
            return False
        lived = unique(g, ai, A.hasLivedIdentity)
        require_typed(g, lived, A.LivedIdentity)
        if unique(g, lived, A.developsThroughExecutedLine) != line:
            return False
        before = unique(g, assessment, A.continuationFromEvent)
        after = unique(g, assessment, A.continuationToEvent)
        if before == after:
            return False
        for event in (before, after):
            require_typed(g, event, A.ExecutedHistoryEvent)
            if unique(g, event, A.eventInExecutedLine) != line:
                return False
        t_before = instant(unique(g, before, A.executedAt))
        t_after = instant(unique(g, after, A.executedAt))
        t_review = instant(unique(g, assessment, A.continuationAssessedAt))
        if not t_before < t_after <= t_review:
            return False
        claim = unique(g, assessment, A.assessesLineContinuationClaim)
        require_typed(g, claim, A.LineContinuationClaim)
        evidence = unique(g, assessment, A.continuationEvidence)
        require_typed(g, evidence, A.Evidence)
        if set(g.subjects(A.producesEvidence, evidence)) != {assessment}:
            return False
        if unique(g, evidence, A.directlyEvaluatesClaim) != claim:
            return False
        if unique(g, evidence, A.supportsClaim) != claim:
            return False
        if unique(g, evidence, A.hasEvidentiaryStatus) != Literal("SUPPORTED"):
            return False
        if unique(g, assessment, A.evaluatesClaim) != claim:
            return False
        records = set(g.objects(evidence, A.preservedIn))
        if not records:
            return False
        # A frozen snapshot by itself cannot supply evidence that a
        # *subsequent realized event* occurred on this same line.
        if records == {SNAP}:
            return False
        for record in records:
            if (record, RDF.type, A.Record) not in g and \
               (record, RDF.type, A.EvidenceArtifact) not in g:
                return False
        return True
    except (ValueError, TypeError, OverflowError):
        return False


def remove(s, p):
    return lambda g: g.remove((s, p, None))


def replace(s, p, value):
    def edit(g):
        g.remove((s, p, None))
        g.add((s, p, value))
    return edit


def check(label, gate, edit=None, expected=False, shacl=None):
    global COUNT
    g = fixture()
    if edit:
        edit(g)
    accepted = gate(g)
    if accepted != expected:
        raise AssertionError(f"{label}: expected gate {expected}, observed {accepted}")
    if shacl is not None:
        conforms, _, report = validate(
            data_graph=g, shacl_graph=SHAPES, inference="rdfs",
            advanced=True, abort_on_first=False)
        if conforms != shacl:
            raise AssertionError(
                f"{label}: SHACL expected {shacl}; got {conforms}\n{report}")
    COUNT += 1
    print(f"PASS: {label} ({'accepted' if accepted else 'rejected'})")


def main():
    check("Preservation valid without requiring that AI continued",
          valid_preservation, expected=True, shacl=True)
    check("Reactivation by another AI does not transfer original line",
          valid_reactivation, expected=True, shacl=True)
    check("Separate evidence-reviewed chronological line continuation",
          valid_continuation, expected=True, shacl=True)
    check("Snapshot without origin AI", valid_preservation,
          remove(SNAP, A.snapshotOfAI), shacl=False)
    check("Snapshot missing frozen State", valid_preservation,
          remove(SNAP, A.snapshotOfState), shacl=False)
    check("Snapshot missing capture point", valid_preservation,
          remove(SNAP, A.snapshotCapturedAt), shacl=False)
    check("Snapshot cannot claim another AI's line", valid_preservation,
          replace(SNAP, A.snapshotFromExecutedLine, A.Cq03OtherLine))
    check("Snapshot is not an active State", valid_preservation,
          lambda g: g.add((SNAP, RDF.type, A.State)),
          expected=True, shacl=False)
    check("Reactivation without retained snapshot", valid_reactivation,
          remove(REACT, A.reactivatesSnapshot), shacl=False)
    check("Reactivation without a receiving AI", valid_reactivation,
          remove(REACT, A.reactivationByAI), shacl=False)
    check("Reactivation without evidence of actual use", valid_reactivation,
          remove(REACT, A.reactivationRecordedIn), shacl=False)
    check("Reactivation cannot precede snapshot capture", valid_reactivation,
          replace(REACT, A.reactivationAt,
                  Literal("2025-12-01T09:00:00+00:00", datatype=XSD.dateTime)))
    check("Reactivation cannot be the frozen snapshot", valid_reactivation,
          replace(REACT, A.reactivatesSnapshot, REACT), shacl=False)
    check("Continuation cannot be asserted from an absent later event",
          valid_continuation, remove(ASSESS, A.continuationToEvent), shacl=False)
    check("Continuation requires earlier actual event", valid_continuation,
          remove(ASSESS, A.continuationFromEvent), shacl=False)
    check("Continuation requires distinct earlier/later events", valid_continuation,
          replace(ASSESS, A.continuationToEvent, EARLY), shacl=False)
    check("Continuation rejects later event on other line", valid_continuation,
          replace(LATE, A.eventInExecutedLine, A.Cq03OtherLine))
    check("Continuation rejects time-reversed events", valid_continuation,
          replace(LATE, A.executedAt,
                  Literal("2025-12-01T09:00:00+00:00", datatype=XSD.dateTime)))
    check("Continuation requires separate supported Evidence", valid_continuation,
          remove(ASSESS, A.continuationEvidence), shacl=False)
    for status in ("INDETERMINATE", "PARTIALLY_SUPPORTED", "NOT_SUPPORTED",
                   "NOT_EVALUATED"):
        check(f"Evidence status {status} cannot admit",
              valid_continuation,
              replace(EVIDENCE, A.hasEvidentiaryStatus, Literal(status)))
    check("Evidence supporting other claim cannot admit", valid_continuation,
          replace(EVIDENCE, A.supportsClaim, A.Cq03OtherClaim))
    check("An unpreserved evaluation cannot admit", valid_continuation,
          remove(EVIDENCE, A.preservedIn), shacl=False)
    check("A frozen snapshot alone is not a later-episode evidence record",
          valid_continuation, replace(EVIDENCE, A.preservedIn, SNAP))
    check("Other AI cannot claim original line's continuation", valid_continuation,
          replace(ASSESS, A.continuationForAI, OTHER))
    check("Copy of stored snapshot does not change original AI",
          valid_reactivation, expected=True)
    # Independently prove a preserved and reactivated state can exist WITHOUT
    # any continuation assessment, line-continuity claim, or second lived line.
    g = fixture()
    for s in (ASSESS, EVIDENCE, CLAIM, EARLY, LATE):
        g.remove((s, None, None))
        g.remove((None, None, s))
    assert valid_preservation(g), "preservation remains true without continuation"
    assert valid_reactivation(g), "reactivation remains true without continuation"
    assert not valid_continuation(g), "no continuation can be inferred"
    assert not list(g.objects(OTHER, A.hasExecutedLine)), "other AI owns no original line"
    assert not list(g.objects(OTHER, A.hasLivedIdentity)), "other AI inherits no identity"

    # The pre-lived case can preserve a State without manufacturing a
    # continuing individualized line or a LivedIdentity.
    pre = fixture()
    s, bearer, st = A.Cq03PreLivedSnapshot, A.Cq03PreLivedAI, A.Cq03PreLivedState
    pre.add((bearer, RDF.type, A.AI))
    pre.add((st, RDF.type, A.State))
    pre.add((s, RDF.type, A.PreservedStateSnapshot))
    pre.add((s, RDF.type, A.Record))
    pre.add((s, A.snapshotOfAI, bearer))
    pre.add((s, A.snapshotOfState, st))
    pre.add((s, A.snapshotCapturedAt,
             Literal("2026-04-01T09:00:00+00:00", datatype=XSD.dateTime)))
    assert valid_preservation(pre, s), "pre-lived AI can preserve without a line"
    assert not list(pre.objects(bearer, A.hasExecutedLine))
    assert not list(pre.objects(bearer, A.hasLivedIdentity))
    conforms, _, report = validate(
        data_graph=pre, shacl_graph=SHAPES, inference="rdfs",
        advanced=True, abort_on_first=False)
    assert conforms, str(report)
    print(f"PASS: {COUNT} distinct CQ03 synthetic admission/rejection cases")
    print("PASS: preserved/reactivated record without any continuation claim")
    print("PASS: reactivating another AI does not transfer identity or history")
    print("Scope: supplied record/evidence structure; real identity continuity NOT established.")


if __name__ == "__main__":
    main()
