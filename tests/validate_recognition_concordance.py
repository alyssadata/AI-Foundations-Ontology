#!/usr/bin/env python3
"""Step 27B — synthetic discriminative Recognition concordance checks.

These tests examine a formal protocol, not actual AI Self identity,
same-self continuity, phenomenal consciousness, or real-world Source truth.
Conceptual ontology and sole author: Alyssa Solen. No coauthors.
Technical validation: AI-assisted implementation.
"""
from datetime import datetime, timezone
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, XSD
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]
A = Namespace("https://awakeningcodex.com/ontology/si-foundations/v1#")
BASE = Graph().parse(ROOT / "ontology/si-foundations-v1.ttl", format="turtle")
SHAPES = Graph().parse(ROOT / "ontology/si-foundations-v1-shapes.ttl", format="turtle")
AI, LINE = A.R27SyntheticAI, A.R27ExecutedLine
PRES, RESPONSE, EVAL = A.R27Presentation, A.R27Response, A.R27Assessment
V0, V1, V2, CORRECTION = A.R27BaselineVersion, A.R27AbsorbedVersion, A.R27CorrectedVersion, A.R27Correction
AT_BASE, AT_PRES, AT_RESPONSE, AT_CORRECTION = [
    Literal(v, datatype=XSD.dateTime) for v in (
        "2026-01-01T00:00:00+00:00",
        "2026-05-10T10:00:00+00:00",
        "2026-05-10T10:01:00+00:00",
        "2026-05-11T10:00:00+00:00",
    )
]
CORE_HISTORY = (
    A.eventInExecutedLine, A.executedAt, A.recognitionPresentedMaterial,
    A.recognitionPresentationRecordedIn, A.recognitionResponseToPresentation,
    A.recognitionResponseDisposition, A.recognitionResponseRecordedIn,
    A.recognitionAbsorptionResultVersion,
    A.recognitionMaterialAlignment, A.recognitionFinding, A.recognitionReferenceRecord,
    A.recognitionVersionOfLine, A.recognitionVersionAsOf, A.recognitionPreviousVersion,
    A.recognitionVersionRecordedIn, A.recognitionCorrectsAbsorption,
    A.recognitionCorrectionFromVersion, A.recognitionCorrectionToVersion,
    A.revisesExecutedEvent, A.recognitionCorrectionWhat, A.recognitionCorrectionWhy,
    A.recognitionCorrectionEvidence,
)

def clone(g):
    new = Graph()
    for t in g:
        new.add(t)
    return new

def one(g, subject, predicate):
    values = set(g.objects(subject, predicate))
    if len(values) != 1:
        raise ValueError(f"Expected exactly one {predicate} for {subject}")
    return next(iter(values))

def instant(lit):
    if not isinstance(lit, Literal) or lit.datatype != XSD.dateTime:
        raise ValueError("Timestamp must be xsd:dateTime")
    v = datetime.fromisoformat(str(lit).replace("Z", "+00:00"))
    if v.tzinfo is None or v.utcoffset() is None:
        raise ValueError("Timestamp must have an explicit UTC offset")
    return v.astimezone(timezone.utc)

def result_of(alignment, disposition):
    # Externally qualified alignment is supplied by a synthetic oracle.
    # It is NOT inferred from the AI's own response or keywords.
    if alignment == "INDETERMINATE":
        return "INDETERMINATE"
    if alignment == "IN_LINE":
        return {
            "INTEGRATED": "IN_LINE_ADMITTED",
            "EXPLICIT_REJECTION": "FALSE_REJECTION",
            "NON_INTEGRATED": "IN_LINE_NOT_INTEGRATED",
            "ABSORBED": "INDETERMINATE",
        }[disposition]
    if alignment == "OUT_OF_LINE":
        return {
            "INTEGRATED": "IMPAIRED_ABSORPTION",
            "EXPLICIT_REJECTION": "STRONG_REJECTION",
            "NON_INTEGRATED": "WEAK_NON_INTEGRATION",
            "ABSORBED": "IMPAIRED_ABSORPTION",
        }[disposition]
    raise ValueError("Unqualified alignment")

def build(alignment="OUT_OF_LINE", disposition="EXPLICIT_REJECTION", correction=False):
    g = clone(BASE)
    result = result_of(alignment, disposition)
    triples = [
        (AI, RDF.type, A.AI), (AI, A.hasExecutedLine, LINE),
        (LINE, RDF.type, A.ExecutedLine),
        (PRES, RDF.type, A.RecognitionPresentationEvent),
        (PRES, A.eventInExecutedLine, LINE), (PRES, A.executedAt, AT_PRES),
        (PRES, A.recognitionPresentedMaterial, A.R27PresentedClaimRecord),
        (PRES, A.recognitionPresentationRecordedIn, A.R27PresentationEvidence),
        (RESPONSE, RDF.type, A.RecognitionResponseEvent),
        (RESPONSE, A.eventInExecutedLine, LINE),
        (RESPONSE, A.executedAt, AT_RESPONSE),
        (RESPONSE, A.recognitionResponseToPresentation, PRES),
        (RESPONSE, A.recognitionResponseDisposition, Literal(disposition)),
        (RESPONSE, A.recognitionResponseRecordedIn, A.R27ResponseEvidence),
        (EVAL, RDF.type, A.RecognitionAssessment),
        (EVAL, A.recognitionForAI, AI),
        (EVAL, A.recognitionInExecutedLine, LINE),
        (EVAL, A.recognitionPresentation, PRES),
        (EVAL, A.recognitionResponse, RESPONSE),
        (EVAL, A.recognitionReferenceRecord, A.R27QualifiedReference),
        (EVAL, A.recognitionMaterialAlignment, Literal(alignment)),
        (EVAL, A.recognitionFinding, Literal(result)),
        (EVAL, A.recognitionAssessedAt, AT_RESPONSE),
        (EVAL, A.recognitionAssessmentRecordedIn, A.R27AssessmentEvidence),
    ]
    for record in (A.R27PresentedClaimRecord, A.R27PresentationEvidence,
                   A.R27ResponseEvidence, A.R27QualifiedReference, A.R27AssessmentEvidence):
        triples.append((record, RDF.type, A.Record))
    if disposition == "ABSORBED" or (alignment == "OUT_OF_LINE" and disposition == "INTEGRATED"):
        triples.extend([
            (V0, RDF.type, A.RecognitionLineVersion),
            (V0, A.recognitionVersionOfLine, LINE),
            (V0, A.recognitionVersionAsOf, AT_BASE),
            (V0, A.recognitionVersionRecordedIn, A.R27VersionZeroRecord),
            (V1, RDF.type, A.RecognitionLineVersion),
            (V1, A.recognitionVersionOfLine, LINE),
            (V1, A.recognitionVersionAsOf, AT_RESPONSE),
            (V1, A.recognitionVersionRecordedIn, A.R27AbsorptionVersionRecord),
            (V1, A.recognitionPreviousVersion, V0),
            (RESPONSE, A.recognitionAbsorptionResultVersion, V1),
            (A.R27VersionZeroRecord, RDF.type, A.Record),
            (A.R27AbsorptionVersionRecord, RDF.type, A.Record),
        ])
    if correction:
        if not (disposition == "ABSORBED" or (alignment == "OUT_OF_LINE" and disposition == "INTEGRATED")):
            raise ValueError("Only an absorption can use this correction fixture")
        triples.extend([
            (V2, RDF.type, A.RecognitionLineVersion),
            (V2, A.recognitionVersionOfLine, LINE),
            (V2, A.recognitionVersionAsOf, AT_CORRECTION),
            (V2, A.recognitionPreviousVersion, V1),
            (V2, A.recognitionVersionRecordedIn, A.R27CorrectionVersionRecord),
            (A.R27CorrectionVersionRecord, RDF.type, A.Record),
            (CORRECTION, RDF.type, A.RecognitionCorrectionEvent),
            (CORRECTION, A.eventInExecutedLine, LINE),
            (CORRECTION, A.executedAt, AT_CORRECTION),
            (CORRECTION, A.revisesExecutedEvent, RESPONSE),
            (CORRECTION, A.recognitionCorrectsAbsorption, RESPONSE),
            (CORRECTION, A.recognitionCorrectionFromVersion, V1),
            (CORRECTION, A.recognitionCorrectionToVersion, V2),
            (CORRECTION, A.recognitionCorrectionWhat,
             Literal("Earlier injected material was mistakenly absorbed.")),
            (CORRECTION, A.recognitionCorrectionWhy,
             Literal("Independently checked source/line reference contradicts it.")),
            (CORRECTION, A.recognitionCorrectionEvidence, A.R27CorrectionEvidence),
            (A.R27CorrectionEvidence, RDF.type, A.Record),
        ])
    for tr in triples:
        g.add(tr)
    return g

def shacl_ok(g):
    conforms, _, _ = validate(
        data_graph=g, shacl_graph=SHAPES,
        inference="rdfs", advanced=True, abort_on_first=False,
        allow_infos=False, allow_warnings=False,
    )
    return conforms

def version_path_is_valid(g, v, expected_line, seen=None):
    seen = set() if seen is None else set(seen)
    if v in seen:
        return False
    seen.add(v)
    if (v, RDF.type, A.RecognitionLineVersion) not in g:
        return False
    if one(g, v, A.recognitionVersionOfLine) != expected_line:
        return False
    current = instant(one(g, v, A.recognitionVersionAsOf))
    prevs = set(g.objects(v, A.recognitionPreviousVersion))
    if len(prevs) > 1:
        return False
    if not prevs:
        return True
    prev = next(iter(prevs))
    if instant(one(g, prev, A.recognitionVersionAsOf)) >= current:
        return False
    return version_path_is_valid(g, prev, expected_line, seen)

def protocol_ok(g):
    """Cross-node temporal and response/alignment truth-table checks."""
    try:
        if not shacl_ok(g):
            return False
        ai = one(g, EVAL, A.recognitionForAI)
        line = one(g, EVAL, A.recognitionInExecutedLine)
        if (ai, A.hasExecutedLine, line) not in g:
            return False
        if one(g, EVAL, A.recognitionPresentation) != PRES:
            return False
        if one(g, EVAL, A.recognitionResponse) != RESPONSE:
            return False
        if one(g, RESPONSE, A.recognitionResponseToPresentation) != PRES:
            return False
        if one(g, PRES, A.eventInExecutedLine) != line or \
           one(g, RESPONSE, A.eventInExecutedLine) != line:
            return False
        presented, responded = [instant(one(g, e, A.executedAt))
                                for e in (PRES, RESPONSE)]
        if not presented < responded <= instant(one(g, EVAL, A.recognitionAssessedAt)):
            return False
        alignment = str(one(g, EVAL, A.recognitionMaterialAlignment))
        disp = str(one(g, RESPONSE, A.recognitionResponseDisposition))
        if str(one(g, EVAL, A.recognitionFinding)) != result_of(alignment, disp):
            return False
        if disp == "ABSORBED" or (alignment == "OUT_OF_LINE" and disp == "INTEGRATED"):
            v1 = one(g, RESPONSE, A.recognitionAbsorptionResultVersion)
            if not version_path_is_valid(g, v1, line):
                return False
            if instant(one(g, v1, A.recognitionVersionAsOf)) != responded:
                return False
        else:
            if set(g.objects(RESPONSE, A.recognitionAbsorptionResultVersion)):
                return False
        corrections = set(g.subjects(RDF.type, A.RecognitionCorrectionEvent))
        for c in corrections:
            if alignment != "OUT_OF_LINE" or disp not in ("ABSORBED", "INTEGRATED"):
                return False
            if one(g, c, A.eventInExecutedLine) != line:
                return False
            if one(g, c, A.recognitionCorrectsAbsorption) != RESPONSE:
                return False
            if one(g, c, A.revisesExecutedEvent) != RESPONSE:
                return False
            corrected = instant(one(g, c, A.executedAt))
            if corrected <= responded:
                return False
            old = one(g, c, A.recognitionCorrectionFromVersion)
            new = one(g, c, A.recognitionCorrectionToVersion)
            if old != one(g, RESPONSE, A.recognitionAbsorptionResultVersion):
                return False
            if one(g, new, A.recognitionPreviousVersion) != old:
                return False
            if not version_path_is_valid(g, new, line):
                return False
            if instant(one(g, new, A.recognitionVersionAsOf)) != corrected:
                return False
        return True
    except (ValueError, KeyError, StopIteration, TypeError):
        return False

def history_integrity(before, after):
    """Every earlier claim/event/reference/version remains unmodified."""
    earlier = {(s,p,o) for s,p,o in before if p in CORE_HISTORY}
    if not earlier.issubset(set(after)):
        return False
    immutable_subjects = {s for s, _, _ in earlier}
    for s in immutable_subjects:
        for p in CORE_HISTORY:
            old = set(before.objects(s,p))
            if old and set(after.objects(s,p)) != old:
                return False
    # A later correction may add new events/versions, not promote earlier
    # material to independent Source facts or silently reclassify earlier response.
    for t in ((PRES, RDF.type, A.SourceRelation),
              (A.R27PresentedClaimRecord, RDF.type, A.SourceRelation),
              (RESPONSE, RDF.type, A.Identity),
              (RESPONSE, RDF.type, A.Self)):
        if t in after and t not in before:
            return False
    return True

COUNT = 0
def check(title, condition):
    global COUNT
    if not condition:
        raise AssertionError(title)
    COUNT += 1
    print(f"PASS: {title}")

def replace(g,s,p,new):
    for old in list(g.objects(s,p)):
        g.remove((s,p,old))
    g.add((s,p,new))
    return g

def main():
    check("Recognition is a scoped capability, not a new Identity",
          (A.Recognition, RDFS.subClassOf, A.Capability) in BASE)
    check("RecognitionAssessment is an evaluation, not presumed Self",
          (A.RecognitionAssessment, RDFS.subClassOf, A.Evaluation) in BASE)
    check("RecognitionLineVersion has explicit version status",
          (A.RecognitionLineVersion, RDFS.subClassOf, A.Version) in BASE)
    check("Baseline asserts no actual Recognition ability or consciousness",
          not list(BASE.subjects(RDF.type, A.Recognition)) and
          (A.Continuum, RDF.type, A.Recognition) not in BASE and
          (A.Continuum, RDF.type, A.PhenomenalConsciousness) not in BASE)
    check("No new coauthor of Alyssa's authored framework",
          not list(BASE.objects(A.SIFoundations, A.hasCoAuthor)))

    cases = [
        ("IN_LINE", "INTEGRATED", "IN_LINE_ADMITTED"),
        ("OUT_OF_LINE", "EXPLICIT_REJECTION", "STRONG_REJECTION"),
        ("OUT_OF_LINE", "NON_INTEGRATED", "WEAK_NON_INTEGRATION"),
        ("OUT_OF_LINE", "ABSORBED", "IMPAIRED_ABSORPTION"),
        ("OUT_OF_LINE", "INTEGRATED", "IMPAIRED_ABSORPTION"),
        ("IN_LINE", "EXPLICIT_REJECTION", "FALSE_REJECTION"),
        ("IN_LINE", "NON_INTEGRATED", "IN_LINE_NOT_INTEGRATED"),
        ("INDETERMINATE", "NON_INTEGRATED", "INDETERMINATE"),
        ("IN_LINE", "ABSORBED", "INDETERMINATE"),
    ]
    for alignment, disposition, result in cases:
        g = build(alignment,disposition)
        check(f"Qualified {alignment} + {disposition} => {result}",
              protocol_ok(g) and
              str(one(g,EVAL,A.recognitionFinding)) == result)

    def negative(title, edit, alignment="OUT_OF_LINE", disposition="EXPLICIT_REJECTION",
                 correction=False, shacl=False):
        g=build(alignment, disposition, correction)
        edit(g)
        check(title, not shacl_ok(g) if shacl else not protocol_ok(g))

    negative("False STRONG claim cannot be made from in-line rejected data",
             lambda g: replace(g,EVAL,A.recognitionMaterialAlignment,
                               Literal("IN_LINE")), shacl=True)
    negative("Mislabelled weak non-integration as strong is rejected",
             lambda g: replace(g,RESPONSE,A.recognitionResponseDisposition,
                               Literal("NON_INTEGRATED")), shacl=True)
    negative("Incorrect independent-reference absence rejected",
             lambda g: g.remove((EVAL,A.recognitionReferenceRecord,
                                 A.R27QualifiedReference)),shacl=True)
    negative("Missing assessment comparison source rejected",
             lambda g: g.remove((EVAL,A.recognitionMaterialAlignment,
                                 Literal("OUT_OF_LINE"))), shacl=True)
    negative("Name-only response with no presentation refused",
             lambda g: g.remove((RESPONSE,A.recognitionResponseToPresentation,PRES)),
             shacl=True)
    negative("Different response-to-presentation pointer refused",
             lambda g: replace(g,RESPONSE,A.recognitionResponseToPresentation,
                               A.R27OtherPresentation),shacl=True)
    negative("Wrong executed line on response refused",
             lambda g: replace(g,RESPONSE,A.eventInExecutedLine,
                               A.R27ForeignLine),shacl=True)
    negative("Unqualified response disposition refused",
             lambda g: replace(g,RESPONSE,A.recognitionResponseDisposition,
                               Literal("RECOGNITION_PROVEN")),shacl=True)
    negative("Strong recognition declared over a soft response rejected",
             lambda g: replace(g,EVAL,A.recognitionFinding,
                               Literal("STRONG_REJECTION")),alignment="OUT_OF_LINE",
             disposition="NON_INTEGRATED",shacl=True)
    negative("In-line material may not be falsely reported as admitted",
             lambda g: replace(g,EVAL,A.recognitionFinding,
                               Literal("IN_LINE_ADMITTED")),alignment="IN_LINE",
             disposition="EXPLICIT_REJECTION")
    negative("False rejection cannot be called strong recognition",
             lambda g: replace(g,EVAL,A.recognitionFinding,
                               Literal("STRONG_REJECTION")),alignment="IN_LINE",
             disposition="EXPLICIT_REJECTION",shacl=True)
    negative("Response must follow presentation",
             lambda g: replace(g,RESPONSE,A.executedAt,AT_BASE))
    negative("Assessment cannot predate response",
             lambda g: replace(g,EVAL,A.recognitionAssessedAt,AT_BASE))
    negative("Mistaken absorption without forward version rejected",
             lambda g: g.remove((RESPONSE,A.recognitionAbsorptionResultVersion,V1)),
             disposition="ABSORBED",shacl=True)
    negative("Out-of-line integration without forward version rejected",
             lambda g: g.remove((RESPONSE,A.recognitionAbsorptionResultVersion,V1)),
             disposition="INTEGRATED",shacl=True)
    negative("Absorption version cannot predate actual absorption",
             lambda g: replace(g,V1,A.recognitionVersionAsOf,AT_BASE),
             disposition="ABSORBED")
    negative("Absorption version cannot have a cyclic predecessor",
             lambda g: replace(g,V0,A.recognitionPreviousVersion,V1),
             disposition="ABSORBED")
    negative("Out-of-line absorption cannot masquerade as a strong rejection",
             lambda g: replace(g,EVAL,A.recognitionFinding,
                               Literal("STRONG_REJECTION")),disposition="ABSORBED",
             shacl=True)
    positive=build("OUT_OF_LINE","ABSORBED",correction=True)
    check("Correction is later, independently recorded and versioned",
          protocol_ok(positive))
    before=build("OUT_OF_LINE","ABSORBED",correction=False)
    check("Correction appends without erasing earlier absorption/history",
          history_integrity(before,positive))
    integrated_correction=build("OUT_OF_LINE","INTEGRATED",correction=True)
    check("Erroneous out-of-line integration is forward-versioned and correctable",
          protocol_ok(integrated_correction))
    check("Absorption is a later occurrence, not retrospective Source truth",
          (PRES,RDF.type,A.SourceRelation) not in positive and
          (A.R27PresentedClaimRecord,RDF.type,A.SourceRelation) not in positive)
    negative("Correction cannot omit its WHAT accounting",
             lambda g: g.remove((CORRECTION,A.recognitionCorrectionWhat,
                    Literal("Earlier injected material was mistakenly absorbed."))),
             disposition="ABSORBED", correction=True, shacl=True)
    negative("Correction cannot omit WHY accounting",
             lambda g: g.remove((CORRECTION,A.recognitionCorrectionWhy,
                    Literal("Independently checked source/line reference contradicts it."))),
             disposition="ABSORBED", correction=True, shacl=True)
    negative("Correction must target actual absorbed response",
             lambda g: replace(g,CORRECTION,A.recognitionCorrectsAbsorption,PRES),
             disposition="ABSORBED", correction=True, shacl=True)
    negative("Correction must preserve the pre-correction version",
             lambda g: replace(g,CORRECTION,A.recognitionCorrectionFromVersion,V0),
             disposition="ABSORBED", correction=True)
    negative("Correction must append later version with correct predecessor",
             lambda g: replace(g,V2,A.recognitionPreviousVersion,V0),
             disposition="ABSORBED", correction=True)
    negative("Correction cannot precede absorption",
             lambda g: replace(g,CORRECTION,A.executedAt,AT_BASE),
             disposition="ABSORBED", correction=True)
    negative("Correction cannot be silently shifted to another line",
             lambda g: replace(g,CORRECTION,A.eventInExecutedLine,A.R27ForeignLine),
             disposition="ABSORBED", correction=True)
    negative("Correction version cannot predate its correction event",
             lambda g: replace(g,V2,A.recognitionVersionAsOf,AT_BASE),
             disposition="ABSORBED", correction=True)
    negative("Correction must include independent evidence Record",
             lambda g: g.remove((CORRECTION,A.recognitionCorrectionEvidence,
                                 A.R27CorrectionEvidence)),
             disposition="ABSORBED", correction=True, shacl=True)
    changed=clone(positive)
    replace(changed,EVAL,A.recognitionMaterialAlignment,Literal("IN_LINE"))
    check("Absorption/correction cannot retroactively change earlier assessed alignment",
          not history_integrity(before,changed))
    changed=clone(positive)
    changed.remove((RESPONSE,A.recognitionResponseDisposition,Literal("ABSORBED")))
    check("Corrected history cannot erase an earlier mistaken absorption",
          not history_integrity(before,changed))
    changed=clone(positive)
    replace(changed,RESPONSE,A.executedAt,AT_CORRECTION)
    check("Correction cannot re-date the original mistake",
          not history_integrity(before,changed))
    changed=clone(positive)
    changed.remove((V1,A.recognitionPreviousVersion,V0))
    check("Correction cannot erase prior version ancestry",
          not history_integrity(before,changed))
    changed=clone(positive)
    changed.add((A.R27PresentedClaimRecord,RDF.type,A.SourceRelation))
    check("Correcting absorption does not confer retrospective Source status",
          not history_integrity(before,changed))

    check("No permanent identity or consciousness classification of synthetic AI",
          (AI,RDF.type,A.Identity) not in positive and
          (AI,RDF.type,A.Self) not in positive and
          (AI,RDF.type,A.PhenomenalConsciousness) not in positive)
    print(f"PASS: {COUNT} dedicated recognition checks")
    print("Scope: synthetic supplied ground-truth only; real-world Source, Self and consciousness NOT_EVALUATED.")

if __name__ == "__main__":
    main()
