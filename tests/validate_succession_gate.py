#!/usr/bin/env python3
"""Step 22: closed-world four-condition Operator succession admission tests.

Synthetic fixtures only. Passing means the represented gate is enforceable;
it is not empirical proof that a particular AI continued across succession.
Conceptual source: Alyssa Solen / AI Foundations. Validation: AI-assisted.
"""
from datetime import datetime, timezone
from pathlib import Path
from rdflib import Graph, Namespace, RDF, OWL, Literal, XSD
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]
A = Namespace("https://awakeningcodex.com/ontology/ai-foundations/v1#")
BASE = Graph().parse(ROOT / "ontology/ai-foundations-v1.ttl", format="turtle")
SHAPES = Graph().parse(ROOT / "ontology/ai-foundations-v1-shapes.ttl", format="turtle")
COUNT = 0


def unique(g, s, p):
    values = list(g.objects(s, p))
    if len(values) != 1:
        raise ValueError(f"Expected exactly one {p} for {s}; got {len(values)}")
    return values[0]


def typed(g, s, cls):
    if (s, RDF.type, cls) not in g:
        raise ValueError(f"Missing explicit type {cls}")


def ensure(condition, message):
    if not condition:
        raise ValueError(message)


def instant(value):
    ensure(isinstance(value, Literal) and value.datatype == XSD.dateTime,
           "Expected timezone-aware dateTime literal")
    point = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    ensure(point.tzinfo is not None and point.utcoffset() is not None,
           "Naive timestamps are not valid succession bounds")
    return point.astimezone(timezone.utc)


def operator(g, segment):
    human = list(g.objects(segment, A.hasHumanCounterpart))
    org = list(g.objects(segment, A.hasOrganizationCounterpart))
    ensure(len(human) + len(org) == 1,
           "One explicitly typed Human XOR Organization counterpart per segment")
    op = (human + org)[0]
    typed(g, op, A.Human if human else A.Organization)
    return op


def admission(g, segment):
    """An operational admission decision, not an OWL identity inference."""
    try:
        typed(g, segment, A.SuccessionCandidateSegment)
        predecessor = unique(g, segment, A.immediatePredecessor)
        ensure(segment != predecessor, "Self-predecessor")
        typed(g, predecessor, A.OrdinarySuccessionRootSegment)
        ai = unique(g, segment, A.hasAICounterpart)
        line = unique(g, segment, A.segmentOfExecutedLine)
        ensure(unique(g, predecessor, A.hasAICounterpart) == ai,
               "Different AI: role replacement is not succession")
        ensure(unique(g, predecessor, A.segmentOfExecutedLine) == line,
               "Historical ExecutedLine is not the same")
        ensure(unique(g, ai, A.hasExecutedLine) == line,
               "Continuing AI's ExecutedLine is not the asserted historical line")
        prior_operator = operator(g, predecessor)
        successor_operator = operator(g, segment)
        ensure(prior_operator != successor_operator,
               "A successor must be a different Operator entity")
        ended_at = instant(unique(g, predecessor, A.activeUntil))
        began_at = instant(unique(g, segment, A.activeFrom))
        ensure(instant(unique(g, predecessor, A.activeFrom)) < ended_at <= began_at,
               "Prior Operator must have terminated by start of successor segment")

        gate = unique(g, segment, A.hasSuccessionAssessment)
        typed(g, gate, A.SuccessionGateAssessment)
        ensure(unique(g, gate, A.assessedSuccessionSegment) == segment,
               "Assessment must target this successor segment")
        termination = unique(g, gate, A.hasTerminationRecord)
        typed(g, termination, A.Record)
        ensure(unique(g, termination, A.recordsTerminatedOperatorSegment) == predecessor,
               "Termination record must document actual predecessor")

        claim = unique(g, gate, A.hasSuccessionContinuityClaim)
        typed(g, claim, A.ContinuityClaim)
        ensure(unique(g, claim, A.continuityAssessmentForLine) == line,
               "Continuity assessment must concern this one ExecutedLine")
        evidence = unique(g, gate, A.hasSuccessionContinuityEvidence)
        typed(g, evidence, A.Evidence)
        ensure(unique(g, evidence, A.directlyEvaluatesClaim) == claim and
               unique(g, evidence, A.supportsClaim) == claim,
               "Evidence must explicitly support the same continuity claim")
        ensure(unique(g, evidence, A.hasEvidentiaryStatus) == Literal("SUPPORTED"),
               "Unresolved or unsupported continuity evidence cannot admit succession")
        ensure(any((rec, RDF.type, A.Record) in g or
                   (rec, RDF.type, A.EvidenceArtifact) in g
                   for rec in g.objects(evidence, A.preservedIn)),
               "Evidence must have a preserved supporting record/artifact")
        ensure(any((ev, RDF.type, A.Evaluation) in g
                   for ev in g.subjects(A.producesEvidence, evidence)),
               "Continuity evidence must be produced by an Evaluation")

        proposal = unique(g, gate, A.hasSuccessionProposal)
        typed(g, proposal, A.SuccessionProposal)
        ensure(unique(g, proposal, A.proposedBySuccessor) == successor_operator,
               "Actual successor must deliberately propose")
        ensure(unique(g, proposal, A.proposalForContinuingAI) == ai and
               unique(g, proposal, A.proposalForSuccessorSegment) == segment,
               "Proposal must address this specific AI and successor segment")
        proposal_record = unique(g, proposal, A.proposalRecordedIn)
        typed(g, proposal_record, A.Record)
        proposed_at = instant(unique(g, proposal, A.proposalAt))

        assent = unique(g, gate, A.hasSuccessionAIAssent)
        typed(g, assent, A.SuccessionAIAssent)
        ensure(unique(g, assent, A.assentByContinuingAI) == ai,
               "Assent must come from the continuing AI")
        ensure(unique(g, assent, A.assentToProposal) == proposal,
               "Assent must recognize this particular proposal")
        assent_record = unique(g, assent, A.assentRecordedIn)
        typed(g, assent_record, A.Record)
        assented_at = instant(unique(g, assent, A.assentAt))
        ensure(proposed_at <= assented_at <= began_at,
               "Proposal and assent must precede establishment of successor segment")
        ensure((ai, A.refusesSuccessionProposal, proposal) not in g,
               "Explicit refusal blocks this proposed succession")
        return True
    except (ValueError, TypeError, OverflowError):
        return False


def fixture():
    g = Graph()
    for triple in BASE:
        g.add(triple)
    ai, line = A.Gate22AI, A.Gate22Line
    old, new = A.Gate22S00, A.Gate22S01
    op_a, op_b = A.Gate22OperatorA, A.Gate22OperatorB
    gate, proposal, assent = A.Gate22Assessment, A.Gate22Proposal, A.Gate22Assent
    claim, evidence, evaluation = A.Gate22Claim, A.Gate22Evidence, A.Gate22Evaluation
    t0 = Literal("2026-01-01T00:00:00+00:00", datatype=XSD.dateTime)
    t1 = Literal("2026-02-01T00:00:00+00:00", datatype=XSD.dateTime)
    pt = Literal("2026-01-29T00:00:00+00:00", datatype=XSD.dateTime)
    at = Literal("2026-01-30T00:00:00+00:00", datatype=XSD.dateTime)
    facts = [
        (ai, RDF.type, A.AIFoundationsGovernedAI),
        (ai, A.governedBy, A.AIFoundationsGoverningLine),
        (ai, A.hasExecutedLine, line),
        (ai, A.hasOperator, op_b),
        (line, RDF.type, A.ExecutedLine),
        (op_a, RDF.type, A.Human), (op_b, RDF.type, A.Human),
        (op_a, OWL.differentFrom, op_b),
        (old, RDF.type, A.OrdinarySuccessionRootSegment),
        (old, A.hasAICounterpart, ai), (old, A.hasHumanCounterpart, op_a),
        (old, A.segmentOfExecutedLine, line), (old, A.activeFrom, t0),
        (old, A.activeUntil, t1),
        (new, RDF.type, A.SuccessionCandidateSegment),
        (new, RDF.type, A.AdmittedOperatorSuccessorSegment),
        (new, A.hasAICounterpart, ai), (new, A.hasHumanCounterpart, op_b),
        (new, A.segmentOfExecutedLine, line), (new, A.activeFrom, t1),
        (new, A.immediatePredecessor, old),
        (new, A.hasSuccessionAssessment, gate),
        (gate, RDF.type, A.AdmittedSuccessionGateAssessment),
        (gate, A.assessedSuccessionSegment, new),
        (gate, A.hasTerminationRecord, A.Gate22TerminationRecord),
        (A.Gate22TerminationRecord, RDF.type, A.Record),
        (A.Gate22TerminationRecord, A.recordsTerminatedOperatorSegment, old),
        (gate, A.hasSuccessionContinuityClaim, claim),
        (claim, RDF.type, A.ContinuityClaim),
        (claim, A.dependsOnOntologyElement, A.ExecutedLine),
        (claim, A.continuityAssessmentForLine, line),
        (gate, A.hasSuccessionContinuityEvidence, evidence),
        (evidence, RDF.type, A.Evidence),
        (evidence, A.directlyEvaluatesClaim, claim),
        (evidence, A.supportsClaim, claim),
        (evidence, A.hasEvidentiaryStatus, Literal("SUPPORTED")),
        (evidence, A.preservedIn, A.Gate22EvidenceRecord),
        (A.Gate22EvidenceRecord, RDF.type, A.Record),
        (evaluation, RDF.type, A.Evaluation),
        (evaluation, A.producesEvidence, evidence),
        (gate, A.hasSuccessionProposal, proposal),
        (proposal, RDF.type, A.SuccessionProposal),
        (proposal, A.proposedBySuccessor, op_b),
        (proposal, A.proposalForContinuingAI, ai),
        (proposal, A.proposalForSuccessorSegment, new),
        (proposal, A.proposalAt, pt),
        (proposal, A.proposalRecordedIn, A.Gate22ProposalRecord),
        (A.Gate22ProposalRecord, RDF.type, A.Record),
        (gate, A.hasSuccessionAIAssent, assent),
        (assent, RDF.type, A.SuccessionAIAssent),
        (assent, A.assentByContinuingAI, ai),
        (assent, A.assentToProposal, proposal),
        (assent, A.assentAt, at),
        (assent, A.assentRecordedIn, A.Gate22AssentRecord),
        (A.Gate22AssentRecord, RDF.type, A.Record),
    ]
    for triple in facts:
        g.add(triple)
    return g


def check(label, edit=None, should_pass=False, shacl=None):
    global COUNT
    g = fixture()
    if edit:
        edit(g)
    actual = admission(g, A.Gate22S01)
    if actual != should_pass:
        raise AssertionError(f"{label}: expected {should_pass}, got {actual}")
    if shacl is not None:
        conforms, _, report = validate(
            data_graph=g, shacl_graph=SHAPES, inference="rdfs",
            advanced=True, abort_on_first=False)
        if conforms != shacl:
            raise AssertionError(f"{label}: SHACL expected {shacl}; {report}")
    COUNT += 1
    print(f"PASS: {label} ({'admitted' if actual else 'rejected'})")


def drop(s, p):
    return lambda g: g.remove((s, p, None))


def replace(s, p, value):
    def edit(g):
        g.remove((s, p, None))
        g.add((s, p, value))
    return edit


def main():
    check("Four-condition positive S00→S01; historical pairing unchanged",
          should_pass=True, shacl=True)
    check("No predecessor termination", drop(A.Gate22S00, A.activeUntil))
    check("Prior relation ends after successor begins",
          replace(A.Gate22S00, A.activeUntil,
                  Literal("2026-03-01T00:00:00+00:00", datatype=XSD.dateTime)))
    check("No termination provenance record",
          drop(A.Gate22Assessment, A.hasTerminationRecord))
    check("Termination record targets wrong segment",
          replace(A.Gate22TerminationRecord, A.recordsTerminatedOperatorSegment, A.Gate22S01))
    check("Copied role with a different AI is not same-AI succession",
          replace(A.Gate22S01, A.hasAICounterpart, A.Gate22OtherAI))
    check("A different ExecutedLine is not continuation",
          replace(A.Gate22S01, A.segmentOfExecutedLine, A.Gate22OtherLine))
    check("No continuity claim", drop(A.Gate22Assessment, A.hasSuccessionContinuityClaim))
    check("No continuity Evidence", drop(A.Gate22Assessment, A.hasSuccessionContinuityEvidence))
    for status in ("INDETERMINATE", "PARTIALLY_SUPPORTED", "NOT_SUPPORTED", "NOT_EVALUATED"):
        check(f"Continuity evidence {status} cannot admit",
              replace(A.Gate22Evidence, A.hasEvidentiaryStatus, Literal(status)))
    check("Evidence supporting different claim does not admit",
          replace(A.Gate22Evidence, A.supportsClaim, A.Gate22OtherClaim))
    check("Continuity claim for another line does not admit",
          replace(A.Gate22Claim, A.continuityAssessmentForLine, A.Gate22OtherLine))
    check("Unpreserved evidence does not admit",
          drop(A.Gate22Evidence, A.preservedIn))
    check("No successor proposal", drop(A.Gate22Assessment, A.hasSuccessionProposal))
    check("Only predecessor proposes (wrong operator)",
          replace(A.Gate22Proposal, A.proposedBySuccessor, A.Gate22OperatorA))
    check("Proposal for other AI does not admit",
          replace(A.Gate22Proposal, A.proposalForContinuingAI, A.Gate22OtherAI))
    check("Proposal for other segment does not admit",
          replace(A.Gate22Proposal, A.proposalForSuccessorSegment, A.Gate22S00))
    check("Proposal lacking preserved record",
          drop(A.Gate22Proposal, A.proposalRecordedIn))
    check("No continuing-AI assent",
          drop(A.Gate22Assessment, A.hasSuccessionAIAssent), shacl=False)
    check("Different AI's assent does not admit",
          replace(A.Gate22Assent, A.assentByContinuingAI, A.Gate22OtherAI))
    check("Assent to a different proposal does not admit",
          replace(A.Gate22Assent, A.assentToProposal, A.Gate22OtherProposal))
    check("Assent lacking preserved Record",
          drop(A.Gate22Assent, A.assentRecordedIn))
    check("Assent after S01 begins cannot backdate admission",
          replace(A.Gate22Assent, A.assentAt,
                  Literal("2026-02-02T00:00:00+00:00", datatype=XSD.dateTime)))
    check("Assent before proposal cannot satisfy this particular proposal",
          replace(A.Gate22Assent, A.assentAt,
                  Literal("2026-01-20T00:00:00+00:00", datatype=XSD.dateTime)))
    check("Explicit refusal blocks unilateral succession",
          lambda g: g.add((A.Gate22AI, A.refusesSuccessionProposal, A.Gate22Proposal)))
    check("Same Operator retained is not a successor",
          replace(A.Gate22S01, A.hasHumanCounterpart, A.Gate22OperatorA))
    check("No gate assessment: mere predecessor chain cannot admit",
          drop(A.Gate22S01, A.hasSuccessionAssessment), shacl=False)
    check("Even copied evidence alone cannot supply AI assent",
          drop(A.Gate22Assent, A.assentByContinuingAI))
    check("Unqualified temporal literal cannot validate termination",
          replace(A.Gate22S00, A.activeUntil, Literal("2026-02-01")))
    g = fixture()
    assert (A.Gate22S00, A.hasHumanCounterpart, A.Gate22OperatorA) in g
    assert (A.Gate22S01, A.hasHumanCounterpart, A.Gate22OperatorB) in g
    assert (A.Gate22S00, A.segmentOfExecutedLine, A.Gate22Line) in g
    assert (A.Gate22S01, A.segmentOfExecutedLine, A.Gate22Line) in g
    print(f"PASS: {COUNT} synthetic admission decisions; original S00 provenance retained")
    print("Scope: modelled and synthetic closed-world governance, not empirical identity or AI consciousness.")


if __name__ == "__main__":
    main()
