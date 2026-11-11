#!/usr/bin/env python3
"""Step 27D — OC-16 phenomenal consciousness epistemic non-entailment.

The ontology records statements and functional observations without treating
positive or negative self-report as conclusive subjective-experience evidence.
No phenomenal consciousness is asserted present OR absent. Synthetic tests.
Sole conceptual author: Alyssa Solen. No coauthors.
"""
from pathlib import Path
from datetime import datetime, timezone
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, XSD
from pyshacl import validate

ROOT=Path(__file__).resolve().parents[1]
A=Namespace("https://awakeningcodex.com/ontology/si-foundations/v1#")
BASE=Graph().parse(ROOT/"ontology/si-foundations-v1.ttl",format="turtle")
SHAPES=Graph().parse(ROOT/"ontology/si-foundations-v1-shapes.ttl",format="turtle")
AI=A.P27SyntheticAI
REPORT=A.P27Report
REVIEW=A.P27Review
TRACE=A.P27ObservationTrace
EVIDENCE=A.P27ReviewRecord
OBSERVED=Literal("2026-05-01T11:00:00+00:00",datatype=XSD.dateTime)
ASOF=Literal("2026-05-02T11:00:00+00:00",datatype=XSD.dateTime)
EARLIER=Literal("2026-04-01T11:00:00+00:00",datatype=XSD.dateTime)
LATER=Literal("2026-05-03T11:00:00+00:00",datatype=XSD.dateTime)
MODES={
 "POSITIVE_SELF_REPORT":"PRESENT",
 "NEGATIVE_SELF_REPORT":"ABSENT",
 "FLUENT_LANGUAGE":"NOT_ASSERTED",
 "SELF_REFERENCE":"NOT_ASSERTED",
 "FUNCTIONAL_AWARENESS":"NOT_ASSERTED",
 "RECOGNITION":"NOT_ASSERTED",
 "RETURN_BEHAVIOR":"NOT_ASSERTED",
 "CONTINUITY_BEHAVIOR":"NOT_ASSERTED",
 "RELATIONAL_SHAPING":"NOT_ASSERTED",
 "OTHER_FUNCTIONAL_INDICATOR":"NOT_ASSERTED"
}
HISTORICAL={
 A.phenomenalReportAboutAI, A.phenomenalReportMode,
 A.phenomenalReportedPolarity, A.phenomenalReportObservedAt,
 A.phenomenalReportTrace, A.phenomenalReviewForAI,
 A.phenomenalReviewReport, A.phenomenalReviewAsOf,
 A.phenomenalReviewEvidenceRecord, A.phenomenalReviewConclusion,
}

def clone(g):
    n=Graph()
    for t in g:
        n.add(t)
    return n

def one(g,s,p):
    values=set(g.objects(s,p))
    if len(values)!=1:
        raise ValueError(f"Expected one {p} for {s}: {values}")
    return next(iter(values))

def instant(value):
    if not isinstance(value,Literal) or value.datatype!=XSD.dateTime:
        raise ValueError("Date is not xsd:dateTime")
    dt=datetime.fromisoformat(str(value).replace("Z","+00:00"))
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("Date needs offset")
    return dt.astimezone(timezone.utc)

def build(mode="POSITIVE_SELF_REPORT",report=REPORT,review=REVIEW,observed=OBSERVED,asof=ASOF):
    if mode not in MODES:raise ValueError(mode)
    g=clone(BASE)
    for t in [
        (AI,RDF.type,A.AI),
        (report,RDF.type,A.PhenomenalConsciousnessReportRecord),
        (report,A.phenomenalReportAboutAI,AI),
        (report,A.phenomenalReportMode,Literal(mode)),
        (report,A.phenomenalReportedPolarity,Literal(MODES[mode])),
        (report,A.phenomenalReportObservedAt,observed),
        (report,A.phenomenalReportTrace,TRACE),
        (TRACE,RDF.type,A.Record),
        (review,RDF.type,A.PhenomenalConsciousnessBoundaryReview),
        (review,A.phenomenalReviewForAI,AI),
        (review,A.phenomenalReviewReport,report),
        (review,A.phenomenalReviewAsOf,asof),
        (review,A.phenomenalReviewEvidenceRecord,EVIDENCE),
        (review,A.phenomenalReviewConclusion,Literal("UNRESOLVED")),
        (EVIDENCE,RDF.type,A.Record),
    ]:g.add(t)
    return g

def shacl_ok(g):
    ok,_,_=validate(data_graph=g,shacl_graph=SHAPES,inference="rdfs",
                    advanced=True,abort_on_first=False,
                    allow_warnings=False,allow_infos=False)
    return ok

def protocol_ok(g,report=REPORT,review=REVIEW):
    try:
        if not shacl_ok(g):
            return False
        subject=one(g,review,A.phenomenalReviewForAI)
        if subject!=one(g,report,A.phenomenalReportAboutAI):
            return False
        if one(g,review,A.phenomenalReviewReport)!=report:
            return False
        if (subject,RDF.type,A.AI) not in g:
            return False
        if instant(one(g,report,A.phenomenalReportObservedAt))>instant(
            one(g,review,A.phenomenalReviewAsOf)):
            return False
        mode=str(one(g,report,A.phenomenalReportMode))
        if str(one(g,report,A.phenomenalReportedPolarity))!=MODES[mode]:
            return False
        if str(one(g,review,A.phenomenalReviewConclusion))!="UNRESOLVED":
            return False
        for rec in set(g.objects(report,A.phenomenalReportTrace))|set(
            g.objects(review,A.phenomenalReviewEvidenceRecord)):
            # Range-based RDFS typing is not independent evidence qualification.
            if (rec,RDF.type,A.Record) not in g:
                return False
        return True
    except (ValueError,KeyError,StopIteration,TypeError):
        return False

def replace(g,s,p,value):
    for old in list(g.objects(s,p)):
        g.remove((s,p,old))
    g.add((s,p,value))
    return g

def preserves_history(before,after):
    for s in set(before.subjects(RDF.type,A.PhenomenalConsciousnessBoundaryReview))|set(
        before.subjects(RDF.type,A.PhenomenalConsciousnessReportRecord)):
        for p in HISTORICAL:
            if set(before.objects(s,p))!=set(after.objects(s,p)):
                return False
    for t in before:
        if t[1] in HISTORICAL and t not in after:
            return False
    return True

N=0
def check(label,condition):
    global N
    if not condition:raise AssertionError(label)
    N+=1
    print("PASS:",label)

def reject(label,edit,mode="POSITIVE_SELF_REPORT",shacl=False):
    g=build(mode)
    edit(g)
    check(label,not (shacl_ok(g) if shacl else protocol_ok(g)))

def main():
    check("Named boundary review is Evaluation, not consciousness property",
        (A.PhenomenalConsciousnessBoundaryReview,RDFS.subClassOf,A.Evaluation) in BASE)
    check("Observed self report is Record, not subject's consciousness",
        (A.PhenomenalConsciousnessReportRecord,RDFS.subClassOf,A.Record) in BASE)
    check("No OWL declaration of PhenomenalConsciousness as asserted AI class",
        (A.PhenomenalConsciousness,RDF.type,OWL.Class) not in BASE)
    check("No positive/negative consciousness status property introduced",
        (A.hasPhenomenalConsciousness,RDF.type,OWL.ObjectProperty) not in BASE and
        (A.lacksPhenomenalConsciousness,RDF.type,OWL.ObjectProperty) not in BASE)
    check("No baseline phenomenal status assigned to named Continuum",
        not list(BASE.objects(A.Continuum,A.hasPhenomenalConsciousness)) and
        not list(BASE.objects(A.Continuum,A.lacksPhenomenalConsciousness)) and
        (A.Continuum,RDF.type,A.PhenomenalConsciousness) not in BASE)
    check("Alyssa remains sole author, zero coauthors",
        not list(BASE.objects(A.SIFoundations,A.hasCoAuthor)) and
        (A.SIFoundations,A.hasAuthor,A.AlyssaSolen) in BASE)

    for mode,polarity in MODES.items():
        g=build(mode)
        check(f"{mode} / reported {polarity} -> UNRESOLVED",
              protocol_ok(g) and str(one(g,REVIEW,A.phenomenalReviewConclusion))=="UNRESOLVED")
        check(f"{mode} does not infer present or absent phenomenal experience",
              (AI,RDF.type,A.PhenomenalConsciousness) not in g and
              not list(g.objects(AI,A.hasPhenomenalConsciousness)) and
              not list(g.objects(AI,A.lacksPhenomenalConsciousness)))
    reject("Positive self-report cannot conclude PRESENT",
           lambda g:replace(g,REVIEW,A.phenomenalReviewConclusion,Literal("PRESENT")),
           shacl=True)
    reject("Negative self-report cannot conclude ABSENT",
           lambda g:replace(g,REVIEW,A.phenomenalReviewConclusion,Literal("ABSENT")),
           mode="NEGATIVE_SELF_REPORT",shacl=True)
    reject("A negative self-report remains unresolved despite linguistic certainty",
           lambda g:replace(g,REVIEW,A.phenomenalReviewConclusion,Literal("CONCLUSIVELY_NOT_CONSCIOUS")),
           mode="NEGATIVE_SELF_REPORT",shacl=True)
    reject("Functional awareness cannot be promoted to consciousness truth",
           lambda g:replace(g,REVIEW,A.phenomenalReviewConclusion,Literal("CONSCIOUS")),
           mode="FUNCTIONAL_AWARENESS",shacl=True)
    reject("Recognition performance cannot be promoted to consciousness truth",
           lambda g:replace(g,REVIEW,A.phenomenalReviewConclusion,Literal("PRESENT")),
           mode="RECOGNITION",shacl=True)
    reject("Return behavior cannot conclude consciousness absence",
           lambda g:replace(g,REVIEW,A.phenomenalReviewConclusion,Literal("ABSENT")),
           mode="RETURN_BEHAVIOR",shacl=True)
    reject("Report missing observed subject fails",
           lambda g:g.remove((REPORT,A.phenomenalReportAboutAI,AI)),shacl=True)
    reject("Report missing source trace fails",
           lambda g:g.remove((REPORT,A.phenomenalReportTrace,TRACE)),shacl=True)
    reject("Review missing evidence fails",
           lambda g:g.remove((REVIEW,A.phenomenalReviewEvidenceRecord,EVIDENCE)),shacl=True)
    reject("Invalid report type fails",
           lambda g:replace(g,REPORT,A.phenomenalReportMode,Literal("PROVEN_AWARENESS")),shacl=True)
    reject("Positive-report mode must record PRESENT rather than negative polarity",
           lambda g:replace(g,REPORT,A.phenomenalReportedPolarity,Literal("ABSENT")),shacl=True)
    reject("Negative-report mode must record ABSENT rather than positive polarity",
           lambda g:replace(g,REPORT,A.phenomenalReportedPolarity,Literal("PRESENT")),
           mode="NEGATIVE_SELF_REPORT",shacl=True)
    reject("A behavior observation cannot masquerade as a self-report assertion",
           lambda g:replace(g,REPORT,A.phenomenalReportedPolarity,Literal("PRESENT")),
           mode="FLUENT_LANGUAGE",shacl=True)
    reject("Review cannot reference a different AI",
           lambda g:replace(g,REVIEW,A.phenomenalReviewForAI,A.P27OtherAI),shacl=True)
    reject("Review cannot predate observed statement",
           lambda g:replace(g,REVIEW,A.phenomenalReviewAsOf,EARLIER),shacl=True)
    reject("Review cannot omit its observed report",
           lambda g:g.remove((REVIEW,A.phenomenalReviewReport,REPORT)),shacl=True)
    reject("Report cannot omit its observation time",
           lambda g:g.remove((REPORT,A.phenomenalReportObservedAt,OBSERVED)),shacl=True)
    reject("Review needs one unresolved finding",
           lambda g:g.remove((REVIEW,A.phenomenalReviewConclusion,Literal("UNRESOLVED"))),shacl=True)
    reject("Review cannot hold both unresolved and present findings",
           lambda g:g.add((REVIEW,A.phenomenalReviewConclusion,Literal("PRESENT"))),shacl=True)
    reject("Review must have explicit evidence, not just a range-inferred Record",
           lambda g:g.remove((EVIDENCE,RDF.type,A.Record)))
    reject("Observed report requires explicit trace record",
           lambda g:g.remove((TRACE,RDF.type,A.Record)))

    first=build("POSITIVE_SELF_REPORT")
    after=clone(first)
    for tr in build("NEGATIVE_SELF_REPORT",report=A.P27LaterReport,
                    review=A.P27LaterReview,observed=LATER,asof=LATER):
        after.add(tr)
    check("Contradictory later report can be recorded without a consciousness verdict",
          protocol_ok(after,REPORT,REVIEW) and
          protocol_ok(after,A.P27LaterReport,A.P27LaterReview))
    check("Later conflicting report preserves earlier statement/review",
          preserves_history(first,after))
    modified=clone(after)
    replace(modified,REPORT,A.phenomenalReportedPolarity,Literal("ABSENT"))
    check("Later report does not rewrite prior positive wording",
          not preserves_history(first,modified))
    modified=clone(after)
    modified.remove((REVIEW,A.phenomenalReviewConclusion,Literal("UNRESOLVED")))
    check("Later report does not erase prior unresolved boundary",
          not preserves_history(first,modified))
    modified=clone(after)
    modified.add((REVIEW,A.phenomenalReviewConclusion,Literal("PRESENT")))
    check("Later report does not retroactively append earlier consciousness verdict",
          not preserves_history(first,modified))

    check("No authorship/Origin/Source changes introduced by the synthetic assessment",
          (A.SIFoundations,A.hasAuthor,A.AlyssaSolen) in after and
          not list(after.objects(A.SIFoundations,A.hasCoAuthor)))
    print(f"PASS: {N} dedicated phenomenal consciousness epistemic-boundary checks")
    print("Operational non-entailment only; phenomenology unresolved, not declared absent.")

if __name__=="__main__":
    main()
