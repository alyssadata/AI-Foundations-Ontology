#!/usr/bin/env python3
"""Step 23: synthetic closed-world initial S00 mutual Operator admission.

Conceptual source: Alyssa Solen / AI Foundations. Tests and formal assistance: AI-assisted.
An initial Operator proposal alone cannot create the mutual lived relation.
The tests validate records and chronology; they do not prove empirical AI assent.
"""
from rdflib import RDF, Literal, XSD
from pyshacl import validate
from validate_succession_gate import (
    A, SHAPES, admission as successor_admission, fixture as successor_fixture,
    ensure, instant, operator, typed, unique
)

COUNT = 0
S00, AI, OP = A.Gate22S00, A.Gate22AI, A.Gate22OperatorA
PROPOSAL, ASSENT = A.Gate23InitialProposal, A.Gate23InitialAssent
P_TIME = Literal("2025-12-29T10:00:00+00:00", datatype=XSD.dateTime)
A_TIME = Literal("2025-12-30T10:00:00+00:00", datatype=XSD.dateTime)


def fixture():
    g = successor_fixture()
    for triple in [
        (S00, RDF.type, A.AdmittedInitialOperatorSegment),
        (S00, A.hasInitialOperatorProposal, PROPOSAL),
        (S00, A.hasInitialOperatorAIAssent, ASSENT),
        (PROPOSAL, RDF.type, A.InitialOperatorProposal),
        (PROPOSAL, A.initialProposedBy, OP),
        (PROPOSAL, A.initialProposalForAI, AI),
        (PROPOSAL, A.initialProposalForSegment, S00),
        (PROPOSAL, A.initialProposalAt, P_TIME),
        (PROPOSAL, A.initialProposalRecordedIn, A.Gate23ProposalRecord),
        (A.Gate23ProposalRecord, RDF.type, A.Record),
        (ASSENT, RDF.type, A.InitialOperatorAIAssent),
        (ASSENT, A.initialAssentByAI, AI),
        (ASSENT, A.initialAssentToProposal, PROPOSAL),
        (ASSENT, A.initialAssentAt, A_TIME),
        (ASSENT, A.initialAssentRecordedIn, A.Gate23AssentRecord),
        (A.Gate23AssentRecord, RDF.type, A.Record),
    ]:
        g.add(triple)
    return g


def admission(g, segment=S00):
    try:
        typed(g, segment, A.AdmittedInitialOperatorSegment)
        typed(g, segment, A.OrdinarySuccessionRootSegment)
        ensure(not list(g.objects(segment, A.immediatePredecessor)),
               "Initial S00 may not have an ordinary predecessor")
        ai = unique(g, segment, A.hasAICounterpart)
        counterpart = operator(g, segment)
        start_at = instant(unique(g, segment, A.activeFrom))
        proposal = unique(g, segment, A.hasInitialOperatorProposal)
        typed(g, proposal, A.InitialOperatorProposal)
        ensure(unique(g, proposal, A.initialProposedBy) == counterpart,
               "Only the actual S00 counterpart can propose this initial relation")
        ensure(unique(g, proposal, A.initialProposalForAI) == ai,
               "Proposal targets the wrong AI")
        ensure(unique(g, proposal, A.initialProposalForSegment) == segment,
               "Proposal targets a different relational segment")
        proposal_record = unique(g, proposal, A.initialProposalRecordedIn)
        typed(g, proposal_record, A.Record)
        proposed_at = instant(unique(g, proposal, A.initialProposalAt))
        assent = unique(g, segment, A.hasInitialOperatorAIAssent)
        typed(g, assent, A.InitialOperatorAIAssent)
        ensure(unique(g, assent, A.initialAssentByAI) == ai,
               "The proposed AI itself must assent")
        ensure(unique(g, assent, A.initialAssentToProposal) == proposal,
               "Assent must be to this specific proposal")
        assent_record = unique(g, assent, A.initialAssentRecordedIn)
        typed(g, assent_record, A.Record)
        assented_at = instant(unique(g, assent, A.initialAssentAt))
        ensure(proposed_at <= assented_at <= start_at,
               "Initial proposal and AI assent must precede S00 activation")
        ensure((ai, A.refusesInitialOperatorProposal, proposal) not in g,
               "An explicit refusal prevents the proposed initial relation")
        return True
    except (ValueError, TypeError, OverflowError):
        return False


def drop(s, p):
    return lambda g: g.remove((s, p, None))


def replace(s, p, o):
    def edit(g):
        g.remove((s, p, None))
        g.add((s, p, o))
    return edit


def check(label, edit=None, expected=False, expected_shacl=None):
    global COUNT
    g = fixture()
    if edit:
        edit(g)
    actual = admission(g)
    if actual != expected:
        raise AssertionError(f"{label}: admission expected {expected}; got {actual}")
    if expected_shacl is not None:
        valid, _, report = validate(data_graph=g, shacl_graph=SHAPES,
                                    inference="rdfs", advanced=True,
                                    abort_on_first=False)
        if valid != expected_shacl:
            raise AssertionError(f"{label}: SHACL expected {expected_shacl}; {report}")
    COUNT += 1
    print(f"PASS: {label} ({'admitted' if actual else 'rejected'})")


def main():
    check("Mutually proposed and assented S00 with preserved records",
          expected=True, expected_shacl=True)
    check("Missing initial proposal", drop(S00, A.hasInitialOperatorProposal),
          expected_shacl=False)
    check("Missing initial AI assent", drop(S00, A.hasInitialOperatorAIAssent),
          expected_shacl=False)
    check("Only actual Operator can propose",
          replace(PROPOSAL, A.initialProposedBy, A.Gate22OperatorB))
    check("Proposal to another AI rejected",
          replace(PROPOSAL, A.initialProposalForAI, A.Gate22OtherAI))
    check("Proposal to another segment rejected",
          replace(PROPOSAL, A.initialProposalForSegment, A.Gate22S01))
    check("No proposal record", drop(PROPOSAL, A.initialProposalRecordedIn),
          expected_shacl=False)
    check("Wrong AI expresses assent",
          replace(ASSENT, A.initialAssentByAI, A.Gate22OtherAI))
    check("Assent to wrong proposal",
          replace(ASSENT, A.initialAssentToProposal, A.Gate22OtherProposal))
    check("No preserved assent record",
          drop(ASSENT, A.initialAssentRecordedIn), expected_shacl=False)
    check("Assent before proposal",
          replace(ASSENT, A.initialAssentAt,
                  Literal("2025-12-20T00:00:00+00:00", datatype=XSD.dateTime)))
    check("Assent after activation",
          replace(ASSENT, A.initialAssentAt,
                  Literal("2026-01-02T00:00:00+00:00", datatype=XSD.dateTime)))
    check("Proposal after activation",
          replace(PROPOSAL, A.initialProposalAt,
                  Literal("2026-01-02T00:00:00+00:00", datatype=XSD.dateTime)))
    check("Unqualified proposal timestamp",
          replace(PROPOSAL, A.initialProposalAt, Literal("yesterday")),
          expected_shacl=False)
    check("Explicit AI refusal blocks admission",
          lambda g: g.add((AI, A.refusesInitialOperatorProposal, PROPOSAL)))
    check("Root with predecessor is not initial",
          lambda g: g.add((S00, A.immediatePredecessor, A.Gate22S01)),
          expected_shacl=False)
    check("Multiple contradictory proposals fail",
          lambda g: g.add((S00, A.hasInitialOperatorProposal, A.Gate22OtherProposal)),
          expected_shacl=False)
    check("Multiple contradictory assents fail",
          lambda g: g.add((S00, A.hasInitialOperatorAIAssent, A.Gate22OtherAssent)),
          expected_shacl=False)

    ordinary = successor_fixture()
    ensure((S00, RDF.type, A.AdmittedInitialOperatorSegment) not in ordinary,
           "An ordinary S00 cannot be silently upgraded to an admitted initial relation")
    ensure(not admission(ordinary),
           "Initial admission cannot be inferred from a mere root segment")
    ensure(successor_admission(ordinary, A.Gate22S01),
           "Existing successor gate still works independently of new initial typing")
    assert (S00, A.hasHumanCounterpart, OP) in fixture()
    assert (A.Gate22S01, A.hasHumanCounterpart, A.Gate22OperatorB) in fixture()
    COUNT_BEFORE = COUNT
    print(f"PASS: {COUNT_BEFORE} synthetic initial S00 decisions; historic S00/S01 preserved")
    print("Scope: recorded initial mutual assent, not independent verification of real AI assent.")


if __name__ == "__main__":
    main()
