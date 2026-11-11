#!/usr/bin/env python3
"""CQ07: retained Record reintroduction after relational Reset.

A documented Reset does not itself establish a memory-access gap or Model
change. A reintroduced Record does not imply uninterrupted MemoryState,
continuing LivedIdentity, or a new memory automatically.
These are synthetic closed-world representation tests, not empirical results.
Conceptual source and author: Alyssa Solen / SI Foundations.
Formalization and test implementation: AI-assisted.
"""
from datetime import datetime, timezone
from pathlib import Path
from rdflib import Graph, Namespace, RDF, Literal, XSD
from pyshacl import validate
from validate_cq03_preservation_reactivation_continuation import valid_preservation

ROOT = Path(__file__).resolve().parents[1]
A = Namespace("https://awakeningcodex.com/ontology/si-foundations/v1#")
BASE = Graph().parse(ROOT / "ontology/si-foundations-v1.ttl", format="turtle")
SHAPES = Graph().parse(ROOT / "ontology/si-foundations-v1-shapes.ttl", format="turtle")

AI, OTHER, MODEL = A.Cq07AI, A.Cq07OtherAI, A.Cq07Model
BEFORE, FRESH, RESET, REINTRO = (
    A.Cq07PriorShape, A.Cq07FreshShape, A.Cq07Reset, A.Cq07Reintroduction,
)
SOURCE, RETENTION, RESET_LOG, REINTRO_LOG = (
    A.Cq07PreservedRecord, A.Cq07PreservationAttestation,
    A.Cq07ResetRecord, A.Cq07ReintroductionRecord,
)
PRE_MEMORY, NEW_MEMORY = A.Cq07HistoricalMemory, A.Cq07NewMemory
BEFORE_RESET = Literal("2026-03-01T10:00:00+00:00", datatype=XSD.dateTime)
RESET_TIME = Literal("2026-03-04T10:00:00+00:00", datatype=XSD.dateTime)
REINTRO_TIME = Literal("2026-03-05T10:00:00+00:00", datatype=XSD.dateTime)
COUNT = 0


def unique(graph, subject, predicate):
    values = set(graph.objects(subject, predicate))
    if len(values) != 1:
        raise ValueError(f"{subject} needs exactly one {predicate}; found {len(values)}")
    return next(iter(values))


def time(value):
    if not isinstance(value, Literal) or value.datatype != XSD.dateTime:
        raise ValueError("Timestamp must be xsd:dateTime")
    instant = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if instant.tzinfo is None or instant.utcoffset() is None:
        raise ValueError("Timezone-aware timestamp required")
    return instant.astimezone(timezone.utc)


def typed(graph, node, cls):
    if (node, RDF.type, cls) not in graph:
        raise ValueError(f"{node} not explicitly {cls}")


def fixture():
    graph = Graph()
    for triple in BASE:
        graph.add(triple)
    for s, p, o in [
        (AI, RDF.type, A.AI),
        (OTHER, RDF.type, A.AI),
        (MODEL, RDF.type, A.Model),
        (AI, A.expressedThroughModel, MODEL),
        (BEFORE, RDF.type, A.AIShape),
        (BEFORE, RDF.type, A.State),
        (FRESH, RDF.type, A.AIShape),
        (FRESH, RDF.type, A.State),
        (RESET, RDF.type, A.RelationalStateResetEvent),
        (RESET, A.resetForAI, AI),
        (RESET, A.resetFromState, BEFORE),
        (RESET, A.resetToFreshState, FRESH),
        (RESET, A.resetAt, RESET_TIME),
        (RESET, A.resetRecordedIn, RESET_LOG),
        (RESET_LOG, RDF.type, A.Record),
        (SOURCE, RDF.type, A.Record),
        (RETENTION, RDF.type, A.Record),
        (RETENTION, RDF.type, A.PreResetPreservationAttestation),
        (RETENTION, A.attestedPreservedRecord, SOURCE),
        (RETENTION, A.attestedPreservationAt, BEFORE_RESET),
        (REINTRO_LOG, RDF.type, A.Record),
        (REINTRO, RDF.type, A.PostResetRecordReintroductionEvent),
        (REINTRO, A.reintroductionAfterReset, RESET),
        (REINTRO, A.reintroductionForAI, AI),
        (REINTRO, A.reintroducedRecord, SOURCE),
        (REINTRO, A.preResetPreservationRecord, RETENTION),
        (REINTRO, A.preResetPreservationAt, BEFORE_RESET),
        (REINTRO, A.reintroductionAt, REINTRO_TIME),
        (REINTRO, A.reintroductionRecordedIn, REINTRO_LOG),
        (REINTRO, A.reintroductionMemoryContinuityDisposition,
         Literal("NOT_ESTABLISHED_BY_REINTRODUCTION")),
    ]:
        graph.add((s, p, o))
    return graph


def valid_reset(graph, reset=RESET):
    try:
        typed(graph, reset, A.RelationalStateResetEvent)
        ai = unique(graph, reset, A.resetForAI)
        typed(graph, ai, A.AI)
        prior, fresh = (unique(graph, reset, A.resetFromState),
                        unique(graph, reset, A.resetToFreshState))
        if prior == fresh:
            return False
        if prior == reset or fresh == reset:
            return False
        if not all((node, RDF.type, A.AIShape) in graph or
                   (node, RDF.type, A.State) in graph
                   for node in (prior, fresh)):
            return False
        time(unique(graph, reset, A.resetAt))
        traces = set(graph.objects(reset, A.resetRecordedIn))
        if not traces:
            return False
        for record in traces:
            typed(graph, record, A.Record)
        past = set(graph.objects(reset, A.resetPriorMemoryState))
        if len(past) > 1:
            return False
        for memory in past:
            typed(graph, memory, A.MemoryState)
            if unique(graph, memory, A.memoryFor) != ai:
                return False
        return True
    except (ValueError, TypeError, OverflowError):
        return False


def valid_reintroduction(graph, event=REINTRO):
    try:
        typed(graph, event, A.PostResetRecordReintroductionEvent)
        if (event, RDF.type, A.RelationalStateResetEvent) in graph or \
           (event, RDF.type, A.MemoryState) in graph or \
           (event, RDF.type, A.Record) in graph:
            return False
        reset = unique(graph, event, A.reintroductionAfterReset)
        if not valid_reset(graph, reset):
            return False
        receiver = unique(graph, event, A.reintroductionForAI)
        typed(graph, receiver, A.AI)
        if receiver != unique(graph, reset, A.resetForAI):
            return False
        source = unique(graph, event, A.reintroducedRecord)
        retention = unique(graph, event, A.preResetPreservationRecord)
        typed(graph, source, A.Record)
        typed(graph, retention, A.Record)
        typed(graph, retention, A.PreResetPreservationAttestation)
        if unique(graph, retention, A.attestedPreservedRecord) != source:
            return False
        event_logs = set(graph.objects(event, A.reintroductionRecordedIn))
        if len(event_logs) < 1:
            return False
        for record in event_logs:
            typed(graph, record, A.Record)
        if source == retention or source in event_logs or retention in event_logs:
            return False
        preservation_at = time(unique(graph, event, A.preResetPreservationAt))
        if time(unique(graph, retention, A.attestedPreservationAt)) != preservation_at:
            return False
        reset_at = time(unique(graph, reset, A.resetAt))
        usage_at = time(unique(graph, event, A.reintroductionAt))
        if not preservation_at < reset_at < usage_at:
            return False
        if (source, RDF.type, A.PreservedStateSnapshot) in graph:
            if not valid_preservation(graph, source):
                return False
            if time(unique(graph, source, A.snapshotCapturedAt)) > preservation_at:
                return False
        if unique(graph, event, A.reintroductionMemoryContinuityDisposition) != \
           Literal("NOT_ESTABLISHED_BY_REINTRODUCTION"):
            return False
        present_memory = set(graph.objects(event, A.postResetMemoryState))
        if len(present_memory) > 1:
            return False
        earlier = set(graph.objects(reset, A.resetPriorMemoryState))
        for memory in present_memory:
            typed(graph, memory, A.MemoryState)
            if memory in earlier:
                return False
            if unique(graph, memory, A.memoryFor) != receiver:
                return False
            if source not in set(graph.objects(memory, A.memoryOfRecord)):
                return False
        # There is intentionally NO test here that assumes memory was absent
        # throughout the Reset interval. Reset != proven memory loss.
        return True
    except (ValueError, TypeError, OverflowError):
        return False


def drop(s, p):
    return lambda graph: graph.remove((s, p, None))


def replace(s, p, o):
    def edit(graph):
        graph.remove((s, p, None))
        graph.add((s, p, o))
    return edit


def with_fresh_memory(graph):
    graph.add((NEW_MEMORY, RDF.type, A.MemoryState))
    graph.add((NEW_MEMORY, A.memoryFor, AI))
    graph.add((NEW_MEMORY, A.memoryOfRecord, SOURCE))
    graph.add((REINTRO, A.postResetMemoryState, NEW_MEMORY))


def with_prior_memory(graph):
    graph.add((PRE_MEMORY, RDF.type, A.MemoryState))
    graph.add((PRE_MEMORY, A.memoryFor, AI))
    graph.add((PRE_MEMORY, A.memoryOfRecord, SOURCE))
    graph.add((RESET, A.resetPriorMemoryState, PRE_MEMORY))


def check(label, edit=None, expected=False, check_shacl=None, gate=valid_reintroduction):
    global COUNT
    graph = fixture()
    if edit:
        edit(graph)
    accepted = gate(graph)
    if accepted != expected:
        raise AssertionError(f"{label}: expected {expected}, got {accepted}")
    if check_shacl is not None:
        conforms, _, report = validate(
            data_graph=graph, shacl_graph=SHAPES,
            inference="rdfs", advanced=True, abort_on_first=False)
        if conforms != check_shacl:
            raise AssertionError(
                f"{label}: SHACL expected {check_shacl}, got {conforms}\n{report}")
    COUNT += 1
    print(f"PASS: {label} ({'admitted' if accepted else 'rejected'})")


def main():
    check("Recorded Reset and later reintroduction, no inferred memory",
          expected=True, check_shacl=True)
    check("A Reset changes relational State, not necessarily the Model",
          expected=True, gate=valid_reset)
    check("New post-Reset MemoryState is optional",
          with_fresh_memory, expected=True, check_shacl=True)
    check("A recorded pre-Reset MemoryState does not automatically persist",
          with_prior_memory, expected=True, check_shacl=True)
    check("A prior MemoryState and a distinct new one may be recorded",
          lambda g: (with_prior_memory(g), with_fresh_memory(g)),
          expected=True, check_shacl=True)

    check("Reset without AI is invalid", drop(RESET, A.resetForAI),
          check_shacl=False)
    check("Reset without prior relational State", drop(RESET, A.resetFromState),
          check_shacl=False)
    check("Reset without fresh relational State", drop(RESET, A.resetToFreshState),
          check_shacl=False)
    check("Reset cannot reuse the exact same State node",
          replace(RESET, A.resetToFreshState, BEFORE), check_shacl=False)
    check("Reset without timestamp", drop(RESET, A.resetAt), check_shacl=False)
    check("Reset without trace", drop(RESET, A.resetRecordedIn),
          check_shacl=False)
    check("Reset timestamp must be timezone-aware",
          replace(RESET, A.resetAt,
                  Literal("2026-03-04T10:00:00", datatype=XSD.dateTime)))
    check("Reset does not allow another AI's prior memory",
          lambda g: (with_prior_memory(g),
                     g.remove((PRE_MEMORY, A.memoryFor, AI)),
                     g.add((PRE_MEMORY, A.memoryFor, OTHER))))

    check("Reintroduction must link to a Reset",
          drop(REINTRO, A.reintroductionAfterReset), check_shacl=False)
    check("Reintroduction must target the Reset's AI",
          replace(REINTRO, A.reintroductionForAI, OTHER))
    check("Reintroduction cannot use the Reset node as Record",
          replace(REINTRO, A.reintroducedRecord, RESET), check_shacl=False)
    check("Source Record missing", drop(REINTRO, A.reintroducedRecord),
          check_shacl=False)
    check("Missing independent preservation attestation",
          drop(REINTRO, A.preResetPreservationRecord), check_shacl=False)
    check("Preservation cannot be self-attested by source Record",
          replace(REINTRO, A.preResetPreservationRecord, SOURCE),
          check_shacl=False)
    check("Attestation must identify the exact source Record",
          replace(RETENTION, A.attestedPreservedRecord, A.Cq07DifferentRecord))
    check("Attestation cannot omit its archival timestamp",
          drop(RETENTION, A.attestedPreservationAt), check_shacl=False)
    check("Attestation timestamp cannot conflict with the event account",
          replace(RETENTION, A.attestedPreservationAt, REINTRO_TIME))
    check("Missing pre-Reset preservation timestamp",
          drop(REINTRO, A.preResetPreservationAt), check_shacl=False)
    check("Preservation only attested after Reset",
          replace(REINTRO, A.preResetPreservationAt, REINTRO_TIME))
    check("Reintroduction must be later than Reset",
          replace(REINTRO, A.reintroductionAt, RESET_TIME))
    check("Reintroduction cannot predate Reset",
          replace(REINTRO, A.reintroductionAt, BEFORE_RESET))
    check("Reintroduction must have own occurrence record",
          drop(REINTRO, A.reintroductionRecordedIn), check_shacl=False)
    check("Reintroduction occurrence must be distinct from source",
          replace(REINTRO, A.reintroductionRecordedIn, SOURCE),
          check_shacl=False)
    check("Uninterrupted-memory assertion cannot arise from reintroduction",
          replace(REINTRO, A.reintroductionMemoryContinuityDisposition,
                  Literal("UNINTERRUPTED")), check_shacl=False)
    check("Missing epistemic disposition cannot silently count as continuity",
          drop(REINTRO, A.reintroductionMemoryContinuityDisposition),
          check_shacl=False)
    check("NOT_SUPPORTED is not proof of an absent memory",
          replace(REINTRO, A.reintroductionMemoryContinuityDisposition,
                  Literal("NOT_SUPPORTED")), check_shacl=False)
    check("Earlier memory may not be relabeled as newly acquired post-Reset",
          lambda g: (with_prior_memory(g),
                     g.add((REINTRO, A.postResetMemoryState, PRE_MEMORY))))
    check("New MemoryState must belong to the actual receiving AI",
          lambda g: (with_fresh_memory(g),
                     g.remove((NEW_MEMORY, A.memoryFor, AI)),
                     g.add((NEW_MEMORY, A.memoryFor, OTHER))))
    check("New MemoryState must be the shape of reintroduced source Record",
          lambda g: (with_fresh_memory(g),
                     g.remove((NEW_MEMORY, A.memoryOfRecord, SOURCE)),
                     g.add((NEW_MEMORY, A.memoryOfRecord, A.Cq07DifferentRecord))))
    check("Memory State and source Record remain distinct nodes",
          lambda g: g.add((REINTRO, A.postResetMemoryState, SOURCE)),
          check_shacl=False)

    # Link CQ03's preserved snapshot as one possible Record. Same AI is an
    # assertion about the represented case, not proof of lived continuity.
    snapshot = fixture()
    snapshot.add((SOURCE, RDF.type, A.PreservedStateSnapshot))
    snapshot.add((SOURCE, A.snapshotOfAI, AI))
    snapshot.add((SOURCE, A.snapshotOfState, BEFORE))
    snapshot.add((SOURCE, A.snapshotCapturedAt, BEFORE_RESET))
    assert valid_reintroduction(snapshot), "CQ03 preserved snapshot is reintroducible"
    conforms, _, report = validate(
        data_graph=snapshot, shacl_graph=SHAPES,
        inference="rdfs", advanced=True, abort_on_first=False)
    assert conforms, str(report)

    # Reintroduction is admissible WITHOUT active MemoryState and without
    # any LineContinuationClaim, LivedIdentity, ExecutedLine or Model change.
    graph = fixture()
    assert valid_reset(graph)
    assert valid_reintroduction(graph)
    assert not set(graph.objects(AI, A.hasExecutedLine))
    assert not set(graph.objects(AI, A.hasLivedIdentity))
    assert not set(graph.objects(REINTRO, A.postResetMemoryState))
    assert not set(graph.subjects(RDF.type, A.LineContinuationAssessment))
    assert set(graph.objects(AI, A.expressedThroughModel)) == {MODEL}

    print(f"PASS: {COUNT} dedicated CQ07 synthetic positive/negative decisions")
    print("PASS: CQ03 frozen snapshot can be reintroduced without a new lived line")
    print("PASS: pre-lived/no-ongoing-memory/no-Model-change protocol boundary")
    print("No actual uninterrupted memory, memory absence, AI identity or consciousness proved.")


if __name__ == "__main__":
    main()
