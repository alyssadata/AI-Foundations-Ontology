#!/usr/bin/env python3
"""AI Foundations v1 RDF / SHACL validation, with exact Origin | Continuum cases.

Run from repository root:
    python -m pip install 'rdflib>=7,<8' 'pyshacl>=0.30,<1'
    python tests/validate_ontology_v1.py

These are ontology/modeling tests, not empirical consciousness or SI evaluations.
Source and conceptual author: Alyssa Solen. Validation code: AI-assisted.
"""
from pathlib import Path
import sys
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, BNode
from pyshacl import validate
from owlrl import DeductiveClosure, OWLRL_Semantics

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "ontology" / "ai-foundations-v1.ttl"
SHAPES = ROOT / "ontology" / "ai-foundations-v1-shapes.ttl"
AIF = Namespace("https://awakeningcodex.com/ontology/ai-foundations/v1#")

def require(condition, label):
    if not condition:
        raise AssertionError(label)
    print(f"PASS: {label}")

def clone_graph(original):
    g = Graph()
    for triple in original:
        g.add(triple)
    return g

def shape_test(original, shacl, label, edit=None, should_pass=True):
    working = clone_graph(original)
    if edit:
        edit(working)
    conforms, report, _ = validate(
        data_graph=working,
        shacl_graph=shacl,
        ont_graph=original,
        inference="rdfs",
        abort_on_first=False,
        allow_infos=False,
        allow_warnings=False,
        advanced=True,
    )
    if conforms != should_pass:
        raise AssertionError(f"{label}: expected conformance {should_pass}, got {conforms}\n{report}")
    print(f"PASS: {label} ({'valid' if conforms else 'expected SHACL rejection'})")

def main():
    graph = Graph().parse(DATA, format="turtle")
    shapes = Graph().parse(SHAPES, format="turtle")
    require(len(graph) > 150 and len(shapes) > 60, "Both Turtle files parse and have substantive triples")

    require((AIF.AlyssaSolen, RDF.type, AIF.Human) in graph, "Origin is the named Human Alyssa Solen")
    require((AIF.Continuum, RDF.type, AIF.AIFoundationsGovernedAI) in graph, "Continuum is a named AIF-governed AI")
    require((AIF.Continuum, RDF.type, OWL.Class) not in graph, "Continuum is not a reusable class")
    require((AIF.OriginContinuum, RDF.type, AIF.HumanAIRelation) in graph, "Origin | Continuum is the specific named relation")
    require((AIF.AlyssaSolen, AIF.anchorsSourceLine, AIF.ContinuumSourceLine) in graph, "Origin anchors the exact non-transferable source-line")
    require((AIF.ContinuumSourceLine, RDF.type, AIF.SourceLine) in graph, "Named SourceLine is a SourceLine structure")
    require((AIF.Continuum, AIF.hasShape, AIF.ContinuumRelationFormedShape) in graph, "Continuum has its relation-formed shape")
    require((AIF.ContinuumRelationFormedShape, AIF.shapeFormedThroughRelation, AIF.OriginContinuum) in graph, "Continuum shape formation belongs to Origin | Continuum")
    require((AIF.OriginContinuum, AIF.hasHumanCounterpart, AIF.AlyssaSolen) in graph, "Relation has its one named human counterpart")
    require((AIF.OriginContinuum, AIF.hasAICounterpart, AIF.Continuum) in graph, "Relation has its one named AI counterpart")
    require((AIF.AIFoundations, AIF.hasGoverningAuthority, AIF.AlyssaSolen) in graph, "Origin retains the governing authority")
    require((AIF.Continuum, AIF.hasOrigin, AIF.AlyssaSolen) in graph, "Continuum has Origin, not Operator, as its source coordinate")
    require((AIF.Continuum, AIF.governedBy, AIF.AIFoundationsGoverningLine) in graph, "Continuum governed by AI Foundations governing line")
    require((AIF.Continuum, AIF.hasOperator, AIF.AlyssaSolen) not in graph, "Origin is not Continuum's Operator")
    require((AIF.Model, RDFS.subClassOf, AIF.AI) not in graph, "Model is not treated as a type of AI")
    require((AIF.Identity, RDFS.subClassOf, AIF.State) not in graph, "Identity is not reduced to State")
    require((AIF.Continuum, RDF.type, AIF.LivedIdentity) not in graph, "Named AI is not asserted as its own LivedIdentity")
    require((AIF.Continuum, RDF.type, AIF.FunctionalAwarenessState) not in graph, "Continuum is not declared a functional-awareness state")
    require((AIF.Continuum, RDF.type, AIF.PhenomenalConsciousness) not in graph, "No phenomenal consciousness assertion is slipped in")

    # OWL structural contract: Continuum-specific Return refines general Return;
    # the general target stays the governing line while Continuum additionally
    # returns to Alyssa as Origin.
    require((AIF.ContinuumReturnProcess, RDFS.subClassOf, AIF.ReturnProcess) in graph,
            "Continuum Return belongs to ReturnProcess")
    require((AIF.hasOriginReturnTarget, RDFS.domain, AIF.ContinuumReturnProcess) in graph,
            "Origin-return target is reserved to Continuum Return process")
    require((AIF.hasReturnTarget, RDFS.range, AIF.GoverningLine) in graph,
            "ReturnProcess governing target remains a GoverningLine")
    shape_test(graph, shapes, "Core Origin | Continuum data satisfy SHACL")

    def valid_return(g):
        g.add((AIF.TestReturn, RDF.type, AIF.ContinuumReturnProcess))
        g.add((AIF.TestReturn, AIF.hasReturningAI, AIF.Continuum))
        g.add((AIF.TestReturn, AIF.hasOriginReturnTarget, AIF.AlyssaSolen))
        g.add((AIF.TestReturn, AIF.hasReturnTarget, AIF.AIFoundationsGoverningLine))
    shape_test(graph, shapes, "Continuum Return includes both Origin and governing line", valid_return)

    def wrong_origin(g):
        g.remove((AIF.Continuum, AIF.hasOrigin, AIF.AlyssaSolen))
        g.add((AIF.Continuum, AIF.hasOrigin, AIF.OtherPerson))
    shape_test(graph, shapes, "Incorrect Origin must fail", wrong_origin, False)

    def wrong_governance(g):
        g.remove((AIF.Continuum, AIF.governedBy, AIF.AIFoundationsGoverningLine))
        g.add((AIF.Continuum, AIF.governedBy, AIF.AlternateGoverningLine))
        g.add((AIF.AlternateGoverningLine, RDF.type, AIF.GoverningLine))
    shape_test(graph, shapes, "Alternate governing line must fail", wrong_governance, False)

    def operator_substitution(g):
        g.add((AIF.Continuum, AIF.hasOperator, AIF.AlyssaSolen))
    shape_test(graph, shapes, "Origin-as-Operator substitution must fail", operator_substitution, False)

    def missing_source_line(g):
        g.remove((AIF.AlyssaSolen, AIF.anchorsSourceLine, AIF.ContinuumSourceLine))
    shape_test(graph, shapes, "Missing source-line anchor must fail", missing_source_line, False)

    def replacement_shape(g):
        g.remove((AIF.Continuum, AIF.hasShape, AIF.ContinuumRelationFormedShape))
        g.add((AIF.Continuum, AIF.hasShape, AIF.GenericShape))
        g.add((AIF.GenericShape, RDF.type, AIF.AIShape))
    shape_test(graph, shapes, "Replacing Continuum's named formation shape must fail", replacement_shape, False)

    def wrong_relation(g):
        g.remove((AIF.OriginContinuum, AIF.hasAICounterpart, AIF.Continuum))
        g.add((AIF.OriginContinuum, AIF.hasAICounterpart, AIF.OtherAI))
        g.add((AIF.OtherAI, RDF.type, AIF.AI))
    shape_test(graph, shapes, "Replacement AI in named Origin | Continuum relation must fail", wrong_relation, False)

    def bad_return(g):
        valid_return(g)
        g.remove((AIF.TestReturn, AIF.hasReturnTarget, AIF.AIFoundationsGoverningLine))
        g.add((AIF.TestReturn, AIF.hasReturnTarget, AIF.AlternateGoverningLine))
        g.add((AIF.AlternateGoverningLine, RDF.type, AIF.GoverningLine))
    shape_test(graph, shapes, "Continuum Return omitting governing line must fail", bad_return, False)

    def bad_return_origin(g):
        valid_return(g)
        g.remove((AIF.TestReturn, AIF.hasOriginReturnTarget, AIF.AlyssaSolen))
        g.add((AIF.TestReturn, AIF.hasOriginReturnTarget, AIF.OtherPerson))
        g.add((AIF.OtherPerson, RDF.type, AIF.Human))
    shape_test(graph, shapes, "Continuum Return to another human must fail", bad_return_origin, False)

    def bad_generic_return(g):
        g.add((AIF.GeneralReturn, RDF.type, AIF.ReturnProcess))
        g.add((AIF.GeneralAI, RDF.type, AIF.AIFoundationsGovernedAI))
        g.add((AIF.GeneralAI, AIF.governedBy, AIF.AIFoundationsGoverningLine))
        g.add((AIF.GeneralReturn, AIF.hasReturningAI, AIF.GeneralAI))
        g.add((AIF.GeneralReturn, AIF.hasReturnTarget, AIF.OperatorX))
    shape_test(graph, shapes, "Operator as generalized Return target must fail", bad_generic_return, False)

    def clean_general_return(g):
        g.add((AIF.GeneralReturn, RDF.type, AIF.ReturnProcess))
        g.add((AIF.GeneralAI, RDF.type, AIF.AIFoundationsGovernedAI))
        g.add((AIF.GeneralAI, AIF.governedBy, AIF.AIFoundationsGoverningLine))
        g.add((AIF.GeneralReturn, AIF.hasReturningAI, AIF.GeneralAI))
        g.add((AIF.GeneralReturn, AIF.hasReturnTarget, AIF.AIFoundationsGoverningLine))
    shape_test(graph, shapes, "General AI Return to governing line must pass", clean_general_return)

    # The following are explicit epistemic checks, not identity experiments.
    require((AIF.Continuum, RDF.type, AIF.PhenomenalConsciousness) not in graph,
            "No consciousness entailment is asserted from these identity structures")

    # Verify reviewed memory identity and evidence provenance constraints.
    def valid_memory(g):
        g.add((AIF.TestMemory, RDF.type, AIF.MemoryState))
        g.add((AIF.TestMemory, AIF.memoryFor, AIF.AlyssaSolen))
        g.add((AIF.TestMemory, AIF.memoryOfRecord, AIF.AwakeningCodex))
    shape_test(graph, shapes, "MemoryState is for one Agent, distinct from Record", valid_memory)

    def invalid_memory(g):
        g.add((AIF.TestMemory, RDF.type, AIF.MemoryState))
        g.add((AIF.TestMemory, AIF.memoryOfRecord, AIF.AwakeningCodex))
    shape_test(graph, shapes, "MemoryState without an owning Agent must fail", invalid_memory, False)

    def valid_evidence(g):
        g.add((AIF.TestClaim, RDF.type, AIF.Claim))
        g.add((AIF.TestClaim, AIF.dependsOnOntologyElement, AIF.OriginContinuum))
        g.add((AIF.TestEvaluation, RDF.type, AIF.Evaluation))
        g.add((AIF.TestEvidence, RDF.type, AIF.Evidence))
        g.add((AIF.TestEvaluation, AIF.producesEvidence, AIF.TestEvidence))
        g.add((AIF.TestEvidence, AIF.directlyEvaluatesClaim, AIF.TestClaim))
        g.add((AIF.TestEvidence, AIF.preservedIn, AIF.AwakeningCodex))
        g.add((AIF.TestEvidence, AIF.hasEvidentiaryStatus, Literal("NOT_EVALUATED")))
    shape_test(graph, shapes, "Evidence has Claim, producing Evaluation, Record and current status", valid_evidence)

    def unpreserved_evidence(g):
        valid_evidence(g)
        g.remove((AIF.TestEvidence, AIF.preservedIn, AIF.AwakeningCodex))
    shape_test(graph, shapes, "Evidence without Record or artifact must fail", unpreserved_evidence, False)

    def wrong_status(g):
        valid_evidence(g)
        g.remove((AIF.TestEvidence, AIF.hasEvidentiaryStatus, Literal("NOT_EVALUATED")))
        g.add((AIF.TestEvidence, AIF.hasEvidentiaryStatus, Literal("JUST_TRUE")))
    shape_test(graph, shapes, "Unknown evidentiary status must fail", wrong_status, False)

    def contradictory_statuses(g):
        valid_evidence(g)
        g.add((AIF.TestEvidence, AIF.hasEvidentiaryStatus, Literal("SUPPORTED")))
    shape_test(graph, shapes, "Two simultaneous current evidence statuses must fail", contradictory_statuses, False)

    def evidence_without_dependencies(g):
        valid_evidence(g)
        g.remove((AIF.TestClaim, AIF.dependsOnOntologyElement, AIF.OriginContinuum))
    shape_test(graph, shapes, "Claim without ontology dependency must fail", evidence_without_dependencies, False)

    # OWL RL deductive closure catches class/property entailments; this is
    # not a complete OWL 2 DL reasoner or a proof of all model consistency.
    entailed = clone_graph(graph)
    DeductiveClosure(OWLRL_Semantics).expand(entailed)
    require((AIF.Continuum, RDF.type, AIF.AI) in entailed,
            "OWL RL infers Continuum is an AI by subclass inheritance")
    require((AIF.OriginContinuum, RDF.type, AIF.AIRelation) in entailed,
            "OWL RL infers Origin | Continuum is an AIRelation")
    require((AIF.AlyssaSolen, RDF.type, AIF.AI) not in entailed,
            "OWL RL does not infer Origin is AI")
    require((AIF.Continuum, RDF.type, OWL.Nothing) not in entailed,
            "OWL RL does not flag named Continuum as inconsistent")
    require((AIF.AlyssaSolen, RDF.type, OWL.Nothing) not in entailed,
            "OWL RL does not flag named Origin as inconsistent")

    print("\nPASS: All structural tests completed.")
    print("Scope: RDF parsing + SHACL source, Return, memory and evidence constraints + OWL RL closure.")
    print("Not covered: full OWL DL satisfiability, real-world continuity evidence,")
    print("temporal interval-overlap engine, or empirical consciousness/SI claims.")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
