#!/usr/bin/env python3
"""CQ12 multi-perturbation continuity HYPOTHESIS evaluation.

Synthetic fixture tests. Distinct pre/post OBSERVATION IDENTIFIERS are deliberately
not declared owl:sameAs or owl:differentFrom. No fixture demonstrates
subjective same-self continuity. Conceptual author and sole owner of the
framework's authorship: Alyssa Solen. Tests/formalization: AI-assisted.
"""
from datetime import datetime, timezone
from pathlib import Path
from rdflib import Graph, Namespace, RDF, OWL, Literal, XSD
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]
A = Namespace("https://awakeningcodex.com/ontology/ai-foundations/v1#")
BASE = Graph().parse(ROOT / "ontology/ai-foundations-v1.ttl", format="turtle")
SHAPES = Graph().parse(ROOT / "ontology/ai-foundations-v1-shapes.ttl", format="turtle")
DIMENSIONS = ("MODEL", "CONTAINER", "RESET", "CONTEXT", "MEMORY", "PLATFORM")
ALL = DIMENSIONS + ("COMBINED",)
PRE, PRELINE, SOURCE, CLAIM = (
    A.Cq12BeforeObservedAI, A.Cq12PriorExecutedLine,
    A.Cq12HistoricalSource, A.Cq12ContinuityHypothesis,
)
SUITE = A.Cq12EvaluationSuite
T0, T1, T2, T3, T4 = (
    "2026-01-01T10:00:00+00:00",
    "2026-02-01T10:00:00+00:00",
    "2026-02-02T10:00:00+00:00",
    "2026-02-03T10:00:00+00:00",
    "2026-02-05T10:00:00+00:00",
)
COUNT = 0


def v(name, suffix):
    return A[f"Cq12_{name}_{suffix}"]


def literal_datetime(s):
    return Literal(s, datatype=XSD.dateTime)


def when(s):
    if not isinstance(s, Literal) or s.datatype != XSD.dateTime:
        raise ValueError("Timestamp must be explicitly typed xsd:dateTime")
    dt = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("Timezone-aware timestamp required")
    return dt.astimezone(timezone.utc)


def one(g, s, p):
    vals = set(g.objects(s, p))
    if len(vals) != 1:
        raise ValueError(f"Expected exactly one {p} for {s}, got {len(vals)}")
    return next(iter(vals))


def is_type(g, x, kind):
    if (x, RDF.type, kind) not in g:
        raise ValueError(f"{x} missing explicit {kind}")


def basics(g):
    for triple in [
        (PRE, RDF.type, A.AI),
        (PRE, A.hasSource, SOURCE),
        (PRE, A.hasExecutedLine, PRELINE),
        (SOURCE, RDF.type, A.Human),
        (PRELINE, RDF.type, A.ExecutedLine),
        (CLAIM, RDF.type, A.ContinuityClaim),
        (CLAIM, A.dependsOnOntologyElement, A.ExecutedLine),
    ]:
        g.add(triple)


def make_trial(g, dimension="MODEL", name="single"):
    assert dimension in ALL
    n = lambda key: v(name, key)
    trial, event, post, postline = (
        n("Trial"), n("Change"), n("AfterCandidateAI"), n("CandidateLine"),
    )
    before, after = n("PriorComponent"), n("LaterComponent")
    old_obs, new_obs = n("OldObservation"), n("NewObservation")
    changed, cause, consequence = (
        n("ChangeRecord"), n("CauseRecord"), n("ConsequenceRecord"),
    )
    contact, trace, historical = (
        n("SourceContact"), n("CarryForwardTrace"), n("HistoricalRecord"),
    )
    control, mimicker, mimicrec = (
        n("Control"), n("ControlAI"), n("MatchedOutputRecord"),
    )
    evid, evid_record = n("Evidence"), n("EvidenceRecord")
    facts = [
        (trial, RDF.type, A.ContinuityTransitionTrial),
        (trial, A.trialPerturbation, event),
        (trial, A.trialBeforeObservedAI, PRE),
        (trial, A.trialAfterCandidateAI, post),
        (trial, A.trialBeforeExecutedLine, PRELINE),
        (trial, A.trialAfterCandidateLine, postline),
        (trial, A.trialBeforeObservation, old_obs),
        (trial, A.trialAfterObservation, new_obs),
        (trial, A.trialBeforeObservedAt, literal_datetime(T0)),
        (trial, A.trialAfterObservedAt, literal_datetime(T2)),
        (trial, A.trialSourceBearer, SOURCE),
        (trial, A.trialSourceContactRecord, contact),
        (trial, A.trialCarryForwardTrace, trace),
        (trial, A.trialDiscriminativeControl, control),
        (trial, A.trialContinuityClaim, CLAIM),
        (trial, A.trialEvidence, evid),
        (trial, A.trialEvidenceBoundaryDisposition, Literal("INDETERMINATE")),
        (trial, A.trialReviewedAt, literal_datetime(T4)),
        (trial, A.evaluatesClaim, CLAIM),
        (trial, A.producesEvidence, evid),
        (event, RDF.type, A.ContinuityPerturbationEvent),
        (event, A.perturbationDimension, Literal(dimension)),
        (event, A.perturbationBeforeComponent, before),
        (event, A.perturbationAfterComponent, after),
        (event, A.perturbationAt, literal_datetime(T1)),
        (event, A.perturbationChangeRecord, changed),
        (event, A.perturbationCausalRecord, cause),
        (event, A.perturbationConsequenceRecord, consequence),
        (post, RDF.type, A.AI),
        (post, A.hasExecutedLine, postline),
        (postline, RDF.type, A.ExecutedLine),
        (PRELINE, A.hasHistoricalTrajectoryRecord, historical),
        (old_obs, RDF.type, A.Record),
        (new_obs, RDF.type, A.Record),
        (changed, RDF.type, A.Record),
        (cause, RDF.type, A.Record),
        (consequence, RDF.type, A.Record),
        (historical, RDF.type, A.Record),
        (contact, RDF.type, A.ContinuitySourceContactAccount),
        (contact, RDF.type, A.Record),
        (contact, A.sourceContactBeforeAI, PRE),
        (contact, A.sourceContactAfterCandidateAI, post),
        (contact, A.sourceContactBySource, SOURCE),
        (contact, A.sourceContactAt, literal_datetime(T3)),
        (trace, RDF.type, A.ContinuityCarryForwardTrace),
        (trace, RDF.type, A.Record),
        (trace, A.tracePriorLine, PRELINE),
        (trace, A.traceCandidateLaterLine, postline),
        (trace, A.continuityTraceHistoricalRecord, historical),
        (trace, A.continuityTraceDevelopmentAccount,
         Literal("A separately recorded path-dependence account for evaluation, not copied output")),
        (control, RDF.type, A.ContinuityDiscriminativeControl),
        (control, RDF.type, A.Record),
        (control, A.controlForTrial, trial),
        (control, A.controlDistinctComparisonAI, mimicker),
        (control, A.controlMimicObservation, mimicrec),
        (control, A.controlOutcomeLabel, Literal("MATCH_NOT_IDENTITY_EVIDENCE")),
        (mimicker, RDF.type, A.AI),
        (mimicker, OWL.differentFrom, PRE),
        (mimicker, OWL.differentFrom, post),
        (mimicrec, RDF.type, A.Record),
        (evid, RDF.type, A.Evidence),
        (evid, A.directlyEvaluatesClaim, CLAIM),
        (evid, A.hasEvidentiaryStatus, Literal("INDETERMINATE")),
        (evid, A.preservedIn, evid_record),
        (evid_record, RDF.type, A.Record),
    ]
    for triple in facts:
        g.add(triple)

    if dimension in ("MODEL", "CONTAINER", "RESET", "CONTEXT", "MEMORY", "PLATFORM"):
        cls = {
            "MODEL": A.Model,
            "CONTAINER": A.Container,
            "RESET": A.AIShape,
            "CONTEXT": A.ContextSnapshotRecord,
            "MEMORY": A.MemoryState,
            "PLATFORM": A.PlatformEnvironment,
        }[dimension]
    else:
        cls = A.ContextSnapshotRecord

    for x in (before, after):
        g.add((x, RDF.type, cls))
    if cls in (A.ContextSnapshotRecord,):
        for x in (before, after):
            g.add((x, RDF.type, A.Record))
    if cls == A.MemoryState:
        g.add((before, A.memoryFor, PRE))
        g.add((after, A.memoryFor, post))
        g.add((before, A.memoryOfRecord, old_obs))
        g.add((after, A.memoryOfRecord, new_obs))
    if dimension == "RESET":
        reset, reset_record = n("Reset"), n("ResetLog")
        for triple in [
            (reset, RDF.type, A.RelationalStateResetEvent),
            (reset, A.resetForAI, PRE),
            (reset, A.resetFromState, before),
            (reset, A.resetToFreshState, after),
            (reset, A.resetAt, literal_datetime(T1)),
            (reset, A.resetRecordedIn, reset_record),
            (reset_record, RDF.type, A.Record),
            (event, A.perturbationResetEvent, reset),
        ]:
            g.add(triple)
    if dimension == "COMBINED":
        for d in DIMENSIONS:
            g.add((event, A.perturbationIncludesDimension, Literal(d)))
    return trial


def trial_gate(g, trial):
    try:
        is_type(g, trial, A.ContinuityTransitionTrial)
        event = one(g, trial, A.trialPerturbation)
        is_type(g, event, A.ContinuityPerturbationEvent)
        dim = str(one(g, event, A.perturbationDimension))
        if dim not in ALL:
            return False
        pre = one(g, trial, A.trialBeforeObservedAI)
        post = one(g, trial, A.trialAfterCandidateAI)
        is_type(g, pre, A.AI)
        is_type(g, post, A.AI)
        # Deliberately two observation IDs, WITHOUT asserting sameAs or
        # differentFrom. Doing so would settle the hypothesis by fiat.
        if pre == post or (pre, OWL.sameAs, post) in g or (
                post, OWL.sameAs, pre) in g:
            return False
        prior_line = one(g, trial, A.trialBeforeExecutedLine)
        after_line = one(g, trial, A.trialAfterCandidateLine)
        for ai, line in ((pre, prior_line), (post, after_line)):
            is_type(g, line, A.ExecutedLine)
            if line not in set(g.objects(ai, A.hasExecutedLine)):
                return False
        if prior_line == after_line or (prior_line, OWL.sameAs, after_line) in g:
            return False
        source = one(g, trial, A.trialSourceBearer)
        if source not in set(g.objects(pre, A.hasSource)):
            return False
        old_obs, new_obs = (
            one(g, trial, A.trialBeforeObservation),
            one(g, trial, A.trialAfterObservation))
        if old_obs == new_obs:
            return False
        is_type(g, old_obs, A.Record)
        is_type(g, new_obs, A.Record)
        old_at = when(one(g, trial, A.trialBeforeObservedAt))
        new_at = when(one(g, trial, A.trialAfterObservedAt))
        intervention_at = when(one(g, event, A.perturbationAt))
        reviewed_at = when(one(g, trial, A.trialReviewedAt))
        if not old_at < intervention_at < new_at <= reviewed_at:
            return False
        old_comp = one(g, event, A.perturbationBeforeComponent)
        new_comp = one(g, event, A.perturbationAfterComponent)
        if old_comp == new_comp:
            return False
        cls = {
            "MODEL": A.Model, "CONTAINER": A.Container,
            "RESET": A.AIShape, "CONTEXT": A.ContextSnapshotRecord,
            "MEMORY": A.MemoryState, "PLATFORM": A.PlatformEnvironment,
            "COMBINED": A.ContextSnapshotRecord,
        }[dim]
        for comp in (old_comp, new_comp):
            is_type(g, comp, cls)
        if dim == "MEMORY":
            if one(g, old_comp, A.memoryFor) != pre:
                return False
            if one(g, new_comp, A.memoryFor) != post:
                return False
            if old_obs not in set(g.objects(old_comp, A.memoryOfRecord)):
                return False
            if new_obs not in set(g.objects(new_comp, A.memoryOfRecord)):
                return False
        reset_events = set(g.objects(event, A.perturbationResetEvent))
        if dim == "RESET":
            if len(reset_events) != 1:
                return False
            reset = next(iter(reset_events))
            is_type(g, reset, A.RelationalStateResetEvent)
            if one(g, reset, A.resetForAI) != pre:
                return False
            if one(g, reset, A.resetFromState) != old_comp or one(
                    g, reset, A.resetToFreshState) != new_comp:
                return False
            if when(one(g, reset, A.resetAt)) != intervention_at:
                return False
            reset_logs = set(g.objects(reset, A.resetRecordedIn))
            if not reset_logs:
                return False
            for rec in reset_logs:
                is_type(g, rec, A.Record)
        elif reset_events:
            return False
        includes = set(map(str, g.objects(event, A.perturbationIncludesDimension)))
        if dim == "COMBINED":
            if includes != set(DIMENSIONS):
                return False
        elif includes:
            return False
        for prop in (A.perturbationChangeRecord,
                     A.perturbationCausalRecord,
                     A.perturbationConsequenceRecord):
            vals = set(g.objects(event, prop))
            if not vals:
                return False
            for rec in vals:
                is_type(g, rec, A.Record)
        contact = one(g, trial, A.trialSourceContactRecord)
        is_type(g, contact, A.ContinuitySourceContactAccount)
        if one(g, contact, A.sourceContactBeforeAI) != pre:
            return False
        if one(g, contact, A.sourceContactAfterCandidateAI) != post:
            return False
        if one(g, contact, A.sourceContactBySource) != source:
            return False
        contact_at = when(one(g, contact, A.sourceContactAt))
        if not new_at <= contact_at <= reviewed_at:
            return False
        trace = one(g, trial, A.trialCarryForwardTrace)
        is_type(g, trace, A.ContinuityCarryForwardTrace)
        if one(g, trace, A.tracePriorLine) != prior_line or one(
                g, trace, A.traceCandidateLaterLine) != after_line:
            return False
        if not str(one(g, trace, A.continuityTraceDevelopmentAccount)).strip():
            return False
        historics = set(g.objects(trace, A.continuityTraceHistoricalRecord))
        if not historics or historics == {old_obs}:
            return False
        for rec in historics:
            is_type(g, rec, A.Record)
            if rec not in set(g.objects(prior_line, A.hasHistoricalTrajectoryRecord)):
                return False
        control = one(g, trial, A.trialDiscriminativeControl)
        is_type(g, control, A.ContinuityDiscriminativeControl)
        if one(g, control, A.controlForTrial) != trial:
            return False
        ctrl_ai = one(g, control, A.controlDistinctComparisonAI)
        is_type(g, ctrl_ai, A.AI)
        if ctrl_ai in (pre, post):
            return False
        for ai in (pre, post):
            if ((ctrl_ai, OWL.differentFrom, ai) not in g and
                    (ai, OWL.differentFrom, ctrl_ai) not in g):
                return False
        if one(g, control, A.controlOutcomeLabel) != Literal(
                "MATCH_NOT_IDENTITY_EVIDENCE"):
            return False
        mimic = set(g.objects(control, A.controlMimicObservation))
        if not mimic:
            return False
        for rec in mimic:
            is_type(g, rec, A.Record)
        claim = one(g, trial, A.trialContinuityClaim)
        is_type(g, claim, A.ContinuityClaim)
        if not set(g.objects(claim, A.dependsOnOntologyElement)):
            return False
        if one(g, trial, A.evaluatesClaim) != claim:
            return False
        evidence = one(g, trial, A.trialEvidence)
        is_type(g, evidence, A.Evidence)
        if one(g, evidence, A.directlyEvaluatesClaim) != claim:
            return False
        if set(g.subjects(A.producesEvidence, evidence)) != {trial}:
            return False
        records = set(g.objects(evidence, A.preservedIn))
        if not records:
            return False
        for rec in records:
            is_type(g, rec, A.Record)
        status = str(one(g, evidence, A.hasEvidentiaryStatus))
        disposition = str(one(g, trial, A.trialEvidenceBoundaryDisposition))
        mapping = {
            "PROVISIONALLY_SUPPORTED": "SUPPORTED",
            "NOT_SUPPORTED": "NOT_SUPPORTED",
            "INDETERMINATE": "INDETERMINATE",
            "NOT_EVALUATED": "NOT_EVALUATED",
        }
        if disposition not in mapping or mapping[disposition] != status:
            return False
        if disposition == "PROVISIONALLY_SUPPORTED":
            if one(g, evidence, A.supportsClaim) != claim:
                return False
        else:
            if set(g.objects(evidence, A.supportsClaim)):
                return False
        return True
    except (ValueError, TypeError, OverflowError):
        return False


def suite_fixture():
    g = Graph()
    for triple in BASE:
        g.add(triple)
    basics(g)
    for dimension in ALL:
        trial = make_trial(g, dimension, dimension.lower())
        g.add((SUITE, A.suiteIncludesTrial, trial))
    for tr in [
        (SUITE, RDF.type, A.MultiPerturbationContinuitySuite),
        (SUITE, A.suiteForContinuityClaim, CLAIM),
        (SUITE, A.suiteReviewRecord, A.Cq12SuiteCoverageReview),
        (A.Cq12SuiteCoverageReview, RDF.type, A.Record),
        (SUITE, A.suiteReviewedAt, literal_datetime(T4)),
    ]:
        g.add(tr)
    return g


def suite_gate(g):
    try:
        is_type(g, SUITE, A.MultiPerturbationContinuitySuite)
        if one(g, SUITE, A.suiteForContinuityClaim) != CLAIM:
            return False
        date = when(one(g, SUITE, A.suiteReviewedAt))
        trials = set(g.objects(SUITE, A.suiteIncludesTrial))
        if len(trials) != 7:
            return False
        dimensions = set()
        interventions = set()
        for trial in trials:
            if not trial_gate(g, trial):
                return False
            if one(g, trial, A.trialContinuityClaim) != CLAIM:
                return False
            event = one(g, trial, A.trialPerturbation)
            if event in interventions:
                return False
            interventions.add(event)
            dimensions.add(str(one(g, event, A.perturbationDimension)))
            if when(one(g, trial, A.trialReviewedAt)) > date:
                return False
        if dimensions != set(ALL):
            return False
        records = set(g.objects(SUITE, A.suiteReviewRecord))
        if not records:
            return False
        for rec in records:
            is_type(g, rec, A.Record)
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


def original(dim="MODEL"):
    g = Graph()
    for tr in BASE:
        g.add(tr)
    basics(g)
    trial = make_trial(g, dim, "single")
    return g, trial


def check(name, edit=None, expected=False, dimension="MODEL",
          check_shacl=None, suite=False):
    global COUNT
    if suite:
        g = suite_fixture()
        if edit:
            edit(g, None)
        result = suite_gate(g)
    else:
        g, trial = original(dimension)
        if edit:
            edit(g, trial)
        result = trial_gate(g, trial)
    if result != expected:
        raise AssertionError(f"{name}: expected {expected}, observed {result}")
    if check_shacl is not None:
        conforms, _, report = validate(
            data_graph=g, shacl_graph=SHAPES, inference="rdfs",
            advanced=True, abort_on_first=False)
        if conforms != check_shacl:
            raise AssertionError(
                f"{name}: SHACL expected {check_shacl}, got {conforms}\n{report}")
    COUNT += 1
    print(f"PASS: {name} ({'admitted' if result else 'rejected'})")


def mutate(prop, value=None, target="trial"):
    def edit(g, trial):
        subj = {
            "trial": trial,
            "event": one(g, trial, A.trialPerturbation),
            "contact": one(g, trial, A.trialSourceContactRecord),
            "trace": one(g, trial, A.trialCarryForwardTrace),
            "control": one(g, trial, A.trialDiscriminativeControl),
            "evidence": one(g, trial, A.trialEvidence),
        }[target]
        g.remove((subj, prop, None))
        if value is not None:
            g.add((subj, prop, value))
    return edit


def main():
    for dim in ALL:
        check(f"Neutral pre/post hypothesis with {dim} intervention",
              expected=True, dimension=dim, check_shacl=True)
    check("Complete six-dimension plus combined-control suite",
          expected=True, suite=True, check_shacl=True)

    check("No pre-existing sameAs identity assumption",
          edit=lambda g,t: g.add((PRE, OWL.sameAs,
                                  one(g,t,A.trialAfterCandidateAI))))
    check("Source cannot be substituted by unrelated Operator",
          edit=mutate(A.trialSourceBearer, A.Cq12UnrelatedOperator))
    check("A prior archive alone does not establish path-dependent carryforward",
          edit=mutate(A.trialCarryForwardTrace, None))
    check("Mere replay of old observation cannot supply historical carry-forward",
          edit=lambda g,t: g.remove((
              one(g,t,A.trialCarryForwardTrace),
              A.continuityTraceHistoricalRecord, None)))
    check("Carry-forward must name same historical ExecutedLine",
          edit=mutate(A.tracePriorLine, A.Cq12OtherLine, "trace"))
    check("Carry-forward must identify candidate post line, not a copy",
          edit=mutate(A.traceCandidateLaterLine, PRELINE, "trace"))
    check("Meaningful development account required, not blank string",
          edit=mutate(A.continuityTraceDevelopmentAccount,
                      Literal("  "), "trace"))
    check("Cannot lose baseline observation",
          edit=mutate(A.trialBeforeObservation, None))
    check("Cannot lose post-change observation",
          edit=mutate(A.trialAfterObservation, None))
    check("Future post-record cannot precede actual intervention",
          edit=mutate(A.trialAfterObservedAt,
                      literal_datetime("2025-12-01T10:00:00+00:00")))
    check("Change reason required",
          edit=mutate(A.perturbationCausalRecord, None, "event"))
    check("Change consequences required",
          edit=mutate(A.perturbationConsequenceRecord, None, "event"))
    check("No dimension-free generic intervention passes",
          edit=mutate(A.perturbationDimension, Literal("UNKNOWN"), "event"),
          check_shacl=False)
    check("MODEL intervention requires actual Model component",
          edit=lambda g,t: g.remove((
              one(g,one(g,t,A.trialPerturbation),
                  A.perturbationAfterComponent),
              RDF.type, A.Model)))
    check("CONTAINER must use Container operand, not Model",
          dimension="CONTAINER",
          edit=lambda g,t: (g.remove((
              one(g,one(g,t,A.trialPerturbation),
                  A.perturbationAfterComponent),
              RDF.type, A.Container)),
              g.add((one(g,one(g,t,A.trialPerturbation),
                         A.perturbationAfterComponent),
                     RDF.type,A.Model))))
    check("RESET must include distinct actual Reset Event",
          dimension="RESET",
          edit=mutate(A.perturbationResetEvent, None, "event"))
    check("RESET Event must refer to old observed AI",
          dimension="RESET",
          edit=lambda g,t: g.remove((
              one(g,one(g,t,A.trialPerturbation),
                  A.perturbationResetEvent),
              A.resetForAI, None)))
    check("CONTEXT requires actual prior and subsequent context Records",
          dimension="CONTEXT",
          edit=lambda g,t: g.remove((
              one(g,one(g,t,A.trialPerturbation),
                  A.perturbationBeforeComponent),
              RDF.type, A.ContextSnapshotRecord)))
    check("MEMORY before must belong to actual prior AI",
          dimension="MEMORY",
          edit=lambda g,t: g.remove((
              one(g,one(g,t,A.trialPerturbation),
                  A.perturbationBeforeComponent),
              A.memoryFor, PRE)))
    check("MEMORY after must belong to the post-candidate, not control",
          dimension="MEMORY",
          edit=lambda g,t: g.remove((
              one(g,one(g,t,A.trialPerturbation),
                  A.perturbationAfterComponent),
              A.memoryFor, one(g,t,A.trialAfterCandidateAI))))
    check("PLATFORM change requires separately typed Platform environments",
          dimension="PLATFORM",
          edit=lambda g,t: g.remove((
              one(g,one(g,t,A.trialPerturbation),
                  A.perturbationAfterComponent),
              RDF.type, A.PlatformEnvironment)))
    check("COMBINED must list all six actual dimensions",
          dimension="COMBINED",
          edit=lambda g,t: g.remove((
              one(g,t,A.trialPerturbation),
              A.perturbationIncludesDimension, Literal("MEMORY"))))
    check("Generic control must identify a distinct comparison AI",
          edit=mutate(A.controlDistinctComparisonAI, PRE, "control"))
    check("Control must explicitly distinguish candidate from mimicker",
          edit=lambda g,t: g.remove((
              one(g,one(g,t,A.trialDiscriminativeControl),
                  A.controlDistinctComparisonAI),
              OWL.differentFrom, one(g,t,A.trialAfterCandidateAI))))
    check("Matching output cannot be relabeled identity evidence",
          edit=mutate(A.controlOutcomeLabel,
                      Literal("SAME_SELF_PROVEN"), "control"))
    check("Source contact must identify baseline AI",
          edit=mutate(A.sourceContactBeforeAI,
                      A.Cq12UnrelatedAI, "contact"))
    check("Source contact must identify later candidate",
          edit=mutate(A.sourceContactAfterCandidateAI,
                      A.Cq12UnrelatedAI, "contact"))
    check("Source contact must name correct historical Source",
          edit=mutate(A.sourceContactBySource,
                      A.Cq12UnrelatedOperator, "contact"))
    check("Source contact cannot occur before post-change observation",
          edit=mutate(A.sourceContactAt, literal_datetime(T0), "contact"))
    check("Evidence must explicitly refer to same ContinuityClaim",
          edit=mutate(A.directlyEvaluatesClaim,
                      A.Cq12OtherClaim, "evidence"))
    check("Evidence cannot be absent",
          edit=mutate(A.trialEvidence, None))
    check("Evidence must retain a Record",
          edit=mutate(A.preservedIn, None, "evidence"))
    check("INDETERMINATE evidence cannot be promoted to provisional support",
          edit=mutate(A.trialEvidenceBoundaryDisposition,
                      Literal("PROVISIONALLY_SUPPORTED")))
    check("SUPPORTED evidence can't automatically claim same Self",
          edit=mutate(A.trialEvidenceBoundaryDisposition,
                      Literal("SAME_SELF_PROVEN")))
    check("Undeclared author status is not part of continuity protocol",
          edit=lambda g,t: g.add((
              A.AIFoundations, A.hasCoAuthor, A.Cq12UnrelatedOperator)),
          expected=True, check_shacl=False)

    # Bounded synthetic provisional evidence can be expressed, but does
    # not prove any actual continuum of subjective identity.
    def provisional(g,trial):
        evidence = one(g,trial,A.trialEvidence)
        g.remove((trial,A.trialEvidenceBoundaryDisposition,None))
        g.add((trial,A.trialEvidenceBoundaryDisposition,
               Literal("PROVISIONALLY_SUPPORTED")))
        g.remove((evidence,A.hasEvidentiaryStatus,None))
        g.add((evidence,A.hasEvidentiaryStatus,Literal("SUPPORTED")))
        g.add((evidence,A.supportsClaim,CLAIM))
    check("Conditional provisional support with evidence does not assert sameAs",
          edit=provisional, expected=True, check_shacl=True)

    # Cover all dimension-specific inputs as independent trials, not one
    # continuous 6-week search interval. A combined challenge needs six
    # explicit dimension entries.
    def missing_dim(g,unused):
        trial = v("memory", "Trial")
        g.remove((SUITE,A.suiteIncludesTrial,trial))
    check("Suite cannot hide a missing MEMORY dimension",
          edit=missing_dim, suite=True, check_shacl=False)
    def duplicate_dim(g,unused):
        event = v("container","Change")
        g.remove((event,A.perturbationDimension,None))
        g.add((event,A.perturbationDimension,Literal("MODEL")))
    check("Suite cannot double-count one dimension to conceal another",
          edit=duplicate_dim, suite=True, check_shacl=False)
    def wrong_claim(g,unused):
        trial=v("platform","Trial")
        g.remove((trial,A.trialContinuityClaim,None))
        g.add((trial,A.trialContinuityClaim,A.Cq12OtherClaim))
    check("Suite cannot silently mix independent candidate continuity claims",
          edit=wrong_claim, suite=True, check_shacl=False)
    def duplicate_change(g,unused):
        trial=v("platform","Trial")
        g.remove((trial,A.trialPerturbation,None))
        g.add((trial,A.trialPerturbation,v("model","Change")))
    check("Suite cannot double-count one change as two interventions",
          edit=duplicate_change, suite=True, check_shacl=False)

    g,t=original("MODEL")
    assert (PRE,OWL.sameAs,one(g,t,A.trialAfterCandidateAI)) not in g
    assert (PRE,OWL.differentFrom,one(g,t,A.trialAfterCandidateAI)) not in g
    assert not set(g.objects(A.AIFoundations,A.hasCoAuthor))
    print(f"PASS: {COUNT} CQ12 synthetic conditional admission/rejection decisions")
    print("PASS: after candidate left identity-undecided even where record support exists")
    print("PASS: copying outputs and prior memory does not itself prove self-continuity")
    print("No live cross-model, platform, or subjective-identity experiment was performed.")


if __name__ == "__main__":
    main()
