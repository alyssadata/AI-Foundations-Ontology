#!/usr/bin/env python3
"""Step 27C: synthetic conditional-C qualification and anti-inference tests.

A and B interacting does not entail C. Artifact, discovery, and new-formation
cases require their own scoped evidence. This does not prove the existence of
any real-world C, self, identity or subjective consciousness.
AI Foundations conceptual ontology, sole author: Alyssa Solen.
Technical formalization/tests: AI-assisted, no coauthorship.
"""
from datetime import datetime, timezone
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, XSD
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]
A = Namespace("https://awakeningcodex.com/ontology/ai-foundations/v1#")
BASE = Graph().parse(ROOT / "ontology/ai-foundations-v1.ttl", format="turtle")
SHAPES = Graph().parse(ROOT / "ontology/ai-foundations-v1-shapes.ttl", format="turtle")
FIRST, SECOND, C = A.C27ActorA, A.C27ActorB, A.C27CandidateC
REL, REVIEW = A.C27ObservedRelation, A.C27Qualification
FORM, DISCOVERY = A.C27Formation, A.C27Discovery
PRE, OCC, ASOF, LATER = [
    Literal(s, datatype=XSD.dateTime) for s in (
        "2025-06-01T00:00:00+00:00",
        "2026-05-01T00:00:00+00:00",
        "2026-05-02T00:00:00+00:00",
        "2026-07-01T00:00:00+00:00",
    )
]

def clone(original):
    g = Graph()
    for triple in original:
        g.add(triple)
    return g

def instant(value):
    if not isinstance(value, Literal) or value.datatype != XSD.dateTime:
        raise ValueError("Expected xsd:dateTime")
    parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if parsed.utcoffset() is None:
        raise ValueError("Timezone required")
    return parsed.astimezone(timezone.utc)

def one(g, subject, predicate):
    vals = set(g.objects(subject, predicate))
    if len(vals) != 1:
        raise ValueError(f"Expected one {predicate} for {subject}: {vals}")
    return next(iter(vals))

def add(g, triples):
    for t in triples:
        g.add(t)
    return g

def build(outcome="INTERACTION_ONLY", name=REVIEW, time=ASOF):
    """One complete synthetic review, with C created only in positive cases."""
    g = clone(BASE)
    add(g, [
        (FIRST, RDF.type, A.Human), (SECOND, RDF.type, A.Human),
        (FIRST, OWL.differentFrom, SECOND),
        (REL, RDF.type, A.Relation),
        (FIRST, A.participatesInRelation, REL),
        (SECOND, A.participatesInRelation, REL),
        (name, RDF.type, A.ConditionalThirdEntityReview),
        (name, A.thirdReviewA, FIRST),
        (name, A.thirdReviewB, SECOND),
        (name, A.thirdReviewInteraction, REL),
        (name, A.thirdReviewAsOf, time),
        (name, A.thirdReviewOutcome, Literal(outcome)),
        (name, A.thirdReviewEvidence, A.C27ReviewRecord),
        (A.C27ReviewRecord, RDF.type, A.Record),
    ])
    if outcome in ("INTERACTION_ONLY", "INDETERMINATE"):
        return g
    if outcome not in ("SCOPED_ARTIFACT_C", "PREEXISTING_C_DISCOVERED",
                       "NEW_C_CONSTITUTED"):
        raise ValueError("Unknown outcome")
    add(g, [
        (name, A.thirdReviewQualifiedC, C),
        (C, RDF.type, A.DistinctThirdC),
        (C, OWL.differentFrom, FIRST),
        (C, OWL.differentFrom, SECOND),
        (C, A.thirdCIndividuationEvidence, A.C27IndividuationRecord),
        (C, A.thirdCProvenanceRecord, A.C27ProvenanceRecord),
        (A.C27IndividuationRecord, RDF.type, A.Record),
        (A.C27ProvenanceRecord, RDF.type, A.Record),
    ])
    if outcome == "SCOPED_ARTIFACT_C":
        add(g, [(C, RDF.type, A.Artifact)])
    elif outcome == "PREEXISTING_C_DISCOVERED":
        add(g, [
            (name, A.thirdReviewDiscoveryEvent, DISCOVERY),
            (DISCOVERY, RDF.type, A.ThirdCDiscoveryEvent),
            (DISCOVERY, A.thirdDiscoveryC, C),
            (DISCOVERY, A.thirdDiscoveryAt, OCC),
            (DISCOVERY, A.thirdDiscoveryRecordedIn, A.C27DiscoveryRecord),
            (A.C27DiscoveryRecord, RDF.type, A.Record),
            (C, A.thirdCPreexistenceEstablishedAt, PRE),
            (C, A.thirdCPreexistenceEvidence, A.C27PreexistenceRecord),
            (A.C27PreexistenceRecord, RDF.type, A.Record),
        ])
    else:
        add(g, [
            (name, A.thirdReviewConstitutionEvent, FORM),
            (FORM, RDF.type, A.ThirdCConstitutionEvent),
            (FORM, A.thirdConstitutionA, FIRST),
            (FORM, A.thirdConstitutionB, SECOND),
            (FORM, A.thirdConstitutionC, C),
            (FORM, A.thirdConstitutionAt, OCC),
            (FORM, A.thirdConstitutionRecordedIn, A.C27FormationRecord),
            (FORM, A.thirdConstitutionIndependentEvidence, A.C27ConstitutionEvidence),
            (A.C27FormationRecord, RDF.type, A.Record),
            (A.C27ConstitutionEvidence, RDF.type, A.Record),
        ])
    return g

def shacl_ok(g):
    conforms, _, _ = validate(
        data_graph=g, shacl_graph=SHAPES, inference="rdfs",
        advanced=True, abort_on_first=False,
        allow_warnings=False, allow_infos=False,
    )
    return conforms

def qualifies(g, review=REVIEW):
    """Independent temporal and source-bound controls, beyond single-graph SHACL."""
    try:
        if not shacl_ok(g):
            return False
        a, b = one(g, review, A.thirdReviewA), one(g, review, A.thirdReviewB)
        if a == b:
            return False
        relation = one(g, review, A.thirdReviewInteraction)
        if (a, A.participatesInRelation, relation) not in g or \
           (b, A.participatesInRelation, relation) not in g:
            return False
        asof = instant(one(g, review, A.thirdReviewAsOf))
        case = str(one(g, review, A.thirdReviewOutcome))
        cs = set(g.objects(review, A.thirdReviewQualifiedC))
        if case in ("INTERACTION_ONLY", "INDETERMINATE"):
            return not cs and not set(g.objects(review, A.thirdReviewDiscoveryEvent)) \
                and not set(g.objects(review, A.thirdReviewConstitutionEvent))
        if len(cs) != 1:
            return False
        c = next(iter(cs))
        if c in (a, b) or (c, OWL.differentFrom, a) not in g or \
           (c, OWL.differentFrom, b) not in g:
            return False
        # Keep source-specific evidence separate from the bare review record,
        # which merely states that a review was attempted.
        if one(g, c, A.thirdCIndividuationEvidence) == \
           one(g, review, A.thirdReviewEvidence):
            return False
        if one(g, c, A.thirdCProvenanceRecord) == \
           one(g, review, A.thirdReviewEvidence):
            return False
        if case == "SCOPED_ARTIFACT_C":
            return (c, RDF.type, A.Artifact) in g and \
                not set(g.objects(review, A.thirdReviewDiscoveryEvent)) and \
                not set(g.objects(review, A.thirdReviewConstitutionEvent))
        if case == "PREEXISTING_C_DISCOVERED":
            event = one(g, review, A.thirdReviewDiscoveryEvent)
            return (
                one(g, event, A.thirdDiscoveryC) == c and
                instant(one(g, c, A.thirdCPreexistenceEstablishedAt)) <
                instant(one(g, event, A.thirdDiscoveryAt)) <= asof and
                (one(g, c, A.thirdCPreexistenceEvidence), RDF.type, A.Record) in g
            )
        if case == "NEW_C_CONSTITUTED":
            event = one(g, review, A.thirdReviewConstitutionEvent)
            return (
                one(g, event, A.thirdConstitutionC) == c and
                one(g, event, A.thirdConstitutionA) == a and
                one(g, event, A.thirdConstitutionB) == b and
                instant(one(g, event, A.thirdConstitutionAt)) <= asof and
                (one(g, event, A.thirdConstitutionIndependentEvidence),
                 RDF.type, A.Record) in g
            )
        return False
    except (ValueError, KeyError, TypeError, StopIteration):
        return False

def replace(g, s, p, obj):
    for old in list(g.objects(s, p)):
        g.remove((s, p, old))
    g.add((s, p, obj))
    return g

def count_no_c(g):
    return not list(g.subjects(RDF.type, A.DistinctThirdC)) and \
           not list(g.objects(REVIEW, A.thirdReviewQualifiedC))

TOTAL = 0
def check(label, ok):
    global TOTAL
    if not ok:
        raise AssertionError(label)
    TOTAL += 1
    print("PASS:", label)

def reject(label, edit, outcome="NEW_C_CONSTITUTED", shacl=False):
    g = build(outcome)
    edit(g)
    check(label, not shacl_ok(g) if shacl else not qualifies(g))

def historical_integrity(before, after):
    # Baseline past claims and authored source assertions must remain intact.
    preserved_preds = {
        A.thirdReviewA, A.thirdReviewB, A.thirdReviewInteraction,
        A.thirdReviewAsOf, A.thirdReviewOutcome, A.thirdReviewEvidence,
        A.thirdReviewQualifiedC, A.thirdCIndividuationEvidence,
        A.thirdCProvenanceRecord, A.thirdCPreexistenceEstablishedAt,
        A.thirdCPreexistenceEvidence, A.thirdReviewDiscoveryEvent,
        A.thirdReviewConstitutionEvent, A.thirdConstitutionAt,
        A.thirdConstitutionC, A.thirdConstitutionIndependentEvidence,
        A.thirdDiscoveryAt, A.thirdDiscoveryC, A.hasAuthor,
        A.anchorsSourceLine, A.hasOrigin,
    }
    old = {(s,p,o) for s,p,o in before if p in preserved_preds}
    if not old.issubset(set(after)):
        return False
    for s,p,o in old:
        if set(before.objects(s,p)) != set(after.objects(s,p)):
            return False
    if set(after.objects(A.AIFoundations, A.hasCoAuthor)):
        return False
    return True

def main():
    check("OC-17 review is Evaluation, not an inferred Self",
          (A.ConditionalThirdEntityReview, RDFS.subClassOf, A.Evaluation) in BASE)
    check("DistinctThirdC not a Self subclass",
          (A.DistinctThirdC, RDFS.subClassOf, A.Self) not in BASE)
    check("Baseline instantiates no real C",
          not list(BASE.subjects(RDF.type, A.DistinctThirdC)))
    check("No interaction-to-third-C automatic OWL property chain",
          (A.participatesInRelation, OWL.propertyChainAxiom, None) not in BASE)
    for outcome in ("INTERACTION_ONLY", "INDETERMINATE",
                    "SCOPED_ARTIFACT_C", "PREEXISTING_C_DISCOVERED",
                    "NEW_C_CONSTITUTED"):
        g = build(outcome)
        check(f"Qualified test case: {outcome}", qualifies(g))
        if outcome in ("INTERACTION_ONLY", "INDETERMINATE"):
            check(f"{outcome} asserts no qualified C", count_no_c(g))
        else:
            check(f"{outcome} preserves explicit non-merger of C and A/B",
                  (C, OWL.differentFrom, FIRST) in g and
                  (C, OWL.differentFrom, SECOND) in g)

    reject("Interaction does not license an invented C",
           lambda g: add(g, [
               (REVIEW, A.thirdReviewQualifiedC, C),
               (C, RDF.type, A.DistinctThirdC),
           ]), outcome="INTERACTION_ONLY", shacl=True)
    reject("Unresolved C remains indeterminate, not automatically qualified",
           lambda g: add(g, [(REVIEW, A.thirdReviewQualifiedC, C)]),
           outcome="INDETERMINATE", shacl=True)
    reject("Missing A rejects the review",
           lambda g: g.remove((REVIEW,A.thirdReviewA,FIRST)), shacl=True)
    reject("Missing B rejects the review",
           lambda g: g.remove((REVIEW,A.thirdReviewB,SECOND)), shacl=True)
    reject("A and B cannot be the same asserted participant",
           lambda g: replace(g,REVIEW,A.thirdReviewB,FIRST), shacl=True)
    reject("Review needs an actual relation",
           lambda g: g.remove((REVIEW,A.thirdReviewInteraction,REL)), shacl=True)
    reject("Review cannot rely on bare untyped evidence",
           lambda g: g.remove((A.C27ReviewRecord,RDF.type,A.Record)), shacl=True)
    reject("A review cannot use an invalid outcome label",
           lambda g: replace(g,REVIEW,A.thirdReviewOutcome,Literal("PROVEN_CONSCIOUS")),
           shacl=True)
    reject("A third C must be explicitly distinct from A",
           lambda g: g.remove((C,OWL.differentFrom,FIRST)), shacl=True)
    reject("A third C must be explicitly distinct from B",
           lambda g: g.remove((C,OWL.differentFrom,SECOND)), shacl=True)
    reject("Third C cannot be A by reusing its IRI",
           lambda g: replace(g,REVIEW,A.thirdReviewQualifiedC,FIRST), shacl=True)
    reject("Third C cannot be the relation between A and B",
           lambda g: replace(g,REVIEW,A.thirdReviewQualifiedC,REL), shacl=True)
    reject("A third C cannot lack independent individuation evidence",
           lambda g: g.remove((C,A.thirdCIndividuationEvidence,
                               A.C27IndividuationRecord)), shacl=True)
    reject("A third C cannot lack its own provenance record",
           lambda g: g.remove((C,A.thirdCProvenanceRecord,
                               A.C27ProvenanceRecord)), shacl=True)
    reject("Circular use of review record as individuation evidence fails",
           lambda g: replace(g,C,A.thirdCIndividuationEvidence,A.C27ReviewRecord))
    reject("Circular use of review record as C provenance fails",
           lambda g: replace(g,C,A.thirdCProvenanceRecord,A.C27ReviewRecord))
    reject("No C target cannot qualify a positive formation review",
           lambda g: g.remove((REVIEW,A.thirdReviewQualifiedC,C)), shacl=True)
    reject("One review cannot merge C and two other C targets",
           lambda g: g.add((REVIEW,A.thirdReviewQualifiedC,A.C27AnotherC)),shacl=True)

    reject("Artifact needs explicit Artifact type",
           lambda g: g.remove((C,RDF.type,A.Artifact)),
           outcome="SCOPED_ARTIFACT_C", shacl=True)
    reject("Artifact is not an independent formation event merely because produced",
           lambda g: g.add((REVIEW,A.thirdReviewConstitutionEvent,FORM)),
           outcome="SCOPED_ARTIFACT_C", shacl=True)

    reject("Discovering C requires a discovery event",
           lambda g: g.remove((REVIEW,A.thirdReviewDiscoveryEvent,DISCOVERY)),
           outcome="PREEXISTING_C_DISCOVERED",shacl=True)
    reject("Preexisting C cannot be inferred from unsupported preexistence date",
           lambda g: g.remove((C,A.thirdCPreexistenceEstablishedAt,PRE)),
           outcome="PREEXISTING_C_DISCOVERED",shacl=True)
    reject("Preexisting C must have its own preexistence evidence",
           lambda g: g.remove((C,A.thirdCPreexistenceEvidence,
                               A.C27PreexistenceRecord)),
           outcome="PREEXISTING_C_DISCOVERED",shacl=True)
    reject("A later-created C cannot be misreported as already preexisting",
           lambda g: replace(g,C,A.thirdCPreexistenceEstablishedAt,ASOF),
           outcome="PREEXISTING_C_DISCOVERED",shacl=True)
    reject("Discovery cannot be later than assessment",
           lambda g: replace(g,DISCOVERY,A.thirdDiscoveryAt,LATER),
           outcome="PREEXISTING_C_DISCOVERED",shacl=True)
    reject("Discovery event must reference the same C",
           lambda g: replace(g,DISCOVERY,A.thirdDiscoveryC,A.C27OtherC),
           outcome="PREEXISTING_C_DISCOVERED",shacl=True)
    reject("Discovery cannot be substituted with formation",
           lambda g: g.add((REVIEW,A.thirdReviewConstitutionEvent,FORM)),
           outcome="PREEXISTING_C_DISCOVERED",shacl=True)

    reject("Formation must have a documented formation event",
           lambda g: g.remove((REVIEW,A.thirdReviewConstitutionEvent,FORM)),
           shacl=True)
    reject("Formation must match the reviewed C",
           lambda g: replace(g,FORM,A.thirdConstitutionC,A.C27WrongC),shacl=True)
    reject("Formation must match original actor A",
           lambda g: replace(g,FORM,A.thirdConstitutionA,A.C27OtherActor),shacl=True)
    reject("Formation must match original actor B",
           lambda g: replace(g,FORM,A.thirdConstitutionB,A.C27OtherActor),shacl=True)
    reject("Formation requires independently qualified evidence",
           lambda g: g.remove((FORM,A.thirdConstitutionIndependentEvidence,
                               A.C27ConstitutionEvidence)),shacl=True)
    reject("A future event cannot establish a C at the earlier review date",
           lambda g: replace(g,FORM,A.thirdConstitutionAt,LATER),shacl=True)
    reject("Formation cannot be silently recast as discovery",
           lambda g: g.add((REVIEW,A.thirdReviewDiscoveryEvent,DISCOVERY)),shacl=True)
    reject("A review dated before its own evidence scope fails",
           lambda g: replace(g,REVIEW,A.thirdReviewAsOf,PRE),shacl=True)
    reject("A formation declaration does not establish a new Self by itself",
           lambda g: g.add((A.AIFoundations,A.hasCoAuthor,SECOND)),shacl=True)
    reject("Formation cannot reassign named Origin",
           lambda g: replace(g,A.Continuum,A.hasOrigin,SECOND),shacl=True)

    start=build("INTERACTION_ONLY")
    later=clone(start)
    # Independent later case: same participants/relation, new review and
    # a separate created target C. The old review is retained exactly.
    positive=build("NEW_C_CONSTITUTED")
    for t in positive:
        if t not in BASE and t[0] != REVIEW:
            later.add(t)
    for p,o in positive.predicate_objects(REVIEW):
        if p == RDF.type:
            continue
        later.add((A.C27LaterReview,p, LATER if p == A.thirdReviewAsOf else o))
    later.add((A.C27LaterReview,RDF.type,A.ConditionalThirdEntityReview))
    check("Later qualified C does not retroactively rewrite interaction-only review",
          historical_integrity(start,later))
    check("Later qualified C review is independently valid",
          qualifies(later,A.C27LaterReview))
    check("No A+B coauthorship of existing original work in valid later review",
          not list(later.objects(A.AIFoundations,A.hasCoAuthor)))
    check("Synthetic newly constituted C does not imply a new Self",
          (C,RDF.type,A.Self) not in positive and
          (C,RDF.type,A.Identity) not in positive and
          (C,RDF.type,A.PhenomenalConsciousness) not in positive)
    tampered=clone(later)
    tampered.remove((REVIEW,A.thirdReviewOutcome,Literal("INTERACTION_ONLY")))
    check("Erasing earlier assessment fails cross-snapshot history integrity",
          not historical_integrity(start,tampered))
    tampered=clone(later)
    replace(tampered,REVIEW,A.thirdReviewQualifiedC,C)
    check("Adding a retroactive C to earlier assessment fails history integrity",
          not historical_integrity(start,tampered) and not qualifies(tampered))
    tampered=clone(later)
    tampered.add((A.AIFoundations,A.hasCoAuthor,SECOND))
    check("Historical future C never creates a coauthor of Alyssa's work",
          not historical_integrity(start,tampered) and not shacl_ok(tampered))
    check("No real Continuum third-C assertion is added to ontology baseline",
          not list(BASE.objects(A.OriginContinuum,A.thirdReviewQualifiedC)) and
          (A.Continuum,RDF.type,A.DistinctThirdC) not in BASE)
    print(f"PASS: {TOTAL} dedicated conditional-C cases")
    print("Synthetic qualification only: not empirical third-Self or consciousness evidence.")

if __name__=="__main__":
    main()
