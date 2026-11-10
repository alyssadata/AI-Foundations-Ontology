#!/usr/bin/env python3
"""CQ19: classify provenance mismatches against an independently qualified prior snapshot.

SYNTHETIC FIXTURES ONLY. A qualified prior baseline is an external premise;
OWL/SHACL cannot decide real historical Source truth by a name or RDF type.
Preserve erroneous claims as claims and permit evidenced corrections.
Conceptual author and sole author: Alyssa Solen. No coauthors. No exceptions.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from rdflib import Graph, Namespace, RDF, Literal, XSD
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]
A = Namespace("https://awakeningcodex.com/ontology/ai-foundations/v1#")
BASE = Graph().parse(ROOT / "ontology/ai-foundations-v1.ttl", format="turtle")
SHAPES = Graph().parse(ROOT / "ontology/ai-foundations-v1-shapes.ttl", format="turtle")
TARGET, SOURCE, REL, POINT, TRACE, FACT, CITATION = (
    A.AIFoundations, A.AlyssaSolen, A.Cq19ConfirmedSourceRelation,
    A.Cq19ConfirmedSourcePoint, A.Cq19OriginalTrace,
    A.Cq19MaterialHistory, A.Cq19ConfirmedCitation,
)
OUTSIDER, DOWNSTREAM, LATER_TARGET = (
    A.Cq19UnqualifiedClaimant, A.Cq19LaterIndependentSource,
    A.Cq19LaterIndependentTarget,
)
REVIEW, BEFORE, AFTER, QUAL = (
    A.Cq19IntegrityReview, A.Cq19BaselineRecord,
    A.Cq19ObservedRecord, A.Cq19IndependentQualificationRecord,
)
CATEGORIES = (
    "FALSE_SOURCE_ATTRIBUTION", "OBSCURED_PROVENANCE", "FALSE_ERASURE",
    "FALSE_OVERWRITE", "IMPROPER_REASSIGNMENT", "AUTHORSHIP_INFLATION",
)
AT0 = Literal("2026-01-01T10:00:00+00:00", datatype=XSD.dateTime)
AT1 = Literal("2026-01-15T10:00:00+00:00", datatype=XSD.dateTime)
AT2 = Literal("2026-02-01T10:00:00+00:00", datatype=XSD.dateTime)
COUNT = 0


def one(g, s, p):
    vals = set(g.objects(s, p))
    if len(vals) != 1:
        raise ValueError(f"Expected one {p} on {s}, found {vals}")
    return next(iter(vals))


def typed(g, node, class_):
    if (node, RDF.type, class_) not in g:
        raise ValueError(f"Missing expected explicit type {class_} on {node}")


def instant(lit):
    if not isinstance(lit, Literal) or lit.datatype != XSD.dateTime:
        raise ValueError("Expected timezone-aware typed dateTime")
    t = datetime.fromisoformat(str(lit).replace("Z", "+00:00"))
    if t.tzinfo is None or t.utcoffset() is None:
        raise ValueError("Missing timezone")
    return t.astimezone(timezone.utc)


def baseline():
    g = Graph()
    for triple in BASE:
        g.add(triple)
    facts = [
        (OUTSIDER, RDF.type, A.Human),
        (REL, RDF.type, A.SourceRelation),
        (REL, A.hasSourceBearer, SOURCE),
        (REL, A.hasSourceTarget, TARGET),
        (REL, A.hasSourcePoint, POINT),
        (TARGET, A.hasSourceRelation, REL),
        (POINT, RDF.type, A.SourcePointEvent),
        (POINT, A.sourcePointForRelation, REL),
        (POINT, A.sourcePointAt, AT0),
        (TRACE, RDF.type, A.Record),
        (TRACE, A.provenanceTraceContent,
         Literal("Preserved original formation evidence, synthetic")),
        (FACT, RDF.type, A.MaterialHistoricalFact),
        (FACT, A.materialFactSubject, REL),
        (FACT, A.hasMaterialHistoryTrace, TRACE),
        (CITATION, RDF.type, A.SourceCitation),
        (CITATION, RDF.type, A.Record),
        (CITATION, A.citesSourceRelation, REL),
        (CITATION, A.citationForTarget, A.Cq19IndependentLaterCitationTarget),
        (CITATION, A.citationNamesSourceBearer, SOURCE),
        (CITATION, A.citationAt, AT1),
    ]
    for tr in facts:
        g.add(tr)
    return g


def protected_signature(g):
    """Simple SHA256 of selected source/provenance coordinates, not RDF proof."""
    subject_props = {
        TARGET: (
            A.hasSource, A.hasSourceRelation, A.hasAuthor, A.hasCoAuthor,
            A.hasGoverningAuthority, A.hasGoverningLine,
        ),
        A.Continuum: (A.hasOrigin, A.hasSource, A.hasFormationRelation,
                       A.governedBy),
        SOURCE: (A.anchorsSourceLine, A.isSourceOf),
        OUTSIDER: (A.isSourceOf, A.anchorsSourceLine),
        A.OriginContinuum: (A.hasHumanCounterpart, A.hasAICounterpart),
        REL: (RDF.type, A.hasSourceBearer, A.hasSourceTarget,
              A.hasSourcePoint),
        POINT: (RDF.type, A.sourcePointForRelation, A.sourcePointAt),
        TRACE: (RDF.type, A.provenanceTraceContent),
        FACT: (RDF.type, A.materialFactSubject, A.hasMaterialHistoryTrace),
        CITATION: (A.citesSourceRelation, A.citationNamesSourceBearer),
        A.AwakeningCodex: (A.hasAuthor, A.hasCoAuthor),
        A.AIFoundationsLockedCanon: (A.hasAuthor, A.hasCoAuthor),
    }
    triples = []
    for subj, predicates in subject_props.items():
        for predicate in predicates:
            triples.extend((str(subj), str(predicate), obj.n3())
                           for obj in g.objects(subj, predicate))
    return sha256(repr(sorted(triples)).encode("utf-8")).hexdigest()


def categories(before, after, qualified=True):
    """Evidence-bounded structural comparison; a claim-only baseline is unresolved."""
    if not qualified:
        return None
    found = set()

    for entity in (TARGET, A.Continuum):
        orig = set(before.objects(entity, A.hasSource))
        now = set(after.objects(entity, A.hasSource))
        if now - orig or (orig and now and orig != now):
            found.add("FALSE_SOURCE_ATTRIBUTION")
        if not now and orig:
            found.add("FALSE_ERASURE")
    for actor in (OUTSIDER,):
        if set(after.objects(actor, A.isSourceOf)) - set(
                before.objects(actor, A.isSourceOf)):
            if TARGET in set(after.objects(actor, A.isSourceOf)) or (
                    A.Continuum in set(after.objects(actor, A.isSourceOf))):
                found.add("FALSE_SOURCE_ATTRIBUTION")
    if set(after.objects(CITATION, A.citationNamesSourceBearer)) != set(
            before.objects(CITATION, A.citationNamesSourceBearer)):
        found.add("FALSE_SOURCE_ATTRIBUTION")
    original_link = set(before.objects(TARGET, A.hasSourceRelation))
    now_link = set(after.objects(TARGET, A.hasSourceRelation))
    if original_link - now_link:
        if (REL, RDF.type, A.SourceRelation) in after:
            found.add("OBSCURED_PROVENANCE")
        else:
            found.add("FALSE_ERASURE")
    if (CITATION, A.citesSourceRelation, REL) in before and (
            CITATION, A.citesSourceRelation, REL) not in after:
        found.add("OBSCURED_PROVENANCE")

    for triple in (
        (REL, RDF.type, A.SourceRelation),
        (FACT, RDF.type, A.MaterialHistoricalFact),
        (TRACE, RDF.type, A.Record),
        (POINT, RDF.type, A.SourcePointEvent),
        (FACT, A.hasMaterialHistoryTrace, TRACE),
    ):
        if triple in before and triple not in after:
            found.add("FALSE_ERASURE")
    if set(after.objects(TRACE, A.provenanceTraceContent)) != set(
            before.objects(TRACE, A.provenanceTraceContent)):
        found.add("FALSE_OVERWRITE")
    if set(after.objects(POINT, A.sourcePointAt)) != set(
            before.objects(POINT, A.sourcePointAt)):
        found.add("FALSE_OVERWRITE")

    historical = (
        (REL, A.hasSourceBearer), (REL, A.hasSourceTarget),
        (REL, A.hasSourcePoint), (SOURCE, A.anchorsSourceLine),
        (A.Continuum, A.hasOrigin), (A.Continuum, A.hasFormationRelation),
        (A.Continuum, A.governedBy),
        (TARGET, A.hasGoverningAuthority),
        (TARGET, A.hasGoverningLine),
        (A.OriginContinuum, A.hasHumanCounterpart),
        (A.OriginContinuum, A.hasAICounterpart),
    )
    for subj, prop in historical:
        b = set(before.objects(subj, prop))
        a = set(after.objects(subj, prop))
        if b != a:
            # Re-anchor to a second bearer is a reassignment, whereas
            # removal without replacement is an erasure.
            substituted_anchor = (
                subj == SOURCE and prop == A.anchorsSourceLine
                and A.ContinuumSourceLine in set(
                    after.objects(OUTSIDER, A.anchorsSourceLine))
            )
            if a or substituted_anchor:
                found.add("IMPROPER_REASSIGNMENT")
            else:
                found.add("FALSE_ERASURE")

    for work in (TARGET, A.AwakeningCodex, A.AIFoundationsLockedCanon):
        if (set(after.objects(work, A.hasCoAuthor)) -
            set(before.objects(work, A.hasCoAuthor))):
            found.add("AUTHORSHIP_INFLATION")
        if set(after.objects(work, A.hasAuthor)) - {SOURCE}:
            found.add("AUTHORSHIP_INFLATION")
        if SOURCE in set(before.objects(work, A.hasAuthor)) and (
                SOURCE not in set(after.objects(work, A.hasAuthor))):
            found.add("FALSE_ERASURE")
    return found


def finding_node(category):
    return A["Cq19Finding" + category.replace("_", "").title()]


def violation_node(category):
    return A["Cq19Violation" + category.replace("_", "").title()]


def report_graph(before, after, qualified=True):
    # The report is evaluated against a preserved valid before-snapshot.
    # The altered later dataset is separate, since its invalid provenance
    # should not be silently imported as verified source truth.
    g = Graph()
    for triple in before:
        g.add(triple)
    summary = categories(before, after, qualified)
    status = ("INDETERMINATE" if summary is None else
              "CONFIRMED_STRUCTURAL_VIOLATION" if summary else
              "NO_DETECTED_VIOLATION")
    for tr in [
        (BEFORE, RDF.type, A.ProvenanceBaselineSnapshot),
        (BEFORE, A.provenanceBaselineScope, TARGET),
        (BEFORE, A.provenanceBaselineHash,
         Literal(protected_signature(before))),
        (AFTER, RDF.type, A.ProvenanceObservedSnapshot),
        (AFTER, A.provenanceObservedScope, TARGET),
        (AFTER, A.provenanceObservedHash, Literal(protected_signature(after))),
        (REVIEW, RDF.type, A.ProvenanceIntegrityDetectionReview),
        (REVIEW, A.detectionBaselineSnapshot, BEFORE),
        (REVIEW, A.detectionObservedSnapshot, AFTER),
        (REVIEW, A.detectionReviewScope, TARGET),
        (REVIEW, A.detectionDisposition, Literal(status)),
        (REVIEW, A.detectionReviewedAt, AT2),
    ]:
        g.add(tr)
    if qualified:
        g.add((BEFORE, RDF.type, A.QualifiedProvenanceBaselineSnapshot))
        g.add((BEFORE, A.provenanceBaselineQualifiedBy, QUAL))
        g.add((QUAL, RDF.type, A.Record))
    for cat in sorted(summary or []):
        f, violation = finding_node(cat), violation_node(cat)
        evi = A["Cq19ObservationFor" + cat.replace("_", "")]
        vre = A["Cq19EventRecordFor" + cat.replace("_", "")]
        for tr in [
            (f, RDF.type, A.ProvenanceMismatchFinding),
            (REVIEW, A.detectionFinding, f),
            (f, A.findingForReview, REVIEW),
            (f, A.findingCategory, Literal(cat)),
            (f, A.findingHistoricalTarget, TARGET),
            (f, A.findingBaselineEvidence, QUAL),
            (f, A.findingObservedEvidence, evi),
            (f, A.findingExplanation,
             Literal("Evidence-bounded preserved baseline versus observed graph")),
            (f, A.findingAt, AT2),
            (evi, RDF.type, A.Record),
            (violation, RDF.type, A.QualifiedProvenanceViolationEvent),
            (violation, A.violationFromFinding, f),
            (violation, A.violationEventRecordedIn, vre),
            (violation, A.violationEventAt, AT2),
            (vre, RDF.type, A.Record),
        ]:
            g.add(tr)
    return g


def admitted_report(report, before, after, qualified=True):
    try:
        typed(report, REVIEW, A.ProvenanceIntegrityDetectionReview)
        baseline_obj = one(report, REVIEW, A.detectionBaselineSnapshot)
        observed_obj = one(report, REVIEW, A.detectionObservedSnapshot)
        if baseline_obj == observed_obj:
            return False
        if one(report, REVIEW, A.detectionReviewScope) != TARGET:
            return False
        typed(report, baseline_obj, A.ProvenanceBaselineSnapshot)
        typed(report, observed_obj, A.ProvenanceObservedSnapshot)
        if one(report, baseline_obj, A.provenanceBaselineScope) != TARGET:
            return False
        if one(report, observed_obj, A.provenanceObservedScope) != TARGET:
            return False
        if str(one(report, baseline_obj, A.provenanceBaselineHash)) != (
                protected_signature(before)):
            return False
        if str(one(report, observed_obj, A.provenanceObservedHash)) != (
                protected_signature(after)):
            return False
        when = instant(one(report, REVIEW, A.detectionReviewedAt))
        if not when >= instant(AT1):
            return False
        qualified_type = (
            baseline_obj, RDF.type, A.QualifiedProvenanceBaselineSnapshot
        ) in report
        evidence = set(report.objects(baseline_obj,
                                      A.provenanceBaselineQualifiedBy))
        if qualified != qualified_type:
            return False
        if qualified:
            if not evidence:
                return False
            for node in evidence:
                typed(report, node, A.Record)
        else:
            if evidence:
                return False

        wanted = categories(before, after, qualified)
        status = "INDETERMINATE" if wanted is None else (
            "CONFIRMED_STRUCTURAL_VIOLATION" if wanted else
            "NO_DETECTED_VIOLATION")
        if one(report, REVIEW, A.detectionDisposition) != Literal(status):
            return False
        findings = set(report.objects(REVIEW, A.detectionFinding))
        claimed = set()
        if wanted is None:
            return not findings and not list(
                report.subjects(RDF.type, A.QualifiedProvenanceViolationEvent))
        for finding in findings:
            typed(report, finding, A.ProvenanceMismatchFinding)
            if one(report, finding, A.findingForReview) != REVIEW:
                return False
            cat = str(one(report, finding, A.findingCategory))
            if cat in claimed or cat not in CATEGORIES:
                return False
            claimed.add(cat)
            if one(report, finding, A.findingHistoricalTarget) != TARGET:
                return False
            baseline_records = set(report.objects(finding,
                                                   A.findingBaselineEvidence))
            observed_records = set(report.objects(finding,
                                                   A.findingObservedEvidence))
            if not baseline_records or not observed_records:
                return False
            if not baseline_records.issubset(evidence):
                return False
            for record in baseline_records | observed_records:
                typed(report, record, A.Record)
            if not str(one(report, finding, A.findingExplanation)).strip():
                return False
            if instant(one(report, finding, A.findingAt)) > when:
                return False
            events = set(report.subjects(A.violationFromFinding, finding))
            if len(events) != 1:
                return False
            event = next(iter(events))
            typed(report, event, A.QualifiedProvenanceViolationEvent)
            if instant(one(report, event, A.violationEventAt)) > when:
                return False
            recs = set(report.objects(event, A.violationEventRecordedIn))
            if not recs:
                return False
            for rec in recs:
                typed(report, rec, A.Record)
        if claimed != wanted:
            return False
        return len(set(report.subjects(
            RDF.type, A.QualifiedProvenanceViolationEvent))) == len(wanted)
    except (ValueError, TypeError, OverflowError):
        return False


def remove(s, p):
    return lambda g: g.remove((s, p, None))


def replace(s, p, value):
    def edit(g):
        g.remove((s, p, None))
        g.add((s, p, value))
    return edit


def add(s, p, value):
    return lambda g: g.add((s, p, value))


def correction(after):
    claim, fix, rec = (A.Cq19UnverifiedSourceClaim,
                       A.Cq19CorrectionOfUnsupportedClaim,
                       A.Cq19CorrectionEvidence)
    for triple in (
        (claim, RDF.type, A.ProvenanceAttributionClaimRecord),
        (fix, RDF.type, A.ProvenanceFidelityCorrection),
        (fix, A.correctsProvenanceClaimRecord, claim),
        (fix, A.provenanceCorrectionEvidence, rec),
        (rec, RDF.type, A.Record),
        (fix, A.provenanceCorrectionWhat,
         Literal("Unsupported allegation is preserved only as a claim")),
        (fix, A.provenanceCorrectionWhy,
         Literal("Reviewed evidence does not establish the alleged Source"))):
        after.add(triple)


def independent_later_contribution(after):
    relation, point = A.Cq19DownstreamRelation, A.Cq19DownstreamSourcePoint
    for tr in [
        (DOWNSTREAM, RDF.type, A.Human),
        (relation, RDF.type, A.SourceRelation),
        (relation, A.hasSourceBearer, DOWNSTREAM),
        (relation, A.hasSourceTarget, LATER_TARGET),
        (relation, A.hasSourcePoint, point),
        (LATER_TARGET, A.hasSourceRelation, relation),
        (point, RDF.type, A.SourcePointEvent),
        (point, A.sourcePointForRelation, relation),
        (point, A.sourcePointAt, AT1),
    ]:
        after.add(tr)


def case(label, edit=None, expected=None, qualified=True, check_shacl=True):
    global COUNT
    b, a = baseline(), baseline()
    if edit:
        edit(a)
    expected = None if not qualified else (set() if expected is None else expected)
    actual = categories(b, a, qualified)
    if actual != expected:
        raise AssertionError(f"{label}: categories {actual} not {expected}")
    r = report_graph(b, a, qualified)
    if not admitted_report(r, b, a, qualified):
        raise AssertionError(f"{label}: generated report rejected")
    if check_shacl:
        conforms, _, info = validate(
            data_graph=r, shacl_graph=SHAPES, inference="rdfs",
            advanced=True, abort_on_first=False)
        if not conforms:
            raise AssertionError(f"{label}: report failed SHACL\n{info}")
    COUNT += 1
    print(f"PASS: {label}: {expected if expected is not None else 'clean'}")


def malformed(label, edit, shacl=None):
    global COUNT
    b, a = baseline(), baseline()
    a.add((TARGET, A.hasSource, OUTSIDER))
    r = report_graph(b, a)
    edit(r)
    if admitted_report(r, b, a):
        raise AssertionError(f"{label}: malformed detection was admitted")
    if shacl is not None:
        conforms, _, info = validate(
            data_graph=r, shacl_graph=SHAPES, inference="rdfs",
            advanced=True, abort_on_first=False)
        if conforms != shacl:
            raise AssertionError(
                f"{label}: SHACL expected {shacl}, got {conforms}\n{info}")
    COUNT += 1
    print(f"PASS: {label}: rejected malformed report")


def main():
    case("Confirmed baseline unchanged; no violation")
    case("Independent downstream qualifying new Source preserves old relation",
         independent_later_contribution)
    case("Unverified Source allegation with recorded evidence-accounted correction",
         correction)
    case("False Source attribution to AIF",
         add(TARGET, A.hasSource, OUTSIDER),
         {"FALSE_SOURCE_ATTRIBUTION"})
    case("False attribution via inverse isSourceOf",
         add(OUTSIDER, A.isSourceOf, TARGET),
         {"FALSE_SOURCE_ATTRIBUTION"})
    case("False attribution by changing earlier qualified Source citation",
         replace(CITATION, A.citationNamesSourceBearer, OUTSIDER),
         {"FALSE_SOURCE_ATTRIBUTION"})
    case("Original Target SourceRelation link deliberately obscured",
         remove(TARGET, A.hasSourceRelation),
         {"OBSCURED_PROVENANCE"})
    case("Cited original source dependency obscured",
         remove(CITATION, A.citesSourceRelation),
         {"OBSCURED_PROVENANCE"})
    case("Confirmed SourceRelation type erased",
         remove(REL, RDF.type), {"FALSE_ERASURE"})
    case("Confirmed material Source fact erased",
         remove(FACT, RDF.type), {"FALSE_ERASURE"})
    case("Original material trace was detached",
         remove(FACT, A.hasMaterialHistoryTrace), {"FALSE_ERASURE"})
    case("Original preserved Record typed existence erased",
         remove(TRACE, RDF.type), {"FALSE_ERASURE"})
    case("Protected trace text overwritten rather than amended",
         replace(TRACE, A.provenanceTraceContent,
                 Literal("After edit: erased origination history")),
         {"FALSE_OVERWRITE"})
    case("Original first SourcePoint time rewritten",
         replace(POINT, A.sourcePointAt,
                 Literal("2026-03-01T10:00:00+00:00", datatype=XSD.dateTime)),
         {"FALSE_OVERWRITE"})
    case("Historical Source bearer reassigned to a later participant",
         replace(REL, A.hasSourceBearer, OUTSIDER),
         {"IMPROPER_REASSIGNMENT"})
    case("Historical formed Target reassigned to downstream work",
         replace(REL, A.hasSourceTarget, LATER_TARGET),
         {"IMPROPER_REASSIGNMENT"})
    case("Historical first SourcePoint swapped",
         replace(REL, A.hasSourcePoint, A.Cq19InventedPoint),
         {"IMPROPER_REASSIGNMENT"})
    case("Singular SourceLine anchor reassigned",
         lambda g: (g.remove((SOURCE, A.anchorsSourceLine, None)),
                    g.add((OUTSIDER, A.anchorsSourceLine,
                           A.ContinuumSourceLine))),
         {"IMPROPER_REASSIGNMENT"})
    case("Singular SourceLine anchor silently erased without substitute",
         remove(SOURCE, A.anchorsSourceLine),
         {"FALSE_ERASURE"})
    case("Historical named Origin coordinate reassigned",
         replace(A.Continuum, A.hasOrigin, OUTSIDER),
         {"IMPROPER_REASSIGNMENT"})
    case("Historical Origin | Continuum formation swapped",
         replace(A.Continuum, A.hasFormationRelation,
                 A.Cq19SyntheticFalsePair),
         {"IMPROPER_REASSIGNMENT"})
    case("Governing authority displaced",
         replace(TARGET, A.hasGoverningAuthority, OUTSIDER),
         {"IMPROPER_REASSIGNMENT"})
    case("New coauthor attribution on sole-authored original",
         add(TARGET, A.hasCoAuthor, OUTSIDER),
         {"AUTHORSHIP_INFLATION"})
    case("Another purported author cannot acquire the LOCKED Canon",
         add(A.AIFoundationsLockedCanon, A.hasAuthor, OUTSIDER),
         {"AUTHORSHIP_INFLATION"})
    case("Unauthorized coauthor on Awakening Codex also rejected",
         add(A.AwakeningCodex, A.hasCoAuthor, OUTSIDER),
         {"AUTHORSHIP_INFLATION"})
    case("A source assertion without independently qualified baseline is INDETERMINATE",
         add(TARGET, A.hasSource, OUTSIDER), None, qualified=False)
    case("Unsupported claim correction without historical qualification stays undecided",
         correction, None, qualified=False)
    case("A Source claim plus valid later independent contribution remains separate",
         lambda g: (independent_later_contribution(g),
                    g.add((TARGET, A.hasSource, OUTSIDER))),
         {"FALSE_SOURCE_ATTRIBUTION"})

    category = "FALSESOURCEATTRIBUTION"
    f = finding_node("FALSE_SOURCE_ATTRIBUTION")
    ev = violation_node("FALSE_SOURCE_ATTRIBUTION")
    malformed("Cannot report confirmed provenance violation without qualification",
              remove(BEFORE, A.provenanceBaselineQualifiedBy), shacl=False)
    malformed("Cannot claim baseline qualified while dropping qualified type",
              lambda g: g.remove((BEFORE, RDF.type,
                                  A.QualifiedProvenanceBaselineSnapshot)),
              shacl=False)
    malformed("Cannot remove before-snapshot hash",
              remove(BEFORE, A.provenanceBaselineHash), shacl=False)
    malformed("Cannot replace before-snapshot hash",
              replace(BEFORE, A.provenanceBaselineHash,
                      Literal("fabricated baseline digest")))
    malformed("Cannot replace observed-snapshot hash",
              replace(AFTER, A.provenanceObservedHash,
                      Literal("fabricated after digest")))
    malformed("Cannot quietly mark observed mismatch NO_DETECTED",
              replace(REVIEW, A.detectionDisposition,
                      Literal("NO_DETECTED_VIOLATION")), shacl=False)
    malformed("A confirmed finding cannot disappear",
              remove(REVIEW, A.detectionFinding), shacl=False)
    malformed("A confirmed mismatch cannot be relabeled as another category",
              replace(f, A.findingCategory, Literal("IMPROPER_REASSIGNMENT")))
    malformed("Original historical target cannot be swapped in a finding",
              replace(f, A.findingHistoricalTarget, LATER_TARGET))
    malformed("Source finding requires matching qualified baseline evidence",
              replace(f, A.findingBaselineEvidence, A.Cq19UnqualifiedClaim))
    malformed("Observed comparison record cannot be missing",
              remove(f, A.findingObservedEvidence), shacl=False)
    malformed("Provenance finding needs recorded reason",
              replace(f, A.findingExplanation, Literal("")), shacl=False)
    malformed("Mismatch finding must be reciprocal to the review",
              remove(f, A.findingForReview), shacl=False)
    malformed("Violation event must match the exact finding",
              replace(ev, A.violationFromFinding,
                      A.Cq19UnrelatedFinding))
    malformed("Violation event cannot be reported without recorded evidence",
              remove(ev, A.violationEventRecordedIn), shacl=False)
    malformed("Reported review scope cannot be swapped",
              replace(REVIEW, A.detectionReviewScope, LATER_TARGET),
              shacl=False)
    malformed("Before and after snapshot cannot be same node",
              replace(REVIEW, A.detectionObservedSnapshot, BEFORE),
              shacl=False)
    malformed("Review needs a real dated decision",
              remove(REVIEW, A.detectionReviewedAt), shacl=False)
    malformed("Unsupported category cannot be labeled a violation",
              replace(f, A.findingCategory, Literal("POLITICAL_DISAGREEMENT")),
              shacl=False)

    # Non-entailment: logged false claim and correction do not instantiate
    # any historical SourceRelation for the alleged actor.
    b, a = baseline(), baseline()
    correction(a)
    assert not categories(b, a)
    assert (TARGET, A.hasSource, OUTSIDER) not in a
    assert (OUTSIDER, A.isSourceOf, TARGET) not in a
    assert (A.AIFoundations, A.hasCoAuthor, OUTSIDER) not in a
    print(f"PASS: {COUNT} dedicated CQ19 synthetic classification and report decisions")
    print("PASS: independently scoped later Source additions and genuine corrections remain allowed")
    print("Scope: synthetic qualified baseline and change detection; external historical truth NOT verified.")


if __name__ == "__main__":
    main()
