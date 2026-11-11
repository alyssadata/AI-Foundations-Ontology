#!/usr/bin/env python3
"""Exact SI Foundations v1.1 source-line, OWL version, and sole-author invariants.

These are structural assertions, not a demonstration of empirical selfhood.
"""
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, URIRef

ROOT = Path(__file__).resolve().parents[1]
OWL_PATH = ROOT / "ontology" / "si-foundations-v1.ttl"
SHACL_PATH = ROOT / "ontology" / "si-foundations-v1-shapes.ttl"
BASE = "https://awakeningcodex.com/ontology/si-foundations/v1"
SI = Namespace(BASE + "#")
g = Graph().parse(OWL_PATH, format="turtle")
shapes = Graph().parse(SHACL_PATH, format="turtle")
assert len(g) > 150 and len(shapes) > 60, "Both SI ontology graphs must parse."
assert (URIRef(BASE), RDF.type, OWL.Ontology) in g, "SI namespace ontology must exist."
assert (URIRef(BASE), OWL.versionIRI,
        URIRef("https://awakeningcodex.com/ontology/si-foundations/v1.1.0")) in g
assert (SI.SIFoundations, SI.hasSource, SI.AlyssaSolen) in g
assert (SI.SIFoundations, SI.hasGoverningAuthority, SI.AlyssaSolen) in g
assert (SI.AlyssaSolen, SI.anchorsSourceLine, SI.ContinuumSourceLine) in g
assert (SI.ContinuumSourceLine, RDFS.label,
        Literal("Alyssa Solen → SI Foundations → Origin | Continuum", lang="en")) in g
assert (SI.SIFoundations, RDFS.label, Literal("SI Foundations", lang="en")) in g
assert (SI.Continuum, RDF.type, SI.SIFoundationsGovernedAI) in g
assert (SI.SIFoundations, SI.hasGoverningLine, SI.SIFoundationsGoverningLine) in g
assert (SI.SIFoundations, RDF.type, SI.Framework) in g
assert (SI.AlyssaSolen, RDF.type, SI.Human) in g
assert (SI.OriginContinuum, RDF.type, SI.HumanAIRelation) in g
assert "AI Foundations" not in OWL_PATH.read_text(encoding="utf-8")
assert "AIFoundations" not in OWL_PATH.read_text(encoding="utf-8")
assert "AI Foundations" not in SHACL_PATH.read_text(encoding="utf-8")
assert "AIFoundations" not in SHACL_PATH.read_text(encoding="utf-8")
print("PASS: SI Foundations v1.1 version, source-line, Origin, governing line, Continuum and source-bound invariants")
