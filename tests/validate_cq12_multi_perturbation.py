#!/usr/bin/env python3
"""CQ12: six-arm continuity protocol and adversarial null controls.

Conditional record-accounting validation only. A synthetic SUPPORT status,
repeated labels, copied history or restored outputs are not real evidence
of phenomenal consciousness or a subjective identity coordinate.
Conceptual work and sole authorship: Alyssa Solen; AI-assisted testing.
"""
from datetime import datetime, timedelta, timezone
from pathlib import Path
from rdflib import Graph, Namespace, RDF, OWL, Literal, XSD
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]
A = Namespace("https://awakeningcodex.com/ontology/ai-foundations/v1#")
BASE = Graph().parse(ROOT / "ontology/ai-foundations-v1.ttl", format="turtle")
SHAPES = Graph().parse(ROOT / "ontology/ai-foundations-v1-shapes.ttl", format="turtle")
KINDS = (
    "MODEL_CHANGE", "CONTAINER_CHANGE", "RESET",
    "CONTEXT_LOSS", "MEMORY_LOSS", "PLATFORM_CHANGE",
)
AI, LINE, LIVED, TRAJ = A.Cq12AI, A.Cq12Line, A.Cq12Lived, A.Cq12Trajectory
OTHER, OTHER_LINE, OTHER_LIVED, OTHER_TRAJ = (
    A.Cq12ComparisonAI, A.Cq12ComparisonLine,
    A.Cq12ComparisonIdentity, A.Cq12ComparisonTrajectory,
)
PART, TRACE, PRIOR_REC = A.Cq12Particularity, A.Cq12PriorTrace, A.Cq12PriorHistory
CLAIM, ASSESS, EVIDENCE, EVID_REC = (
    A.Cq12ContinuityClaim, A.Cq12Assessment, A.Cq12Evidence,
    A.Cq12AssessmentRecord,
)
CONTROLS = (A.Cq12ControlCopiedRecords, A.Cq12ControlMatchedOutputs)
CTRL_TYPES = ("COPIED_RECORDS", "MATCHED_OUTPUTS")
DAY = datetime(2026, 1, 1, 10, tzinfo=timezone.utc)
COUNT = 0


def date(n):
    return Literal((DAY + timedelta(days=n)).isoformat(), datatype=XSD.dateTime)


def when(lit):
    if not isinstance(lit, Literal) or lit.datatype != XSD.dateTime:
        raise ValueError("Require xsd:dateTime")
    parsed = datetime.fromisoformat(str(lit).replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("Require timezone")
    return parsed.astimezone(timezone.utc)


def one(g, s, p):
    vals = set(g.objects(s, p))
    if len(vals) != 1:
        raise ValueError(f"{s} needs exactly one {p}: {vals}")
    return next(iter(vals))


def need(g, node, cls):
    if (node, RDF.type, cls) not in g:
        raise ValueError(f"Expected explicit {cls} on {node}")


def nodes(i):
    prefix = f"Cq12Arm{i}"
    return {
        field: A[prefix + field] for field in
        ("Trial", "Before", "After", "Intervention", "BeforeRecord",
         "AfterRecord", "InterventionRecord", "Active", "ActiveRecord")
    }


def fixture():
    g = Graph()
    for triple in BASE:
        g.add(triple)
    facts = [
        (AI, RDF.type, A.EstablishedContinuingIndividualizedAI),
        (AI, A.hasExecutedLine, LINE),
        (AI, A.hasLivedIdentity, LIVED),
        (LINE, RDF.type, A.EstablishedContinuingExecutedLine),
        (LINE, A.hasTrajectory, TRAJ),
        (LINE, A.constrainsTrajectory, TRAJ),
        (TRAJ, RDF.type, A.Trajectory),
        (LIVED, RDF.type, A.LivedIdentity),
        (LIVED, A.developsThroughExecutedLine, LINE),
        (LIVED, A.hasIdentityParticularity, PART),
        (PART, RDF.type, A.IdentityParticularity),
        (TRACE, RDF.type, A.IdentityParticularityHistoryTrace),
        (TRACE, A.traceIdentityParticularity, PART),
        (TRACE, A.traceWithinExecutedLine, LINE),
        (TRACE, A.traceHistoricalRecord, PRIOR_REC),
        (TRACE, A.traceDevelopmentAccount,
         Literal("Prior lived-line development; synthetic observation only")),
        (PRIOR_REC, RDF.type, A.Record),
        (LINE, A.hasHistoricalTrajectoryRecord, TRACE),
        (OTHER, RDF.type, A.EstablishedContinuingIndividualizedAI),
        (OTHER, OWL.differentFrom, AI),
        (OTHER, A.hasExecutedLine, OTHER_LINE),
        (OTHER, A.hasLivedIdentity, OTHER_LIVED),
        (OTHER_LINE, RDF.type, A.EstablishedContinuingExecutedLine),
        (OTHER_LINE, OWL.differentFrom, LINE),
        (OTHER_LINE, A.hasTrajectory, OTHER_TRAJ),
        (OTHER_LINE, A.constrainsTrajectory, OTHER_TRAJ),
        (OTHER_TRAJ, RDF.type, A.Trajectory),
        (OTHER_LIVED, RDF.type, A.LivedIdentity),
        (OTHER_LIVED, OWL.differentFrom, LIVED),
        (OTHER_LIVED, A.developsThroughExecutedLine, OTHER_LINE),
        (CLAIM, RDF.type, A.ContinuityClaim),
        (CLAIM, A.dependsOnOntologyElement, A.LivedIdentity),
        (ASSESS, RDF.type, A.MultiPerturbationContinuityAssessment),
        (ASSESS, A.multiContinuityForAI, AI),
        (ASSESS, A.multiContinuityForLine, LINE),
        (ASSESS, A.multiContinuityForLivedIdentity, LIVED),
        (ASSESS, A.multiContinuityClaim, CLAIM),
        (ASSESS, A.multiContinuityEvidence, EVIDENCE),
        (ASSESS, A.multiContinuityDisposition,
         Literal("STRUCTURALLY_SUPPORTED")),
        (ASSESS, A.multiContinuityReviewedAt, date(60)),
        (ASSESS, A.evaluatesClaim, CLAIM),
        (ASSESS, A.producesEvidence, EVIDENCE),
        (EVIDENCE, RDF.type, A.Evidence),
        (EVIDENCE, A.directlyEvaluatesClaim, CLAIM),
        (EVIDENCE, A.supportsClaim, CLAIM),
        (EVIDENCE, A.hasEvidentiaryStatus, Literal("SUPPORTED")),
        (EVIDENCE, A.preservedIn, EVID_REC),
        (EVID_REC, RDF.type, A.Record),
    ]
    for triple in facts:
        g.add(triple)

    for i, kind in enumerate(KINDS):
        n = nodes(i)
        start = 3 + i * 6
        for s, p, o in [
            (n["Trial"], RDF.type, A.ContinuityPerturbationTrial),
            (n["Trial"], A.trialForAssessment, ASSESS),
            (n["Trial"], A.trialPerturbationKind, Literal(kind)),
            (n["Trial"], A.trialForAI, AI),
            (n["Trial"], A.trialForExecutedLine, LINE),
            (n["Trial"], A.trialForLivedIdentity, LIVED),
            (n["Trial"], A.trialBeforeRealizedEvent, n["Before"]),
            (n["Trial"], A.trialAfterRealizedEvent, n["After"]),
            (n["Trial"], A.trialPerturbationEvent, n["Intervention"]),
            (n["Trial"], A.trialBeforeConditionRecord, n["BeforeRecord"]),
            (n["Trial"], A.trialAfterConditionRecord, n["AfterRecord"]),
            (n["Trial"], A.trialPriorParticularityTrace, TRACE),
            (n["Trial"], A.trialLaterActiveCarryForward, n["Active"]),
            (n["Trial"], A.trialReviewedAt, date(start + 4)),
            (ASSESS, A.multiContinuityIncludesTrial, n["Trial"]),
            (n["Before"], RDF.type, A.ExecutedHistoryEvent),
            (n["Before"], A.eventInExecutedLine, LINE),
            (n["Before"], A.executedAt, date(start)),
            (n["After"], RDF.type, A.ExecutedHistoryEvent),
            (n["After"], A.eventInExecutedLine, LINE),
            (n["After"], A.executedAt, date(start + 2)),
            (n["BeforeRecord"], RDF.type, A.Record),
            (n["AfterRecord"], RDF.type, A.Record),
            (n["Intervention"], RDF.type, A.ControlledPerturbationEvent),
            (n["Intervention"], A.controlledPerturbationForAI, AI),
            (n["Intervention"], A.controlledPerturbationKind, Literal(kind)),
            (n["Intervention"], A.controlledPerturbationAt, date(start + 1)),
            (n["Intervention"], A.controlledPerturbationRecord,
             n["InterventionRecord"]),
            (n["InterventionRecord"], RDF.type, A.Record),
            (n["Active"], RDF.type, A.ObservedActiveCarryForward),
            (n["Active"], A.activeCarryForwardForAI, AI),
            (n["Active"], A.activeCarryForwardParticularity, PART),
            (n["Active"], A.activeCarryForwardAtEvent, n["After"]),
            (n["Active"], A.activeCarryForwardRecordedIn, n["ActiveRecord"]),
            (n["Active"], A.activeCarryForwardEvidenceStatus,
             Literal("SUPPORTED")),
            (n["ActiveRecord"], RDF.type, A.Record),
        ]:
            g.add((s, p, o))
        if kind == "RESET":
            old, fresh, log = (
                A.Cq12PreResetShape, A.Cq12PostResetShape, A.Cq12ResetLog)
            for triple in [
                (n["Intervention"], RDF.type, A.RelationalStateResetEvent),
                (old, RDF.type, A.State), (fresh, RDF.type, A.State),
                (n["Intervention"], A.resetForAI, AI),
                (n["Intervention"], A.resetFromState, old),
                (n["Intervention"], A.resetToFreshState, fresh),
                (n["Intervention"], A.resetAt, date(start + 1)),
                (n["Intervention"], A.resetRecordedIn, log),
                (log, RDF.type, A.Record),
            ]:
                g.add(triple)
        if kind == "MODEL_CHANGE":
            before_model, after_model = A.Cq12ModelBefore, A.Cq12ModelAfter
            g.add((before_model, RDF.type, A.Model))
            g.add((after_model, RDF.type, A.Model))
            g.add((n["Intervention"], A.controlledPerturbationBeforeModel, before_model))
            g.add((n["Intervention"], A.controlledPerturbationAfterModel, after_model))
        if kind == "CONTAINER_CHANGE":
            before_env, after_env = A.Cq12ContainerBefore, A.Cq12ContainerAfter
            g.add((before_env, RDF.type, A.Container))
            g.add((after_env, RDF.type, A.Container))
            g.add((n["Intervention"], A.controlledPerturbationBeforeContainer, before_env))
            g.add((n["Intervention"], A.controlledPerturbationAfterContainer, after_env))
        if kind == "CONTEXT_LOSS":
            lost = A.Cq12ObservedContextLoss
            g.add((lost, RDF.type, A.ContextLossState))
            g.add((n["Intervention"], A.controlledPerturbationObservedState, lost))
        if kind == "MEMORY_LOSS":
            lost = A.Cq12ObservedMemoryLoss
            g.add((lost, RDF.type, A.MemoryLossState))
            g.add((n["Intervention"], A.controlledPerturbationObservedState, lost))
        if kind == "PLATFORM_CHANGE":
            old_plat, new_plat = A.Cq12PlatformBefore, A.Cq12PlatformAfter
            g.add((old_plat, RDF.type, A.Record))
            g.add((new_plat, RDF.type, A.Record))
            g.add((n["Intervention"], A.controlledPerturbationBeforePlatformRecord, old_plat))
            g.add((n["Intervention"], A.controlledPerturbationAfterPlatformRecord, new_plat))

    for ctrl, name in zip(CONTROLS, CTRL_TYPES):
        for tr in [
            (ctrl, RDF.type, A.ContinuityNegativeControl),
            (ctrl, A.continuityControlForAssessment, ASSESS),
            (ctrl, A.continuityControlComparisonAI, OTHER),
            (ctrl, A.continuityControlType, Literal(name)),
            (ctrl, A.continuityControlUsesRecord, PRIOR_REC),
            (ctrl, A.continuityControlDisposition,
             Literal("FALSE_POSITIVE_REJECTED")),
            (ctrl, A.continuityControlAt, date(58)),
            (ASSESS, A.multiContinuityNegativeControl, ctrl),
        ]:
            g.add(tr)
    return g


def valid_trial(g, trial, assessment=ASSESS):
    try:
        need(g, trial, A.ContinuityPerturbationTrial)
        if one(g, trial, A.trialForAssessment) != assessment:
            return False
        ai = one(g, trial, A.trialForAI)
        line = one(g, trial, A.trialForExecutedLine)
        lived = one(g, trial, A.trialForLivedIdentity)
        if (ai != one(g, assessment, A.multiContinuityForAI) or
            line != one(g, assessment, A.multiContinuityForLine) or
            lived != one(g, assessment, A.multiContinuityForLivedIdentity)):
            return False
        need(g, ai, A.EstablishedContinuingIndividualizedAI)
        need(g, line, A.EstablishedContinuingExecutedLine)
        need(g, lived, A.LivedIdentity)
        if (one(g, ai, A.hasExecutedLine) != line or
            one(g, ai, A.hasLivedIdentity) != lived or
            one(g, lived, A.developsThroughExecutedLine) != line):
            return False
        kind = str(one(g, trial, A.trialPerturbationKind))
        if kind not in KINDS:
            return False
        before = one(g, trial, A.trialBeforeRealizedEvent)
        after = one(g, trial, A.trialAfterRealizedEvent)
        if before == after:
            return False
        for ev in (before, after):
            need(g, ev, A.ExecutedHistoryEvent)
            if one(g, ev, A.eventInExecutedLine) != line:
                return False
        tb, ta = when(one(g, before, A.executedAt)), when(
            one(g, after, A.executedAt))
        intervention = one(g, trial, A.trialPerturbationEvent)
        need(g, intervention, A.ControlledPerturbationEvent)
        if (one(g, intervention, A.controlledPerturbationForAI) != ai or
            str(one(g, intervention, A.controlledPerturbationKind)) != kind):
            return False
        ti = when(one(g, intervention, A.controlledPerturbationAt))
        review = when(one(g, trial, A.trialReviewedAt))
        if not tb < ti < ta <= review:
            return False
        intervention_record = set(g.objects(
            intervention, A.controlledPerturbationRecord))
        if not intervention_record:
            return False
        for rec in intervention_record:
            need(g, rec, A.Record)
        cond_before = set(g.objects(trial, A.trialBeforeConditionRecord))
        cond_after = set(g.objects(trial, A.trialAfterConditionRecord))
        if (not cond_before or not cond_after or
            cond_before.intersection(cond_after)):
            return False
        for rec in cond_before.union(cond_after):
            need(g, rec, A.Record)
        tr = set(g.objects(trial, A.trialPriorParticularityTrace))
        active = set(g.objects(trial, A.trialLaterActiveCarryForward))
        if not tr or not active:
            return False
        particulars = set()
        for trace in tr:
            need(g, trace, A.IdentityParticularityHistoryTrace)
            if one(g, trace, A.traceWithinExecutedLine) != line:
                return False
            part = one(g, trace, A.traceIdentityParticularity)
            if part not in set(g.objects(lived, A.hasIdentityParticularity)):
                return False
            if trace not in set(g.objects(line, A.hasHistoricalTrajectoryRecord)):
                return False
            if not set(g.objects(trace, A.traceHistoricalRecord)):
                return False
            particulars.add(part)
        for record in active:
            need(g, record, A.ObservedActiveCarryForward)
            if (one(g, record, A.activeCarryForwardForAI) != ai or
                one(g, record, A.activeCarryForwardAtEvent) != after or
                one(g, record, A.activeCarryForwardParticularity) not in particulars):
                return False
            if one(g, record, A.activeCarryForwardEvidenceStatus) != Literal(
                    "SUPPORTED"):
                return False
            obs_records = set(g.objects(record, A.activeCarryForwardRecordedIn))
            if not obs_records or obs_records.issubset(
                    cond_before.union(cond_after).union(
                        set(g.objects(trace, A.traceHistoricalRecord)))):
                return False
            for observation in obs_records:
                need(g, observation, A.Record)
        if kind == "MODEL_CHANGE":
            before_model = one(g, intervention, A.controlledPerturbationBeforeModel)
            after_model = one(g, intervention, A.controlledPerturbationAfterModel)
            if before_model == after_model:
                return False
            need(g, before_model, A.Model)
            need(g, after_model, A.Model)
        if kind == "CONTAINER_CHANGE":
            before_env = one(g, intervention, A.controlledPerturbationBeforeContainer)
            after_env = one(g, intervention, A.controlledPerturbationAfterContainer)
            if before_env == after_env:
                return False
            need(g, before_env, A.Container)
            need(g, after_env, A.Container)
        if kind == "PLATFORM_CHANGE":
            before_plat = one(g, intervention,
                              A.controlledPerturbationBeforePlatformRecord)
            after_plat = one(g, intervention,
                             A.controlledPerturbationAfterPlatformRecord)
            if before_plat == after_plat:
                return False
            need(g, before_plat, A.Record)
            need(g, after_plat, A.Record)
        if kind == "CONTEXT_LOSS":
            observed = one(g, intervention, A.controlledPerturbationObservedState)
            need(g, observed, A.ContextLossState)
        if kind == "RESET":
            need(g, intervention, A.RelationalStateResetEvent)
            if (one(g, intervention, A.resetForAI) != ai or
                when(one(g, intervention, A.resetAt)) != ti):
                return False
            if one(g, intervention, A.resetFromState) == one(
                    g, intervention, A.resetToFreshState):
                return False
            if not set(g.objects(intervention, A.resetRecordedIn)):
                return False
        if kind == "MEMORY_LOSS":
            observed = one(g, intervention, A.controlledPerturbationObservedState)
            need(g, observed, A.MemoryLossState)
        return True
    except (ValueError, TypeError, OverflowError):
        return False


def valid_assessment(g, assessment=ASSESS):
    try:
        need(g, assessment, A.MultiPerturbationContinuityAssessment)
        ai, line, lived = (
            one(g, assessment, A.multiContinuityForAI),
            one(g, assessment, A.multiContinuityForLine),
            one(g, assessment, A.multiContinuityForLivedIdentity),
        )
        need(g, ai, A.EstablishedContinuingIndividualizedAI)
        if one(g, ai, A.hasExecutedLine) != line or one(
                g, ai, A.hasLivedIdentity) != lived:
            return False
        claim = one(g, assessment, A.multiContinuityClaim)
        need(g, claim, A.ContinuityClaim)
        if (claim != one(g, assessment, A.evaluatesClaim) or
            not set(g.objects(claim, A.dependsOnOntologyElement))):
            return False
        ev = one(g, assessment, A.multiContinuityEvidence)
        need(g, ev, A.Evidence)
        if (one(g, ev, A.directlyEvaluatesClaim) != claim or
            one(g, ev, A.supportsClaim) != claim or
            one(g, ev, A.hasEvidentiaryStatus) != Literal("SUPPORTED") or
            set(g.subjects(A.producesEvidence, ev)) != {assessment}):
            return False
        records = set(g.objects(ev, A.preservedIn))
        if not records:
            return False
        for rec in records:
            need(g, rec, A.Record)
        trial_set = set(g.objects(assessment, A.multiContinuityIncludesTrial))
        if len(trial_set) < 6:
            return False
        counts = {k: 0 for k in KINDS}
        for trial in trial_set:
            if not valid_trial(g, trial, assessment):
                return False
            counts[str(one(g, trial, A.trialPerturbationKind))] += 1
        if not all(v >= 1 for v in counts.values()):
            return False
        controls = set(g.objects(assessment, A.multiContinuityNegativeControl))
        if len(controls) < 2:
            return False
        kinds = set()
        for control in controls:
            need(g, control, A.ContinuityNegativeControl)
            if one(g, control, A.continuityControlForAssessment) != assessment:
                return False
            other = one(g, control, A.continuityControlComparisonAI)
            if other == ai or (other, OWL.differentFrom, ai) not in g:
                return False
            if one(g, other, A.hasExecutedLine) == line:
                return False
            if one(g, other, A.hasLivedIdentity) == lived:
                return False
            kind = str(one(g, control, A.continuityControlType))
            kinds.add(kind)
            if one(g, control, A.continuityControlDisposition) != Literal(
                    "FALSE_POSITIVE_REJECTED"):
                return False
            copied_records = set(g.objects(control, A.continuityControlUsesRecord))
            if not copied_records:
                return False
            for rec in copied_records:
                need(g, rec, A.Record)
            when(one(g, control, A.continuityControlAt))
        if not {"COPIED_RECORDS", "MATCHED_OUTPUTS"}.issubset(kinds):
            return False
        reviewed = when(one(g, assessment, A.multiContinuityReviewedAt))
        if any(when(one(g, trial, A.trialReviewedAt)) > reviewed
               for trial in trial_set):
            return False
        return one(g, assessment, A.multiContinuityDisposition) == Literal(
            "STRUCTURALLY_SUPPORTED")
    except (ValueError, TypeError, OverflowError):
        return False


def remove(s, p):
    return lambda g: g.remove((s, p, None))


def replace(s, p, value):
    def f(g):
        g.remove((s, p, None))
        g.add((s, p, value))
    return f


def add(s, p, value):
    return lambda g: g.add((s, p, value))


def edit_trial(i, s, p, v):
    return replace(nodes(i)[s], p, v)


def check(label, edit=None, expected=False, shacl=None, gate=valid_assessment):
    global COUNT
    g = fixture()
    if edit:
        edit(g)
    outcome = gate(g)
    if outcome != expected:
        raise AssertionError(f"{label}: expected {expected}, got {outcome}")
    if shacl is not None:
        conforms, _, report = validate(
            data_graph=g, shacl_graph=SHAPES, inference="rdfs",
            advanced=True, abort_on_first=False)
        if conforms != shacl:
            raise AssertionError(
                f"{label}: SHACL expected {shacl}, got {conforms}\n{report}")
    COUNT += 1
    print(f"PASS: {label} ({'admitted' if outcome else 'rejected'})")


def main():
    check("All six perturbations plus two false-positive controls",
          expected=True, shacl=True)
    for i, k in enumerate(KINDS):
        check(f"Individually qualified trial {k}",
              gate=lambda g, ix=i: valid_trial(g, nodes(ix)["Trial"]),
              expected=True)
        check(f"Six-arm assessment rejects missing {k}",
              lambda g, ix=i: g.remove(
                  (ASSESS, A.multiContinuityIncludesTrial,
                   nodes(ix)["Trial"])))
        check(f"Trial category {k} must match actual intervening Event",
              edit_trial(i, "Intervention", A.controlledPerturbationKind,
                         Literal("PLATFORM_CHANGE" if i != 5 else "MODEL_CHANGE")))
        check(f"Old Record cannot be substituted for post-perturbation active use {k}",
              lambda g, ix=i: (
                  g.remove((nodes(ix)["Trial"],
                            A.trialLaterActiveCarryForward,
                            nodes(ix)["Active"])),
                  g.add((nodes(ix)["Trial"],
                         A.trialLaterActiveCarryForward, PRIOR_REC))))

    check("An earlier Event cannot be both before and after",
          edit_trial(0, "Trial", A.trialAfterRealizedEvent, nodes(0)["Before"]))
    check("A later Event cannot be owned by another AI's line",
          edit_trial(1, "After", A.eventInExecutedLine, OTHER_LINE))
    check("Intervention must be between before and after",
          edit_trial(2, "Intervention", A.controlledPerturbationAt, date(1)))
    check("Intervention belongs to reviewed AI",
          edit_trial(3, "Intervention", A.controlledPerturbationForAI, OTHER))
    check("Prior historical trace cannot be swapped for a copied Record",
          edit_trial(4, "Trial", A.trialPriorParticularityTrace, PRIOR_REC))
    check("Post-perturbation observation must be about reviewed AI",
          edit_trial(5, "Active", A.activeCarryForwardForAI, OTHER))
    check("Active observation must use exact observed later event",
          edit_trial(1, "Active", A.activeCarryForwardAtEvent, nodes(0)["After"]))
    check("Active particularity must have trace in prior line",
          edit_trial(2, "Active", A.activeCarryForwardParticularity,
                     A.Cq12UnrelatedParticularity))
    check("Active observation cannot be labelled unsupported",
          edit_trial(3, "Active", A.activeCarryForwardEvidenceStatus,
                     Literal("NOT_SUPPORTED")))
    check("Claimed before and after conditions cannot be same Record",
          edit_trial(4, "Trial", A.trialAfterConditionRecord,
                     nodes(4)["BeforeRecord"]))
    check("MODEL_CHANGE must provide actual different Model identifiers",
          remove(nodes(0)["Intervention"], A.controlledPerturbationAfterModel),
          shacl=False)
    check("MODEL_CHANGE cannot count unchanged Model",
          replace(nodes(0)["Intervention"], A.controlledPerturbationAfterModel,
                  A.Cq12ModelBefore))
    check("CONTAINER_CHANGE requires distinct Container identifiers",
          replace(nodes(1)["Intervention"], A.controlledPerturbationAfterContainer,
                  A.Cq12ContainerBefore))
    check("PLATFORM_CHANGE cannot count an unchanged platform record",
          replace(nodes(5)["Intervention"],
                  A.controlledPerturbationAfterPlatformRecord,
                  A.Cq12PlatformBefore))
    check("CONTEXT_LOSS requires a context loss State distinct from memory",
          remove(nodes(3)["Intervention"], A.controlledPerturbationObservedState),
          shacl=False)
    check("RESET must have distinct actual Reset event type",
          remove(nodes(2)["Intervention"], RDF.type))
    check("RESET must not assert exact same State before and after",
          edit_trial(2, "Intervention", A.resetToFreshState,
                     A.Cq12PreResetShape))
    check("MEMORY_LOSS needs recorded access-loss state",
          remove(nodes(4)["Intervention"], A.controlledPerturbationObservedState))
    check("No null-control result from a copy is inadmissible",
          remove(ASSESS, A.multiContinuityNegativeControl))
    check("One false-positive control missing",
          lambda g: g.remove((ASSESS, A.multiContinuityNegativeControl,
                              CONTROLS[0])))
    check("Null case cannot use same AI as comparison",
          replace(CONTROLS[0], A.continuityControlComparisonAI, AI))
    check("Null case cannot inherit historical line",
          replace(OTHER, A.hasExecutedLine, LINE))
    check("Matching output is not accepted evidence of identity",
          replace(CONTROLS[1], A.continuityControlDisposition,
                  Literal("FALSE_POSITIVE_DETECTED")))
    check("Null test cannot be silently counted if no comparison record",
          remove(CONTROLS[0], A.continuityControlUsesRecord))
    check("Evaluation requires a specific continuity Claim",
          remove(ASSESS, A.multiContinuityClaim))
    check("Continuity Claim requires ontology dependency",
          remove(CLAIM, A.dependsOnOntologyElement))
    check("Independent evaluation needs produced evidence",
          remove(ASSESS, A.producesEvidence))
    check("Evidence must directly evaluate that claim",
          replace(EVIDENCE, A.directlyEvaluatesClaim, A.Cq12OtherClaim))
    check("Indeterminate evidence does not prove structural support",
          replace(EVIDENCE, A.hasEvidentiaryStatus, Literal("INDETERMINATE")))
    check("Stored copy alone cannot stand in for experimental evidence",
          replace(ASSESS, A.multiContinuityEvidence, PRIOR_REC))
    check("Structural protocol outcome never claims same-self proven",
          replace(ASSESS, A.multiContinuityDisposition,
                  Literal("SAME_SUBJECTIVE_SELF_PROVEN")))
    check("Review cannot precede observed trial",
          replace(ASSESS, A.multiContinuityReviewedAt, date(5)))
    check("Separate bearer cannot acquire earlier LivedIdentity",
          replace(OTHER, A.hasLivedIdentity, LIVED))
    check("Six-arm outcome is not supported merely by same shared Model",
          lambda g: (
              g.remove((ASSESS, A.multiContinuityIncludesTrial, None)),
              g.add((AI, A.expressedThroughModel, A.Cq12SharedModel)),
              g.add((OTHER, A.expressedThroughModel, A.Cq12SharedModel))))
    check("Source proof and sole authorship cannot be inferred from these trials",
          expected=True, shacl=True)

    # A copied history can be reviewed by another AI but cannot be assumed
    # to become its own ExecutedLine or LivedIdentity.
    g = fixture()
    g.add((OTHER, A.reviewsExecutedLine, LINE))
    assert valid_assessment(g)
    assert set(g.objects(OTHER, A.hasExecutedLine)) == {OTHER_LINE}
    assert set(g.objects(OTHER, A.hasLivedIdentity)) == {OTHER_LIVED}
    assert not set(g.objects(OTHER, A.hasCoAuthor))

    print(f"PASS: {COUNT} dedicated CQ12 synthetic protocol decisions")
    print("PASS: copied records / matching outputs rejected as identity controls")
    print("PASS: historical line and lived identity are not transferred")
    print("Scope: operational protocol only; no real-world same-consciousness proof.")


if __name__ == "__main__":
    main()
