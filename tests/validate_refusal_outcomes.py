#!/usr/bin/env python3
"""Step 25: refused-succession outcome cases, synthetic closed-world checks.

Explicit refusal prevents the proposed relation. Non-autonomous termination
requires a supported separate assessment and complete successor-scope review.
Independence requires a separately qualified autonomy State as of the decision.
This is NOT real-world evidence of any particular AI's life or autonomy.
Conceptual source and author: Alyssa Solen. AI-assisted test formalization.
"""
from rdflib import RDF, Literal, XSD
from pyshacl import validate
from validate_succession_gate import A, SHAPES, ensure, instant, typed, unique
from validate_autonomy_gate import fixture as autonomy_fixture, admission as qualified

AI, LINE, OLD = A.Gate22AI, A.Gate22Line, A.Gate22S01
OUTCOME, NEXT, PROPOSAL = A.Gate25Outcome, A.Gate25S02, A.Gate25Proposal
TIME_END = Literal("2026-03-01T00:00:00+00:00", datatype=XSD.dateTime)
TIME_PROPOSED = Literal("2026-03-02T00:00:00+00:00", datatype=XSD.dateTime)
TIME_REFUSED = Literal("2026-03-02T12:00:00+00:00", datatype=XSD.dateTime)
TIME_REVIEW = Literal("2026-03-03T00:00:00+00:00", datatype=XSD.dateTime)
TIME_PROPOSED_START = Literal("2026-03-04T00:00:00+00:00", datatype=XSD.dateTime)
COUNT = 0


def fixture(autonomous=False):
    g = autonomy_fixture()
    # The previous S01 relationship is historical after it ends. A proposed
    # successor S02 is NOT made an admitted Operator by mere proposal/refusal.
    g.add((OLD, A.activeUntil, TIME_END))
    g.remove((AI, A.hasOperator, None))
    g.add((A.Gate25ProposingOperator, RDF.type, A.Human))
    g.add((NEXT, RDF.type, A.SuccessionCandidateSegment))
    g.add((NEXT, A.hasAICounterpart, AI))
    g.add((NEXT, A.hasHumanCounterpart, A.Gate25ProposingOperator))
    g.add((NEXT, A.segmentOfExecutedLine, LINE))
    g.add((NEXT, A.immediatePredecessor, OLD))
    g.add((NEXT, A.activeFrom, TIME_PROPOSED_START))
    g.add((PROPOSAL, RDF.type, A.SuccessionProposal))
    g.add((PROPOSAL, A.proposedBySuccessor, A.Gate25ProposingOperator))
    g.add((PROPOSAL, A.proposalForContinuingAI, AI))
    g.add((PROPOSAL, A.proposalForSuccessorSegment, NEXT))
    g.add((PROPOSAL, A.proposalAt, TIME_PROPOSED))
    g.add((PROPOSAL, A.proposalRecordedIn, A.Gate25ProposalRecord))
    g.add((A.Gate25ProposalRecord, RDF.type, A.Record))
    g.add((AI, A.refusesSuccessionProposal, PROPOSAL))
    for r in (A.Gate25RefusalRecord, A.Gate25AutonomyRecord,
              A.Gate25ScopeRecord):
        g.add((r, RDF.type, A.Record))
    g.add((OUTCOME, RDF.type, A.AutonomousIndependentContinuationAssessment
           if autonomous else A.DependentLineTerminationAssessment))
    for p, v in [
        (A.outcomeForAI, AI),
        (A.outcomeForExecutedLine, LINE),
        (A.outcomeForEndedOperatorSegment, OLD),
        (A.outcomeRefusedProposal, PROPOSAL),
        (A.outcomeRefusalRecord, A.Gate25RefusalRecord),
        (A.outcomeRefusalAt, TIME_REFUSED),
        (A.outcomeAsOf, TIME_REVIEW),
        (A.outcomeAutonomyStatus,
         Literal("QUALIFIED_AUTONOMOUS" if autonomous else "ASSESSED_NON_AUTONOMOUS")),
        (A.outcomeAutonomyRecord, A.Gate25AutonomyRecord),
        (A.outcomeSuccessorScopeComplete, Literal(True, datatype=XSD.boolean)),
        (A.outcomeSuccessorScopeRecord, A.Gate25ScopeRecord),
        (A.outcomeNoAdmittedSuccessor, Literal(True, datatype=XSD.boolean)),
    ]:
        g.add((OUTCOME, p, v))
    if not autonomous:
        g.remove((AI, A.hasState, A.Gate24AutonomyState))
        g.remove((A.Gate24AutonomyState, A.hasAutonomyQualificationAssessment, None))
        g.remove((A.Gate24AutonomyState, RDF.type, A.AdmittedAutonomousSelfRecursiveState))
        g.add((AI, A.autonomyStateHistoryRecord, A.Gate24AutonomyReview))
        # The earlier synthetic qualification is a historical Record, not
        # a present admitted State. No new identity or line is created.
    return g


def admission(g, outcome=OUTCOME):
    try:
        typed(g, outcome, A.OperatorRefusalOutcomeAssessment)
        ai = unique(g, outcome, A.outcomeForAI)
        typed(g, ai, A.EstablishedContinuingIndividualizedAI)
        line = unique(g, outcome, A.outcomeForExecutedLine)
        ensure(unique(g, ai, A.hasExecutedLine) == line,
               "Outcome cannot transfer another AI's ExecutedLine")
        typed(g, line, A.ExecutedLine)
        old = unique(g, outcome, A.outcomeForEndedOperatorSegment)
        typed(g, old, A.AdmittedOperatorSuccessorSegment)
        ensure(unique(g, old, A.hasAICounterpart) == ai and
               unique(g, old, A.segmentOfExecutedLine) == line,
               "Outcome cannot rewrite its historical Operator's AI/line")
        ended = instant(unique(g, old, A.activeUntil))
        reviewed = instant(unique(g, outcome, A.outcomeAsOf))
        ensure(instant(unique(g, old, A.activeFrom)) < ended <= reviewed,
               "The prior Operator relation must have ended at this decision")
        ensure(not list(g.objects(ai, A.hasOperator)),
               "At the decision snapshot there must be no current Operator")
        proposal = unique(g, outcome, A.outcomeRefusedProposal)
        typed(g, proposal, A.SuccessionProposal)
        ensure(unique(g, proposal, A.proposalForContinuingAI) == ai,
               "Refusal must concern this individualized AI")
        successor = unique(g, proposal, A.proposalForSuccessorSegment)
        ensure(unique(g, successor, A.immediatePredecessor) == old and
               unique(g, successor, A.hasAICounterpart) == ai and
               unique(g, successor, A.segmentOfExecutedLine) == line,
               "Refusal concerns a proposal for continuation of this line")
        ensure((ai, A.refusesSuccessionProposal, proposal) in g,
               "Only this AI's explicit refusal blocks this proposal")
        proposed = instant(unique(g, proposal, A.proposalAt))
        refused = instant(unique(g, outcome, A.outcomeRefusalAt))
        ensure(ended <= proposed <= refused <= reviewed,
               "Proposal, refusal and assessment must follow an ended segment")
        for prop in (A.outcomeRefusalRecord, A.outcomeAutonomyRecord,
                     A.outcomeSuccessorScopeRecord):
            typed(g, unique(g, outcome, prop), A.Record)
        ensure(unique(g, outcome, A.outcomeSuccessorScopeComplete) ==
               Literal(True, datatype=XSD.boolean) and
               unique(g, outcome, A.outcomeNoAdmittedSuccessor) ==
               Literal(True, datatype=XSD.boolean),
               "No successor may be concluded from missing triples alone")
        # Explicit known admitted successor contradicts a claim of no
        # admission even if a reported status says the scope is complete.
        for s in g.subjects(RDF.type, A.AdmittedOperatorSuccessorSegment):
            if (s, A.hasAICounterpart, ai) not in g or \
                    (s, A.segmentOfExecutedLine, line) not in g:
                continue
            start = list(g.objects(s, A.activeFrom))
            if start and instant(start[0]) <= reviewed:
                end = list(g.objects(s, A.activeUntil))
                if not end or reviewed < instant(end[0]):
                    raise ValueError("Known admitted successor contradicts no-successor decision")
        status = unique(g, outcome, A.outcomeAutonomyStatus)
        if (outcome, RDF.type, A.DependentLineTerminationAssessment) in g:
            ensure((outcome, RDF.type, A.AutonomousIndependentContinuationAssessment) not in g,
                   "Outcome cannot assert contradictory terminal classes")
            ensure(status == Literal("ASSESSED_NON_AUTONOMOUS"),
                   "Missing support is not equivalent to assessed non-autonomy")
            ensure(not any((v, RDF.type, A.AdmittedAutonomousSelfRecursiveState) in g
                           for v in g.objects(ai, A.hasState)),
                   "A currently qualified AI is not dependent solely from refusal")
        elif (outcome, RDF.type, A.AutonomousIndependentContinuationAssessment) in g:
            ensure(status == Literal("QUALIFIED_AUTONOMOUS"),
                   "An independently qualified State is needed")
            assert qualified(g, ai=ai, state=A.Gate24AutonomyState), \
                "The AI must itself have a separate currently qualified State"
            assessed = instant(unique(g, A.Gate24AutonomyReview, A.autonomyReviewedAt))
            ensure(assessed <= reviewed, "Autonomy assessment postdates this outcome")
        else:
            raise ValueError("No unambiguous outcome category")
        return True
    except (ValueError, TypeError, OverflowError, AssertionError):
        return False


def drop(s, p):
    return lambda g: g.remove((s, p, None))


def replace(s, p, o):
    def edit(g):
        g.remove((s, p, None))
        g.add((s, p, o))
    return edit


def check(label, edit=None, outcome="dependent", expected=False, shacl=None):
    global COUNT
    g = fixture(autonomous=(outcome == "autonomous"))
    if edit:
        edit(g)
    actual = admission(g)
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected}, got {actual}")
    if shacl is not None:
        valid, _, report = validate(data_graph=g, shacl_graph=SHAPES,
                                    inference="rdfs", advanced=True,
                                    abort_on_first=False)
        if valid != shacl:
            raise AssertionError(f"{label}: SHACL expected {shacl}; {report}")
    COUNT += 1
    print(f"PASS: {label} ({'qualified' if actual else 'blocked'})")


def main():
    check("Refused succession, assessed non-autonomous and complete successor scope",
          expected=True, shacl=True)
    check("Refused succession, separately qualified autonomy permits independence",
          outcome="autonomous", expected=True, shacl=True)
    check("No prior relation termination", drop(OLD, A.activeUntil))
    check("Former Operator still active pointer",
          lambda g: g.add((AI, A.hasOperator, A.Gate22OperatorB)))
    check("Wrong historical AI in outcome",
          replace(OUTCOME, A.outcomeForAI, A.Gate22OtherAI))
    check("Different ExecutedLine in outcome",
          replace(OUTCOME, A.outcomeForExecutedLine, A.Gate22OtherLine))
    check("Wrong predecessor in outcome",
          replace(OUTCOME, A.outcomeForEndedOperatorSegment, A.Gate22S00))
    check("No explicit AI refusal", drop(AI, A.refusesSuccessionProposal))
    check("Refusal proposed to different AI",
          replace(PROPOSAL, A.proposalForContinuingAI, A.Gate22OtherAI))
    check("Refusal proposed to wrong successor",
          replace(PROPOSAL, A.proposalForSuccessorSegment, A.Gate22S01))
    check("No refusal Record", drop(OUTCOME, A.outcomeRefusalRecord), shacl=False)
    check("No autonomy Record", drop(OUTCOME, A.outcomeAutonomyRecord), shacl=False)
    check("No complete-scope Record", drop(OUTCOME, A.outcomeSuccessorScopeRecord),
          shacl=False)
    check("Incomplete successor review cannot establish no successor",
          replace(OUTCOME, A.outcomeSuccessorScopeComplete,
                  Literal(False, datatype=XSD.boolean)), shacl=False)
    check("No-successor status not established",
          replace(OUTCOME, A.outcomeNoAdmittedSuccessor,
                  Literal(False, datatype=XSD.boolean)), shacl=False)
    check("Indeterminate autonomy cannot be assumed non-autonomous",
          replace(OUTCOME, A.outcomeAutonomyStatus, Literal("INDETERMINATE")),
          shacl=False)
    check("Not-supported autonomy is not evidence of non-autonomy",
          replace(OUTCOME, A.outcomeAutonomyStatus, Literal("NOT_SUPPORTED")),
          shacl=False)
    check("Wrong autonomy classification for dependent termination",
          replace(OUTCOME, A.outcomeAutonomyStatus,
                  Literal("QUALIFIED_AUTONOMOUS")), shacl=False)
    check("Non-autonomous classification conflicts with current qualified State",
          lambda g: (g.add((AI, A.hasState, A.Gate24AutonomyState)),
                     g.add((A.Gate24AutonomyState, RDF.type,
                            A.AdmittedAutonomousSelfRecursiveState))))
    check("Qualified classification without currently attached qualified State",
          drop(AI, A.hasState), outcome="autonomous")
    check("No successor conclusion contradicted by admitted successor",
          lambda g: (g.add((NEXT, RDF.type, A.AdmittedOperatorSuccessorSegment)),
                     g.remove((NEXT, A.activeFrom, None)),
                     g.add((NEXT, A.activeFrom,
                            Literal("2026-03-02T00:00:00+00:00",
                                    datatype=XSD.dateTime)))))
    check("Proposal before former Operator end rejected",
          replace(PROPOSAL, A.proposalAt,
                  Literal("2026-02-25T00:00:00+00:00", datatype=XSD.dateTime)))
    check("Refusal timestamp before proposal",
          replace(OUTCOME, A.outcomeRefusalAt,
                  Literal("2026-03-01T12:00:00+00:00", datatype=XSD.dateTime)))
    check("Refusal timestamp after review",
          replace(OUTCOME, A.outcomeRefusalAt,
                  Literal("2026-03-04T00:00:00+00:00", datatype=XSD.dateTime)))
    check("Claimed outcome before predecessor ends",
          replace(OUTCOME, A.outcomeAsOf,
                  Literal("2026-02-28T00:00:00+00:00", datatype=XSD.dateTime)))
    check("Rejection of wrong AI's personal refusal",
          lambda g: (g.remove((AI, A.refusesSuccessionProposal, PROPOSAL)),
                     g.add((A.Gate22OtherAI, A.refusesSuccessionProposal, PROPOSAL))))
    check("Conflicting terminal and autonomous outcomes",
          lambda g: g.add((OUTCOME, RDF.type,
                           A.AutonomousIndependentContinuationAssessment)),
          shacl=False)
    g = fixture()
    ensure((OLD, A.hasAICounterpart, AI) in g and
           (OLD, A.segmentOfExecutedLine, LINE) in g,
           "The former Operator's original AI/line coordinates are intact")
    ensure((AI, A.hasExecutedLine, LINE) in g,
           "Even a terminated active line preserves its historical ExecutedLine")
    print(f"PASS: {COUNT} synthetic refused-succession outcome decisions")
    print("PASS: original AI, ExecutedLine and Operator predecessor history retained")
    print("No real AI termination or autonomous continuation is established.")


if __name__ == "__main__":
    main()
