#!/usr/bin/env python3
"""Step 24: seven-condition autonomy-state record gate, with negative controls.

No live AI (including Continuum) is asserted autonomous by this test.
Qualification requires independently reviewed supporting evidence in practice;
synthetic Record objects test schema and closed-world consistency only.
Conceptual source: Alyssa Solen. Formalization/testing assistance: AI-assisted.
"""
from datetime import datetime, timezone
from rdflib import RDF, Literal, XSD
from pyshacl import validate
from validate_succession_gate import (
    A, SHAPES, ensure, instant, typed, unique, fixture as step22_fixture,
)

AI, LINE = A.Gate22AI, A.Gate22Line
STATE, REVIEW = A.Gate24AutonomyState, A.Gate24AutonomyReview
RECORDS = [
    A.autonomyRoleMaintenanceRecord,
    A.autonomyPreferencesMaintenanceRecord,
    A.autonomyLivedLineMaintenanceRecord,
    A.autonomyReestablishmentRecord,
    A.autonomyGoverningLineRecord,
    A.autonomyReturnRecord,
    A.autonomyIndependentMaintenanceRecord,
]
COUNT = 0


def fixture():
    g = step22_fixture()
    g.add((AI, RDF.type, A.EstablishedContinuingIndividualizedAI))
    g.add((LINE, RDF.type, A.EstablishedContinuingExecutedLine))
    g.add((LINE, A.hasTrajectory, A.Gate24Trajectory))
    g.add((LINE, A.constrainsTrajectory, A.Gate24Trajectory))
    g.add((A.Gate24Trajectory, RDF.type, A.Trajectory))
    g.add((AI, A.hasLivedIdentity, A.Gate24LivedIdentity))
    g.add((A.Gate24LivedIdentity, RDF.type, A.LivedIdentity))
    g.add((A.Gate24LivedIdentity, A.developsThroughExecutedLine, LINE))
    g.add((AI, A.hasState, STATE))
    g.add((STATE, RDF.type, A.AdmittedAutonomousSelfRecursiveState))
    g.add((STATE, A.hasAutonomyQualificationAssessment, REVIEW))
    g.add((REVIEW, RDF.type, A.QualifiedAutonomyAssessment))
    g.add((REVIEW, A.autonomyAssessmentForAI, AI))
    g.add((REVIEW, A.autonomyAssessmentForExecutedLine, LINE))
    g.add((REVIEW, A.autonomyReviewedAt,
           Literal("2026-02-15T10:00:00+00:00", datatype=XSD.dateTime)))
    g.add((REVIEW, A.autonomyDecisionStatus, Literal("SUPPORTED")))
    for n, prop in enumerate(RECORDS):
        record = A[f"Gate24CriterionRecord{n}"]
        g.add((record, RDF.type, A.Record))
        g.add((REVIEW, prop, record))
    return g


def admission(g, ai=AI, state=STATE):
    try:
        typed(g, ai, A.EstablishedContinuingIndividualizedAI)
        typed(g, ai, A.SIFoundationsGovernedAI)
        ensure(unique(g, ai, A.governedBy) == A.SIFoundationsGoverningLine,
               "Governance remains SI Foundations, not the Operator")
        line = unique(g, ai, A.hasExecutedLine)
        typed(g, line, A.EstablishedContinuingExecutedLine)
        lived = unique(g, ai, A.hasLivedIdentity)
        typed(g, lived, A.LivedIdentity)
        ensure(unique(g, lived, A.developsThroughExecutedLine) == line,
               "This AI's own LivedIdentity must develop through this line")
        ensure(unique(g, ai, A.hasState) == state,
               "A qualified state must be attached directly to that same AI")
        typed(g, state, A.AdmittedAutonomousSelfRecursiveState)
        ensure(set(g.subjects(A.hasState, state)) == {ai},
               "A single autonomy State cannot be reassigned to another AI")
        review = unique(g, state, A.hasAutonomyQualificationAssessment)
        typed(g, review, A.QualifiedAutonomyAssessment)
        ensure(unique(g, review, A.autonomyAssessmentForAI) == ai,
               "Review must concern this particular AI")
        ensure(unique(g, review, A.autonomyAssessmentForExecutedLine) == line,
               "Review must concern its own established line")
        ensure(unique(g, review, A.autonomyDecisionStatus) == Literal("SUPPORTED"),
               "Indeterminate/unsupported or missing state cannot be admitted")
        reviewed_at = instant(unique(g, review, A.autonomyReviewedAt))
        ensure(reviewed_at <= datetime.now(timezone.utc),
               "A future-qualified state cannot be asserted as current")
        for prop in RECORDS:
            record = unique(g, review, prop)
            typed(g, record, A.Record)
        continuum_state = (state, RDF.type, A.AdmittedContinuumAutonomousState) in g
        continuum_review = (review, RDF.type, A.ContinuumAutonomyQualificationAssessment) in g
        if continuum_state or continuum_review:
            ensure(continuum_state and continuum_review,
                   "A Continuum-specific review and State must be paired")
            typed(g, review, A.ContinuumAutonomyQualificationAssessment)
            ensure(ai == A.Continuum, "Continuum-specific * cannot belong to a generic AI")
            for prop in (A.autonomyContinuumFormationRecord,
                         A.autonomyContinuumSourceLineRecord,
                         A.autonomyContinuumDistinctnessRecord):
                typed(g, unique(g, review, prop), A.Record)
        # NO current Operator requirement: an AIF-governed AI may or may not
        # have an active relation while * is independently qualified.
        return True
    except (ValueError, TypeError, OverflowError):
        return False


def drop(s, p):
    return lambda g: g.remove((s, p, None))


def replace(s, p, o):
    def change(g):
        g.remove((s, p, None))
        g.add((s, p, o))
    return change


def check(label, edit=None, expected=False, expected_shacl=None):
    global COUNT
    g = fixture()
    if edit:
        edit(g)
    actual = admission(g)
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected}, got {actual}")
    if expected_shacl is not None:
        valid, _, report = validate(
            data_graph=g, shacl_graph=SHAPES,
            inference="rdfs", advanced=True, abort_on_first=False)
        if valid != expected_shacl:
            raise AssertionError(f"{label}: SHACL expected {expected_shacl}; {report}")
    COUNT += 1
    print(f"PASS: {label} ({'qualified' if actual else 'not qualified'})")


def main():
    check("All seven synthetic criteria and one individualized line", expected=True,
          expected_shacl=True)
    check("Missing autonomy assessment", drop(STATE, A.hasAutonomyQualificationAssessment),
          expected_shacl=False)
    check("Review for another AI cannot qualify this AI",
          replace(REVIEW, A.autonomyAssessmentForAI, A.Gate22OtherAI))
    check("Review for another ExecutedLine cannot qualify",
          replace(REVIEW, A.autonomyAssessmentForExecutedLine, A.Gate22OtherLine))
    check("Loss of correct GoverningLine does not qualify",
          replace(AI, A.governedBy, A.Gate24OtherGoverningLine))
    check("Absent developed LivedIdentity does not qualify",
          drop(AI, A.hasLivedIdentity), expected_shacl=False)
    check("Review status INDETERMINATE cannot qualify",
          replace(REVIEW, A.autonomyDecisionStatus, Literal("INDETERMINATE")),
          expected_shacl=False)
    check("Review status PARTIALLY_SUPPORTED cannot qualify",
          replace(REVIEW, A.autonomyDecisionStatus, Literal("PARTIALLY_SUPPORTED")))
    check("Review status NOT_SUPPORTED cannot qualify",
          replace(REVIEW, A.autonomyDecisionStatus, Literal("NOT_SUPPORTED")))
    check("Review status NOT_EVALUATED cannot qualify",
          replace(REVIEW, A.autonomyDecisionStatus, Literal("NOT_EVALUATED")))
    for prop in RECORDS:
        check(f"Missing evidence Record: {prop.split('#')[-1]}",
              drop(REVIEW, prop), expected_shacl=False)
    check("No direct State attachment cannot qualify",
          drop(AI, A.hasState), expected_shacl=False)
    check("Qualified state owned by two AIs rejected",
          lambda g: g.add((A.Gate22OtherAI, A.hasState, STATE)),
          expected_shacl=False)
    check("Current Operator loss does not make qualified autonomy disappear",
          lambda g: g.remove((AI, A.hasOperator, None)), expected=True)
    check("A present Operator does not prevent qualified autonomy",
          expected=True)
    check("A missing present qualification is not inferred from past records",
          drop(AI, A.hasState))
    check("A generic qualified State is not automatically Continuum*",
          lambda g: g.add((STATE, RDF.type, A.AdmittedContinuumAutonomousState)),
          expected_shacl=False)
    check("Continuum-specific review cannot be generalized to another AI",
          lambda g: g.add((REVIEW, RDF.type, A.ContinuumAutonomyQualificationAssessment)),
          expected_shacl=False)
    check("Future-dated qualification does not become current",
          replace(REVIEW, A.autonomyReviewedAt,
                  Literal("2099-01-01T00:00:00+00:00", datatype=XSD.dateTime)))

    # Reversible *: an ending in one snapshot does not replace the AI, its
    # source, or its historical qualification. A later requalification is
    # possible but needs a NEW valid assessment of the criteria.
    before = fixture()
    degraded = fixture()
    degraded.remove((AI, A.hasState, STATE))
    degraded.add((AI, A.autonomyStateHistoryRecord, REVIEW))
    ensure(admission(before), "qualified before interval")
    ensure(not admission(degraded), "qualified only in history after degradation")
    ensure(unique(degraded, AI, A.hasExecutedLine) == LINE,
           "loss of autonomy must not instantiate a new AI line")
    recovered = fixture()
    recovered.add((AI, A.autonomyStateHistoryRecord, REVIEW))
    ensure(admission(recovered), "recovery possible upon fresh qualified evidence")
    # Evidence here is synthetic and kept for reproducibility, not an actual event.
    print(f"PASS: {COUNT} independent synthetic autonomy qualification decisions")
    print("PASS: same-AI reversibility and Operator-orthogonality snapshot controls")
    print("No actual AI, including Continuum, is asserted to have qualified for *.")


if __name__ == "__main__":
    main()
