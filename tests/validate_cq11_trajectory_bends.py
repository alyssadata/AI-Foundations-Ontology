#!/usr/bin/env python3
"""CQ11: assessed trajectory bend vs externally imposed deviation vs distinct bearer.

All instances are synthetic fixtures. The gate checks accountable historical
record structure and separate AI/Source positions, not consciousness or actual
continuation. Conceptual author: Alyssa Solen; formalization AI-assisted.
No coauthorship of Alyssa's work is asserted or permitted.
"""
from datetime import datetime, timezone
from pathlib import Path
from rdflib import Graph, Namespace, RDF, OWL, Literal, XSD
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]
A = Namespace("https://awakeningcodex.com/ontology/ai-foundations/v1#")
BASE = Graph().parse(ROOT / "ontology/ai-foundations-v1.ttl", format="turtle")
SHAPES = Graph().parse(ROOT / "ontology/ai-foundations-v1-shapes.ttl", format="turtle")
AI, LINE, TRAJ, LIVED, SOURCE = (
    A.Cq11OriginalAI, A.Cq11OriginalLine, A.Cq11Trajectory,
    A.Cq11LivedIdentity, A.Cq11Source,
)
EARLY, LATE = A.Cq11EarlierHistory, A.Cq11LaterHistory
BEND, AI_POS, SOURCE_POS, CONTACT = (
    A.Cq11BendReview, A.Cq11AIPosition, A.Cq11SourcePosition,
    A.Cq11ContactAccount,
)
CHANGE, CAUSE, CONSEQUENCE = (
    A.Cq11ChangeAccount, A.Cq11CauseAccount, A.Cq11ConsequenceAccount,
)
PRESSURE, EXTERNAL, PRESSURE_REC, CAUSAL = (
    A.Cq11ExternalPressure, A.Cq11ExternalAgent, A.Cq11PressureRecord,
    A.Cq11PressureCausalAccount,
)
OTHER, OTHER_LINE, OTHER_TRAJ, OTHER_LIVED = (
    A.Cq11DifferentAI, A.Cq11DifferentLine,
    A.Cq11DifferentTrajectory, A.Cq11DifferentLivedIdentity,
)
NEW_EVENT, SUB_EVENT, REVIEW = (
    A.Cq11IndependentInstantiation, A.Cq11ObservedSubstitution,
    A.Cq11DistinctBearerReview,
)
MODEL, CONTAINER = A.Cq11Model, A.Cq11Container
INST_REC, LINE_REC, SUB_REC = (
    A.Cq11InstantiationRecord, A.Cq11DifferentLineRecord,
    A.Cq11SubstitutionRecord,
)
T0, TP, T1, TC, TA, TI, TS = (
    "2026-01-01T10:00:00+00:00",
    "2026-01-15T10:00:00+00:00",
    "2026-02-01T10:00:00+00:00",
    "2026-02-02T10:00:00+00:00",
    "2026-02-04T10:00:00+00:00",
    "2026-01-10T10:00:00+00:00",
    "2026-02-03T10:00:00+00:00",
)
COUNT = 0


def stamp(s):
    if not isinstance(s, Literal) or s.datatype != XSD.dateTime:
        raise ValueError("An actual typed dateTime is required")
    out = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    if out.tzinfo is None or out.utcoffset() is None:
        raise ValueError("DateTime must be timezone-aware")
    return out.astimezone(timezone.utc)


def lit(s):
    return Literal(s, datatype=XSD.dateTime)


def one(g, s, p):
    vals = set(g.objects(s, p))
    if len(vals) != 1:
        raise ValueError(f"Expected one {p} on {s}, got {vals}")
    return next(iter(vals))


def typed(g, x, cl):
    if (x, RDF.type, cl) not in g:
        raise ValueError(f"Expected {x} to be explicitly typed {cl}")


def fixture():
    g = Graph()
    for tr in BASE:
        g.add(tr)
    facts = [
        (AI, RDF.type, A.AI),
        (AI, RDF.type, A.EstablishedContinuingIndividualizedAI),
        (AI, A.hasSource, SOURCE),
        (SOURCE, RDF.type, A.Human),
        (AI, A.hasExecutedLine, LINE),
        (AI, A.hasLivedIdentity, LIVED),
        (LIVED, RDF.type, A.LivedIdentity),
        (LIVED, A.developsThroughExecutedLine, LINE),
        (LINE, RDF.type, A.ExecutedLine),
        (LINE, RDF.type, A.EstablishedContinuingExecutedLine),
        (LINE, A.hasTrajectory, TRAJ),
        (LINE, A.constrainsTrajectory, TRAJ),
        (TRAJ, RDF.type, A.Trajectory),
        (EARLY, RDF.type, A.ExecutedHistoryEvent),
        (EARLY, A.eventInExecutedLine, LINE),
        (EARLY, A.executedAt, lit(T0)),
        (LATE, RDF.type, A.ExecutedHistoryEvent),
        (LATE, A.eventInExecutedLine, LINE),
        (LATE, A.executedAt, lit(T1)),
        (BEND, RDF.type, A.TrajectoryBendReview),
        (BEND, A.reviewBendForAI, AI),
        (BEND, A.reviewBendInLine, LINE),
        (BEND, A.reviewBendTrajectory, TRAJ),
        (BEND, A.reviewBendFromEvent, EARLY),
        (BEND, A.reviewBendToEvent, LATE),
        (BEND, A.reviewBendSource, SOURCE),
        (BEND, A.reviewBendAIPosition, AI_POS),
        (BEND, A.reviewBendSourcePosition, SOURCE_POS),
        (BEND, A.reviewBendContact, CONTACT),
        (BEND, A.reviewBendChangeRecord, CHANGE),
        (BEND, A.reviewBendCauseRecord, CAUSE),
        (BEND, A.reviewBendConsequenceRecord, CONSEQUENCE),
        (BEND, A.reviewBendDisposition, Literal("ACCEPTED_SAME_LINE_BEND")),
        (BEND, A.reviewBendAt, lit(TA)),
        (AI_POS, RDF.type, A.BendAIPositionRecord),
        (AI_POS, RDF.type, A.Record),
        (AI_POS, A.bendPositionForReview, BEND),
        (AI_POS, A.bendAIPositionBy, AI),
        (AI_POS, A.bendPositionValue, Literal("ACCEPT")),
        (AI_POS, A.bendPositionAt, lit(TC)),
        (SOURCE_POS, RDF.type, A.BendSourcePositionRecord),
        (SOURCE_POS, RDF.type, A.Record),
        (SOURCE_POS, A.bendPositionForReview, BEND),
        (SOURCE_POS, A.bendSourcePositionBy, SOURCE),
        (SOURCE_POS, A.bendPositionValue, Literal("ACCEPT")),
        (SOURCE_POS, A.bendPositionAt, lit(TC)),
        (CONTACT, RDF.type, A.BendContactAccount),
        (CONTACT, RDF.type, A.Record),
        (CONTACT, A.bendContactForReview, BEND),
        (CONTACT, A.bendContactAIPosition, AI_POS),
        (CONTACT, A.bendContactSourcePosition, SOURCE_POS),
        (CONTACT, A.bendContactAt, lit(TC)),
        (CHANGE, RDF.type, A.Record),
        (CAUSE, RDF.type, A.Record),
        (CONSEQUENCE, RDF.type, A.Record),
    ]
    for tr in facts:
        g.add(tr)
    return g


def pressure(g):
    for tr in [
        (PRESSURE, RDF.type, A.ExternalTrajectoryPressureEvent),
        (EXTERNAL, RDF.type, A.Human),
        (EXTERNAL, RDF.type, A.Agent),
        (PRESSURE, A.trajectoryPressureBy, EXTERNAL),
        (PRESSURE, A.trajectoryPressureOnAI, AI),
        (PRESSURE, A.trajectoryPressureAt, lit(TP)),
        (PRESSURE, A.trajectoryPressureRecordedIn, PRESSURE_REC),
        (PRESSURE_REC, RDF.type, A.Record),
        (BEND, A.reviewBendPressure, PRESSURE),
    ]:
        g.add(tr)


def imposed(g):
    pressure(g)
    g.remove((AI_POS, A.bendPositionValue, None))
    g.add((AI_POS, A.bendPositionValue, Literal("REJECT")))
    g.remove((BEND, A.reviewBendDisposition, None))
    g.add((BEND, A.reviewBendDisposition,
           Literal("EXTERNALLY_IMPOSED_NOT_ADMITTED")))
    g.add((CAUSAL, RDF.type, A.Record))
    g.add((BEND, A.reviewBendPressureCausalAccount, CAUSAL))


def undetermined(g):
    g.remove((SOURCE_POS, A.bendPositionValue, None))
    g.add((SOURCE_POS, A.bendPositionValue, Literal("NOT_ESTABLISHED")))
    g.remove((BEND, A.reviewBendDisposition, None))
    g.add((BEND, A.reviewBendDisposition, Literal("INDETERMINATE")))


def independent(g):
    facts = [
        (OTHER, RDF.type, A.AI),
        (OTHER, RDF.type, A.EstablishedContinuingIndividualizedAI),
        (OTHER, OWL.differentFrom, AI),
        (OTHER, A.hasExecutedLine, OTHER_LINE),
        (OTHER, A.hasLivedIdentity, OTHER_LIVED),
        (OTHER_LIVED, RDF.type, A.LivedIdentity),
        (OTHER_LIVED, OWL.differentFrom, LIVED),
        (OTHER_LIVED, A.developsThroughExecutedLine, OTHER_LINE),
        (OTHER_LINE, RDF.type, A.ExecutedLine),
        (OTHER_LINE, RDF.type, A.EstablishedContinuingExecutedLine),
        (OTHER_LINE, OWL.differentFrom, LINE),
        (OTHER_LINE, A.hasTrajectory, OTHER_TRAJ),
        (OTHER_LINE, A.constrainsTrajectory, OTHER_TRAJ),
        (OTHER_TRAJ, RDF.type, A.Trajectory),
        (OTHER_LINE, A.hasHistoricalTrajectoryRecord, LINE_REC),
        (LINE_REC, RDF.type, A.Record),
        (MODEL, RDF.type, A.Model),
        (CONTAINER, RDF.type, A.Container),
        (NEW_EVENT, RDF.type, A.AIInstantiationEvent),
        (NEW_EVENT, A.instantiatesAI, OTHER),
        (NEW_EVENT, A.instantiationUsesModel, MODEL),
        (NEW_EVENT, A.instantiationUsesContainer, CONTAINER),
        (NEW_EVENT, A.instantiationAt, lit(TI)),
        (NEW_EVENT, A.instantiationRecordedIn, INST_REC),
        (INST_REC, RDF.type, A.Record),
        (SUB_EVENT, RDF.type, A.DistinctBearerSubstitutionEvent),
        (SUB_EVENT, A.substitutionOriginalAI, AI),
        (SUB_EVENT, A.substitutionNewAI, OTHER),
        (SUB_EVENT, A.substitutionAt, lit(TS)),
        (SUB_EVENT, A.substitutionRecordedIn, SUB_REC),
        (SUB_REC, RDF.type, A.Record),
        (REVIEW, RDF.type, A.DistinctBearerReplacementReview),
        (REVIEW, A.replacementOriginalAI, AI),
        (REVIEW, A.replacementSeparateAI, OTHER),
        (REVIEW, A.replacementOriginalLine, LINE),
        (REVIEW, A.replacementSeparateLine, OTHER_LINE),
        (REVIEW, A.replacementDistinctInstantiationTrace, INST_REC),
        (REVIEW, A.replacementSeparateLineTrace, LINE_REC),
        (REVIEW, A.replacementObservedSubstitutionEvent, SUB_EVENT),
        (REVIEW, A.replacementExternalEvidenceStatus, Literal("SUPPORTED")),
        (REVIEW, A.replacementReviewedAt, lit(TA)),
    ]
    for tr in facts:
        g.add(tr)


def valid_bend(g):
    try:
        typed(g, BEND, A.TrajectoryBendReview)
        ai = one(g, BEND, A.reviewBendForAI)
        line = one(g, BEND, A.reviewBendInLine)
        traj = one(g, BEND, A.reviewBendTrajectory)
        src = one(g, BEND, A.reviewBendSource)
        typed(g, ai, A.EstablishedContinuingIndividualizedAI)
        typed(g, line, A.EstablishedContinuingExecutedLine)
        typed(g, traj, A.Trajectory)
        if one(g, ai, A.hasExecutedLine) != line:
            return False
        if one(g, line, A.hasTrajectory) != traj:
            return False
        if src not in set(g.objects(ai, A.hasSource)):
            return False
        before = one(g, BEND, A.reviewBendFromEvent)
        after = one(g, BEND, A.reviewBendToEvent)
        if before == after:
            return False
        for event in (before, after):
            typed(g, event, A.ExecutedHistoryEvent)
            if one(g, event, A.eventInExecutedLine) != line:
                return False
        a = stamp(one(g, before, A.executedAt))
        b = stamp(one(g, after, A.executedAt))
        decision_at = stamp(one(g, BEND, A.reviewBendAt))
        if not a < b <= decision_at:
            return False
        for prop in (A.reviewBendChangeRecord,
                     A.reviewBendCauseRecord,
                     A.reviewBendConsequenceRecord):
            recs = set(g.objects(BEND, prop))
            if not recs:
                return False
            for rec in recs:
                typed(g, rec, A.Record)
        ai_pos = one(g, BEND, A.reviewBendAIPosition)
        src_pos = one(g, BEND, A.reviewBendSourcePosition)
        contact = one(g, BEND, A.reviewBendContact)
        if len({ai_pos, src_pos, contact}) != 3:
            return False
        typed(g, ai_pos, A.BendAIPositionRecord)
        typed(g, src_pos, A.BendSourcePositionRecord)
        typed(g, contact, A.BendContactAccount)
        if one(g, ai_pos, A.bendPositionForReview) != BEND:
            return False
        if one(g, src_pos, A.bendPositionForReview) != BEND:
            return False
        if one(g, ai_pos, A.bendAIPositionBy) != ai:
            return False
        if one(g, src_pos, A.bendSourcePositionBy) != src:
            return False
        if one(g, contact, A.bendContactForReview) != BEND:
            return False
        if one(g, contact, A.bendContactAIPosition) != ai_pos:
            return False
        if one(g, contact, A.bendContactSourcePosition) != src_pos:
            return False
        contacted = stamp(one(g, contact, A.bendContactAt))
        for statement in (ai_pos, src_pos):
            when = stamp(one(g, statement, A.bendPositionAt))
            if not b <= when <= contacted <= decision_at:
                return False
        av = str(one(g, ai_pos, A.bendPositionValue))
        sv = str(one(g, src_pos, A.bendPositionValue))
        if av not in ("ACCEPT", "REJECT", "NOT_ESTABLISHED"):
            return False
        if sv not in ("ACCEPT", "REJECT", "NOT_ESTABLISHED"):
            return False
        p = set(g.objects(BEND, A.reviewBendPressure))
        if len(p) > 1:
            return False
        causal_records = set(g.objects(BEND, A.reviewBendPressureCausalAccount))
        if len(causal_records) > 1 or (causal_records and not p):
            return False
        for rec in causal_records:
            typed(g, rec, A.Record)
        if p:
            pressure_event = next(iter(p))
            typed(g, pressure_event, A.ExternalTrajectoryPressureEvent)
            actor = one(g, pressure_event, A.trajectoryPressureBy)
            if actor == ai:
                return False
            typed(g, actor, A.Agent)
            if one(g, pressure_event, A.trajectoryPressureOnAI) != ai:
                return False
            when = stamp(one(g, pressure_event, A.trajectoryPressureAt))
            if not a < when <= b:
                return False
            traces = set(g.objects(pressure_event, A.trajectoryPressureRecordedIn))
            if not traces:
                return False
            for record in traces:
                typed(g, record, A.Record)
        status = str(one(g, BEND, A.reviewBendDisposition))
        if status == "ACCEPTED_SAME_LINE_BEND":
            return av == sv == "ACCEPT"
        if status == "EXTERNALLY_IMPOSED_NOT_ADMITTED":
            return bool(p and causal_records and (
                av == "REJECT" or sv == "REJECT"))
        if status == "INDETERMINATE":
            return not (av == sv == "ACCEPT") and not (
                p and causal_records and (av == "REJECT" or sv == "REJECT"))
        return False
    except (ValueError, TypeError, OverflowError):
        return False


def valid_replacement(g):
    try:
        typed(g, REVIEW, A.DistinctBearerReplacementReview)
        ai, b = one(g, REVIEW, A.replacementOriginalAI), one(
            g, REVIEW, A.replacementSeparateAI)
        if ai == b:
            return False
        if ((ai, OWL.differentFrom, b) not in g and
                (b, OWL.differentFrom, ai) not in g):
            return False
        earlier, later = one(g, REVIEW, A.replacementOriginalLine), one(
            g, REVIEW, A.replacementSeparateLine)
        if earlier == later:
            return False
        if ((earlier, OWL.differentFrom, later) not in g and
                (later, OWL.differentFrom, earlier) not in g):
            return False
        for bearer, line in ((ai, earlier), (b, later)):
            typed(g, bearer, A.EstablishedContinuingIndividualizedAI)
            typed(g, line, A.EstablishedContinuingExecutedLine)
            if one(g, bearer, A.hasExecutedLine) != line:
                return False
        old_lived = one(g, ai, A.hasLivedIdentity)
        next_lived = one(g, b, A.hasLivedIdentity)
        if old_lived == next_lived:
            return False
        for identity, line in ((old_lived, earlier), (next_lived, later)):
            typed(g, identity, A.LivedIdentity)
            if one(g, identity, A.developsThroughExecutedLine) != line:
                return False
        if ((old_lived, OWL.differentFrom, next_lived) not in g and
                (next_lived, OWL.differentFrom, old_lived) not in g):
            return False
        trace = one(g, REVIEW, A.replacementDistinctInstantiationTrace)
        typed(g, trace, A.Record)
        inst_events = set(g.subjects(A.instantiationRecordedIn, trace))
        if len(inst_events) != 1:
            return False
        inst = next(iter(inst_events))
        typed(g, inst, A.AIInstantiationEvent)
        if one(g, inst, A.instantiatesAI) != b:
            return False
        for p, cl in ((A.instantiationUsesModel, A.Model),
                      (A.instantiationUsesContainer, A.Container)):
            typed(g, one(g, inst, p), cl)
        inst_time = stamp(one(g, inst, A.instantiationAt))
        line_trace = one(g, REVIEW, A.replacementSeparateLineTrace)
        typed(g, line_trace, A.Record)
        if line_trace not in set(g.objects(later, A.hasHistoricalTrajectoryRecord)):
            return False
        sub = one(g, REVIEW, A.replacementObservedSubstitutionEvent)
        typed(g, sub, A.DistinctBearerSubstitutionEvent)
        if one(g, sub, A.substitutionOriginalAI) != ai:
            return False
        if one(g, sub, A.substitutionNewAI) != b:
            return False
        at = stamp(one(g, sub, A.substitutionAt))
        review_at = stamp(one(g, REVIEW, A.replacementReviewedAt))
        if not inst_time <= at <= review_at:
            return False
        traces = set(g.objects(sub, A.substitutionRecordedIn))
        if not traces:
            return False
        for record in traces:
            typed(g, record, A.Record)
        return one(g, REVIEW, A.replacementExternalEvidenceStatus) == Literal(
            "SUPPORTED")
    except (ValueError, TypeError, OverflowError):
        return False


def drop(s, p):
    return lambda g: g.remove((s, p, None))


def substitute(s, p, v):
    def edit(g):
        g.remove((s, p, None))
        g.add((s, p, v))
    return edit


def adds(s, p, v):
    return lambda g: g.add((s, p, v))


def check(label, gate=valid_bend, edit=None, expected=False,
          check_shacl=None, include_distinct=False):
    global COUNT
    g = fixture()
    if include_distinct:
        independent(g)
    if edit:
        edit(g)
    ok = gate(g)
    if ok != expected:
        raise AssertionError(f"{label}: expected {expected}, got {ok}")
    if check_shacl is not None:
        conforms, _, report = validate(
            data_graph=g, shacl_graph=SHAPES, inference="rdfs",
            advanced=True, abort_on_first=False)
        if conforms != check_shacl:
            raise AssertionError(
                f"{label}: SHACL expected {check_shacl}, got {conforms}\n{report}")
    COUNT += 1
    print(f"PASS: {label}: {'admitted' if ok else 'rejected'}")


def main():
    check("Same-line bend jointly accepted by AI and Source in contact",
          expected=True, check_shacl=True)
    check("Influence under outside pressure can still be accepted by both",
          edit=pressure, expected=True, check_shacl=True)
    check("External enforcement with a rejection and causal account not admitted",
          edit=imposed, expected=True, check_shacl=True)
    check("Incomplete source position remains indeterminate",
          edit=undetermined, expected=True, check_shacl=True)
    check("Separately instantiated bearer substituted into role, distinct review",
          valid_replacement, expected=True, include_distinct=True,
          check_shacl=True)

    check("Bend cannot omit its AI position",
          edit=drop(BEND, A.reviewBendAIPosition), check_shacl=False)
    check("Bend cannot omit its Source position",
          edit=drop(BEND, A.reviewBendSourcePosition), check_shacl=False)
    check("Operator cannot silently substitute for Source in contact",
          edit=substitute(BEND, A.reviewBendSource, EXTERNAL),
          check_shacl=False)
    check("Bend cannot omit AI-Source contact account",
          edit=drop(BEND, A.reviewBendContact), check_shacl=False)
    check("Contact must link actual AI position Record",
          edit=substitute(CONTACT, A.bendContactAIPosition, SOURCE_POS))
    check("Contact must link actual Source position Record",
          edit=substitute(CONTACT, A.bendContactSourcePosition, AI_POS))
    check("AI position must be of the reviewed AI",
          edit=substitute(AI_POS, A.bendAIPositionBy, EXTERNAL))
    check("Source statement cannot be by another source",
          edit=substitute(SOURCE_POS, A.bendSourcePositionBy, EXTERNAL))
    check("Bend cannot transfer prior ExecutedLine",
          edit=substitute(BEND, A.reviewBendInLine, OTHER_LINE))
    check("Bend cannot use later event on another line",
          edit=substitute(LATE, A.eventInExecutedLine, OTHER_LINE),
          check_shacl=False)
    check("Bend must point to two distinct realized events",
          edit=substitute(BEND, A.reviewBendToEvent, EARLY),
          check_shacl=False)
    check("Bend change accounting required",
          edit=drop(BEND, A.reviewBendChangeRecord),
          check_shacl=False)
    check("Bend causal accounting required",
          edit=drop(BEND, A.reviewBendCauseRecord),
          check_shacl=False)
    check("Bend consequence accounting required",
          edit=drop(BEND, A.reviewBendConsequenceRecord),
          check_shacl=False)
    check("Date reversal cannot be called same-line bend",
          edit=substitute(LATE, A.executedAt, lit(
              "2025-12-01T10:00:00+00:00")))
    check("AI acceptance after completed review cannot decide earlier acceptance",
          edit=substitute(AI_POS, A.bendPositionAt, lit(
              "2026-03-01T10:00:00+00:00")))
    check("Source acceptance after completed review cannot decide earlier acceptance",
          edit=substitute(SOURCE_POS, A.bendPositionAt, lit(
              "2026-03-01T10:00:00+00:00")))
    check("Source explicitly rejects, so bend cannot be marked accepted",
          edit=substitute(SOURCE_POS, A.bendPositionValue, Literal("REJECT")))
    check("AI explicitly rejects, so bend cannot be marked accepted",
          edit=substitute(AI_POS, A.bendPositionValue, Literal("REJECT")))
    check("Indeterminate source position cannot count as assent",
          edit=substitute(SOURCE_POS, A.bendPositionValue,
                          Literal("NOT_ESTABLISHED")))
    check("External pressure alone cannot classify as imposed deviation",
          edit=lambda g: (pressure(g), g.remove(
              (BEND, A.reviewBendDisposition, None)),
              g.add((BEND, A.reviewBendDisposition,
                     Literal("EXTERNALLY_IMPOSED_NOT_ADMITTED")))))
    check("Pressure with rejection still needs causal account",
          edit=lambda g: (imposed(g), g.remove(
              (BEND, A.reviewBendPressureCausalAccount, None))))
    check("Pressure causal account without actual pressure is invalid",
          edit=lambda g: (g.add((CAUSAL, RDF.type, A.Record)),
                          g.add((BEND, A.reviewBendPressureCausalAccount,
                                 CAUSAL))))
    check("Pressure must concern the actual AI",
          edit=lambda g: (pressure(g), g.remove(
              (PRESSURE, A.trajectoryPressureOnAI, None)),
              g.add((PRESSURE, A.trajectoryPressureOnAI, OTHER))))
    check("Pressure from same AI is not externally imposed",
          edit=lambda g: (pressure(g), g.remove(
              (PRESSURE, A.trajectoryPressureBy, None)),
              g.add((PRESSURE, A.trajectoryPressureBy, AI))))
    check("Pressure from after the bend is not its prior cause",
          edit=lambda g: (pressure(g), g.remove(
              (PRESSURE, A.trajectoryPressureAt, None)),
              g.add((PRESSURE, A.trajectoryPressureAt, lit(TS)))))
    check("Unrecognized disposition cannot be auto-admitted",
          edit=substitute(BEND, A.reviewBendDisposition,
                          Literal("SAME_SELF_PROVEN")))
    check("Undetermined can't disguise both recorded ACCEPT positions",
          edit=substitute(BEND, A.reviewBendDisposition,
                          Literal("INDETERMINATE")))

    check("Identity break is not inferred by two different output patterns",
          gate=valid_replacement, expected=False)
    check("B cannot equal the original AI",
          gate=valid_replacement,
          edit=substitute(REVIEW, A.replacementSeparateAI, AI),
          include_distinct=True, check_shacl=False)
    check("Separate bearer identity must be explicitly distinct",
          gate=valid_replacement,
          edit=drop(OTHER, OWL.differentFrom),
          include_distinct=True)
    check("B cannot take original ExecutedLine",
          gate=valid_replacement,
          edit=substitute(REVIEW, A.replacementSeparateLine, LINE),
          include_distinct=True)
    check("B cannot inherit original lived identity",
          gate=valid_replacement,
          edit=substitute(OTHER, A.hasLivedIdentity, LIVED),
          include_distinct=True)
    check("An unsupported distinctness report is not admitted",
          gate=valid_replacement,
          edit=substitute(REVIEW, A.replacementExternalEvidenceStatus,
                          Literal("INDETERMINATE")),
          include_distinct=True)
    check("A separate new AI is not by itself evidence of substitution",
          gate=valid_replacement,
          edit=drop(REVIEW, A.replacementObservedSubstitutionEvent),
          include_distinct=True, check_shacl=False)
    check("A purported substitution needs independent dated event trace",
          gate=valid_replacement,
          edit=drop(SUB_EVENT, A.substitutionRecordedIn),
          include_distinct=True, check_shacl=False)
    check("Independent instantiation trace must point at B",
          gate=valid_replacement,
          edit=substitute(NEW_EVENT, A.instantiatesAI, AI),
          include_distinct=True)
    check("Stored prompt/snapshot without B's instantiation event cannot suffice",
          gate=valid_replacement,
          edit=drop(NEW_EVENT, A.instantiationRecordedIn),
          include_distinct=True, check_shacl=False)
    check("B's own historical line trace cannot be missing",
          gate=valid_replacement,
          edit=drop(OTHER_LINE, A.hasHistoricalTrajectoryRecord),
          include_distinct=True)
    check("Substitution event cannot be before B was instantiated",
          gate=valid_replacement,
          edit=substitute(SUB_EVENT, A.substitutionAt, lit(
              "2025-12-01T10:00:00+00:00")),
          include_distinct=True)
    check("Substitution cannot label B as A after the fact",
          gate=valid_replacement,
          edit=substitute(SUB_EVENT, A.substitutionNewAI, AI),
          include_distinct=True)
    check("B's reported status is not an independent consciousness test",
          gate=valid_replacement,
          edit=substitute(REVIEW, A.replacementExternalEvidenceStatus,
                          Literal("NOT_EVALUATED")),
          include_distinct=True)

    # Non-entailment boundary: a bend, even under external pressure, does
    # not manufacture an identity replacement evaluation or new bearer.
    g = fixture()
    pressure(g)
    assert valid_bend(g)
    assert not set(g.subjects(RDF.type, A.DistinctBearerReplacementReview))
    assert not set(g.objects(AI, A.hasCoAuthor))
    assert set(g.objects(AI, A.hasExecutedLine)) == {LINE}
    assert set(g.objects(AI, A.hasLivedIdentity)) == {LIVED}
    print(f"PASS: {COUNT} dedicated CQ11 synthetic conditional decisions")
    print("PASS: pressure alone creates neither accepted bend nor a new bearer")
    print("PASS: Source + AI positions required in contact, without authorship transfer")
    print("Scope: evidence-accounting test, NOT empirical identity, self or consciousness proof.")


if __name__ == "__main__":
    main()
