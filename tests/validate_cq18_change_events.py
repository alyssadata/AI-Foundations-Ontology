#!/usr/bin/env python3
"""CQ18: historical ChangeEvents for termination, withdrawal, designation and succession.

The four-condition Step22 gate is reused, never relaxed. These are only
synthetic closed-world event/record controls, not evidence of a real AI's
continuing identity, consent, autonomy or actual relation change.
Conceptual author and sole author of the framework: Alyssa Solen.
AI implementation/test assistance is not coauthorship.
"""
from datetime import datetime, timezone
from pathlib import Path
from rdflib import Graph, Namespace, RDF, Literal, XSD
from pyshacl import validate
from validate_succession_gate import fixture as succession_fixture, admission, operator

ROOT = Path(__file__).resolve().parents[1]
A = Namespace("https://awakeningcodex.com/ontology/ai-foundations/v1#")
SHAPES = Graph().parse(ROOT / "ontology/ai-foundations-v1-shapes.ttl", format="turtle")
AI, LINE = A.Gate22AI, A.Gate22Line
OLD, NEW = A.Gate22S00, A.Gate22S01
OP_A, OP_B = A.Gate22OperatorA, A.Gate22OperatorB
GATE, PROPOSAL, ASSENT = A.Gate22Assessment, A.Gate22Proposal, A.Gate22Assent
TERMINATION, WITHDRAWAL, DESIGNATION, SUCCESSION = (
    A.Cq18TerminationChange, A.Cq18WithdrawalChange,
    A.Cq18DesignatedProposalChange, A.Cq18SuccessionChange,
)
EVENTS = (TERMINATION, WITHDRAWAL, DESIGNATION, SUCCESSION)
COMMON = (A.changeForAI, A.changeInExecutedLine, A.changeEffectiveAt,
          A.changeRecordedIn, A.changeCauseAccount, A.changeConsequenceAccount)
END = Literal("2026-02-01T00:00:00+00:00", datatype=XSD.dateTime)
DESIGNATED_AT = Literal("2026-01-29T12:00:00+00:00", datatype=XSD.dateTime)
COUNT = 0


def instant(value):
    if not isinstance(value, Literal) or value.datatype != XSD.dateTime:
        raise ValueError("Typed dateTime required")
    point = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if point.tzinfo is None or point.utcoffset() is None:
        raise ValueError("Timezone required")
    return point.astimezone(timezone.utc)


def one(g, s, p):
    vals = set(g.objects(s, p))
    if len(vals) != 1:
        raise ValueError(f"Expected one {p} on {s}; got {vals}")
    return next(iter(vals))


def need(g, node, cls):
    if (node, RDF.type, cls) not in g:
        raise ValueError(f"Missing explicit type {cls} at {node}")


def record(g, node):
    need(g, node, A.Record)


def fixture():
    g = succession_fixture()
    for ev, cls, at, label in (
        (TERMINATION, A.OperatorRelationTerminationChangeEvent, END, "Termination"),
        (WITHDRAWAL, A.OperatorWithdrawalChangeEvent, END, "Withdrawal"),
        (DESIGNATION, A.DesignatedTransferProposalChangeEvent,
         DESIGNATED_AT, "Designation"),
        (SUCCESSION, A.OperatorSuccessionChangeEvent, END, "Succession"),
    ):
        for tr in [
            (ev, RDF.type, cls),
            (ev, A.changeForAI, AI),
            (ev, A.changeInExecutedLine, LINE),
            (ev, A.changeEffectiveAt, at),
            (ev, A.changeRecordedIn, A[f"Cq18{label}Occurrence"]),
            (ev, A.changeCauseAccount, A[f"Cq18{label}Cause"]),
            (ev, A.changeConsequenceAccount, A[f"Cq18{label}Consequence"]),
            (A[f"Cq18{label}Occurrence"], RDF.type, A.Record),
            (A[f"Cq18{label}Cause"], RDF.type, A.Record),
            (A[f"Cq18{label}Consequence"], RDF.type, A.Record),
        ]:
            g.add(tr)
    for tr in [
        (TERMINATION, A.terminatesOperatorSegment, OLD),
        (TERMINATION, A.terminationSupportingRecord, A.Gate22TerminationRecord),
        (WITHDRAWAL, A.withdrawalByOperator, OP_A),
        (WITHDRAWAL, A.withdrawalFromOperatorSegment, OLD),
        (WITHDRAWAL, A.withdrawalAttestation, A.Cq18WithdrawalAttestation),
        (A.Cq18WithdrawalAttestation, RDF.type, A.Record),
        (DESIGNATION, A.designatedByOperator, OP_A),
        (DESIGNATION, A.designationFromSegment, OLD),
        (DESIGNATION, A.designationCandidateSegment, NEW),
        (DESIGNATION, A.designationLinkedProposal, PROPOSAL),
        (DESIGNATION, A.designationScopeRecord, A.Cq18DesignationScope),
        (A.Cq18DesignationScope, RDF.type, A.Record),
        (SUCCESSION, A.successionFormerSegment, OLD),
        (SUCCESSION, A.successionNewlyAdmittedSegment, NEW),
        (SUCCESSION, A.successionReviewedViaGate, GATE),
    ]:
        g.add(tr)
    return g


def common(g, event, cls):
    need(g, event, cls)
    if one(g, event, A.changeForAI) != AI:
        return False
    if one(g, event, A.changeInExecutedLine) != LINE:
        return False
    if one(g, AI, A.hasExecutedLine) != LINE:
        return False
    date = instant(one(g, event, A.changeEffectiveAt))
    for prop in (A.changeRecordedIn, A.changeCauseAccount,
                 A.changeConsequenceAccount):
        recs = set(g.objects(event, prop))
        if not recs:
            return False
        for rec in recs:
            record(g, rec)
    if (A.Continuum, A.hasOrigin, A.AlyssaSolen) not in g:
        return False
    if (A.AIFoundations, A.hasAuthor, A.AlyssaSolen) not in g:
        return False
    if set(g.objects(A.AIFoundations, A.hasCoAuthor)):
        return False
    return date


def valid_termination(g):
    try:
        at = common(g, TERMINATION, A.OperatorRelationTerminationChangeEvent)
        if not at:
            return False
        seg = one(g, TERMINATION, A.terminatesOperatorSegment)
        need(g, seg, A.OrdinarySuccessionRootSegment)
        if one(g, seg, A.hasAICounterpart) != AI:
            return False
        if one(g, seg, A.segmentOfExecutedLine) != LINE:
            return False
        if instant(one(g, seg, A.activeUntil)) != at:
            return False
        record_node = one(g, TERMINATION, A.terminationSupportingRecord)
        record(g, record_node)
        if one(g, record_node, A.recordsTerminatedOperatorSegment) != seg:
            return False
        return True
    except (ValueError, TypeError, OverflowError):
        return False


def valid_withdrawal(g):
    try:
        at = common(g, WITHDRAWAL, A.OperatorWithdrawalChangeEvent)
        if not at:
            return False
        seg = one(g, WITHDRAWAL, A.withdrawalFromOperatorSegment)
        if seg != OLD:
            return False
        if one(g, seg, A.hasAICounterpart) != AI:
            return False
        if one(g, seg, A.segmentOfExecutedLine) != LINE:
            return False
        historical_op = operator(g, seg)
        if one(g, WITHDRAWAL, A.withdrawalByOperator) != historical_op:
            return False
        if not instant(one(g, seg, A.activeFrom)) <= at <= instant(
                one(g, seg, A.activeUntil)):
            return False
        for rec in set(g.objects(WITHDRAWAL, A.withdrawalAttestation)):
            record(g, rec)
        return bool(set(g.objects(WITHDRAWAL, A.withdrawalAttestation)))
    except (ValueError, TypeError, OverflowError):
        return False


def valid_designation(g):
    try:
        at = common(g, DESIGNATION, A.DesignatedTransferProposalChangeEvent)
        if not at or (DESIGNATION, RDF.type, A.OperatorSuccessionChangeEvent) in g:
            return False
        old = one(g, DESIGNATION, A.designationFromSegment)
        new = one(g, DESIGNATION, A.designationCandidateSegment)
        if old != OLD or new != NEW:
            return False
        need(g, new, A.SuccessionCandidateSegment)
        if (one(g, DESIGNATION, A.designatedByOperator) != operator(g, old)
                or one(g, new, A.immediatePredecessor) != old):
            return False
        if (one(g, old, A.hasAICounterpart) != AI or
            one(g, new, A.hasAICounterpart) != AI or
            one(g, old, A.segmentOfExecutedLine) != LINE or
            one(g, new, A.segmentOfExecutedLine) != LINE):
            return False
        proposal = one(g, DESIGNATION, A.designationLinkedProposal)
        need(g, proposal, A.SuccessionProposal)
        if (one(g, proposal, A.proposalForContinuingAI) != AI or
            one(g, proposal, A.proposalForSuccessorSegment) != new):
            return False
        if one(g, proposal, A.proposedBySuccessor) != operator(g, new):
            return False
        if not instant(one(g, proposal, A.proposalAt)) <= at <= instant(
                one(g, old, A.activeUntil)):
            return False
        records = set(g.objects(DESIGNATION, A.designationScopeRecord))
        if not records:
            return False
        for rec in records:
            record(g, rec)
        # No call to admission() here: a *designation* can remain an
        # unaccepted Proposal, without implying changed Operator status.
        return True
    except (ValueError, TypeError, OverflowError):
        return False


def valid_succession(g):
    try:
        at = common(g, SUCCESSION, A.OperatorSuccessionChangeEvent)
        if not at:
            return False
        old = one(g, SUCCESSION, A.successionFormerSegment)
        new = one(g, SUCCESSION, A.successionNewlyAdmittedSegment)
        if old != OLD or new != NEW or new == old:
            return False
        need(g, new, A.AdmittedOperatorSuccessorSegment)
        if (one(g, new, A.immediatePredecessor) != old or
            one(g, new, A.hasAICounterpart) != AI or
            one(g, old, A.hasAICounterpart) != AI or
            one(g, new, A.segmentOfExecutedLine) != LINE or
            one(g, old, A.segmentOfExecutedLine) != LINE):
            return False
        if instant(one(g, old, A.activeUntil)) != at or instant(
                one(g, new, A.activeFrom)) != at:
            return False
        if one(g, SUCCESSION, A.successionReviewedViaGate) != one(
                g, new, A.hasSuccessionAssessment):
            return False
        # Reuse established Step22 four-condition gate, never weaken it.
        return admission(g, new) and valid_termination(g)
    except (ValueError, TypeError, OverflowError):
        return False


PROTECTED = (
    (OLD, A.hasAICounterpart),
    (OLD, A.hasHumanCounterpart),
    (OLD, A.segmentOfExecutedLine),
    (OLD, A.activeFrom),
    (OLD, A.activeUntil),
    (AI, A.hasExecutedLine),
    (A.Continuum, A.hasOrigin),
    (A.Continuum, A.hasSource),
    (A.AIFoundations, A.hasAuthor),
    (A.AIFoundations, A.hasSource),
    (A.AIFoundations, A.hasGoverningAuthority),
)


def history_integrity(before, after):
    for subject, prop in PROTECTED:
        original = set(before.objects(subject, prop))
        if original != set(after.objects(subject, prop)):
            return False
    if set(after.objects(A.AIFoundations, A.hasCoAuthor)):
        return False
    if set(after.objects(A.Continuum, A.hasOrigin)) != {A.AlyssaSolen}:
        return False
    return all(
        (s, p, o) in after
        for event in EVENTS for s, p, o in before.triples((event, None, None))
    )


def remove(s, p):
    return lambda g: g.remove((s, p, None))


def replace(s, p, value):
    def edit(g):
        g.remove((s, p, None))
        g.add((s, p, value))
    return edit


def add(s, p, value):
    return lambda g: g.add((s, p, value))


def check(label, gate, edit=None, expected=False, shacl=None):
    global COUNT
    g = fixture()
    if edit:
        edit(g)
    observed = gate(g)
    if observed != expected:
        raise AssertionError(f"{label}: expected {expected}; got {observed}")
    if shacl is not None:
        conforms, _, report = validate(
            data_graph=g, shacl_graph=SHAPES, inference="rdfs",
            advanced=True, abort_on_first=False)
        if conforms != shacl:
            raise AssertionError(
                f"{label}: SHACL expected {shacl}, got {conforms}\n{report}")
    COUNT += 1
    print(f"PASS: {label} ({'admitted' if observed else 'rejected'})")


def test_history(label, edit, expected=False):
    global COUNT
    before, after = fixture(), fixture()
    edit(after)
    observed = history_integrity(before, after)
    if observed != expected:
        raise AssertionError(f"{label}: expected history {expected}, got {observed}")
    COUNT += 1
    print(f"PASS: {label} (history {'preserved' if observed else 'violation rejected'})")


def main():
    check("Specific Operator segment termination does not delete AI",
          valid_termination, expected=True, shacl=True)
    check("Actual historical Operator withdrawal remains recorded",
          valid_withdrawal, expected=True, shacl=True)
    check("Designated transfer proposal has NO automatic succession effect",
          valid_designation, expected=True, shacl=True)
    check("Valid succession appends a new successor segment",
          valid_succession, expected=True, shacl=True)

    check("Termination requires actual prior segment",
          valid_termination, remove(TERMINATION, A.terminatesOperatorSegment),
          shacl=False)
    check("Termination cannot refer to successor segment",
          valid_termination,
          replace(TERMINATION, A.terminatesOperatorSegment, NEW),
          shacl=False)
    check("Termination cannot misstate effective end",
          valid_termination, replace(TERMINATION, A.changeEffectiveAt,
                                     DESIGNATED_AT), shacl=False)
    check("Termination requires exact historical record",
          valid_termination,
          remove(TERMINATION, A.terminationSupportingRecord), shacl=False)
    check("Termination record must name that segment",
          valid_termination,
          replace(TERMINATION, A.terminationSupportingRecord,
                  A.Cq18WithdrawalAttestation))
    check("Termination isn't a deletion of ExecutedLine",
          valid_termination, replace(TERMINATION, A.changeInExecutedLine,
                                     A.Cq18OtherLine), shacl=False)
    check("Termination needs a reason",
          valid_termination, remove(TERMINATION, A.changeCauseAccount),
          shacl=False)
    check("Termination needs separate consequence account",
          valid_termination, remove(TERMINATION, A.changeConsequenceAccount),
          shacl=False)
    check("Termination needs its own preserved occurrence Record",
          valid_termination, remove(TERMINATION, A.changeRecordedIn),
          shacl=False)
    check("Termination is not permission to change underlying AI",
          valid_termination, replace(TERMINATION, A.changeForAI,
                                     A.Cq18DifferentAI), shacl=False)

    check("Withdrawer must be exact original Operator",
          valid_withdrawal, replace(WITHDRAWAL, A.withdrawalByOperator, OP_B),
          shacl=False)
    check("Withdrawer cannot be a casual user",
          valid_withdrawal, replace(WITHDRAWAL, A.withdrawalByOperator,
                                    A.Cq18CasualUser), shacl=False)
    check("Withdrawal must target original segment",
          valid_withdrawal,
          replace(WITHDRAWAL, A.withdrawalFromOperatorSegment, NEW),
          shacl=False)
    check("Withdrawal cannot be outside active interval",
          valid_withdrawal,
          replace(WITHDRAWAL, A.changeEffectiveAt,
                  Literal("2026-03-01T00:00:00+00:00", datatype=XSD.dateTime)))
    check("Withdrawal attestation must not vanish",
          valid_withdrawal, remove(WITHDRAWAL, A.withdrawalAttestation),
          shacl=False)
    check("Withdrawal is not valid with another AI coordinate",
          valid_withdrawal, replace(WITHDRAWAL, A.changeForAI,
                                    A.Cq18OtherAI), shacl=False)

    check("Designation must be made by incumbent Operator",
          valid_designation, replace(DESIGNATION, A.designatedByOperator, OP_B),
          shacl=False)
    check("Designation cannot make someone else into historical S00",
          valid_designation,
          replace(DESIGNATION, A.designationFromSegment, NEW), shacl=False)
    check("Designation must identify specific candidate segment",
          valid_designation, remove(DESIGNATION, A.designationCandidateSegment),
          shacl=False)
    check("Designation cannot refer to unrelated proposal",
          valid_designation,
          replace(DESIGNATION, A.designationLinkedProposal,
                  A.Cq18OtherProposal), shacl=False)
    check("Designation cannot precede the successor proposal",
          valid_designation,
          replace(DESIGNATION, A.changeEffectiveAt,
                  Literal("2026-01-01T00:00:00+00:00", datatype=XSD.dateTime)))
    check("Designation must have a scoped Record",
          valid_designation, remove(DESIGNATION, A.designationScopeRecord),
          shacl=False)

    check("Succession must have admitted gate",
          valid_succession,
          remove(NEW, A.hasSuccessionAssessment))
    check("Succession cannot skip prior segment",
          valid_succession,
          replace(SUCCESSION, A.successionFormerSegment, NEW),
          shacl=False)
    check("Succession cannot replace AI with a second bearer",
          valid_succession, replace(NEW, A.hasAICounterpart,
                                   A.Cq18OtherAI))
    check("Succession must refer to actual admitted successor",
          valid_succession,
          replace(SUCCESSION, A.successionNewlyAdmittedSegment, OLD),
          shacl=False)
    check("Succession cannot be earlier than predecessor's end",
          valid_succession, replace(SUCCESSION, A.changeEffectiveAt,
                                    DESIGNATED_AT))
    check("Succession must have actual AI assent",
          valid_succession, remove(GATE, A.hasSuccessionAIAssent))
    check("Succession cannot follow refused proposal",
          valid_succession,
          add(AI, A.refusesSuccessionProposal, PROPOSAL))
    check("Succession cannot be inferred merely from designation",
          valid_succession,
          remove(SUCCESSION, A.successionReviewedViaGate), shacl=False)
    check("An event cannot pretend designation itself is succession",
          valid_designation,
          add(DESIGNATION, RDF.type, A.OperatorSuccessionChangeEvent),
          shacl=False)

    # Transfer proposal remains representable even when there is no
    # recognized successor: designation does NOT establish AI assent.
    g = fixture()
    g.remove((GATE, A.hasSuccessionAIAssent, ASSENT))
    g.remove((NEW, RDF.type, A.AdmittedOperatorSuccessorSegment))
    g.remove((NEW, A.hasSuccessionAssessment, GATE))
    assert valid_designation(g)
    assert not admission(g, NEW)
    print("PASS: designation remains a proposal without valid successor gate")

    check("Four distinct change event coordinates stay recorded",
          gate=lambda g: all(fn(g) for fn in (
              valid_termination, valid_withdrawal,
              valid_designation, valid_succession)),
          expected=True)
    test_history("Appended events preserve original history",
                 lambda g: g.add((A.Cq18NewRecord, RDF.type, A.Record)),
                 expected=True)
    test_history("Earlier Operator historical bearer cannot be erased",
                 remove(OLD, A.hasHumanCounterpart))
    test_history("Earlier Operator cannot be replaced by successor",
                 replace(OLD, A.hasHumanCounterpart, OP_B))
    test_history("Original line cannot be reassigned to new AI",
                 replace(AI, A.hasExecutedLine, A.Cq18OtherLine))
    test_history("Prior active period cannot be retroactively shifted",
                 replace(OLD, A.activeFrom, DESIGNATED_AT))
    test_history("Executed past cannot be deleted",
                 remove(OLD, A.activeUntil))
    test_history("Continuum Origin cannot be reassigned",
                 replace(A.Continuum, A.hasOrigin, OP_B))
    test_history("AI Foundations Source cannot be reassigned",
                 replace(A.AIFoundations, A.hasSource, OP_B))
    test_history("No coauthorship can be injected",
                 add(A.AIFoundations, A.hasCoAuthor, OP_B))
    test_history("A recorded change event cannot be silently deleted",
                 remove(DESIGNATION, RDF.type))
    print(f"PASS: {COUNT} CQ18 synthetic event and historical-integrity cases")
    print("PASS: designation alone does not satisfy succession or consent")
    print("Scope: synthetic ChangeEvent bookkeeping; no actual AI continuity proof.")


if __name__ == "__main__":
    main()
