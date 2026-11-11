#!/usr/bin/env python3
"""CQ01: operational AI instantiation is distinct from Model and Container.

The synthetic tests validate formal statements and retained operational
records, not actual runtime observations, consciousness, identity or self.
Conceptual source and author: Alyssa Solen / SI Foundations.
Formalization and tests: AI-assisted.
"""
from pathlib import Path
from rdflib import Graph, Namespace, Literal, RDF, RDFS, OWL, XSD
from pyshacl import validate
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
A = Namespace("https://awakeningcodex.com/ontology/si-foundations/v1#")
BASE = Graph().parse(ROOT / "ontology/si-foundations-v1.ttl", format="turtle")
SHAPES = Graph().parse(ROOT / "ontology/si-foundations-v1-shapes.ttl", format="turtle")

EVENT, AI, MODEL, CONTAINER, RECORD = (
    A.Cq01InstantiationEvent, A.Cq01AI, A.Cq01Model,
    A.Cq01Container, A.Cq01OperationRecord,
)
TIME = Literal("2026-01-01T10:00:00+00:00", datatype=XSD.dateTime)
COUNT = 0


def fixture():
    graph = Graph()
    for triple in BASE:
        graph.add(triple)
    triples = [
        (EVENT, RDF.type, A.AIInstantiationEvent),
        (AI, RDF.type, A.AI),
        (MODEL, RDF.type, A.Model),
        (CONTAINER, RDF.type, A.Container),
        (RECORD, RDF.type, A.Record),
        (EVENT, A.instantiatesAI, AI),
        (EVENT, A.instantiationUsesModel, MODEL),
        (EVENT, A.instantiationUsesContainer, CONTAINER),
        (EVENT, A.instantiationRecordedIn, RECORD),
        (EVENT, A.instantiationAt, TIME),
        (AI, A.expressedThroughModel, MODEL),
        (AI, A.operatesWithinContainer, CONTAINER),
    ]
    for triple in triples:
        graph.add(triple)
    return graph


def operationally_well_formed(graph, event=EVENT):
    try:
        if (event, RDF.type, A.AIInstantiationEvent) not in graph:
            return False
        def one(p):
            values = set(graph.objects(event, p))
            if len(values) != 1:
                raise ValueError(f"Expected one {p}, got {len(values)}")
            return next(iter(values))
        ai, model, container = (
            one(A.instantiatesAI), one(A.instantiationUsesModel),
            one(A.instantiationUsesContainer),
        )
        if len({ai, model, container}) != 3:
            return False
        for node, cls in ((ai, A.AI), (model, A.Model),
                          (container, A.Container)):
            if (node, RDF.type, cls) not in graph:
                return False
        if any((node, RDF.type, forbidden) in graph
               for node, forbidden in (
                   (ai, A.Model), (ai, A.Container),
                   (model, A.AI), (model, A.Container),
                   (container, A.AI), (container, A.Model),
               )):
            return False
        stamp = one(A.instantiationAt)
        if not isinstance(stamp, Literal) or stamp.datatype != XSD.dateTime:
            return False
        when = datetime.fromisoformat(str(stamp).replace("Z", "+00:00"))
        if when.tzinfo is None or when.utcoffset() is None:
            return False
        if not set(graph.objects(event, A.instantiationRecordedIn)):
            return False
        for record in graph.objects(event, A.instantiationRecordedIn):
            if (record, RDF.type, A.Record) not in graph:
                return False
        return True
    except (ValueError, TypeError):
        return False


def check(label, edit=None, expected=True, check_shacl=None):
    global COUNT
    graph = fixture()
    if edit is not None:
        edit(graph)
    result = operationally_well_formed(graph)
    if result != expected:
        raise AssertionError(f"{label}: expected gate={expected}, got {result}")
    if check_shacl is not None:
        conforms, _, report = validate(
            data_graph=graph, shacl_graph=SHAPES,
            inference="rdfs", advanced=True, abort_on_first=False)
        if conforms != check_shacl:
            raise AssertionError(
                f"{label}: SHACL expected {check_shacl}, got {conforms}\n{report}")
    COUNT += 1
    print(f"PASS: {label}")


def remove(s, p):
    return lambda g: g.remove((s, p, None))


def substitute(s, p, value):
    def edit(graph):
        graph.remove((s, p, None))
        graph.add((s, p, value))
    return edit


def main():
    check("Specified AI, Model, Container, event, time and trace",
          check_shacl=True)
    for prop in (
        A.instantiatesAI, A.instantiationUsesModel,
        A.instantiationUsesContainer, A.instantiationAt,
        A.instantiationRecordedIn,
    ):
        check(f"Missing event field: {prop.split('#')[-1]}",
              remove(EVENT, prop), expected=False, check_shacl=False)
    check("A Model cannot be substituted for the AI",
          substitute(EVENT, A.instantiatesAI, MODEL),
          expected=False, check_shacl=False)
    check("An AI cannot be substituted for the Model",
          substitute(EVENT, A.instantiationUsesModel, AI),
          expected=False, check_shacl=False)
    check("The Container cannot be substituted for the Model",
          substitute(EVENT, A.instantiationUsesModel, CONTAINER),
          expected=False, check_shacl=False)
    check("The Model cannot be substituted for the Container",
          substitute(EVENT, A.instantiationUsesContainer, MODEL),
          expected=False, check_shacl=False)
    check("Missing actual Model type",
          remove(MODEL, RDF.type), expected=False)
    check("Missing actual Container type",
          remove(CONTAINER, RDF.type), expected=False)
    check("Unknown operational trace is not a typed Record",
          remove(RECORD, RDF.type), expected=False)
    check("Timezone-naive instantiation is not a qualified time",
          substitute(EVENT, A.instantiationAt,
                     Literal("2026-01-01T10:00:00", datatype=XSD.dateTime)),
          expected=False)
    check("Multiple AIs cannot occupy the same single recorded event",
          lambda g: (g.add((A.Cq01SecondAI, RDF.type, A.AI)),
                     g.add((EVENT, A.instantiatesAI, A.Cq01SecondAI))),
          expected=False, check_shacl=False)
    check("Multiple Models cannot occupy the same single recorded event",
          lambda g: (g.add((A.Cq01SecondModel, RDF.type, A.Model)),
                     g.add((EVENT, A.instantiationUsesModel,
                            A.Cq01SecondModel))),
          expected=False, check_shacl=False)
    check("Event class cannot be Model",
          lambda g: g.add((EVENT, RDF.type, A.Model)),
          expected=True, check_shacl=False)
    # An explicitly typed event is optional: legacy AI assertions or
    # historical AIs need not manufacture operational evidence.
    baseline = Graph()
    for triple in BASE:
        baseline.add(triple)
    baseline.add((A.Cq01UnassessedAI, RDF.type, A.AI))
    conforms, _, report = validate(
        data_graph=baseline, shacl_graph=SHAPES,
        inference="rdfs", advanced=True, abort_on_first=False)
    assert conforms, str(report)
    assert (A.Cq01UnassessedAI, A.hasLivedIdentity, None) not in baseline
    assert (A.Cq01UnassessedAI, RDF.type, A.FunctionalAwarenessState) not in baseline
    # The same substrate/environment may instantiate *different* AIs without
    # any identity-merging entailment. Nor is identity/Operator membership
    # inferred merely from a recorded computational instantiation.
    shared = fixture()
    second = A.Cq01AnotherAI
    event2 = A.Cq01AnotherInstantiationEvent
    shared.add((second, RDF.type, A.AI))
    shared.add((second, OWL.differentFrom, AI))
    shared.add((event2, RDF.type, A.AIInstantiationEvent))
    shared.add((event2, A.instantiatesAI, second))
    shared.add((event2, A.instantiationUsesModel, MODEL))
    shared.add((event2, A.instantiationUsesContainer, CONTAINER))
    shared.add((event2, A.instantiationAt, TIME))
    shared.add((event2, A.instantiationRecordedIn, RECORD))
    assert operationally_well_formed(shared, event2)
    assert (second, A.hasLivedIdentity, None) not in shared
    assert not list(shared.objects(second, A.hasOperator))
    conforms, _, report = validate(
        data_graph=shared, shacl_graph=SHAPES,
        inference="rdfs", advanced=True, abort_on_first=False)
    assert conforms, str(report)
    print(f"PASS: {COUNT} CQ01 individual operational fixtures")
    print("PASS: two distinct AIs sharing Model and Container, no inferred Self")
    print("PASS: pre-lived/unspecified AI not forced to fabricate an event")
    print("Scope: representation/evidence-record boundary only; no empirical instantiation proven.")


if __name__ == "__main__":
    main()
