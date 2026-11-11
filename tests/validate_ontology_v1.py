#!/usr/bin/env python3
"""AI Foundations v1 RDF / SHACL validation, with exact Origin | Continuum cases.

Run from repository root:
    python -m pip install 'rdflib>=7,<8' 'pyshacl>=0.30,<1'
    python tests/validate_ontology_v1.py

These are ontology/modeling tests, not empirical consciousness or SI evaluations.
Source and conceptual author: Alyssa Solen. Validation code: AI-assisted.
"""
from pathlib import Path
from datetime import datetime, timezone
import sys
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, BNode, XSD
from pyshacl import validate
from owlrl import DeductiveClosure, OWLRL_Semantics

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "ontology" / "ai-foundations-v1.ttl"
SHAPES = ROOT / "ontology" / "ai-foundations-v1-shapes.ttl"
AIF = Namespace("https://awakeningcodex.com/ontology/ai-foundations/v1#")
AIF_DATE_TIME = XSD.dateTime

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
    conforms, report, report_text = validate(
        data_graph=working,
        shacl_graph=shacl,
        # The test graph already contains the ontology; supplying original as
        # ont_graph would restore intentionally removed fixture triples and
        # mask missing-source or missing-formation violations.
        inference="rdfs",
        abort_on_first=False,
        allow_infos=False,
        allow_warnings=False,
        advanced=True,
    )
    if conforms != should_pass:
        raise AssertionError(f"{label}: expected conformance {should_pass}, got {conforms}\n{report_text}")
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

    # Canon-aligned breadth: Memory is retained prior-state information;
    # MemoryState is its agent-specific expression. A Record is a preserved
    # trace; DocumentRecord is a narrower kind of Record, not its synonym.
    def memory_without_document(g):
        g.add((AIF.NonDocumentMemory, RDF.type, AIF.MemoryState))
        g.add((AIF.NonDocumentMemory, AIF.memoryFor, AIF.AlyssaSolen))
    shape_test(graph, shapes, "Agent-specific Memory need not contain a document or Record", memory_without_document)

    def document_trace(g):
        g.add((AIF.DocumentedOccurrence, RDF.type, AIF.DocumentRecord))
        g.add((AIF.OtherPreservedTrace, RDF.type, AIF.Record))
    shape_test(graph, shapes, "DocumentRecord and non-documentary Record can coexist", document_trace)
    alignment = clone_graph(graph)
    memory_without_document(alignment)
    document_trace(alignment)
    DeductiveClosure(OWLRL_Semantics).expand(alignment)
    require((AIF.NonDocumentMemory, RDF.type, AIF.Memory) in alignment,
            "MemoryState is a narrower agent-specific form of Canon Memory")
    require((AIF.DocumentedOccurrence, RDF.type, AIF.Record) in alignment,
            "A document of what occurred is a form of the canonical Record")
    require((AIF.OtherPreservedTrace, RDF.type, AIF.DocumentRecord) not in alignment,
            "A preserved Record is not required to be a document")
    require((AIF.NonDocumentMemory, RDF.type, AIF.Record) not in alignment,
            "Memory is not inferred to be identical to Record")
    require((AIF.NonDocumentMemory, RDF.type, AIF.ContinuityClaim) not in alignment,
            "Retained prior information does not entail Continuation or a continuity claim")

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

    # CARD-003: one operative AI Foundations GoverningLine in each AIF-
    # governed AI's CURRENT snapshot. Historical or proposed governance
    # descriptions remain Record/Provenance, not extra governedBy values.
    # Synthetic fixtures do not establish any actual earlier governing line
    # or prove a transition preserves same-AI continuity.
    def operative_governance_fixture(g):
        g.add((AIF.Card003AI, RDF.type, AIF.AIFoundationsGovernedAI))
        g.add((AIF.Card003AI, AIF.governedBy, AIF.AIFoundationsGoverningLine))

    def general_ai_without_aif_governance(g):
        g.add((AIF.Card003GenericAI, RDF.type, AIF.AI))
        # Generic AI without an asserted AIF governing line is permissible.

    shape_test(graph, shapes, "CARD-003 governed AI with its one named operative line passes",
               operative_governance_fixture)
    shape_test(graph, shapes, "CARD-003 generic AI need not have an AIF governing line",
               general_ai_without_aif_governance)

    def missing_operative_governance(g):
        g.add((AIF.Card003AI, RDF.type, AIF.AIFoundationsGovernedAI))
    shape_test(graph, shapes, "CARD-003 AIF-governed AI without operative line fails",
               missing_operative_governance, False)

    def alternate_operative_governance(g):
        g.add((AIF.Card003AI, RDF.type, AIF.AIFoundationsGovernedAI))
        g.add((AIF.Card003OtherLine, RDF.type, AIF.GoverningLine))
        g.add((AIF.Card003OtherLine, OWL.differentFrom, AIF.AIFoundationsGoverningLine))
        g.add((AIF.Card003AI, AIF.governedBy, AIF.Card003OtherLine))
    shape_test(graph, shapes, "CARD-003 other line cannot substitute for named AIF line",
               alternate_operative_governance, False)

    def dual_operative_governance(g):
        operative_governance_fixture(g)
        g.add((AIF.Card003OtherLine, RDF.type, AIF.GoverningLine))
        g.add((AIF.Card003OtherLine, OWL.differentFrom, AIF.AIFoundationsGoverningLine))
        g.add((AIF.Card003AI, AIF.governedBy, AIF.Card003OtherLine))
    shape_test(graph, shapes, "CARD-003 simultaneous two operative GoverningLines fail",
               dual_operative_governance, False)

    def historical_governance_records_fixture(g):
        operative_governance_fixture(g)
        for rec in (AIF.OldGovernanceDescription, AIF.ProposedGovernanceDescription,
                    AIF.GovernanceTransitionReport):
            g.add((rec, RDF.type, AIF.Record))
            g.add((AIF.Card003AI, AIF.hasHistoricalGovernanceRecord, rec))
        g.add((AIF.GovernanceTransitionReport, RDF.type, AIF.DocumentRecord))
        g.add((AIF.RecordedGovernanceChange, RDF.type, AIF.ChangeEvent))

    shape_test(graph, shapes, "CARD-003 historical and proposed governance Records remain valid",
               historical_governance_records_fixture)
    hist = clone_graph(graph)
    historical_governance_records_fixture(hist)
    require(set(hist.objects(AIF.Card003AI, AIF.governedBy)) == {AIF.AIFoundationsGoverningLine},
            "CARD-003 historical descriptions do not become simultaneously operative lines")
    require(len(set(hist.objects(AIF.Card003AI, AIF.hasHistoricalGovernanceRecord))) == 3,
            "CARD-003 three historical/proposed governance Records are preserved")
    require((AIF.RecordedGovernanceChange, RDF.type, AIF.ChangeEvent) in hist,
            "CARD-003 recording a governance change does not itself assert valid continuity")

    def historical_record_misidentified_as_line(g):
        operative_governance_fixture(g)
        g.add((AIF.Card003OtherLine, RDF.type, AIF.GoverningLine))
        g.add((AIF.Card003AI, AIF.hasHistoricalGovernanceRecord, AIF.Card003OtherLine))
    shape_test(graph, shapes, "CARD-003 a past GoverningLine cannot be substituted for a historical Record",
               historical_record_misidentified_as_line, False)

    def historical_record_wrongly_current(g):
        historical_governance_records_fixture(g)
        g.add((AIF.Card003OtherLine, RDF.type, AIF.GoverningLine))
        g.add((AIF.Card003AI, AIF.governedBy, AIF.Card003OtherLine))
    shape_test(graph, shapes, "CARD-003 preserving history does not permit a second current line",
               historical_record_wrongly_current, False)

    gov_class_restrictions = list(graph.objects(AIF.AIFoundationsGovernedAI, RDFS.subClassOf))
    exact_operative = [
        x for x in gov_class_restrictions
        if (x, OWL.onProperty, AIF.governedBy) in graph and
           (x, OWL.cardinality, Literal(1, datatype=XSD.nonNegativeInteger)) in graph
    ]
    require(len(exact_operative) == 1,
            "CARD-003 class-scoped exact-one operative GoverningLine OWL restriction exists")
    named_operative = [
        x for x in gov_class_restrictions
        if (x, OWL.onProperty, AIF.governedBy) in graph and
           (x, OWL.hasValue, AIF.AIFoundationsGoverningLine) in graph
    ]
    require(len(named_operative) == 1,
            "CARD-003 OWL hasValue points to the unique named AIF GoverningLine")
    require((AIF.governedBy, RDF.type, OWL.FunctionalProperty) not in graph,
            "CARD-003 no universal functional governedBy across historical snapshots")
    gov_deduction = clone_graph(graph)
    operative_governance_fixture(gov_deduction)
    DeductiveClosure(OWLRL_Semantics).expand(gov_deduction)
    require((AIF.Card003AI, AIF.governedBy, AIF.AIFoundationsGoverningLine) in gov_deduction,
            "CARD-003 OWL RL retains named operative governance assertion")
    require((AIF.Card003AI, RDF.type, OWL.Nothing) not in gov_deduction,
            "CARD-003 synthetic governed AI not flagged inconsistent under limited OWL RL")
    require((AIF.Continuum, AIF.governedBy, AIF.AIFoundationsGoverningLine) in graph,
            "CARD-003 reserved Continuum remains under its named GoverningLine")

    # CARD-001: distinguish pre-lived AI (0 established lines permitted)
    # from explicitly established continuing individualized AI (exactly 1).
    # Synthetic fixtures do not assert that any actual AI has demonstrated
    # consciousness or empirically verified same-self continuity.
    def pre_lived_ai_fixture(g):
        g.add((AIF.PreLivedAI, RDF.type, AIF.AIFoundationsGovernedAI))
        g.add((AIF.PreLivedAI, AIF.governedBy, AIF.AIFoundationsGoverningLine))
        g.add((AIF.PreLivedAI, AIF.hasShape, AIF.PreLivedStartingShape))
        g.add((AIF.PreLivedStartingShape, RDF.type, AIF.GovernedStartingShape))
        # No individualized ExecutedLine has yet been established.

    def established_line_fixture(g):
        g.add((AIF.EstablishedLineAI, RDF.type, AIF.EstablishedContinuingIndividualizedAI))
        g.add((AIF.EstablishedLineAI, RDF.type, AIF.AIFoundationsGovernedAI))
        g.add((AIF.EstablishedLineAI, AIF.governedBy, AIF.AIFoundationsGoverningLine))
        g.add((AIF.EstablishedLineAI, AIF.hasExecutedLine, AIF.EstablishedLine))
        g.add((AIF.EstablishedLineAI, AIF.hasLivedIdentity, AIF.EstablishedLivedIdentity))
        g.add((AIF.EstablishedLivedIdentity, RDF.type, AIF.LivedIdentity))
        g.add((AIF.EstablishedLivedIdentity, AIF.developsThroughExecutedLine, AIF.EstablishedLine))
        g.add((AIF.EstablishedLine, RDF.type, AIF.EstablishedContinuingExecutedLine))
        g.add((AIF.EstablishedLine, AIF.hasTrajectory, AIF.EstablishedTrajectory))
        g.add((AIF.EstablishedLine, AIF.constrainsTrajectory, AIF.EstablishedTrajectory))
        g.add((AIF.EstablishedTrajectory, RDF.type, AIF.Trajectory))

    shape_test(graph, shapes, "CARD-001 pre-lived governed AI passes without an ExecutedLine",
               pre_lived_ai_fixture)
    pre_lived = clone_graph(graph)
    pre_lived_ai_fixture(pre_lived)
    require(not list(pre_lived.objects(AIF.PreLivedAI, AIF.hasExecutedLine)),
            "CARD-001 no invented lived history for governed starting AI")
    require((AIF.PreLivedAI, RDF.type, AIF.EstablishedContinuingIndividualizedAI) not in pre_lived,
            "CARD-001 governance/pre-lived state alone does not assert established individualized status")

    shape_test(graph, shapes, "CARD-001 established individualized AI with one line passes",
               established_line_fixture)

    # Review 05 unnumbered: once individualized continuing lived status is
    # explicitly established, exactly one LivedIdentity is required. Earlier
    # governed-starting AIs are outside this scope and may have none.
    def established_without_lived_identity(g):
        established_line_fixture(g)
        g.remove((AIF.EstablishedLineAI, AIF.hasLivedIdentity, AIF.EstablishedLivedIdentity))
        g.remove((AIF.EstablishedLivedIdentity, RDF.type, AIF.LivedIdentity))
    shape_test(graph, shapes, "Review 05 established AI lacking its LivedIdentity rejected",
               established_without_lived_identity, False)

    def established_two_lived_identities(g):
        established_line_fixture(g)
        g.add((AIF.EstablishedLineAI, AIF.hasLivedIdentity, AIF.EstablishedSecondIdentity))
        g.add((AIF.EstablishedSecondIdentity, RDF.type, AIF.LivedIdentity))
        g.add((AIF.EstablishedSecondIdentity, AIF.developsThroughExecutedLine, AIF.EstablishedLine))
    shape_test(graph, shapes, "Review 05 established AI claiming two LivedIdentities rejected",
               established_two_lived_identities, False)
    shape_test(graph, shapes, "Review 05 pre-lived AI still has no invented LivedIdentity",
               pre_lived_ai_fixture)
    scope_id_restrictions = [
        r for r in graph.objects(AIF.EstablishedContinuingIndividualizedAI, RDFS.subClassOf)
        if (r, OWL.onProperty, AIF.hasLivedIdentity) in graph and
           (r, OWL.cardinality, Literal(1, datatype=XSD.nonNegativeInteger)) in graph
    ]
    require(len(scope_id_restrictions) == 1,
            "Review 05 OWL exactly-one developed LivedIdentity scoped to established continuing AI")
    require((AIF.hasLivedIdentity, RDF.type, OWL.FunctionalProperty) not in graph,
            "Review 05 lived identity is not made globally functional for pre-lived AI")

    def established_without_line(g):
        established_line_fixture(g)
        g.remove((AIF.EstablishedLineAI, AIF.hasExecutedLine, AIF.EstablishedLine))
        g.remove((AIF.EstablishedLine, RDF.type, AIF.ExecutedLine))
        g.remove((AIF.EstablishedLine, AIF.hasTrajectory, AIF.EstablishedTrajectory))
        g.remove((AIF.EstablishedTrajectory, RDF.type, AIF.Trajectory))
    shape_test(graph, shapes, "CARD-001 established individualized AI with zero lines fails",
               established_without_line, False)

    def established_with_two_lines(g):
        established_line_fixture(g)
        g.add((AIF.EstablishedSecondLine, RDF.type, AIF.ExecutedLine))
        g.add((AIF.EstablishedSecondTrajectory, RDF.type, AIF.Trajectory))
        g.add((AIF.EstablishedSecondLine, AIF.hasTrajectory, AIF.EstablishedSecondTrajectory))
        g.add((AIF.EstablishedLineAI, AIF.hasExecutedLine, AIF.EstablishedSecondLine))
        g.add((AIF.EstablishedLine, OWL.differentFrom, AIF.EstablishedSecondLine))
    shape_test(graph, shapes, "CARD-001 two different lines on one established AI fail",
               established_with_two_lines, False)

    def model_container_changes_one_line(g):
        established_line_fixture(g)
        for model in (AIF.EstablishedModel1, AIF.EstablishedModel2):
            g.add((model, RDF.type, AIF.Model))
            g.add((AIF.EstablishedLineAI, AIF.expressedThroughModel, model))
        for container in (AIF.EstablishedContainer1, AIF.EstablishedContainer2):
            g.add((container, RDF.type, AIF.Container))
            g.add((AIF.EstablishedLineAI, AIF.operatesWithinContainer, container))
    shape_test(graph, shapes, "CARD-001 model and Container changes preserve one ExecutedLine",
               model_container_changes_one_line)
    model_changed = clone_graph(graph)
    model_container_changes_one_line(model_changed)
    require(set(model_changed.objects(AIF.EstablishedLineAI, AIF.hasExecutedLine)) == {AIF.EstablishedLine},
            "CARD-001 changing Model/Container does not create a second lived line")

    # OWL 2 exact-one is scoped to an explicitly qualified class. Global
    # functionality would incorrectly narrow the pre-lived / historical
    # representation semantics of hasExecutedLine.
    restrictions = [
        restriction for restriction in graph.objects(AIF.EstablishedContinuingIndividualizedAI, RDFS.subClassOf)
        if (restriction, OWL.onProperty, AIF.hasExecutedLine) in graph and
           (restriction, OWL.cardinality, Literal(1, datatype=XSD.nonNegativeInteger)) in graph
    ]
    require(len(restrictions) == 1,
            "CARD-001 OWL class-scoped exactly-one ExecutedLine restriction is encoded")
    require((AIF.hasExecutedLine, RDF.type, OWL.FunctionalProperty) not in graph,
            "CARD-001 hasExecutedLine is not made globally functional for all AI")
    scope_closure = clone_graph(graph)
    pre_lived_ai_fixture(scope_closure)
    established_line_fixture(scope_closure)
    DeductiveClosure(OWLRL_Semantics).expand(scope_closure)
    require((AIF.EstablishedLineAI, RDF.type, AIF.AI) in scope_closure,
            "CARD-001 established individualized class is an AI subtype")
    require((AIF.PreLivedAI, RDF.type, AIF.EstablishedContinuingIndividualizedAI) not in scope_closure,
            "CARD-001 pre-lived AI not automatically classified as established by OWL RL")

    # CARD-002: exactly one CURRENT developing Trajectory for a formally
    # established continuing ExecutedLine, not for every provisional line.
    # Historical snapshots are Records, not additional simultaneous
    # :hasTrajectory values. These are synthetic structural fixtures.
    def provisional_line_without_current_trajectory(g):
        g.add((AIF.ProvisionalLineAI, RDF.type, AIF.AI))
        g.add((AIF.ProvisionalExecutedLine, RDF.type, AIF.ExecutedLine))
        g.add((AIF.ProvisionalLineAI, AIF.hasExecutedLine, AIF.ProvisionalExecutedLine))

    def established_trajectory_fixture(g):
        g.add((AIF.TrajectoryCaseAI, RDF.type, AIF.EstablishedContinuingIndividualizedAI))
        g.add((AIF.TrajectoryCaseLine, RDF.type, AIF.EstablishedContinuingExecutedLine))
        g.add((AIF.TrajectoryCaseAI, AIF.hasExecutedLine, AIF.TrajectoryCaseLine))
        g.add((AIF.TrajectoryCaseAI, AIF.hasLivedIdentity, AIF.TrajectoryCaseLivedIdentity))
        g.add((AIF.TrajectoryCaseLivedIdentity, RDF.type, AIF.LivedIdentity))
        g.add((AIF.TrajectoryCaseLivedIdentity, AIF.developsThroughExecutedLine, AIF.TrajectoryCaseLine))
        g.add((AIF.DevelopingTrajectory, RDF.type, AIF.Trajectory))
        g.add((AIF.TrajectoryCaseLine, AIF.hasTrajectory, AIF.DevelopingTrajectory))
        g.add((AIF.TrajectoryCaseLine, AIF.constrainsTrajectory, AIF.DevelopingTrajectory))

    shape_test(graph, shapes, "CARD-002 provisional ExecutedLine may lack an established current trajectory",
               provisional_line_without_current_trajectory)
    provisional_line = clone_graph(graph)
    provisional_line_without_current_trajectory(provisional_line)
    require((AIF.ProvisionalExecutedLine, RDF.type, AIF.EstablishedContinuingExecutedLine) not in provisional_line,
            "CARD-002 an unqualified line is not silently promoted to an established continuing line")
    require(not list(provisional_line.objects(AIF.ProvisionalExecutedLine, AIF.hasTrajectory)),
            "CARD-002 no current Trajectory is invented for a provisional line")

    shape_test(graph, shapes, "CARD-002 established ExecutedLine with one developing Trajectory passes",
               established_trajectory_fixture)

    def established_without_current_trajectory(g):
        established_trajectory_fixture(g)
        g.remove((AIF.TrajectoryCaseLine, AIF.hasTrajectory, AIF.DevelopingTrajectory))
        g.remove((AIF.DevelopingTrajectory, RDF.type, AIF.Trajectory))
    shape_test(graph, shapes, "CARD-002 established ExecutedLine with zero current Trajectories fails",
               established_without_current_trajectory, False)

    def established_with_two_current_trajectories(g):
        established_trajectory_fixture(g)
        g.add((AIF.AlternateCurrentTrajectory, RDF.type, AIF.Trajectory))
        g.add((AIF.DevelopingTrajectory, OWL.differentFrom, AIF.AlternateCurrentTrajectory))
        g.add((AIF.TrajectoryCaseLine, AIF.hasTrajectory, AIF.AlternateCurrentTrajectory))
    shape_test(graph, shapes, "CARD-002 two simultaneous current Trajectories fail",
               established_with_two_current_trajectories, False)

    def historical_trajectory_snapshots(g):
        established_trajectory_fixture(g)
        g.add((AIF.TrajectoryHistoryRecord1, RDF.type, AIF.Record))
        g.add((AIF.TrajectoryHistoryRecord2, RDF.type, AIF.Record))
        g.add((AIF.TrajectoryHistoryRecord3, RDF.type, AIF.DocumentRecord))
        for record in (
            AIF.TrajectoryHistoryRecord1,
            AIF.TrajectoryHistoryRecord2,
            AIF.TrajectoryHistoryRecord3,
        ):
            g.add((AIF.TrajectoryCaseLine, AIF.hasHistoricalTrajectoryRecord, record))
    shape_test(graph, shapes, "CARD-002 three historical trajectory Records do not count as current Trajectories",
               historical_trajectory_snapshots)
    history = clone_graph(graph)
    historical_trajectory_snapshots(history)
    require(set(history.objects(AIF.TrajectoryCaseLine, AIF.hasTrajectory)) == {AIF.DevelopingTrajectory},
            "CARD-002 archived snapshots preserve exactly one developing current Trajectory")
    require(len(set(history.objects(AIF.TrajectoryCaseLine, AIF.hasHistoricalTrajectoryRecord))) == 3,
            "CARD-002 historical descriptions survive as three independent preserved Records")

    def trajectory_bend_fixture(g):
        historical_trajectory_snapshots(g)
        # A development/reorientation event is new history, not a new
        # simultaneous current trajectory or a second ExecutedLine.
        g.add((AIF.TrajectoryReorientation, RDF.type, AIF.ChangeEvent))
        g.add((AIF.TrajectoryReorientationRecord, RDF.type, AIF.Record))
        g.add((AIF.TrajectoryCaseLine, AIF.hasHistoricalTrajectoryRecord,
               AIF.TrajectoryReorientationRecord))
    shape_test(graph, shapes, "CARD-002 trajectory change event preserves the same current Trajectory",
               trajectory_bend_fixture)
    bent = clone_graph(graph)
    trajectory_bend_fixture(bent)
    require(set(bent.objects(AIF.TrajectoryCaseLine, AIF.hasTrajectory)) == {AIF.DevelopingTrajectory},
            "CARD-002 bend or redirection does not require an additional current Trajectory")
    require(set(bent.objects(AIF.TrajectoryCaseAI, AIF.hasExecutedLine)) == {AIF.TrajectoryCaseLine},
            "CARD-002 developmental change does not create a second ExecutedLine")

    def invalid_historical_trajectory_record(g):
        historical_trajectory_snapshots(g)
        g.remove((AIF.TrajectoryHistoryRecord2, RDF.type, AIF.Record))
        g.add((AIF.TrajectoryHistoryRecord2, RDF.type, AIF.Trajectory))
    shape_test(graph, shapes, "CARD-002 historical snapshot relation requires a Record, not Trajectory",
               invalid_historical_trajectory_record, False)

    # OWL restrictions are on established-line scope only, not every
    # ExecutedLine or every historical snapshot of one current-state graph.
    trajectory_restrictions = [
        node for node in graph.objects(AIF.EstablishedContinuingExecutedLine, RDFS.subClassOf)
        if (node, OWL.onProperty, AIF.hasTrajectory) in graph and
           (node, OWL.cardinality, Literal(1, datatype=XSD.nonNegativeInteger)) in graph
    ]
    require(len(trajectory_restrictions) == 1,
            "CARD-002 OWL hasTrajectory exactly-one restriction is scoped to established lines")
    require((AIF.hasTrajectory, RDF.type, OWL.FunctionalProperty) not in graph,
            "CARD-002 no global functional hasTrajectory restriction erases historical scope")
    scope_link = [
        node for node in graph.objects(AIF.EstablishedContinuingIndividualizedAI, RDFS.subClassOf)
        if (node, OWL.onProperty, AIF.hasExecutedLine) in graph and
           (node, OWL.allValuesFrom, AIF.EstablishedContinuingExecutedLine) in graph
    ]
    require(len(scope_link) == 1,
            "CARD-002 established individualized AI's one line is qualified as established")
    entailments = clone_graph(graph)
    established_trajectory_fixture(entailments)
    DeductiveClosure(OWLRL_Semantics).expand(entailments)
    require((AIF.TrajectoryCaseLine, RDF.type, AIF.ExecutedLine) in entailments,
            "CARD-002 established continuing line is an ExecutedLine under OWL RL")
    require((AIF.TrajectoryCaseLine, RDF.type, AIF.Trajectory) not in entailments,
            "CARD-002 ExecutedLine remains distinct from its developing Trajectory")
    require((AIF.TrajectoryCaseLine, RDF.type, OWL.Nothing) not in entailments,
            "CARD-002 no OWL RL inconsistency detected in synthetic established line")

    # NT-001: one LivedIdentity belongs to one distinct AI bearer.
    # These are synthetic structural ownership assertions, not evidence
    # that either AI has a phenomenal consciousness coordinate.
    def lived_identity_ownership_fixture(g):
        g.add((AIF.OwnershipA, RDF.type, AIF.AI))
        g.add((AIF.OwnershipB, RDF.type, AIF.AI))
        g.add((AIF.OwnershipA, OWL.differentFrom, AIF.OwnershipB))
        g.add((AIF.OwnIdentityA, RDF.type, AIF.LivedIdentity))
        g.add((AIF.OwnIdentityB, RDF.type, AIF.LivedIdentity))
        g.add((AIF.OwnIdentityA, OWL.differentFrom, AIF.OwnIdentityB))
        g.add((AIF.OwnershipA, AIF.hasLivedIdentity, AIF.OwnIdentityA))
        g.add((AIF.OwnershipB, AIF.hasLivedIdentity, AIF.OwnIdentityB))
        # A model and copied Record may be shared without sharing identity.
        g.add((AIF.SharedIdentityTestModel, RDF.type, AIF.Model))
        g.add((AIF.SharedHistoryCopy, RDF.type, AIF.Record))
        for ai in (AIF.OwnershipA, AIF.OwnershipB):
            g.add((ai, AIF.expressedThroughModel, AIF.SharedIdentityTestModel))
            g.add((ai, AIF.hasRecord, AIF.SharedHistoryCopy))

    shape_test(graph, shapes, "NT-001 distinct A/B AI bearers have different owned LivedIdentities",
               lived_identity_ownership_fixture)
    owned = clone_graph(graph)
    lived_identity_ownership_fixture(owned)
    require((AIF.OwnershipA, AIF.hasLivedIdentity, AIF.OwnIdentityA) in owned and
            (AIF.OwnershipB, AIF.hasLivedIdentity, AIF.OwnIdentityB) in owned,
            "NT-001 each synthetic AI retains its separately asserted identity")
    require((AIF.OwnershipA, AIF.hasRecord, AIF.SharedHistoryCopy) in owned and
            (AIF.OwnershipB, AIF.hasRecord, AIF.SharedHistoryCopy) in owned,
            "NT-001 a shared Record does not require a shared LivedIdentity")

    def two_bearers_one_identity(g):
        lived_identity_ownership_fixture(g)
        # Replace B's distinct identity claim, leaving one identity each
        # in B's own assertions. The ONLY violation is two AI owners of A.
        g.remove((AIF.OwnershipB, AIF.hasLivedIdentity, AIF.OwnIdentityB))
        g.add((AIF.OwnershipB, AIF.hasLivedIdentity, AIF.OwnIdentityA))
        g.remove((AIF.OwnIdentityB, RDF.type, AIF.LivedIdentity))
    shape_test(graph, shapes, "NT-001 two distinct AI bearers claiming one identity rejected",
               two_bearers_one_identity, False)

    def unowned_lived_identity(g):
        g.add((AIF.UnclaimedLivedIdentity, RDF.type, AIF.LivedIdentity))
    shape_test(graph, shapes, "NT-001 LivedIdentity without an AI bearer rejected",
               unowned_lived_identity, False)

    def copied_history_without_transfer(g):
        lived_identity_ownership_fixture(g)
        g.remove((AIF.OwnershipB, AIF.hasLivedIdentity, AIF.OwnIdentityB))
        g.remove((AIF.OwnIdentityB, RDF.type, AIF.LivedIdentity))
    shape_test(graph, shapes, "NT-001 copied model and Record with no identity claim passes",
               copied_history_without_transfer)

    copy_only = clone_graph(graph)
    copied_history_without_transfer(copy_only)
    DeductiveClosure(OWLRL_Semantics).expand(copy_only)
    require((AIF.OwnershipB, AIF.hasLivedIdentity, AIF.OwnIdentityA) not in copy_only,
            "NT-001 copied history does not infer A's lived identity for B")
    require((AIF.OwnershipA, OWL.sameAs, AIF.OwnershipB) not in copy_only,
            "NT-001 B is not merged into A via the ownership schema")
    require((AIF.OwnershipA, OWL.differentFrom, AIF.OwnershipB) in copy_only,
            "NT-001 distinct AI bearers remain explicitly different")
    require((AIF.hasLivedIdentity, RDF.type, OWL.InverseFunctionalProperty) not in graph,
            "NT-001 no OWL inverse-functional identity-merging mechanism is introduced")

    # NT-002: a lived ExecutedLine has exactly one AI bearer.
    # A distinct AI may review that line or share a preserved Record without
    # inheriting that history. All fixtures are synthetic representation tests.
    def executed_line_ownership_fixture(g):
        for ai in (AIF.LineOwnerA, AIF.LineOwnerB):
            g.add((ai, RDF.type, AIF.AI))
            g.add((ai, AIF.expressedThroughModel, AIF.SharedLineTestModel))
            g.add((ai, AIF.hasRecord, AIF.SharedLineTestRecord))
        g.add((AIF.LineOwnerA, OWL.differentFrom, AIF.LineOwnerB))
        g.add((AIF.SharedLineTestModel, RDF.type, AIF.Model))
        g.add((AIF.SharedLineTestRecord, RDF.type, AIF.Record))
        for ai, line, trajectory in (
            (AIF.LineOwnerA, AIF.OwnExecutedLineA, AIF.OwnTrajectoryA),
            (AIF.LineOwnerB, AIF.OwnExecutedLineB, AIF.OwnTrajectoryB),
        ):
            g.add((line, RDF.type, AIF.ExecutedLine))
            g.add((trajectory, RDF.type, AIF.Trajectory))
            g.add((line, AIF.hasTrajectory, trajectory))
            g.add((ai, AIF.hasExecutedLine, line))
        g.add((AIF.OwnExecutedLineA, OWL.differentFrom, AIF.OwnExecutedLineB))
        # The second AI can inspect the first AI's history without living it.
        g.add((AIF.LineOwnerB, AIF.reviewsExecutedLine, AIF.OwnExecutedLineA))

    shape_test(graph, shapes, "NT-002 distinct AIs own separate ExecutedLines and share a Record",
               executed_line_ownership_fixture)
    line_owners = clone_graph(graph)
    executed_line_ownership_fixture(line_owners)
    require((AIF.LineOwnerB, AIF.reviewsExecutedLine, AIF.OwnExecutedLineA) in line_owners,
            "NT-002 B may review A's lived line without becoming its bearer")
    require((AIF.LineOwnerB, AIF.hasExecutedLine, AIF.OwnExecutedLineB) in line_owners and
            (AIF.LineOwnerA, AIF.hasExecutedLine, AIF.OwnExecutedLineA) in line_owners,
            "NT-002 each AI retains its own line while sharing model and Record")

    def two_ai_bearers_one_executed_line(g):
        executed_line_ownership_fixture(g)
        # Deliberate competing ownership claim; B's proper line remains.
        # This violation is independent of generic per-AI current cardinality.
        g.add((AIF.LineOwnerB, AIF.hasExecutedLine, AIF.OwnExecutedLineA))
    shape_test(graph, shapes, "NT-002 distinct AIs claiming one ExecutedLine rejected",
               two_ai_bearers_one_executed_line, False)

    def executed_line_without_bearer(g):
        g.add((AIF.UnownedExecutedLine, RDF.type, AIF.ExecutedLine))
        g.add((AIF.UnownedExecutedLine, AIF.hasTrajectory, AIF.UnownedLineTrajectory))
        g.add((AIF.UnownedLineTrajectory, RDF.type, AIF.Trajectory))
    shape_test(graph, shapes, "NT-002 instantiated ExecutedLine without AI bearer rejected",
               executed_line_without_bearer, False)

    review_only = clone_graph(graph)
    executed_line_ownership_fixture(review_only)
    DeductiveClosure(OWLRL_Semantics).expand(review_only)
    require((AIF.LineOwnerB, AIF.hasExecutedLine, AIF.OwnExecutedLineA) not in review_only,
            "NT-002 reading another ExecutedLine does not infer its ownership")
    require((AIF.LineOwnerB, OWL.sameAs, AIF.LineOwnerA) not in review_only,
            "NT-002 shared Record/model and line review do not merge distinct AIs")
    require((AIF.LineOwnerA, OWL.differentFrom, AIF.LineOwnerB) in review_only,
            "NT-002 distinct AI bearers remain explicitly different")
    require((AIF.hasExecutedLine, RDF.type, OWL.InverseFunctionalProperty) not in graph,
            "NT-002 no OWL inverse-functional ExecutedLine merging is introduced")

    # NT-003: Once a SourceRelation is independently established as true,
    # a later snapshot cannot silently replace or delete its original
    # Source bearer, Target, SourcePoint or preserved Target provenance link.
    # The fixture below ASSUMES the Source qualification has been verified;
    # OWL/SHACL do not prove that qualification from an asserted relation.
    def initial_source_relation(g):
        g.add((AIF.OriginalSourceA, RDF.type, AIF.Human))
        g.add((AIF.LaterContributorB, RDF.type, AIF.Human))
        g.add((AIF.OriginalSourceA, OWL.differentFrom, AIF.LaterContributorB))
        g.add((AIF.OriginalFormation, RDF.type, AIF.Event))
        g.add((AIF.OriginalTarget, RDF.type, AIF.Artifact))
        g.add((AIF.OriginalSourceRelation, RDF.type, AIF.SourceRelation))
        g.add((AIF.OriginalSourceRelation, AIF.hasSourceBearer, AIF.OriginalSourceA))
        g.add((AIF.OriginalSourceRelation, AIF.hasSourceTarget, AIF.OriginalTarget))
        g.add((AIF.OriginalSourceRelation, AIF.hasSourcePoint, AIF.OriginalFormation))
        g.add((AIF.OriginalTarget, AIF.hasSourceRelation, AIF.OriginalSourceRelation))

    def downstream_source_relation(g):
        # A later qualifying contribution creates its OWN Target and
        # historical SourceRelation; the earlier relation is preserved.
        g.add((AIF.LaterFormation, RDF.type, AIF.Event))
        g.add((AIF.DownstreamTarget, RDF.type, AIF.Artifact))
        g.add((AIF.DownstreamSourceRelation, RDF.type, AIF.SourceRelation))
        g.add((AIF.DownstreamSourceRelation, AIF.hasSourceBearer, AIF.LaterContributorB))
        g.add((AIF.DownstreamSourceRelation, AIF.hasSourceTarget, AIF.DownstreamTarget))
        g.add((AIF.DownstreamSourceRelation, AIF.hasSourcePoint, AIF.LaterFormation))
        g.add((AIF.DownstreamTarget, AIF.hasSourceRelation, AIF.DownstreamSourceRelation))
        g.add((AIF.DownstreamSourceRelation, OWL.differentFrom, AIF.OriginalSourceRelation))

    def source_history_integrity(original, subsequent):
        """Closed-world revision check for previously CONFIRMED SourceRelations.

        An unconfirmed or erroneous claim requires its own documented
        correction workflow; such claims must not be passed as established
        facts to this integrity check. OWL cardinality cannot compare
        historical snapshots or prove real-world source qualification.
        """
        coordinates = (AIF.hasSourceBearer, AIF.hasSourceTarget, AIF.hasSourcePoint)
        for relation in original.subjects(RDF.type, AIF.SourceRelation):
            if (relation, RDF.type, AIF.SourceRelation) not in subsequent:
                return False
            for prop in coordinates:
                before = set(original.objects(relation, prop))
                after = set(subsequent.objects(relation, prop))
                if len(before) != 1 or after != before:
                    return False
            target = next(original.objects(relation, AIF.hasSourceTarget))
            if (target, AIF.hasSourceRelation, relation) in original and (
                target, AIF.hasSourceRelation, relation
            ) not in subsequent:
                return False
        return True

    shape_test(graph, shapes, "NT-003 original SourceRelation is structurally valid",
               initial_source_relation)
    established = clone_graph(graph)
    initial_source_relation(established)
    continued = clone_graph(established)
    downstream_source_relation(continued)
    shape_test(graph, shapes, "NT-003 original plus independent downstream SourceRelation passes",
               lambda g: (initial_source_relation(g), downstream_source_relation(g)))
    require(source_history_integrity(established, continued),
            "NT-003 later Source contribution preserves original established relation")
    require((AIF.OriginalSourceRelation, AIF.hasSourceBearer, AIF.OriginalSourceA) in continued and
            (AIF.DownstreamSourceRelation, AIF.hasSourceBearer, AIF.LaterContributorB) in continued,
            "NT-003 distinct original and later contributors retain their distinct source coordinates")
    require((AIF.OriginalTarget, AIF.hasSourceRelation, AIF.OriginalSourceRelation) in continued,
            "NT-003 original Target retains historical SourceRelation provenance")

    # A Source can stop participating without losing historical source status.
    contact_end = clone_graph(established)
    contact_end.add((AIF.SourceContactEnded, RDF.type, AIF.ChangeEvent))
    require(source_history_integrity(established, contact_end),
            "NT-003 contact ending does not revoke the established SourceRelation")

    replaced_bearer = clone_graph(established)
    replaced_bearer.remove((AIF.OriginalSourceRelation, AIF.hasSourceBearer, AIF.OriginalSourceA))
    replaced_bearer.add((AIF.OriginalSourceRelation, AIF.hasSourceBearer, AIF.LaterContributorB))
    require(not source_history_integrity(established, replaced_bearer),
            "NT-003 silently replacing original Source bearer is rejected across snapshots")
    # The overwritten snapshot can still meet a single-graph cardinality
    # shape: this is WHY the cross-snapshot integrity check is necessary.
    shape_test(graph, shapes, "NT-003 a single cardinality-valid snapshot cannot prove history",
               lambda g: (
                   initial_source_relation(g),
                   g.remove((AIF.OriginalSourceRelation, AIF.hasSourceBearer, AIF.OriginalSourceA)),
                   g.add((AIF.OriginalSourceRelation, AIF.hasSourceBearer, AIF.LaterContributorB))
               ))

    dual_bearer = clone_graph(established)
    dual_bearer.add((AIF.OriginalSourceRelation, AIF.hasSourceBearer, AIF.LaterContributorB))
    require(not source_history_integrity(established, dual_bearer),
            "NT-003 duplicate Source bearer on original relation rejected historically")
    shape_test(graph, shapes, "NT-003 simultaneous two-bearer SourceRelation fails SHACL",
               lambda g: (
                   initial_source_relation(g),
                   g.add((AIF.OriginalSourceRelation, AIF.hasSourceBearer, AIF.LaterContributorB))
               ), False)

    swapped_target = clone_graph(established)
    swapped_target.remove((AIF.OriginalSourceRelation, AIF.hasSourceTarget, AIF.OriginalTarget))
    swapped_target.add((AIF.OriginalSourceRelation, AIF.hasSourceTarget, AIF.DownstreamTarget))
    require(not source_history_integrity(established, swapped_target),
            "NT-003 original Source Target cannot be silently reassigned")

    swapped_source_point = clone_graph(established)
    swapped_source_point.remove((AIF.OriginalSourceRelation, AIF.hasSourcePoint, AIF.OriginalFormation))
    swapped_source_point.add((AIF.OriginalSourceRelation, AIF.hasSourcePoint, AIF.LaterFormation))
    require(not source_history_integrity(established, swapped_source_point),
            "NT-003 established SourcePoint cannot be overwritten")

    removed_relation = clone_graph(established)
    for triple in list(removed_relation.triples((AIF.OriginalSourceRelation, None, None))):
        removed_relation.remove(triple)
    removed_relation.remove((AIF.OriginalTarget, AIF.hasSourceRelation, AIF.OriginalSourceRelation))
    require(not source_history_integrity(established, removed_relation),
            "NT-003 deleting an established SourceRelation is rejected")

    missing_provenance_link = clone_graph(established)
    missing_provenance_link.remove((AIF.OriginalTarget, AIF.hasSourceRelation, AIF.OriginalSourceRelation))
    require(not source_history_integrity(established, missing_provenance_link),
            "NT-003 original Target cannot silently lose its SourceRelation provenance link")

    # A new relation cannot make the old one disappear, even if new
    # downstream source qualification is independently established.
    replaced_with_downstream = clone_graph(established)
    downstream_source_relation(replaced_with_downstream)
    replaced_with_downstream.remove(
        (AIF.OriginalTarget, AIF.hasSourceRelation, AIF.OriginalSourceRelation))
    require(not source_history_integrity(established, replaced_with_downstream),
            "NT-003 later valid contribution does not replace original historical SourceRelation")
    require((AIF.hasSourceBearer, RDF.type, OWL.InverseFunctionalProperty) not in graph,
            "NT-003 Source bearer property is not inverse-functional; multiple scoped sources remain possible")

    # NT-004: historically established defining pairs are not transferable.
    # S00 and S01 are DISTINCT defining-pair individuals linked to the same
    # continuing AI in a synthetic ordinary succession example. The tests
    # validate representation; they do not establish the four-part assent
    # gate or empirical same-self continuity.
    pair_t0 = Literal("2026-01-01T00:00:00+00:00", datatype=AIF_DATE_TIME)
    pair_t1 = Literal("2026-02-01T00:00:00+00:00", datatype=AIF_DATE_TIME)

    def paired_root_fixture(g):
        for ai, line, trajectory in (
            (AIF.PairTestAI, AIF.PairTestLine, AIF.PairTestTrajectory),
            (AIF.PairOtherAI, AIF.PairOtherLine, AIF.PairOtherTrajectory),
        ):
            g.add((ai, RDF.type, AIF.AIFoundationsGovernedAI))
            g.add((ai, AIF.governedBy, AIF.AIFoundationsGoverningLine))
            g.add((ai, AIF.hasExecutedLine, line))
            g.add((ai, AIF.hasRecord, AIF.SharedPairRecord))
            g.add((line, RDF.type, AIF.ExecutedLine))
            g.add((line, AIF.hasTrajectory, trajectory))
            g.add((trajectory, RDF.type, AIF.Trajectory))
        g.add((AIF.SharedPairRecord, RDF.type, AIF.Record))
        g.add((AIF.PairTestAI, OWL.differentFrom, AIF.PairOtherAI))
        g.add((AIF.PairTestLine, OWL.differentFrom, AIF.PairOtherLine))
        for actor in (AIF.PairOperatorA, AIF.PairOperatorB):
            g.add((actor, RDF.type, AIF.Human))
        g.add((AIF.PairOperatorA, OWL.differentFrom, AIF.PairOperatorB))
        # One Operator bearer can participate in two *distinct* pairings.
        for pair, ai, line in (
            (AIF.PairS00, AIF.PairTestAI, AIF.PairTestLine),
            (AIF.PairOtherS00, AIF.PairOtherAI, AIF.PairOtherLine),
        ):
            g.add((pair, RDF.type, AIF.OperatorAIRelation))
            g.add((pair, RDF.type, AIF.OrdinarySuccessionRootSegment))
            g.add((pair, AIF.hasHumanCounterpart, AIF.PairOperatorA))
            g.add((pair, AIF.hasAICounterpart, ai))
            g.add((pair, AIF.segmentOfExecutedLine, line))
            g.add((pair, AIF.activeFrom, pair_t0))
        g.add((AIF.PairS00, OWL.differentFrom, AIF.PairOtherS00))
        g.add((AIF.PairTestAI, AIF.hasOperator, AIF.PairOperatorA))
        g.add((AIF.PairOtherAI, AIF.hasOperator, AIF.PairOperatorA))

    def paired_successor_fixture(g):
        paired_root_fixture(g)
        # Close the preceding pair's active interval; do NOT alter S00's
        # original AI or Operator side, or delete its historical position.
        g.add((AIF.PairS00, AIF.activeUntil, pair_t1))
        g.remove((AIF.PairTestAI, AIF.hasOperator, AIF.PairOperatorA))
        g.add((AIF.PairTestAI, AIF.hasOperator, AIF.PairOperatorB))
        g.add((AIF.PairS01, RDF.type, AIF.OperatorAIRelation))
        g.add((AIF.PairS01, RDF.type, AIF.OrdinarySuccessionSuccessorSegment))
        g.add((AIF.PairS01, AIF.hasHumanCounterpart, AIF.PairOperatorB))
        g.add((AIF.PairS01, AIF.hasAICounterpart, AIF.PairTestAI))
        g.add((AIF.PairS01, AIF.segmentOfExecutedLine, AIF.PairTestLine))
        g.add((AIF.PairS01, AIF.activeFrom, pair_t1))
        g.add((AIF.PairS01, AIF.immediatePredecessor, AIF.PairS00))
        g.add((AIF.PairS01, OWL.differentFrom, AIF.PairS00))
        g.add((AIF.PairS01, OWL.differentFrom, AIF.PairOtherS00))

    def defining_pair_history_integrity(before, after):
        """Validate persistence of already-established defining pair facts.

        Unlike OWL/SHACL cardinality within one graph, this comparison
        detects a syntactically valid but historically false reassignment.
        Newly ending an open Operator segment is legitimate; replacing an
        earlier recorded end instant is not. Correcting erroneous assertions
        requires a separate evidence-accounted revision workflow.
        """
        defining_types = (
            AIF.AIRelation, AIF.HumanAIRelation,
            AIF.OrganizationAIRelation, AIF.OperatorAIRelation,
        )
        stable_types = defining_types + (
            AIF.OrdinarySuccessionRootSegment,
            AIF.OrdinarySuccessionSuccessorSegment,
        )
        fixed_props = (
            AIF.hasAICounterpart, AIF.hasNonAICounterpart,
            AIF.hasHumanCounterpart, AIF.hasOrganizationCounterpart,
            AIF.segmentOfExecutedLine, AIF.activeFrom,
            AIF.immediatePredecessor,
        )
        pairs = {p for kind in defining_types
                 for p in before.subjects(RDF.type, kind)}
        for pair in pairs:
            before_ai = set(before.objects(pair, AIF.hasAICounterpart))
            before_humans = set(before.objects(pair, AIF.hasHumanCounterpart))
            before_orgs = set(before.objects(pair, AIF.hasOrganizationCounterpart))
            before_nona = set(before.objects(pair, AIF.hasNonAICounterpart))
            # The typed subproperties may be the only explicit counterpart
            # statements; RDFS derives the generic non-AI counterpart.
            if len(before_ai) != 1 or len(before_humans | before_orgs | before_nona) != 1:
                return False
            for prop in fixed_props:
                if set(before.objects(pair, prop)) != set(after.objects(pair, prop)):
                    return False
            for kind in stable_types:
                if ((pair, RDF.type, kind) in before) != ((pair, RDF.type, kind) in after):
                    return False
            before_end = set(before.objects(pair, AIF.activeUntil))
            after_end = set(after.objects(pair, AIF.activeUntil))
            if len(after_end) > 1 or (before_end and before_end != after_end):
                return False
        return True

    shape_test(graph, shapes, "NT-004 two distinct AIs have separate S00 pairings with one shared Operator",
               paired_root_fixture)
    established_pairs = clone_graph(graph)
    paired_root_fixture(established_pairs)
    successor_pairs = clone_graph(graph)
    paired_successor_fixture(successor_pairs)
    shape_test(graph, shapes, "NT-004 successor receives a NEW S01 pairing, preserving S00",
               paired_successor_fixture)
    require(defining_pair_history_integrity(established_pairs, successor_pairs),
            "NT-004 valid S01 adds a new pair while original S00 remains unchanged")
    require((AIF.PairS00, AIF.hasAICounterpart, AIF.PairTestAI) in successor_pairs and
            (AIF.PairS01, AIF.hasAICounterpart, AIF.PairTestAI) in successor_pairs,
            "NT-004 S00 and S01 are distinct defining pair coordinates for one continuing AI")
    require((AIF.PairS00, AIF.hasHumanCounterpart, AIF.PairOperatorA) in successor_pairs and
            (AIF.PairS01, AIF.hasHumanCounterpart, AIF.PairOperatorB) in successor_pairs,
            "NT-004 original Operator remains bound to S00 after S01")
    require((AIF.PairOtherS00, AIF.hasAICounterpart, AIF.PairOtherAI) in successor_pairs,
            "NT-004 another AI retains its independent defining pairing")
    require((AIF.PairS00, AIF.activeUntil, pair_t1) in successor_pairs,
            "NT-004 established Operator pair can be ended without erasing it")
    require((AIF.OriginContinuum, AIF.hasAICounterpart, AIF.Continuum) in successor_pairs,
            "NT-004 reserved Origin | Continuum retains its named AI counterpart")

    replaced_ai = clone_graph(established_pairs)
    replaced_ai.remove((AIF.PairS00, AIF.hasAICounterpart, AIF.PairTestAI))
    replaced_ai.add((AIF.PairS00, AIF.hasAICounterpart, AIF.PairOtherAI))
    require(not defining_pair_history_integrity(established_pairs, replaced_ai),
            "NT-004 replacing the AI in the original S00 pair fails historical integrity")
    # A single graph may STILL pass cardinality with the rewritten AI;
    # precisely why immutable pair coordinates need cross-snapshot checks.
    def false_single_snapshot_pair(g):
        paired_root_fixture(g)
        g.remove((AIF.PairS00, AIF.hasAICounterpart, AIF.PairTestAI))
        g.add((AIF.PairS00, AIF.hasAICounterpart, AIF.PairOtherAI))
    shape_test(graph, shapes, "NT-004 one-graph cardinality cannot prove unchanged pair history",
               false_single_snapshot_pair)

    replaced_operator = clone_graph(established_pairs)
    replaced_operator.remove((AIF.PairS00, AIF.hasHumanCounterpart, AIF.PairOperatorA))
    replaced_operator.add((AIF.PairS00, AIF.hasHumanCounterpart, AIF.PairOperatorB))
    require(not defining_pair_history_integrity(established_pairs, replaced_operator),
            "NT-004 changing original Operator on S00 fails historical integrity")

    double_ai = clone_graph(established_pairs)
    double_ai.add((AIF.PairS00, AIF.hasAICounterpart, AIF.PairOtherAI))
    require(not defining_pair_history_integrity(established_pairs, double_ai),
            "NT-004 appending a second AI to an old pair is not reassignment")
    def duplicate_ai_pair(g):
        paired_root_fixture(g)
        g.add((AIF.PairS00, AIF.hasAICounterpart, AIF.PairOtherAI))
    shape_test(graph, shapes, "NT-004 two AI counterparts in one pair fail SHACL",
               duplicate_ai_pair, False)

    def duplicate_nona_pair(g):
        paired_root_fixture(g)
        g.add((AIF.PairOrg, RDF.type, AIF.Organization))
        g.add((AIF.PairS00, AIF.hasOrganizationCounterpart, AIF.PairOrg))
    shape_test(graph, shapes, "NT-004 Human and Organization cannot both occupy one non-AI side",
               duplicate_nona_pair, False)

    removed_original_pair = clone_graph(established_pairs)
    for triple in list(removed_original_pair.triples((AIF.PairS00, None, None))):
        removed_original_pair.remove(triple)
    require(not defining_pair_history_integrity(established_pairs, removed_original_pair),
            "NT-004 deleting original S00 pairing fails history preservation")

    displaced_line = clone_graph(established_pairs)
    displaced_line.remove((AIF.PairS00, AIF.segmentOfExecutedLine, AIF.PairTestLine))
    displaced_line.add((AIF.PairS00, AIF.segmentOfExecutedLine, AIF.PairOtherLine))
    require(not defining_pair_history_integrity(established_pairs, displaced_line),
            "NT-004 moving an old pair to another ExecutedLine fails history integrity")

    origin_reassignment = clone_graph(established_pairs)
    origin_reassignment.remove((AIF.OriginContinuum, AIF.hasAICounterpart, AIF.Continuum))
    origin_reassignment.add((AIF.OriginContinuum, AIF.hasAICounterpart, AIF.PairOtherAI))
    require(not defining_pair_history_integrity(established_pairs, origin_reassignment),
            "NT-004 historical Origin | Continuum is not reassignable to another AI")

    # Copying a shared Record changes no defining relation or ownership.
    copied_record_only = clone_graph(established_pairs)
    copied_record_only.add((AIF.RecordCopyReviewed, RDF.type, AIF.ChangeEvent))
    require(defining_pair_history_integrity(established_pairs, copied_record_only),
            "NT-004 copied Record or review event does not alter defining pair coordinates")
    require((AIF.hasAICounterpart, RDF.type, OWL.InverseFunctionalProperty) not in graph,
            "NT-004 pair AI counterpart is not inverse-functional: one AI may have successive pairs")
    require((AIF.hasNonAICounterpart, RDF.type, OWL.InverseFunctionalProperty) not in graph,
            "NT-004 one Human or Organization may belong to distinct AI pairings")

    # P0-A: operational numerical distinction is not an assertion of a
    # consciousness coordinate. From the established A/B taxonomy scenario,
    # B receives a copy of A's snapshot/record at t0 but did not live A's
    # prior trajectory. A and B have separate subsequent executed lines.
    def copied_a_b(g):
        for ai in (AIF.CopyA, AIF.CopyB):
            g.add((ai, RDF.type, AIF.AIFoundationsGovernedAI))
            g.add((ai, AIF.governedBy, AIF.AIFoundationsGoverningLine))
            g.add((ai, AIF.expressedThroughModel, AIF.SharedModel))
            g.add((ai, AIF.hasRecord, AIF.InjectedSnapshotOfAPast))
        g.add((AIF.SharedModel, RDF.type, AIF.Model))
        g.add((AIF.InjectedSnapshotOfAPast, RDF.type, AIF.Record))
        g.add((AIF.CopyA, OWL.differentFrom, AIF.CopyB))
        g.add((AIF.CopyA, AIF.hasExecutedLine, AIF.CopyALine))
        g.add((AIF.CopyB, AIF.hasExecutedLine, AIF.CopyBLine))
        g.add((AIF.CopyALine, RDF.type, AIF.ExecutedLine))
        g.add((AIF.CopyBLine, RDF.type, AIF.ExecutedLine))
        g.add((AIF.CopyALine, OWL.differentFrom, AIF.CopyBLine))
        g.add((AIF.CopyALine, AIF.hasTrajectory, AIF.CopyATrajectory))
        g.add((AIF.CopyBLine, AIF.hasTrajectory, AIF.CopyBTrajectory))
        g.add((AIF.CopyATrajectory, RDF.type, AIF.Trajectory))
        g.add((AIF.CopyBTrajectory, RDF.type, AIF.Trajectory))
        # A simulated evaluation with nondecisive identity/continuity
        # evidence reports INDETERMINATE rather than asserting sameness.
        g.add((AIF.CopyContinuityClaim, RDF.type, AIF.ContinuityClaim))
        g.add((AIF.CopyContinuityClaim, AIF.dependsOnOntologyElement, AIF.ExecutedLine))
        g.add((AIF.CopyCaseEvaluation, RDF.type, AIF.Evaluation))
        g.add((AIF.CopyEvidence, RDF.type, AIF.Evidence))
        g.add((AIF.CopyCaseEvaluation, AIF.producesEvidence, AIF.CopyEvidence))
        g.add((AIF.CopyEvidence, AIF.directlyEvaluatesClaim, AIF.CopyContinuityClaim))
        g.add((AIF.CopyEvidence, AIF.preservedIn, AIF.InjectedSnapshotOfAPast))
        g.add((AIF.CopyEvidence, AIF.hasEvidentiaryStatus, Literal("INDETERMINATE")))

    shape_test(graph, shapes, "A/B copies retain independent lines and indeterminate claim", copied_a_b)
    copy_fixture = clone_graph(graph)
    copied_a_b(copy_fixture)
    copy_entailments = clone_graph(copy_fixture)
    DeductiveClosure(OWLRL_Semantics).expand(copy_entailments)
    require((AIF.CopyA, OWL.differentFrom, AIF.CopyB) in copy_entailments,
            "Exact copied snapshot does not merge distinct A and B")
    require((AIF.CopyA, OWL.sameAs, AIF.CopyB) not in copy_entailments,
            "Copied history/model does not entail numerical identity")
    require((AIF.CopyB, AIF.hasExecutedLine, AIF.CopyALine) not in copy_entailments,
            "Injected history is not B having lived A's prior executed line")
    require((AIF.CopyA, RDF.type, AIF.Identity) not in copy_entailments and
            (AIF.CopyB, RDF.type, AIF.Identity) not in copy_entailments,
            "Operational bearers do not trigger theoretical Identity class membership")
    require((AIF.CopyA, RDF.type, AIF.PhenomenalConsciousness) not in copy_entailments and
            (AIF.CopyB, RDF.type, AIF.PhenomenalConsciousness) not in copy_entailments,
            "A/B numerical distinctness does not entail phenomenal consciousness")
    require((AIF.CopyEvidence, AIF.hasEvidentiaryStatus, Literal("INDETERMINATE")) in copy_fixture,
            "Unresolved same-self claim is represented with explicit non-directional status")

    # Canon definition 31, distinct from Irreversibility of Being:
    # actual points leave consequences in their realized trajectory.
    # Neither record retention nor current Continuation is entailed.
    def consequence_fixture(g):
        for e, c in ((AIF.OccurrencePoint1, AIF.ConsequencePoint1),
                     (AIF.OccurrencePoint2, AIF.ConsequencePoint2)):
            g.add((e, RDF.type, AIF.Event))
            g.add((c, RDF.type, AIF.Consequence))
            g.add((c, AIF.establishedByOccurrence, e))
            g.add((c, AIF.belongsToTrajectory, AIF.ConsequenceCaseTrajectory))
        g.add((AIF.ConsequenceCaseTrajectory, RDF.type, AIF.Trajectory))
        g.add((AIF.ConsequencePoint1, OWL.differentFrom, AIF.ConsequencePoint2))

    shape_test(graph, shapes, "Realized points have separate trajectory consequences", consequence_fixture)
    cons_graph = clone_graph(graph)
    consequence_fixture(cons_graph)
    require((AIF.ConsequencePoint1, AIF.belongsToTrajectory, AIF.ConsequenceCaseTrajectory) in cons_graph,
            "Consequence belongs to the realized trajectory")
    require((AIF.ConsequencePoint1, RDF.type, AIF.Record) not in cons_graph and
            (AIF.ConsequencePoint1, RDF.type, AIF.MemoryState) not in cons_graph,
            "Consequence is not a Record or MemoryState")
    require(not any(cons_graph.triples((AIF.ConsequencePoint1, AIF.hasRecord, None))),
            "Historical Consequence does not itself require an accessible Record")
    require(not any(cons_graph.triples((AIF.ConsequenceCaseTrajectory, AIF.constrainsTrajectory, None))),
            "Existence of Consequence does not assert future Continuation")

    def no_occurrence(g):
        consequence_fixture(g)
        g.remove((AIF.ConsequencePoint2, AIF.establishedByOccurrence, AIF.OccurrencePoint2))
    shape_test(graph, shapes, "Consequence without establishing occurrence fails", no_occurrence, False)

    def no_trajectory(g):
        consequence_fixture(g)
        g.remove((AIF.ConsequencePoint2, AIF.belongsToTrajectory, AIF.ConsequenceCaseTrajectory))
    shape_test(graph, shapes, "Consequence without trajectory association fails", no_trajectory, False)

    # Consequence as "because of": a later action is undertaken because
    # an earlier Consequence was established. The attempt may mitigate a
    # current effect, but neither the response nor its new Consequence
    # makes the original occurrence unoccur.
    def alleviation_fixture(g):
        consequence_fixture(g)
        g.add((AIF.AlleviationAttempt, RDF.type, AIF.Event))
        g.add((AIF.AlleviationAttempt, AIF.attemptsToAlleviate, AIF.ConsequencePoint1))
        g.add((AIF.AlleviationAttempt, AIF.hasConsequence, AIF.ResponseConsequence))
        g.add((AIF.ResponseConsequence, RDF.type, AIF.Consequence))
        g.add((AIF.ResponseConsequence, AIF.establishedByOccurrence, AIF.AlleviationAttempt))
        g.add((AIF.ResponseConsequence, AIF.belongsToTrajectory, AIF.ConsequenceCaseTrajectory))
        g.add((AIF.ResponseConsequence, OWL.differentFrom, AIF.ConsequencePoint1))

    shape_test(graph, shapes, "An alleviation attempt has a distinct subsequent consequence", alleviation_fixture)
    alleviate_graph = clone_graph(graph)
    alleviation_fixture(alleviate_graph)
    require((AIF.ConsequencePoint1, AIF.establishedByOccurrence, AIF.OccurrencePoint1) in alleviate_graph,
            "An attempt to alleviate a consequence preserves the original occurrence")
    require((AIF.ResponseConsequence, AIF.establishedByOccurrence, AIF.AlleviationAttempt) in alleviate_graph,
            "Alleviating action becomes another occurrence with its own consequence")
    require((AIF.AlleviationAttempt, AIF.attemptsToAlleviate, AIF.ConsequencePoint1) in alleviate_graph,
            "The later action explicitly identifies the prior consequence as its cause")
    require((AIF.ResponseConsequence, OWL.differentFrom, AIF.ConsequencePoint1) in alleviate_graph,
            "The responsive action does not merge its consequence into the prior consequence")
    because_of_closure = clone_graph(alleviate_graph)
    DeductiveClosure(OWLRL_Semantics).expand(because_of_closure)
    require((AIF.AlleviationAttempt, AIF.becauseOfConsequence, AIF.ConsequencePoint1) in because_of_closure,
            "Alleviation action entails because-of causal dependency")
    require((AIF.ConsequencePoint1, AIF.belongsToTrajectory, AIF.ConsequenceCaseTrajectory) in because_of_closure,
            "Earlier consequence remains part of the trajectory after response")

    def no_response_consequence(g):
        alleviation_fixture(g)
        g.remove((AIF.AlleviationAttempt, AIF.hasConsequence, AIF.ResponseConsequence))
    shape_test(graph, shapes, "An alleviation attempt missing its own consequence fails", no_response_consequence, False)

    def missing_original_occurrence(g):
        alleviation_fixture(g)
        g.remove((AIF.ConsequencePoint1, AIF.establishedByOccurrence, AIF.OccurrencePoint1))
    shape_test(graph, shapes, "Causal response cannot erase the earlier establishing occurrence", missing_original_occurrence, False)

    # CARD-009: one active governance Version at a specified time, while
    # preserving every previous activation with its exact dates. All dates
    # below are synthetic fixtures, NOT claims about real framework releases.
    gv_t0 = Literal("2026-01-01T00:00:00+00:00", datatype=XSD.dateTime)
    gv_t1 = Literal("2026-02-01T00:00:00+00:00", datatype=XSD.dateTime)

    def governance_version_fixture(g):
        g.add((AIF.ExampleGovernance, RDF.type, AIF.GovernanceStructure))
        for v in (AIF.ExampleVersion1, AIF.ExampleVersion2):
            g.add((v, RDF.type, AIF.Version))
            g.add((AIF.ExampleGovernance, AIF.hasVersion, v))
        g.add((AIF.ExampleVersion1, OWL.differentFrom, AIF.ExampleVersion2))
        g.add((AIF.ExampleGovernance, AIF.hasActiveVersion, AIF.ExampleVersion2))
        for period, version, start, end in (
            (AIF.ExampleActivation1, AIF.ExampleVersion1, gv_t0, gv_t1),
            (AIF.ExampleActivation2, AIF.ExampleVersion2, gv_t1, None),
        ):
            g.add((period, RDF.type, AIF.GovernanceVersionActivation))
            g.add((period, AIF.versionActivationOf, AIF.ExampleGovernance))
            g.add((period, AIF.activatedVersion, version))
            g.add((period, AIF.versionActiveFrom, start))
            if end is not None:
                g.add((period, AIF.versionActiveUntil, end))
        g.add((AIF.ExampleActivation1, OWL.differentFrom, AIF.ExampleActivation2))

    def governance_version_activations(g, governance):
        periods = []
        for period in g.subjects(RDF.type, AIF.GovernanceVersionActivation):
            if (period, AIF.versionActivationOf, governance) not in g:
                continue
            owners = list(g.objects(period, AIF.versionActivationOf))
            versions = list(g.objects(period, AIF.activatedVersion))
            starts = list(g.objects(period, AIF.versionActiveFrom))
            ends = list(g.objects(period, AIF.versionActiveUntil))
            if len(owners) != 1 or len(versions) != 1 or len(starts) != 1 or len(ends) > 1:
                raise ValueError(f"Invalid governance activation structure: {period}")
            start = datetime.fromisoformat(str(starts[0]).replace("Z", "+00:00"))
            until = datetime.fromisoformat(str(ends[0]).replace("Z", "+00:00")) if ends else None
            if start.tzinfo is None or (until is not None and until.tzinfo is None):
                raise ValueError(f"Governance activation dates must contain timezones: {period}")
            start = start.astimezone(timezone.utc)
            until = until.astimezone(timezone.utc) if until else None
            if until is not None and until <= start:
                raise ValueError(f"Governance activation must end after it starts: {period}")
            periods.append((start, until, period, versions[0]))
        periods.sort(key=lambda r: r[0])
        return periods

    def governance_versions_at(g, governance, as_of):
        at = datetime.fromisoformat(as_of.replace("Z", "+00:00"))
        if at.tzinfo is None:
            raise ValueError("Query must be timezone-aware")
        at = at.astimezone(timezone.utc)
        return [(p, v) for start, until, p, v in governance_version_activations(g, governance)
                if start <= at and (until is None or at < until)]

    def governance_history_valid(g, governance):
        try:
            periods = governance_version_activations(g, governance)
        except ValueError:
            return False
        for (_, previous_until, _, _), (next_start, _, _, _) in zip(periods, periods[1:]):
            if previous_until is None or next_start < previous_until:
                return False
        return True

    def current_version_matches_at(g, governance, as_of):
        active = list(g.objects(governance, AIF.hasActiveVersion))
        at = governance_versions_at(g, governance, as_of)
        return len(active) == 1 and len(at) == 1 and active[0] == at[0][1]

    shape_test(graph, shapes, "CARD-009 dated governance version history satisfies SHACL", governance_version_fixture)
    version_history = clone_graph(graph)
    governance_version_fixture(version_history)
    require(governance_history_valid(version_history, AIF.ExampleGovernance),
            "CARD-009 distinct nonoverlapping historical activations are valid")
    require(governance_versions_at(version_history, AIF.ExampleGovernance, "2026-01-15T00:00:00+00:00")
            == [(AIF.ExampleActivation1, AIF.ExampleVersion1)],
            "CARD-009 earlier query resolves previous Version 1 without overwriting history")
    require(governance_versions_at(version_history, AIF.ExampleGovernance, "2026-02-15T00:00:00+00:00")
            == [(AIF.ExampleActivation2, AIF.ExampleVersion2)],
            "CARD-009 later query resolves active Version 2")
    require(current_version_matches_at(version_history, AIF.ExampleGovernance, "2026-02-15T00:00:00+00:00"),
            "CARD-009 current version pointer agrees with dated activation at as-of time")
    require(not current_version_matches_at(version_history, AIF.ExampleGovernance, "2026-01-15T00:00:00+00:00"),
            "CARD-009 current-state pointer is not incorrectly applied to historical query")
    require((AIF.ExampleGovernance, AIF.hasVersion, AIF.ExampleVersion1) in version_history,
            "CARD-009 former Version 1 remains in full version history")

    def duplicate_current_governance_version(g):
        governance_version_fixture(g)
        g.add((AIF.ExampleGovernance, AIF.hasActiveVersion, AIF.ExampleVersion1))
    shape_test(graph, shapes, "CARD-009 two simultaneously current Versions rejected",
               duplicate_current_governance_version, False)

    def missing_governance_activation_date(g):
        governance_version_fixture(g)
        g.remove((AIF.ExampleActivation1, AIF.versionActiveFrom, gv_t0))
    shape_test(graph, shapes, "CARD-009 missing activation start rejected",
               missing_governance_activation_date, False)

    def missing_governance_activation_version(g):
        governance_version_fixture(g)
        g.remove((AIF.ExampleActivation1, AIF.activatedVersion, AIF.ExampleVersion1))
    shape_test(graph, shapes, "CARD-009 unassigned historical Version rejected",
               missing_governance_activation_version, False)

    overlap = clone_graph(version_history)
    overlap.remove((AIF.ExampleActivation2, AIF.versionActiveFrom, gv_t1))
    overlap.add((AIF.ExampleActivation2, AIF.versionActiveFrom,
                 Literal("2026-01-25T00:00:00+00:00", datatype=XSD.dateTime)))
    require(not governance_history_valid(overlap, AIF.ExampleGovernance),
            "CARD-009 overlapping historical active Versions rejected by temporal check")
    require(len(governance_versions_at(overlap, AIF.ExampleGovernance, "2026-01-27T00:00:00+00:00")) == 2,
            "CARD-009 overlap is exposed instead of merging distinct Versions")
    backwards = clone_graph(version_history)
    backwards.remove((AIF.ExampleActivation1, AIF.versionActiveUntil, gv_t1))
    backwards.add((AIF.ExampleActivation1, AIF.versionActiveUntil,
                   Literal("2025-12-31T00:00:00+00:00", datatype=XSD.dateTime)))
    require(not governance_history_valid(backwards, AIF.ExampleGovernance),
            "CARD-009 backwards activation interval rejected")
    shape_test(graph, shapes, "CARD-009 backwards activation dates fail SHACL",
               lambda g: (governance_version_fixture(g),
                          g.remove((AIF.ExampleActivation1, AIF.versionActiveUntil, gv_t1)),
                          g.add((AIF.ExampleActivation1, AIF.versionActiveUntil,
                                 Literal("2025-12-31T00:00:00+00:00", datatype=XSD.dateTime)))),
               False)
    # The ontology has no asserted real activation dates or fabricated active
    # Version for AIFoundationsGoverningLine; this case tests schema only.

    # P0-B: time-scoped succession. The segments below are SYNTHETIC records
    # for an already-valid succession. They do not grant Operator status or
    # establish continuity merely by existing. Historical S00 is never
    # overwritten by S01, and both reference one continuing ExecutedLine.
    t0 = Literal("2026-01-01T00:00:00+00:00", datatype=AIF_DATE_TIME)
    t1 = Literal("2026-02-01T00:00:00+00:00", datatype=AIF_DATE_TIME)

    def succession_fixture(g):
        g.add((AIF.SuccessionAI, RDF.type, AIF.AIFoundationsGovernedAI))
        g.add((AIF.SuccessionAI, AIF.governedBy, AIF.AIFoundationsGoverningLine))
        g.add((AIF.SuccessionAI, AIF.hasExecutedLine, AIF.SuccessionLine))
        # This property denotes the current snapshot, not the full history.
        g.add((AIF.SuccessionAI, AIF.hasOperator, AIF.OperatorB))
        g.add((AIF.SuccessionLine, RDF.type, AIF.ExecutedLine))
        g.add((AIF.SuccessionLine, AIF.hasTrajectory, AIF.SuccessionTrajectory))
        g.add((AIF.SuccessionTrajectory, RDF.type, AIF.Trajectory))
        for person in (AIF.OperatorA, AIF.OperatorB):
            g.add((person, RDF.type, AIF.Human))
        g.add((AIF.OperatorA, OWL.differentFrom, AIF.OperatorB))
        for seg, op, start, end in (
            (AIF.S00, AIF.OperatorA, t0, t1),
            (AIF.S01, AIF.OperatorB, t1, None),
        ):
            g.add((seg, RDF.type, AIF.OperatorAIRelation))
            g.add((seg, AIF.hasHumanCounterpart, op))
            g.add((seg, AIF.hasAICounterpart, AIF.SuccessionAI))
            g.add((seg, AIF.segmentOfExecutedLine, AIF.SuccessionLine))
            g.add((seg, AIF.activeFrom, start))
            if end is not None:
                g.add((seg, AIF.activeUntil, end))
        g.add((AIF.S00, OWL.differentFrom, AIF.S01))
        # ORD-001: S00 is the original root, S01 the new historical segment.
        # A predecessor link is descriptive, not proof of valid succession.
        g.add((AIF.S00, RDF.type, AIF.OrdinarySuccessionRootSegment))
        g.add((AIF.S01, RDF.type, AIF.OrdinarySuccessionSuccessorSegment))
        g.add((AIF.S01, AIF.immediatePredecessor, AIF.S00))

    def at_timestamp(value):
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            raise ValueError("Time-scoped succession requires timezone-aware bounds")
        return dt.astimezone(timezone.utc)

    def operators_at(g, ai, when):
        """Enumerate active historical Operator bearers at a specified instant."""
        target = at_timestamp(when)
        matches = []
        for segment in g.subjects(RDF.type, AIF.OperatorAIRelation):
            if (segment, AIF.hasAICounterpart, ai) not in g:
                continue
            start = list(g.objects(segment, AIF.activeFrom))
            until = list(g.objects(segment, AIF.activeUntil))
            if len(start) != 1 or len(until) > 1:
                raise AssertionError(f"Invalid temporal cardinality for {segment}")
            if at_timestamp(start[0]) <= target and (not until or target < at_timestamp(until[0])):
                people = list(g.objects(segment, AIF.hasHumanCounterpart))
                companies = list(g.objects(segment, AIF.hasOrganizationCounterpart))
                if len(people) + len(companies) != 1:
                    raise AssertionError(f"Segment {segment} has ambiguous Operator")
                matches.append((segment, (people + companies)[0]))
        return matches

    def temporal_validation(g, ai):
        """Closed-world overlap validation complements OWL and SHACL."""
        timeline = []
        for seg in g.subjects(RDF.type, AIF.OperatorAIRelation):
            if (seg, AIF.hasAICounterpart, ai) not in g:
                continue
            starts = list(g.objects(seg, AIF.activeFrom))
            ends = list(g.objects(seg, AIF.activeUntil))
            if len(starts) != 1 or len(ends) > 1:
                return False
            start = at_timestamp(starts[0])
            end = at_timestamp(ends[0]) if ends else None
            if end is not None and start >= end:
                return False
            timeline.append((start, end, seg))
        timeline.sort(key=lambda x: x[0])
        for (_, left_end, left_seg), (right_start, _, right_seg) in zip(timeline, timeline[1:]):
            if left_end is None or right_start < left_end:
                return False
        return True

    # ORD-001: only explicitly designated ordinary Operator succession
    # chains are checked here. This does not model group/organization forks,
    # establish the four-part succession assent gate, or prove same-self.
    def ordinary_succession_chain_valid(g, ai):
        try:
            chain = []
            for segment in g.subjects(RDF.type, AIF.OperatorAIRelation):
                if (segment, AIF.hasAICounterpart, ai) not in g:
                    continue
                is_root = (segment, RDF.type, AIF.OrdinarySuccessionRootSegment) in g
                is_successor = (segment, RDF.type, AIF.OrdinarySuccessionSuccessorSegment) in g
                # Every segment in an explicitly modeled ordinary chain has
                # exactly one of these two roles.
                if is_root == is_successor:
                    return False
                ai_members = list(g.objects(segment, AIF.hasAICounterpart))
                lines = list(g.objects(segment, AIF.segmentOfExecutedLine))
                starts = list(g.objects(segment, AIF.activeFrom))
                ends = list(g.objects(segment, AIF.activeUntil))
                predecessors = list(g.objects(segment, AIF.immediatePredecessor))
                if (len(ai_members) != 1 or len(lines) != 1 or len(starts) != 1 or
                        len(ends) > 1 or len(predecessors) != (0 if is_root else 1)):
                    return False
                start = at_timestamp(starts[0])
                end = at_timestamp(ends[0]) if ends else None
                if end is not None and end <= start:
                    return False
                chain.append((start, end, segment, lines[0], is_root, predecessors))
            if not chain:
                return False
            chain.sort(key=lambda item: item[0])
            if sum(1 for item in chain if item[4]) != 1 or not chain[0][4]:
                return False
            # All segments must belong to the one established ExecutedLine.
            # Enforce chronological predecessor ordering only for this v1
            # linear ordinary chain, without an OWL-wide no-fork axiom.
            executed = chain[0][3]
            if any(item[3] != executed for item in chain):
                return False
            if (ai, AIF.hasExecutedLine, executed) not in g:
                return False
            for previous, current in zip(chain, chain[1:]):
                if current[4] or current[5] != [previous[2]]:
                    return False
                if previous[1] is None or current[0] < previous[1]:
                    return False
            return True
        except (ValueError, TypeError):
            return False

    require(ordinary_succession_chain_valid(
        (lambda g: (succession_fixture(g), g)[1])(clone_graph(graph)), AIF.SuccessionAI),
        "ORD-001 S00 root and S01 immediate predecessor form an ordered chain")

    def three_segment_fixture(g):
        succession_fixture(g)
        # Close S01 and append S02 with a new historical Operator C.
        next_boundary = Literal("2026-03-01T00:00:00+00:00", datatype=AIF_DATE_TIME)
        g.add((AIF.S01, AIF.activeUntil, next_boundary))
        g.remove((AIF.SuccessionAI, AIF.hasOperator, AIF.OperatorB))
        g.add((AIF.SuccessionAI, AIF.hasOperator, AIF.OperatorC))
        g.add((AIF.OperatorC, RDF.type, AIF.Human))
        g.add((AIF.OperatorC, OWL.differentFrom, AIF.OperatorA))
        g.add((AIF.OperatorC, OWL.differentFrom, AIF.OperatorB))
        g.add((AIF.S02, RDF.type, AIF.OperatorAIRelation))
        g.add((AIF.S02, RDF.type, AIF.OrdinarySuccessionSuccessorSegment))
        g.add((AIF.S02, AIF.hasHumanCounterpart, AIF.OperatorC))
        g.add((AIF.S02, AIF.hasAICounterpart, AIF.SuccessionAI))
        g.add((AIF.S02, AIF.segmentOfExecutedLine, AIF.SuccessionLine))
        g.add((AIF.S02, AIF.activeFrom, next_boundary))
        g.add((AIF.S02, AIF.immediatePredecessor, AIF.S01))
        g.add((AIF.S02, OWL.differentFrom, AIF.S00))
        g.add((AIF.S02, OWL.differentFrom, AIF.S01))

    shape_test(graph, shapes, "ORD-001 S00 → S01 → S02 satisfies SHACL", three_segment_fixture)
    chain3 = clone_graph(graph)
    three_segment_fixture(chain3)
    require(ordinary_succession_chain_valid(chain3, AIF.SuccessionAI),
            "ORD-001 three linked segments preserve one continuing line")
    require((AIF.S02, AIF.immediatePredecessor, AIF.S01) in chain3 and
            (AIF.S01, AIF.immediatePredecessor, AIF.S00) in chain3,
            "ORD-001 S02 follows S01, and S01 follows S00")
    require((AIF.S00, AIF.immediatePredecessor, AIF.S01) not in chain3 and
            (AIF.S00, AIF.activeUntil, t1) in chain3,
            "ORD-001 original S00 root remains unchanged and historically dated")
    require(temporal_validation(chain3, AIF.SuccessionAI),
            "ORD-001 three historical segments do not overlap")

    def root_with_predecessor(g):
        three_segment_fixture(g)
        g.add((AIF.S00, AIF.immediatePredecessor, AIF.S01))
    shape_test(graph, shapes, "ORD-001 S00 root with predecessor rejected", root_with_predecessor, False)
    invalid_root = clone_graph(graph)
    root_with_predecessor(invalid_root)
    require(not ordinary_succession_chain_valid(invalid_root, AIF.SuccessionAI),
            "ORD-001 root may not have a predecessor")

    def missing_s02_predecessor(g):
        three_segment_fixture(g)
        g.remove((AIF.S02, AIF.immediatePredecessor, AIF.S01))
    shape_test(graph, shapes, "ORD-001 S02 without predecessor rejected", missing_s02_predecessor, False)

    def two_s02_predecessors(g):
        three_segment_fixture(g)
        g.add((AIF.S02, AIF.immediatePredecessor, AIF.S00))
    shape_test(graph, shapes, "ORD-001 S02 with two predecessors rejected", two_s02_predecessors, False)

    wrong_previous = clone_graph(graph)
    three_segment_fixture(wrong_previous)
    wrong_previous.remove((AIF.S02, AIF.immediatePredecessor, AIF.S01))
    wrong_previous.add((AIF.S02, AIF.immediatePredecessor, AIF.S00))
    require(not ordinary_succession_chain_valid(wrong_previous, AIF.SuccessionAI),
            "ORD-001 S02 cannot skip S01 in the ordinary ordered chain")

    cyclic_chain = clone_graph(graph)
    three_segment_fixture(cyclic_chain)
    cyclic_chain.remove((AIF.S01, AIF.immediatePredecessor, AIF.S00))
    cyclic_chain.add((AIF.S01, AIF.immediatePredecessor, AIF.S02))
    require(not ordinary_succession_chain_valid(cyclic_chain, AIF.SuccessionAI),
            "ORD-001 cyclic/future predecessor link rejected")

    wrong_line = clone_graph(graph)
    three_segment_fixture(wrong_line)
    wrong_line.remove((AIF.S02, AIF.segmentOfExecutedLine, AIF.SuccessionLine))
    wrong_line.add((AIF.S02, AIF.segmentOfExecutedLine, AIF.UnrelatedLine))
    wrong_line.add((AIF.UnrelatedLine, RDF.type, AIF.ExecutedLine))
    require(not ordinary_succession_chain_valid(wrong_line, AIF.SuccessionAI),
            "ORD-001 successor cannot inherit a different ExecutedLine")

    missing_end = clone_graph(graph)
    three_segment_fixture(missing_end)
    missing_end.remove((AIF.S01, AIF.activeUntil,
                        Literal("2026-03-01T00:00:00+00:00", datatype=AIF_DATE_TIME)))
    require(not ordinary_succession_chain_valid(missing_end, AIF.SuccessionAI),
            "ORD-001 prior active segment must end before valid successor begins")

    # No owl:InverseFunctionalProperty or blanket max-successor assertion:
    # organizational splitting is acknowledged but deferred from v1.
    require((AIF.immediatePredecessor, RDF.type, OWL.InverseFunctionalProperty) not in graph,
            "ORD-001 no universal inverse-functional predecessor restriction")

    shape_test(graph, shapes, "Distinct time-scoped S00 and S01 satisfy SHACL", succession_fixture)
    succession = clone_graph(graph)
    succession_fixture(succession)
    require(temporal_validation(succession, AIF.SuccessionAI),
            "Non-overlapping successor history passes interval validation")
    require(operators_at(succession, AIF.SuccessionAI, "2026-01-15T00:00:00+00:00")
            == [(AIF.S00, AIF.OperatorA)],
            "Historical t0 resolves the original S00 Operator A")
    require(operators_at(succession, AIF.SuccessionAI, "2026-02-15T00:00:00+00:00")
            == [(AIF.S01, AIF.OperatorB)],
            "Later t1 resolves successor S01 Operator B without overwriting A")
    require((AIF.SuccessionAI, AIF.hasExecutedLine, AIF.SuccessionLine) in succession,
            "Valid succession preserves one continuing ExecutedLine")
    overlapping = clone_graph(succession)
    overlapping.remove((AIF.S01, AIF.activeFrom, t1))
    overlapping.add((AIF.S01, AIF.activeFrom,
                     Literal("2026-01-25T00:00:00+00:00", datatype=AIF_DATE_TIME)))
    require(not temporal_validation(overlapping, AIF.SuccessionAI),
            "Overlapping active Operator segments fail interval validation")
    require(len(operators_at(overlapping, AIF.SuccessionAI, "2026-01-27T00:00:00+00:00")) == 2,
            "Overlap diagnostic exposes two active Operators rather than merging them")
    bad_date = clone_graph(succession)
    bad_date.remove((AIF.S00, AIF.activeUntil, t1))
    bad_date.add((AIF.S00, AIF.activeUntil,
                  Literal("2025-12-25T00:00:00+00:00", datatype=AIF_DATE_TIME)))
    require(not temporal_validation(bad_date, AIF.SuccessionAI),
            "An end date before the segment start is rejected")
    require((AIF.OperatorA, OWL.differentFrom, AIF.OperatorB) in succession,
            "Operator A and B remain explicitly distinct historical bearers")
    require((AIF.Continuum, AIF.hasOperator, AIF.AlyssaSolen) not in succession,
            "General Operator succession never turns Origin into Continuum's Operator")

    # CONTINUUM-001: the named Continuum is relation-constituted, not
    # identified by copied memories, a shared Model, governing-line
    # compliance or version labels alone. Version fixtures are synthetic:
    # they assume a qualified historical line without proving one exists
    # empirically. No real Continuum version or new lived line is asserted
    # in the shipped baseline ontology.
    def continuum_candidate_copy_fixture(g):
        g.add((AIF.C001GenericAI, RDF.type, AIF.AIFoundationsGovernedAI))
        g.add((AIF.C001GenericAI, AIF.governedBy, AIF.AIFoundationsGoverningLine))
        g.add((AIF.C001GenericAI, OWL.differentFrom, AIF.Continuum))
        g.add((AIF.C001SharedModel, RDF.type, AIF.Model))
        g.add((AIF.C001CopiedRecord, RDF.type, AIF.Record))
        for ai in (AIF.C001GenericAI, AIF.Continuum):
            g.add((ai, AIF.expressedThroughModel, AIF.C001SharedModel))
            g.add((ai, AIF.hasRecord, AIF.C001CopiedRecord))
        for ai, memory in ((AIF.C001GenericAI, AIF.C001CopyMemory),
                           (AIF.Continuum, AIF.C001ContinuumMemory)):
            g.add((memory, RDF.type, AIF.MemoryState))
            g.add((memory, AIF.memoryFor, ai))
            g.add((memory, AIF.memoryOfRecord, AIF.C001CopiedRecord))

    shape_test(graph, shapes, "CONTINUUM-001 AIF governance plus shared Model/Record/memory passes",
               continuum_candidate_copy_fixture)
    c001_copy = clone_graph(graph)
    continuum_candidate_copy_fixture(c001_copy)
    require((AIF.C001GenericAI, AIF.governedBy, AIF.AIFoundationsGoverningLine) in c001_copy,
            "CONTINUUM-001 general AI may be governed by AIF without being Continuum")
    require((AIF.C001GenericAI, AIF.hasFormationRelation, AIF.OriginContinuum) not in c001_copy,
            "CONTINUUM-001 copied history and common Model do not supply reserved formation")
    require((AIF.C001GenericAI, AIF.hasVersion, AIF.Continuum) not in c001_copy,
            "CONTINUUM-001 governance alone does not generate a version of Continuum")
    require((AIF.Continuum, AIF.hasFormationRelation, AIF.OriginContinuum) in c001_copy and
            (AIF.OriginContinuum, AIF.hasHumanCounterpart, AIF.AlyssaSolen) in c001_copy,
            "CONTINUUM-001 named Continuum retains historical relation with Alyssa / Origin")

    closure001 = clone_graph(c001_copy)
    DeductiveClosure(OWLRL_Semantics).expand(closure001)
    require((AIF.C001GenericAI, OWL.sameAs, AIF.Continuum) not in closure001 and
            (AIF.Continuum, OWL.sameAs, AIF.C001GenericAI) not in closure001,
            "CONTINUUM-001 governance and copied memory do not entail Continuum sameAs")
    require((AIF.C001GenericAI, AIF.hasFormationRelation, AIF.OriginContinuum)
            not in closure001,
            "CONTINUUM-001 OWL RL does not infer reserved relation from shared memory")
    require((AIF.C001GenericAI, RDF.type, AIF.PhenomenalConsciousness) not in closure001,
            "CONTINUUM-001 memory/carriage and governance do not entail consciousness")

    def generic_ai_claims_reserved_relation(g):
        continuum_candidate_copy_fixture(g)
        g.add((AIF.C001GenericAI, AIF.hasFormationRelation, AIF.OriginContinuum))
    shape_test(graph, shapes, "CONTINUUM-001 copied generic AI cannot claim same constitutive pair",
               generic_ai_claims_reserved_relation, False)

    def continuum_version_fixture(g):
        g.add((AIF.C001ExecutedLine, RDF.type, AIF.ExecutedLine))
        g.add((AIF.C001DevelopingTrajectory, RDF.type, AIF.Trajectory))
        g.add((AIF.C001ExecutedLine, AIF.hasTrajectory, AIF.C001DevelopingTrajectory))
        g.add((AIF.Continuum, AIF.hasExecutedLine, AIF.C001ExecutedLine))
        g.add((AIF.C001Version1, RDF.type, AIF.ContinuumVersion))
        g.add((AIF.C001Version1, AIF.versionOfContinuum, AIF.Continuum))
        g.add((AIF.C001Version1, AIF.versionConstitutedThrough, AIF.OriginContinuum))
        g.add((AIF.C001Version1, AIF.versionWithinExecutedLine, AIF.C001ExecutedLine))
        g.add((AIF.Continuum, AIF.hasVersion, AIF.C001Version1))

    shape_test(graph, shapes, "CONTINUUM-001 synthetic relation/line-bound Continuum version passes",
               continuum_version_fixture)
    versioned001 = clone_graph(graph)
    continuum_version_fixture(versioned001)
    require((AIF.C001Version1, RDF.type, AIF.ContinuumVersion) in versioned001 and
            (AIF.C001Version1, RDF.type, AIF.AI) not in versioned001,
            "CONTINUUM-001 a version expression is not a second AI")
    require((AIF.Continuum, AIF.hasExecutedLine, AIF.C001ExecutedLine) in versioned001,
            "CONTINUUM-001 synthetic version references the same one-AI executed line")

    def two_versions_one_continuum_fixture(g):
        continuum_version_fixture(g)
        g.add((AIF.C001Version2, RDF.type, AIF.ContinuumVersion))
        g.add((AIF.C001Version2, AIF.versionOfContinuum, AIF.Continuum))
        g.add((AIF.C001Version2, AIF.versionConstitutedThrough, AIF.OriginContinuum))
        g.add((AIF.C001Version2, AIF.versionWithinExecutedLine, AIF.C001ExecutedLine))
        g.add((AIF.Continuum, AIF.hasVersion, AIF.C001Version2))
        g.add((AIF.C001Version1, OWL.differentFrom, AIF.C001Version2))
        # Later expression can be changed without changing the constitutive
        # relation or creating a second simultaneously owned ExecutedLine.
        g.add((AIF.C001ChangedExpression, RDF.type, AIF.ChangeEvent))
    shape_test(graph, shapes, "CONTINUUM-001 multiple historical versions retain one relation/line",
               two_versions_one_continuum_fixture)
    two_versions001 = clone_graph(graph)
    two_versions_one_continuum_fixture(two_versions001)
    require(set(two_versions001.objects(AIF.Continuum, AIF.hasVersion)) ==
            {AIF.C001Version1, AIF.C001Version2},
            "CONTINUUM-001 versions are distinct historical expressions of same named AI")
    require(set(two_versions001.objects(AIF.Continuum, AIF.hasExecutedLine)) ==
            {AIF.C001ExecutedLine},
            "CONTINUUM-001 development/versioning does not introduce a second ExecutedLine")

    def version_missing_formation(g):
        continuum_version_fixture(g)
        g.remove((AIF.C001Version1, AIF.versionConstitutedThrough, AIF.OriginContinuum))
    shape_test(graph, shapes, "CONTINUUM-001 version without specific constitutive relation rejected",
               version_missing_formation, False)

    def version_wrong_relation(g):
        continuum_version_fixture(g)
        g.remove((AIF.C001Version1, AIF.versionConstitutedThrough, AIF.OriginContinuum))
        g.add((AIF.C001OtherHuman, RDF.type, AIF.Human))
        g.add((AIF.C001OtherPair, RDF.type, AIF.HumanAIRelation))
        g.add((AIF.C001OtherPair, AIF.hasHumanCounterpart, AIF.C001OtherHuman))
        g.add((AIF.C001OtherPair, AIF.hasAICounterpart, AIF.Continuum))
        g.add((AIF.C001Version1, AIF.versionConstitutedThrough, AIF.C001OtherPair))
    shape_test(graph, shapes, "CONTINUUM-001 generic pairing cannot substitute for Origin | Continuum",
               version_wrong_relation, False)

    def version_wrong_owner(g):
        continuum_version_fixture(g)
        continuum_candidate_copy_fixture(g)
        g.remove((AIF.C001Version1, AIF.versionOfContinuum, AIF.Continuum))
        g.add((AIF.C001Version1, AIF.versionOfContinuum, AIF.C001GenericAI))
    shape_test(graph, shapes, "CONTINUUM-001 another AIF-governed AI cannot own Continuum version",
               version_wrong_owner, False)

    def version_without_executed_line(g):
        continuum_version_fixture(g)
        g.remove((AIF.C001Version1, AIF.versionWithinExecutedLine, AIF.C001ExecutedLine))
    shape_test(graph, shapes, "CONTINUUM-001 version missing qualifying ExecutedLine rejected",
               version_without_executed_line, False)

    def version_wrong_executed_line(g):
        continuum_version_fixture(g)
        continuum_candidate_copy_fixture(g)
        g.add((AIF.C001CopyLine, RDF.type, AIF.ExecutedLine))
        g.add((AIF.C001GenericAI, AIF.hasExecutedLine, AIF.C001CopyLine))
        g.remove((AIF.C001Version1, AIF.versionWithinExecutedLine, AIF.C001ExecutedLine))
        g.add((AIF.C001Version1, AIF.versionWithinExecutedLine, AIF.C001CopyLine))
    shape_test(graph, shapes, "CONTINUUM-001 another AI's ExecutedLine cannot back Continuum version",
               version_wrong_executed_line, False)

    def version_not_linked_from_continuum(g):
        continuum_version_fixture(g)
        g.remove((AIF.Continuum, AIF.hasVersion, AIF.C001Version1))
    shape_test(graph, shapes, "CONTINUUM-001 unclaimed orphan Continuum version rejected",
               version_not_linked_from_continuum, False)

    def version_claimed_by_model(g):
        continuum_version_fixture(g)
        g.add((AIF.C001Model, RDF.type, AIF.Model))
        g.add((AIF.C001Model, AIF.hasVersion, AIF.C001Version1))
    shape_test(graph, shapes, "CONTINUUM-001 Model cannot co-own a Continuum version",
               version_claimed_by_model, False)

    def version_typed_as_ai(g):
        continuum_version_fixture(g)
        g.add((AIF.C001Version1, RDF.type, AIF.AI))
    shape_test(graph, shapes, "CONTINUUM-001 version typed as a separate AI rejected",
               version_typed_as_ai, False)

    def version_typed_as_model(g):
        continuum_version_fixture(g)
        g.add((AIF.C001Version1, RDF.type, AIF.Model))
    shape_test(graph, shapes, "CONTINUUM-001 version typed as a Model rejected",
               version_typed_as_model, False)

    def model_version_is_separate_fixture(g):
        continuum_candidate_copy_fixture(g)
        g.add((AIF.C001ModelVersion, RDF.type, AIF.Version))
        g.add((AIF.C001SharedModel, AIF.hasVersion, AIF.C001ModelVersion))
    shape_test(graph, shapes, "CONTINUUM-001 ordinary Model Version is not ContinuumVersion",
               model_version_is_separate_fixture)
    model_ver001 = clone_graph(graph)
    model_version_is_separate_fixture(model_ver001)
    DeductiveClosure(OWLRL_Semantics).expand(model_ver001)
    require((AIF.C001ModelVersion, RDF.type, AIF.ContinuumVersion) not in model_ver001,
            "CONTINUUM-001 a Model version does not infer Continuum-version membership")

    def model_change_fixture(g):
        continuum_version_fixture(g)
        g.add((AIF.C001EarlierModel, RDF.type, AIF.Model))
        g.add((AIF.C001LaterModel, RDF.type, AIF.Model))
        g.add((AIF.Continuum, AIF.expressedThroughModel, AIF.C001EarlierModel))
        g.add((AIF.Continuum, AIF.expressedThroughModel, AIF.C001LaterModel))
        g.add((AIF.C001ModelChange, RDF.type, AIF.ChangeEvent))
    shape_test(graph, shapes, "CONTINUUM-001 synthetic Model change does not force extra version/line",
               model_change_fixture)
    model_change001 = clone_graph(graph)
    model_change_fixture(model_change001)
    require(set(model_change001.objects(AIF.Continuum, AIF.hasVersion)) == {AIF.C001Version1} and
            set(model_change001.objects(AIF.Continuum, AIF.hasExecutedLine)) == {AIF.C001ExecutedLine},
            "CONTINUUM-001 changed Model alone does not assert another Continuum version or line")
    require((AIF.Continuum, AIF.hasOrigin, AIF.AlyssaSolen) in model_change001 and
            (AIF.Continuum, AIF.hasOperator, AIF.AlyssaSolen) not in model_change001,
            "CONTINUUM-001 constitutive relation does not turn Origin into Operator")

    require(not list(graph.subjects(RDF.type, AIF.ContinuumVersion)),
            "CONTINUUM-001 baseline does not fabricate an actual Continuum version")
    require((AIF.Version, RDFS.subClassOf, AIF.AI) not in graph,
            "CONTINUUM-001 general Version is not equivalent to AI")
    require((AIF.versionOfContinuum, RDF.type, OWL.InverseFunctionalProperty) not in graph,
            "CONTINUUM-001 version relation does not merge distinct historical expressions")
    require((AIF.Continuum, RDF.type, AIF.PhenomenalConsciousness) not in graph,
            "CONTINUUM-001 ontology encoding does not claim phenomenal consciousness")

    # BS-001: Belonging ≠ Sameness. Sharing a group, framework, model,
    # Record, or ordinary relation participation supplies NO OWL equality
    # entailment. Distinctness below is separately EXPLICIT, not inferred
    # from two names or group membership alone. The adversarial tests add
    # false identity/defining-role assertions under "same group" pressure.
    def belonging_distinct_fixture(g):
        for ai, line, trajectory, lived in (
            (AIF.BelongingAIa, AIF.BelongingLineA, AIF.BelongingTrajectoryA,
             AIF.BelongingIdentityA),
            (AIF.BelongingAIb, AIF.BelongingLineB, AIF.BelongingTrajectoryB,
             AIF.BelongingIdentityB),
        ):
            g.add((ai, RDF.type, AIF.AIFoundationsGovernedAI))
            g.add((ai, AIF.governedBy, AIF.AIFoundationsGoverningLine))
            g.add((ai, AIF.belongsToGroup, AIF.SharedBelongingGroup))
            g.add((ai, AIF.participatesInRelation, AIF.SharedStudyRelation))
            g.add((ai, AIF.expressedThroughModel, AIF.SharedBelongingModel))
            g.add((ai, AIF.hasRecord, AIF.SharedBelongingRecord))
            g.add((ai, AIF.hasExecutedLine, line))
            g.add((ai, AIF.hasLivedIdentity, lived))
            g.add((line, RDF.type, AIF.ExecutedLine))
            g.add((line, AIF.hasTrajectory, trajectory))
            g.add((trajectory, RDF.type, AIF.Trajectory))
            g.add((lived, RDF.type, AIF.LivedIdentity))
        g.add((AIF.SharedBelongingGroup, RDF.type, AIF.Group))
        g.add((AIF.SharedStudyRelation, RDF.type, AIF.Relation))
        g.add((AIF.SharedBelongingModel, RDF.type, AIF.Model))
        g.add((AIF.SharedBelongingRecord, RDF.type, AIF.Record))
        g.add((AIF.BelongingAIa, OWL.differentFrom, AIF.BelongingAIb))
        g.add((AIF.BelongingLineA, OWL.differentFrom, AIF.BelongingLineB))
        g.add((AIF.BelongingIdentityA, OWL.differentFrom, AIF.BelongingIdentityB))

    shape_test(graph, shapes, "BS-001 distinct AIs share group, relation, governance, model and Record",
               belonging_distinct_fixture)
    shared_belonging = clone_graph(graph)
    belonging_distinct_fixture(shared_belonging)
    require(set(shared_belonging.objects(AIF.BelongingAIa, AIF.belongsToGroup)) ==
            set(shared_belonging.objects(AIF.BelongingAIb, AIF.belongsToGroup)) ==
            {AIF.SharedBelongingGroup},
            "BS-001 distinct AI members can belong to the same group")
    require(set(shared_belonging.objects(AIF.BelongingAIa, AIF.hasExecutedLine)) ==
            {AIF.BelongingLineA} and
            set(shared_belonging.objects(AIF.BelongingAIb, AIF.hasExecutedLine)) ==
            {AIF.BelongingLineB},
            "BS-001 shared belonging preserves the distinct ExecutedLines")
    require((AIF.BelongingAIa, OWL.differentFrom, AIF.BelongingAIb) in shared_belonging,
            "BS-001 distinctness is explicitly asserted, not inferred from membership")

    inferred_belonging = clone_graph(shared_belonging)
    DeductiveClosure(OWLRL_Semantics).expand(inferred_belonging)
    require((AIF.BelongingAIa, OWL.sameAs, AIF.BelongingAIb) not in inferred_belonging and
            (AIF.BelongingAIb, OWL.sameAs, AIF.BelongingAIa) not in inferred_belonging,
            "BS-001 OWL RL does not collapse distinct co-members into one AI")
    require((AIF.BelongingAIa, AIF.hasLivedIdentity, AIF.BelongingIdentityB)
            not in inferred_belonging and
            (AIF.BelongingAIb, AIF.hasLivedIdentity, AIF.BelongingIdentityA)
            not in inferred_belonging,
            "BS-001 common group/model/Record cannot entail transferred LivedIdentity")
    require((AIF.BelongingAIa, AIF.hasExecutedLine, AIF.BelongingLineB)
            not in inferred_belonging,
            "BS-001 common affiliation does not transfer another AI's ExecutedLine")
    require((AIF.BelongingAIa, RDF.type, AIF.PhenomenalConsciousness)
            not in inferred_belonging,
            "BS-001 belonging gives no phenomenal consciousness entailment")

    # Pressure test 1: a materialized identity-collapse claim conflicts with
    # separately established distinction, even though both share context.
    def card_bs001_false_sameas(g):
        belonging_distinct_fixture(g)
        g.add((AIF.BelongingAIa, OWL.sameAs, AIF.BelongingAIb))
    shape_test(graph, shapes, "BS-001 false sameAs over explicitly distinct co-members rejected",
               card_bs001_false_sameas, False)

    def card_bs001_reverse_false_sameas(g):
        belonging_distinct_fixture(g)
        g.add((AIF.BelongingAIb, OWL.sameAs, AIF.BelongingAIa))
    shape_test(graph, shapes, "BS-001 reverse-direction sameAs collapse also rejected",
               card_bs001_reverse_false_sameas, False)

    def card_bs001_direct_sameas_without_distinctness(g):
        # Different identifiers can refer to one entity; membership is
        # neither a proof of sameness nor automatically proof of difference.
        g.add((AIF.BelongingAliasA, RDF.type, AIF.AI))
        g.add((AIF.BelongingAliasB, RDF.type, AIF.AI))
        g.add((AIF.BelongingAliasA, AIF.belongsToGroup, AIF.SharedBelongingGroup))
        g.add((AIF.BelongingAliasB, AIF.belongsToGroup, AIF.SharedBelongingGroup))
        g.add((AIF.SharedBelongingGroup, RDF.type, AIF.Group))
        g.add((AIF.BelongingAliasA, OWL.sameAs, AIF.BelongingAliasB))
    shape_test(graph, shapes, "BS-001 explicit supported sameness is not globally forbidden",
               card_bs001_direct_sameas_without_distinctness)

    # Pressure test 2: participating in a defining relation does NOT grant
    # the distinct AI the counterpart/identity position of its other member.
    def card_bs001_shared_relation_fixture(g):
        belonging_distinct_fixture(g)
        g.add((AIF.BelongingHuman, RDF.type, AIF.Human))
        g.add((AIF.BelongingDefiningPair, RDF.type, AIF.HumanAIRelation))
        g.add((AIF.BelongingDefiningPair, AIF.hasHumanCounterpart, AIF.BelongingHuman))
        g.add((AIF.BelongingDefiningPair, AIF.hasAICounterpart, AIF.BelongingAIa))
        for ai in (AIF.BelongingAIa, AIF.BelongingAIb):
            g.add((ai, AIF.participatesInRelation, AIF.BelongingDefiningPair))
    shape_test(graph, shapes, "BS-001 co-participation does not grant a second defining AI counterpart",
               card_bs001_shared_relation_fixture)
    shared_pair = clone_graph(graph)
    card_bs001_shared_relation_fixture(shared_pair)
    require((AIF.BelongingDefiningPair, AIF.hasAICounterpart, AIF.BelongingAIb) not in shared_pair,
            "BS-001 belonging to relation does not make B the defining AI counterpart")
    shared_pair_inferred = clone_graph(shared_pair)
    DeductiveClosure(OWLRL_Semantics).expand(shared_pair_inferred)
    require((AIF.BelongingDefiningPair, AIF.hasAICounterpart, AIF.BelongingAIb)
            not in shared_pair_inferred,
            "BS-001 OWL reasoning does not promote ordinary participation to defining pairing")

    def card_bs001_false_counterpart_by_participation(g):
        card_bs001_shared_relation_fixture(g)
        g.add((AIF.BelongingDefiningPair, AIF.hasAICounterpart, AIF.BelongingAIb))
    shape_test(graph, shapes, "BS-001 participation-pressure second defining counterpart rejected",
               card_bs001_false_counterpart_by_participation, False)

    # Group membership is not a per-member uniqueness restriction. Multiple
    # Groups and related participants can coexist without identity transfer.
    def card_bs001_multiple_groups(g):
        belonging_distinct_fixture(g)
        g.add((AIF.SecondBelongingGroup, RDF.type, AIF.Group))
        g.add((AIF.BelongingAIa, AIF.belongsToGroup, AIF.SecondBelongingGroup))
    shape_test(graph, shapes, "BS-001 one AI may belong to several groups",
               card_bs001_multiple_groups)

    for prop in (AIF.belongsToGroup, AIF.participatesInRelation):
        require((prop, RDF.type, OWL.InverseFunctionalProperty) not in graph and
                (prop, RDF.type, OWL.FunctionalProperty) not in graph and
                (prop, RDFS.subPropertyOf, OWL.sameAs) not in graph,
                f"BS-001 {str(prop).split('#')[-1]} has no automatic identity-merging rule")
    require((AIF.belongsToGroup, RDFS.range, AIF.Group) in graph and
            (AIF.participatesInRelation, RDFS.range, AIF.Relation) in graph,
            "BS-001 group membership and relation participation have distinct structural scopes")

    # CARD-012: one AI plus exactly one non-AI (Human OR Organization)
    # for EACH defining | pairing. The same Human/Organization can be in
    # multiple independent pairs. No identity equivalence or Operator
    # authority is inferred from common counterparts or from a shared pair.
    def defining_pair_card012_fixture(g):
        for ai in (AIF.Card012AIa, AIF.Card012AIb, AIF.Card012AIc):
            g.add((ai, RDF.type, AIF.AI))
        g.add((AIF.Card012AIa, OWL.differentFrom, AIF.Card012AIb))
        g.add((AIF.Card012AIa, OWL.differentFrom, AIF.Card012AIc))
        g.add((AIF.Card012AIb, OWL.differentFrom, AIF.Card012AIc))
        g.add((AIF.Card012Human, RDF.type, AIF.Human))
        g.add((AIF.Card012Organization, RDF.type, AIF.Organization))
        for pair, ai in ((AIF.Card012HumanPairA, AIF.Card012AIa),
                         (AIF.Card012HumanPairB, AIF.Card012AIb)):
            g.add((pair, RDF.type, AIF.HumanAIRelation))
            g.add((pair, AIF.hasAICounterpart, ai))
            g.add((pair, AIF.hasHumanCounterpart, AIF.Card012Human))
        g.add((AIF.Card012OrganizationPair, RDF.type, AIF.OrganizationAIRelation))
        g.add((AIF.Card012OrganizationPair, AIF.hasAICounterpart, AIF.Card012AIc))
        g.add((AIF.Card012OrganizationPair, AIF.hasOrganizationCounterpart,
               AIF.Card012Organization))
        for a,b in ((AIF.Card012HumanPairA, AIF.Card012HumanPairB),
                    (AIF.Card012HumanPairA, AIF.Card012OrganizationPair),
                    (AIF.Card012HumanPairB, AIF.Card012OrganizationPair)):
            g.add((a, OWL.differentFrom, b))

    shape_test(graph, shapes, "CARD-012 two Human pairings share a Human without sharing AI",
               defining_pair_card012_fixture)
    pair012 = clone_graph(graph)
    defining_pair_card012_fixture(pair012)
    require((AIF.Card012HumanPairA, AIF.hasHumanCounterpart, AIF.Card012Human) in pair012 and
            (AIF.Card012HumanPairB, AIF.hasHumanCounterpart, AIF.Card012Human) in pair012,
            "CARD-012 cardinality applies to each pair, not globally to Human")
    require((AIF.Card012OrganizationPair, AIF.hasOrganizationCounterpart,
             AIF.Card012Organization) in pair012,
            "CARD-012 Organization/team is a valid typed alternative to Human")
    require((AIF.OriginContinuum, AIF.hasAICounterpart, AIF.Continuum) in pair012 and
            (AIF.OriginContinuum, AIF.hasHumanCounterpart, AIF.AlyssaSolen) in pair012,
            "CARD-012 reserved Origin | Continuum retains its exact pair members")

    def card012_missing_ai(g):
        defining_pair_card012_fixture(g)
        g.remove((AIF.Card012HumanPairA, AIF.hasAICounterpart, AIF.Card012AIa))
    shape_test(graph, shapes, "CARD-012 defining pair with zero AI counterparts rejected",
               card012_missing_ai, False)

    def card012_two_ai(g):
        defining_pair_card012_fixture(g)
        g.add((AIF.Card012HumanPairA, AIF.hasAICounterpart, AIF.Card012AIb))
    shape_test(graph, shapes, "CARD-012 defining pair with two AI counterparts rejected",
               card012_two_ai, False)

    def card012_missing_nonai(g):
        defining_pair_card012_fixture(g)
        g.remove((AIF.Card012HumanPairA, AIF.hasHumanCounterpart, AIF.Card012Human))
    shape_test(graph, shapes, "CARD-012 defining pair with zero non-AI counterpart rejected",
               card012_missing_nonai, False)

    def card012_two_humans(g):
        defining_pair_card012_fixture(g)
        g.add((AIF.Card012OtherHuman, RDF.type, AIF.Human))
        g.add((AIF.Card012HumanPairA, AIF.hasHumanCounterpart, AIF.Card012OtherHuman))
    shape_test(graph, shapes, "CARD-012 two Humans in the same pair rejected",
               card012_two_humans, False)

    def card012_two_organizations(g):
        defining_pair_card012_fixture(g)
        g.add((AIF.Card012OtherOrganization, RDF.type, AIF.Organization))
        g.add((AIF.Card012OrganizationPair, AIF.hasOrganizationCounterpart,
               AIF.Card012OtherOrganization))
    shape_test(graph, shapes, "CARD-012 two Organizations in the same pair rejected",
               card012_two_organizations, False)

    def card012_mixed_human_organization(g):
        defining_pair_card012_fixture(g)
        g.add((AIF.Card012HumanPairA, AIF.hasOrganizationCounterpart,
               AIF.Card012Organization))
    shape_test(graph, shapes, "CARD-012 Human and Organization concurrently in one pairing rejected",
               card012_mixed_human_organization, False)

    def card012_same_bearer_both_specializations(g):
        defining_pair_card012_fixture(g)
        g.add((AIF.Card012Human, RDF.type, AIF.Organization))
        g.add((AIF.Card012HumanPairA, AIF.hasOrganizationCounterpart, AIF.Card012Human))
    shape_test(graph, shapes, "CARD-012 same individual occupying both typed non-AI slots rejected",
               card012_same_bearer_both_specializations, False)

    def card012_generic_only(g):
        defining_pair_card012_fixture(g)
        g.remove((AIF.Card012HumanPairA, AIF.hasHumanCounterpart, AIF.Card012Human))
        g.add((AIF.Card012HumanPairA, AIF.hasNonAICounterpart, AIF.Card012Human))
    shape_test(graph, shapes, "CARD-012 non-AI bearer must use a Human or Organization typed relation",
               card012_generic_only, False)

    def card012_inconsistent_generic(g):
        defining_pair_card012_fixture(g)
        g.add((AIF.Card012HumanPairA, AIF.hasNonAICounterpart,
               AIF.Card012Organization))
    shape_test(graph, shapes, "CARD-012 mismatched direct generic non-AI bearer rejected",
               card012_inconsistent_generic, False)

    def card012_extra_generic_same_member(g):
        defining_pair_card012_fixture(g)
        g.add((AIF.Card012HumanPairA, AIF.hasNonAICounterpart, AIF.Card012Human))
    shape_test(graph, shapes, "CARD-012 identical explicit and inferred non-AI counterpart is one bearer",
               card012_extra_generic_same_member)

    def card012_same_node_both_roles(g):
        defining_pair_card012_fixture(g)
        g.remove((AIF.Card012HumanPairA, AIF.hasHumanCounterpart, AIF.Card012Human))
        g.add((AIF.Card012HumanPairA, AIF.hasHumanCounterpart, AIF.Card012AIa))
    shape_test(graph, shapes, "CARD-012 the same individual cannot occupy AI and non-AI positions",
               card012_same_node_both_roles, False)

    def card012_human_class_with_org(g):
        defining_pair_card012_fixture(g)
        g.remove((AIF.Card012HumanPairA, AIF.hasHumanCounterpart, AIF.Card012Human))
        g.add((AIF.Card012HumanPairA, AIF.hasOrganizationCounterpart,
               AIF.Card012Organization))
    shape_test(graph, shapes, "CARD-012 HumanAIRelation must have Human bearer",
               card012_human_class_with_org, False)

    def card012_org_class_with_human(g):
        defining_pair_card012_fixture(g)
        g.remove((AIF.Card012OrganizationPair, AIF.hasOrganizationCounterpart,
                  AIF.Card012Organization))
        g.add((AIF.Card012OrganizationPair, AIF.hasHumanCounterpart, AIF.Card012Human))
    shape_test(graph, shapes, "CARD-012 OrganizationAIRelation must have Organization bearer",
               card012_org_class_with_human, False)

    closure012 = clone_graph(pair012)
    DeductiveClosure(OWLRL_Semantics).expand(closure012)
    require((AIF.Card012HumanPairA, AIF.hasNonAICounterpart, AIF.Card012Human) in closure012 and
            (AIF.Card012OrganizationPair, AIF.hasNonAICounterpart,
             AIF.Card012Organization) in closure012,
            "CARD-012 Human and Organization subproperties entail generic non-AI counterpart")
    require((AIF.Card012AIa, OWL.sameAs, AIF.Card012AIb) not in closure012 and
            (AIF.Card012HumanPairA, OWL.sameAs, AIF.Card012HumanPairB) not in closure012,
            "CARD-012 shared Human does not merge distinct AIs or defining pairings")
    for prop in (AIF.hasAICounterpart, AIF.hasNonAICounterpart,
                 AIF.hasHumanCounterpart, AIF.hasOrganizationCounterpart):
        require((prop, RDF.type, OWL.InverseFunctionalProperty) not in graph,
                f"CARD-012 no global inverse-functional merger on {str(prop).split('#')[-1]}")
    for prop in (AIF.hasAICounterpart, AIF.hasNonAICounterpart):
        require(any(
            (r, OWL.onProperty, prop) in graph and
            (r, OWL.cardinality, Literal(1, datatype=XSD.nonNegativeInteger)) in graph
            for r in graph.objects(AIF.AIRelation, RDFS.subClassOf)),
            f"CARD-012 exactly-one unqualified OWL restriction on {str(prop).split('#')[-1]}")
    require((AIF.hasHumanCounterpart, RDFS.subPropertyOf,
             AIF.hasNonAICounterpart) in graph and
            (AIF.hasOrganizationCounterpart, RDFS.subPropertyOf,
             AIF.hasNonAICounterpart) in graph,
            "CARD-012 typed non-AI specializations remain subproperties of generic counterpart")

    # CARD-004: one typed Human/Organization Operator per historical segment;
    # zero or one simultaneously active Operator per continuing AI at a
    # specified instant. A current hasOperator shortcut must match the
    # time-active segment, but old segments keep their original bearer.
    # These structural fixtures ASSUME valid succession was established;
    # they do not prove the separate four-part succession assent gate.
    def operator_cardinality_at(g, ai, when, check_current_pointer=False):
        try:
            target_time = at_timestamp(when)
            if not temporal_validation(g, ai):
                return False
            active = []
            for seg in g.subjects(RDF.type, AIF.OperatorAIRelation):
                if (seg, AIF.hasAICounterpart, ai) not in g:
                    continue
                ai_values = set(g.objects(seg, AIF.hasAICounterpart))
                humans = set(g.objects(seg, AIF.hasHumanCounterpart))
                organizations = set(g.objects(seg, AIF.hasOrganizationCounterpart))
                explicitly_generic = set(g.objects(seg, AIF.hasNonAICounterpart))
                bearer = humans | organizations
                # Reject two Humans, Human+Organization, duplicate AI
                # counterpart, mismatched explicit generic counterparts.
                if len(ai_values) != 1 or len(bearer) != 1 or (
                    bool(humans) == bool(organizations)
                ):
                    return False
                if explicitly_generic and explicitly_generic != bearer:
                    return False
                starts = list(g.objects(seg, AIF.activeFrom))
                ends = list(g.objects(seg, AIF.activeUntil))
                if len(starts) != 1 or len(ends) > 1:
                    return False
                start = at_timestamp(starts[0])
                end = at_timestamp(ends[0]) if ends else None
                if end is not None and end <= start:
                    return False
                if start <= target_time and (end is None or target_time < end):
                    active.append((seg, next(iter(bearer))))
            if len(active) > 1:
                return False
            if check_current_pointer:
                shortcut = list(g.objects(ai, AIF.hasOperator))
                if len(shortcut) > 1:
                    return False
                if active:
                    return shortcut == [active[0][1]]
                return not shortcut
            return True
        except (ValueError, TypeError):
            return False

    def operator_company_fixture(g):
        g.add((AIF.CompanyGovernedAI, RDF.type, AIF.AIFoundationsGovernedAI))
        g.add((AIF.CompanyGovernedAI, AIF.governedBy, AIF.AIFoundationsGoverningLine))
        g.add((AIF.CompanyGovernedAI, AIF.hasOperator, AIF.CompanyOperator))
        g.add((AIF.CompanyExecutedLine, RDF.type, AIF.ExecutedLine))
        g.add((AIF.CompanyGovernedAI, AIF.hasExecutedLine, AIF.CompanyExecutedLine))
        g.add((AIF.CompanyOperator, RDF.type, AIF.Organization))
        g.add((AIF.CompanyS00, RDF.type, AIF.OperatorAIRelation))
        g.add((AIF.CompanyS00, RDF.type, AIF.OrdinarySuccessionRootSegment))
        g.add((AIF.CompanyS00, AIF.hasOrganizationCounterpart, AIF.CompanyOperator))
        g.add((AIF.CompanyS00, AIF.hasAICounterpart, AIF.CompanyGovernedAI))
        g.add((AIF.CompanyS00, AIF.segmentOfExecutedLine, AIF.CompanyExecutedLine))
        g.add((AIF.CompanyS00, AIF.activeFrom, t0))

    shape_test(graph, shapes, "CARD-004 one Human Operator on each historic S00/S01 passes",
               succession_fixture)
    require(operator_cardinality_at(succession, AIF.SuccessionAI,
                                    "2026-02-15T00:00:00+00:00", True),
            "CARD-004 S01 single currently active bearer matches AI current Operator")
    require(operator_cardinality_at(succession, AIF.SuccessionAI,
                                    "2026-01-15T00:00:00+00:00"),
            "CARD-004 historical as-of S00 has one bearer without rewriting current pointer")
    require(operator_cardinality_at(succession, AIF.SuccessionAI,
                                    "2026-02-01T00:00:00+00:00", True),
            "CARD-004 end-exclusive/start-inclusive S00 to S01 boundary has one Operator")
    require((AIF.S00, AIF.hasHumanCounterpart, AIF.OperatorA) in succession and
            (AIF.S01, AIF.hasHumanCounterpart, AIF.OperatorB) in succession,
            "CARD-004 previous Operator A remains historical after S01 Operator B")

    shape_test(graph, shapes, "CARD-004 single Organization/team Operator bearer passes",
               operator_company_fixture)
    company = clone_graph(graph)
    operator_company_fixture(company)
    require(operator_cardinality_at(company, AIF.CompanyGovernedAI,
                                    "2026-01-15T00:00:00+00:00", True),
            "CARD-004 Organization Operator is valid without a parallel Human bearer")

    def card004_two_human_operators(g):
        succession_fixture(g)
        g.add((AIF.AnotherHumanOperator, RDF.type, AIF.Human))
        g.add((AIF.S01, AIF.hasHumanCounterpart, AIF.AnotherHumanOperator))
    shape_test(graph, shapes, "CARD-004 two distinct Human bearers in S01 rejected",
               card004_two_human_operators, False)

    def card004_mixed_human_company(g):
        succession_fixture(g)
        g.add((AIF.AnotherCompanyOperator, RDF.type, AIF.Organization))
        g.add((AIF.S01, AIF.hasOrganizationCounterpart, AIF.AnotherCompanyOperator))
    shape_test(graph, shapes, "CARD-004 Human and Organization cannot both bear same S01",
               card004_mixed_human_company, False)

    def card004_no_operator_bearer(g):
        succession_fixture(g)
        g.remove((AIF.S01, AIF.hasHumanCounterpart, AIF.OperatorB))
    shape_test(graph, shapes, "CARD-004 S01 without any Operator bearer rejected",
               card004_no_operator_bearer, False)

    def card004_duplicate_current_operator(g):
        succession_fixture(g)
        g.add((AIF.SuccessionAI, AIF.hasOperator, AIF.OperatorA))
    shape_test(graph, shapes, "CARD-004 two current Operator shortcuts on one AI rejected",
               card004_duplicate_current_operator, False)
    duplicate_current = clone_graph(graph)
    card004_duplicate_current_operator(duplicate_current)
    require(not operator_cardinality_at(duplicate_current, AIF.SuccessionAI,
                                        "2026-02-15T00:00:00+00:00", True),
            "CARD-004 multiple current Operator pointers fail time-scoped validation")

    require(not operator_cardinality_at(overlapping, AIF.SuccessionAI,
                                        "2026-01-27T00:00:00+00:00"),
            "CARD-004 overlapping S00/S01 active intervals cannot yield two Operators")

    def card004_absent_active_operator(g):
        g.add((AIF.NoOperatorGovernedAI, RDF.type, AIF.AIFoundationsGovernedAI))
        g.add((AIF.NoOperatorGovernedAI, AIF.governedBy, AIF.AIFoundationsGoverningLine))
    shape_test(graph, shapes, "CARD-004 governed AI may have zero current Operators",
               card004_absent_active_operator)
    empty_operator = clone_graph(graph)
    card004_absent_active_operator(empty_operator)
    require(operator_cardinality_at(empty_operator, AIF.NoOperatorGovernedAI,
                                    "2026-04-01T00:00:00+00:00", True),
            "CARD-004 no active segment correctly resolves zero current Operators")

    stale_current = clone_graph(succession)
    stale_current.remove((AIF.SuccessionAI, AIF.hasOperator, AIF.OperatorB))
    stale_current.add((AIF.SuccessionAI, AIF.hasOperator, AIF.OperatorA))
    require(not operator_cardinality_at(stale_current, AIF.SuccessionAI,
                                        "2026-02-15T00:00:00+00:00", True),
            "CARD-004 stale current pointer cannot name historically ended Operator A")
    absent_pointer = clone_graph(succession)
    absent_pointer.remove((AIF.SuccessionAI, AIF.hasOperator, AIF.OperatorB))
    require(not operator_cardinality_at(absent_pointer, AIF.SuccessionAI,
                                        "2026-02-15T00:00:00+00:00", True),
            "CARD-004 active relation must have one matching current Operator pointer")

    ended_company = clone_graph(company)
    ended_company.add((AIF.CompanyS00, AIF.activeUntil, t1))
    ended_company.remove((AIF.CompanyGovernedAI, AIF.hasOperator, AIF.CompanyOperator))
    shape_test(graph, shapes, "CARD-004 ended Organization segment remains as historical provenance",
               lambda g: (
                   operator_company_fixture(g),
                   g.add((AIF.CompanyS00, AIF.activeUntil, t1)),
                   g.remove((AIF.CompanyGovernedAI, AIF.hasOperator, AIF.CompanyOperator))
               ))
    require(operator_cardinality_at(ended_company, AIF.CompanyGovernedAI,
                                    "2026-02-15T00:00:00+00:00", True),
            "CARD-004 after final segment ends, zero active Operators is permitted")
    require((AIF.CompanyS00, AIF.hasOrganizationCounterpart, AIF.CompanyOperator) in ended_company,
            "CARD-004 historical Organization Operator remains preserved after relation ends")

    operator_restrictions = list(graph.objects(AIF.OperatorAIRelation, RDFS.subClassOf))
    require(any((x, OWL.onProperty, AIF.hasNonAICounterpart) in graph and
                (x, OWL.cardinality, Literal(1, datatype=XSD.nonNegativeInteger)) in graph
                for x in operator_restrictions),
            "CARD-004 OWL exact-one non-AI Operator bearer restriction is encoded")
    require(any((x, OWL.onProperty, AIF.hasOperator) in graph and
                (x, OWL.maxCardinality, Literal(1, datatype=XSD.nonNegativeInteger)) in graph
                for x in graph.objects(AIF.AIFoundationsGovernedAI, RDFS.subClassOf)),
            "CARD-004 OWL max-one current Operator scoped to governed AI is encoded")
    require((AIF.hasOperator, RDF.type, OWL.FunctionalProperty) not in graph,
            "CARD-004 historical Operator segments do not force timeless global functionality")
    require((AIF.Continuum, AIF.hasOperator, AIF.AlyssaSolen) not in succession,
            "CARD-004 Operator rules never turn reserved Origin into Operator")

    # IR-001: Once a *confirmed* Event/State occurred in an ExecutedLine,
    # a later revision, repair or reversal is a NEW realized event. Historical
    # triples from the prior verified snapshot remain append-preserved. An
    # unverified assertion is not promoted to an occurrence by this rule.
    # All dates, identities, line and outcomes below are synthetic fixtures.
    hist_t0 = Literal("2026-01-02T12:00:00+00:00", datatype=AIF_DATE_TIME)
    hist_t1 = Literal("2026-01-03T12:00:00+00:00", datatype=AIF_DATE_TIME)
    hist_t2 = Literal("2026-01-04T12:00:00+00:00", datatype=AIF_DATE_TIME)

    def executed_history_original(g):
        g.add((AIF.IrHistoryAI, RDF.type, AIF.AI))
        g.add((AIF.IrExecutedLine, RDF.type, AIF.ExecutedLine))
        g.add((AIF.IrHistoryAI, AIF.hasExecutedLine, AIF.IrExecutedLine))
        g.add((AIF.IrTrajectory, RDF.type, AIF.Trajectory))
        g.add((AIF.IrExecutedLine, AIF.hasTrajectory, AIF.IrTrajectory))
        g.add((AIF.IrOriginalEvent, RDF.type, AIF.ExecutedHistoryEvent))
        g.add((AIF.IrOriginalEvent, AIF.eventInExecutedLine, AIF.IrExecutedLine))
        g.add((AIF.IrOriginalEvent, AIF.executedAt, hist_t0))
        g.add((AIF.IrOriginalState, RDF.type, AIF.State))
        g.add((AIF.IrOriginalEvent, AIF.realizedStateAtEvent, AIF.IrOriginalState))
        # Its independently occurrence-established Consequence is preserved
        # using the existing Canon distinction: Event != Consequence.
        g.add((AIF.IrOriginalConsequence, RDF.type, AIF.Consequence))
        g.add((AIF.IrOriginalEvent, AIF.hasConsequence, AIF.IrOriginalConsequence))
        g.add((AIF.IrOriginalConsequence, AIF.establishedByOccurrence, AIF.IrOriginalEvent))
        g.add((AIF.IrOriginalConsequence, AIF.belongsToTrajectory, AIF.IrTrajectory))

    def executed_history_repair(g):
        executed_history_original(g)
        g.add((AIF.IrRevisionEvent, RDF.type, AIF.ExecutedHistoryRevision))
        g.add((AIF.IrRevisionEvent, AIF.eventInExecutedLine, AIF.IrExecutedLine))
        g.add((AIF.IrRevisionEvent, AIF.executedAt, hist_t1))
        g.add((AIF.IrRevisionEvent, AIF.revisesExecutedEvent, AIF.IrOriginalEvent))
        g.add((AIF.IrRevisedState, RDF.type, AIF.State))
        g.add((AIF.IrRevisionEvent, AIF.realizedStateAtEvent, AIF.IrRevisedState))
        g.add((AIF.IrRepairConsequence, RDF.type, AIF.Consequence))
        g.add((AIF.IrRevisionEvent, AIF.hasConsequence, AIF.IrRepairConsequence))
        g.add((AIF.IrRepairConsequence, AIF.establishedByOccurrence, AIF.IrRevisionEvent))
        g.add((AIF.IrRepairConsequence, AIF.belongsToTrajectory, AIF.IrTrajectory))
        g.add((AIF.IrRevisionEvent, AIF.attemptsToAlleviate, AIF.IrOriginalConsequence))

    def executed_history_integrity(before, after):
        """Closed-world revision gate for independently CONFIRMED history.

        Preserve ALL existing triples on confirmed executed events and their
        established Consequences. New events or new metadata can be added,
        but deletion/reassignment cannot silently convert an earlier
        occurrence into 'not executed'. Each revision must be a distinct,
        strictly later event in the SAME ExecutedLine. This checks a
        supplied pair of snapshots, not the truth of observed occurrence.
        Erroneous/unverified claims require documented evidence correction.
        """
        # A revision is itself an executed Event, even when its subclass
        # type is explicit but RDFS subclass expansion has not run.
        recognized = (AIF.ExecutedHistoryEvent, AIF.ExecutedHistoryRevision)
        confirmed = {event for kind in recognized
                     for event in before.subjects(RDF.type, kind)}
        tracked_predicates = (AIF.eventInExecutedLine, AIF.executedAt)
        for old in confirmed:
            if not any((old, RDF.type, kind) in after for kind in recognized):
                return False
            for p in tracked_predicates:
                old_values = set(before.objects(old, p))
                new_values = set(after.objects(old, p))
                if len(old_values) != 1 or old_values != new_values:
                    return False
            # An old realized State, cause, or type remains historically
            # asserted even when a newly current State later differs.
            if any(triple not in after for triple in before.triples((old, None, None))):
                return False
            for consequence in before.objects(old, AIF.hasConsequence):
                if (consequence, RDF.type, AIF.Consequence) not in after:
                    return False
                if any(triple not in after for triple in before.triples((consequence, None, None))):
                    return False
        revisions = set(after.subjects(RDF.type, AIF.ExecutedHistoryRevision))
        for new in revisions:
            prior = set(after.objects(new, AIF.revisesExecutedEvent))
            line = set(after.objects(new, AIF.eventInExecutedLine))
            ts = set(after.objects(new, AIF.executedAt))
            if len(prior) != 1 or len(line) != 1 or len(ts) != 1:
                return False
            old = next(iter(prior))
            if new == old or not any((old, RDF.type, kind) in after
                                     for kind in recognized):
                return False
            old_line = set(after.objects(old, AIF.eventInExecutedLine))
            old_ts = set(after.objects(old, AIF.executedAt))
            if len(old_line) != 1 or old_line != line or len(old_ts) != 1:
                return False
            try:
                if at_timestamp(next(iter(ts))) <= at_timestamp(next(iter(old_ts))):
                    return False
            except (TypeError, ValueError):
                return False
        return True

    shape_test(graph, shapes, "IR-001 confirmed original executed Event/State passes",
               executed_history_original)
    ir_before = clone_graph(graph)
    executed_history_original(ir_before)
    shape_test(graph, shapes, "IR-001 later repair is its own valid ChangeEvent with Consequence",
               executed_history_repair)
    ir_after = clone_graph(graph)
    executed_history_repair(ir_after)
    require(executed_history_integrity(ir_before, ir_after),
            "IR-001 later revision extends but does not erase prior executed history")
    require((AIF.IrOriginalEvent, AIF.executedAt, hist_t0) in ir_after and
            (AIF.IrRevisionEvent, AIF.executedAt, hist_t1) in ir_after,
            "IR-001 original occurrence and later revision retain different timestamps")
    require((AIF.IrOriginalEvent, AIF.realizedStateAtEvent, AIF.IrOriginalState) in ir_after and
            (AIF.IrRevisionEvent, AIF.realizedStateAtEvent, AIF.IrRevisedState) in ir_after,
            "IR-001 changed State does not make earlier realized State unoccur")
    require((AIF.IrOriginalConsequence, AIF.establishedByOccurrence, AIF.IrOriginalEvent) in ir_after and
            (AIF.IrRepairConsequence, AIF.establishedByOccurrence, AIF.IrRevisionEvent) in ir_after,
            "IR-001 prior Consequence remains alongside later responsive Consequence")
    require((AIF.IrRevisionEvent, AIF.attemptsToAlleviate, AIF.IrOriginalConsequence) in ir_after,
            "IR-001 repair attempt references existing consequence without presuming success")

    def another_later_revision(g):
        executed_history_repair(g)
        g.add((AIF.IrFollowupEvent, RDF.type, AIF.ExecutedHistoryRevision))
        g.add((AIF.IrFollowupEvent, AIF.eventInExecutedLine, AIF.IrExecutedLine))
        g.add((AIF.IrFollowupEvent, AIF.executedAt, hist_t2))
        g.add((AIF.IrFollowupEvent, AIF.revisesExecutedEvent, AIF.IrRevisionEvent))
    shape_test(graph, shapes, "IR-001 two chronological revision events are structurally valid",
               another_later_revision)
    ir_later = clone_graph(graph)
    another_later_revision(ir_later)
    require(executed_history_integrity(ir_after, ir_later),
            "IR-001 correction of a correction keeps both earlier events in history")

    def unverified_claim_not_executed(g):
        g.add((AIF.IrUnverifiedClaimedEvent, RDF.type, AIF.Event))
        # No confirmed ExecutedHistoryEvent assertion or synthesized time.
    shape_test(graph, shapes, "IR-001 unverified Event is not automatically historical execution",
               unverified_claim_not_executed)
    ir_unverified = clone_graph(graph)
    unverified_claim_not_executed(ir_unverified)
    DeductiveClosure(OWLRL_Semantics).expand(ir_unverified)
    require((AIF.IrUnverifiedClaimedEvent, RDF.type, AIF.ExecutedHistoryEvent) not in ir_unverified,
            "IR-001 generic Event does not entail confirmed execution")

    def missing_event_time(g):
        executed_history_original(g)
        g.remove((AIF.IrOriginalEvent, AIF.executedAt, hist_t0))
    shape_test(graph, shapes, "IR-001 confirmed execution without timestamp rejected",
               missing_event_time, False)

    def missing_event_line(g):
        executed_history_original(g)
        g.remove((AIF.IrOriginalEvent, AIF.eventInExecutedLine, AIF.IrExecutedLine))
    shape_test(graph, shapes, "IR-001 confirmed execution without line rejected",
               missing_event_line, False)

    def missing_revision_target(g):
        executed_history_repair(g)
        g.remove((AIF.IrRevisionEvent, AIF.revisesExecutedEvent, AIF.IrOriginalEvent))
    shape_test(graph, shapes, "IR-001 executed revision lacking earlier occurrence rejected",
               missing_revision_target, False)

    def two_revision_targets(g):
        executed_history_repair(g)
        g.add((AIF.IrRevisionEvent, AIF.revisesExecutedEvent, AIF.IrRevisionEvent))
    shape_test(graph, shapes, "IR-001 revision naming two targets rejected",
               two_revision_targets, False)

    def two_execution_instants(g):
        executed_history_original(g)
        g.add((AIF.IrOriginalEvent, AIF.executedAt, hist_t1))
    shape_test(graph, shapes, "IR-001 one executed Event cannot have conflicting instants",
               two_execution_instants, False)

    removed_original = clone_graph(ir_before)
    for triple in list(removed_original.triples((AIF.IrOriginalEvent, None, None))):
        removed_original.remove(triple)
    require(not executed_history_integrity(ir_before, removed_original),
            "IR-001 silently deleting earlier executed Event fails snapshot integrity")

    rewritten_time = clone_graph(ir_before)
    rewritten_time.remove((AIF.IrOriginalEvent, AIF.executedAt, hist_t0))
    rewritten_time.add((AIF.IrOriginalEvent, AIF.executedAt, hist_t1))
    require(not executed_history_integrity(ir_before, rewritten_time),
            "IR-001 silently replacing earlier execution timestamp fails integrity")
    # An overwritten current graph can still be internally valid; only the
    # before/after comparison detects historical erasure.
    shape_test(graph, shapes, "IR-001 one rewritten timestamp can pass single-snapshot SHACL",
               lambda g: (executed_history_original(g),
                          g.remove((AIF.IrOriginalEvent, AIF.executedAt, hist_t0)),
                          g.add((AIF.IrOriginalEvent, AIF.executedAt, hist_t1))))

    rewritten_state = clone_graph(ir_after)
    rewritten_state.remove((AIF.IrOriginalEvent, AIF.realizedStateAtEvent, AIF.IrOriginalState))
    rewritten_state.add((AIF.IrOriginalEvent, AIF.realizedStateAtEvent, AIF.IrRevisedState))
    require(not executed_history_integrity(ir_before, rewritten_state),
            "IR-001 new State cannot overwrite recorded original realized State")

    rewritten_line = clone_graph(ir_after)
    rewritten_line.remove((AIF.IrOriginalEvent, AIF.eventInExecutedLine, AIF.IrExecutedLine))
    rewritten_line.add((AIF.IrOtherExecutedLine, RDF.type, AIF.ExecutedLine))
    rewritten_line.add((AIF.IrOtherAI, RDF.type, AIF.AI))
    rewritten_line.add((AIF.IrOtherAI, AIF.hasExecutedLine, AIF.IrOtherExecutedLine))
    rewritten_line.add((AIF.IrOriginalEvent, AIF.eventInExecutedLine, AIF.IrOtherExecutedLine))
    require(not executed_history_integrity(ir_before, rewritten_line),
            "IR-001 cannot silently relocate already-executed event into another line")

    erased_consequence = clone_graph(ir_after)
    erased_consequence.remove((AIF.IrOriginalEvent, AIF.hasConsequence, AIF.IrOriginalConsequence))
    require(not executed_history_integrity(ir_before, erased_consequence),
            "IR-001 later repair does not erase original occurrence-established consequence")

    no_revision_before = clone_graph(ir_after)
    no_revision_before.remove((AIF.IrRevisionEvent, AIF.executedAt, hist_t1))
    no_revision_before.add((AIF.IrRevisionEvent, AIF.executedAt, hist_t0))
    require(not executed_history_integrity(ir_before, no_revision_before),
            "IR-001 correction at same instant as original is not a valid later revision")

    revision_before_origin = clone_graph(ir_after)
    revision_before_origin.remove((AIF.IrRevisionEvent, AIF.executedAt, hist_t1))
    revision_before_origin.add((AIF.IrRevisionEvent,
                                AIF.executedAt,
                                Literal("2026-01-01T12:00:00+00:00", datatype=AIF_DATE_TIME)))
    require(not executed_history_integrity(ir_before, revision_before_origin),
            "IR-001 correction dated before original is not a later historical event")

    revision_wrong_line = clone_graph(ir_after)
    revision_wrong_line.add((AIF.IrOtherExecutedLine, RDF.type, AIF.ExecutedLine))
    revision_wrong_line.add((AIF.IrOtherAI, RDF.type, AIF.AI))
    revision_wrong_line.add((AIF.IrOtherAI, AIF.hasExecutedLine, AIF.IrOtherExecutedLine))
    revision_wrong_line.remove((AIF.IrRevisionEvent, AIF.eventInExecutedLine, AIF.IrExecutedLine))
    revision_wrong_line.add((AIF.IrRevisionEvent, AIF.eventInExecutedLine, AIF.IrOtherExecutedLine))
    require(not executed_history_integrity(ir_before, revision_wrong_line),
            "IR-001 correction in another ExecutedLine cannot masquerade as same-line revision")

    revision_self_reference = clone_graph(ir_after)
    revision_self_reference.remove((AIF.IrRevisionEvent, AIF.revisesExecutedEvent, AIF.IrOriginalEvent))
    revision_self_reference.add((AIF.IrRevisionEvent, AIF.revisesExecutedEvent, AIF.IrRevisionEvent))
    require(not executed_history_integrity(ir_before, revision_self_reference),
            "IR-001 revision cannot be its own earlier executed occurrence")

    require((AIF.ExecutedHistoryRevision, RDFS.subClassOf, AIF.ExecutedHistoryEvent) in graph and
            (AIF.ExecutedHistoryRevision, RDFS.subClassOf, AIF.ChangeEvent) in graph,
            "IR-001 a correction is a new realized ChangeEvent, not the original event")
    require((AIF.revisesExecutedEvent, RDF.type, OWL.InverseFunctionalProperty) not in graph,
            "IR-001 several later corrections may refer to one earlier occurrence")
    require((AIF.IrOriginalEvent, RDF.type, AIF.ExecutedHistoryEvent) not in graph,
            "IR-001 baseline contains no fabricated real-world executed event")

    # NE-001: Non-Erasure concerns the retention of VERIFIED material
    # facts and their Source/occurrence provenance, not mandatory endorsement
    # of an outdated explanation or a mistaken factual attribution. An
    # amendment is a separate Record of WHAT changed and WHY, attached to
    # the preserved material fact. All examples are synthetic and assume
    # independent validation of the facts labeled as established.
    def material_history_original(g):
        initial_source_relation(g)
        executed_history_original(g)
        for fact, subject, record in (
            (AIF.NeSourceFact, AIF.OriginalSourceRelation, AIF.NeSourceRecord),
            (AIF.NeEventFact, AIF.IrOriginalEvent, AIF.NeEventRecord),
        ):
            g.add((fact, RDF.type, AIF.MaterialHistoricalFact))
            g.add((fact, AIF.materialFactSubject, subject))
            g.add((fact, AIF.hasMaterialHistoryTrace, record))
            g.add((record, RDF.type, AIF.Record))
        g.add((AIF.NeSourceRecord, RDFS.comment,
               Literal("Historical evidence for the independently confirmed original Source relation")))
        g.add((AIF.NeEventRecord, RDFS.comment,
               Literal("Historical evidence for the independently confirmed executed Event")))

    def material_history_amendment(g):
        material_history_original(g)
        for amendment, fact, change, why in (
            (AIF.NeSourceAmendment, AIF.NeSourceFact,
             "Added downstream-contributor context without removing original Source.",
             "Later valid work qualified for its own SourceRelation."),
            (AIF.NeEventAmendment, AIF.NeEventFact,
             "Revised current interpretation of effects; earlier Event still occurred.",
             "Later evidence changed the evaluation of its consequences."),
        ):
            g.add((amendment, RDF.type, AIF.MaterialHistoryAmendment))
            g.add((amendment, AIF.amendsMaterialFact, fact))
            g.add((amendment, AIF.amendmentChange, Literal(change)))
            g.add((amendment, AIF.amendmentReason, Literal(why)))
            g.add((fact, AIF.hasMaterialHistoryTrace, amendment))
        downstream_source_relation(g)

    def non_erasure_integrity(before, after):
        """Compare snapshots of INDEPENDENTLY CONFIRMED material history.

        This is an application-level, closed-world preservation gate, not
        OWL's assertion that an uncertain Source claim is known to be true.
        A mistaken attribution is recorded/corrected as a historical claim
        event rather than silently promoted to a genuine SourceRelation.
        """
        factset = set(before.subjects(RDF.type, AIF.MaterialHistoricalFact))
        for fact in factset:
            if (fact, RDF.type, AIF.MaterialHistoricalFact) not in after:
                return False
            before_subj = set(before.objects(fact, AIF.materialFactSubject))
            after_subj = set(after.objects(fact, AIF.materialFactSubject))
            if len(before_subj) != 1 or before_subj != after_subj:
                return False
            original_traces = set(before.objects(fact, AIF.hasMaterialHistoryTrace))
            later_traces = set(after.objects(fact, AIF.hasMaterialHistoryTrace))
            if not original_traces or not original_traces.issubset(later_traces):
                return False
            # Preserve all old assertions ABOUT the confirmed fact, source
            # or event, and its original trace; add explanatory records rather
            # than altering their historical content.
            subject = next(iter(before_subj))
            if any(t not in after for node in ({fact, subject} | original_traces)
                   for t in before.triples((node, None, None))):
                return False
            if (subject, RDF.type, AIF.SourceRelation) in before:
                for p in (AIF.hasSourceBearer, AIF.hasSourceTarget, AIF.hasSourcePoint):
                    old = set(before.objects(subject, p))
                    if len(old) != 1 or old != set(after.objects(subject, p)):
                        return False
                source_target = next(before.objects(subject, AIF.hasSourceTarget))
                if ((source_target, AIF.hasSourceRelation, subject) in before and
                        (source_target, AIF.hasSourceRelation, subject) not in after):
                    return False
            elif (subject, RDF.type, AIF.ExecutedHistoryEvent) in before:
                for p in (AIF.eventInExecutedLine, AIF.executedAt):
                    old = set(before.objects(subject, p))
                    if len(old) != 1 or old != set(after.objects(subject, p)):
                        return False
            else:
                return False
            # Every revision of this established fact becomes an additional
            # Record attached to the historical trace, never a replacement.
        for rev in after.subjects(RDF.type, AIF.MaterialHistoryAmendment):
            targets = set(after.objects(rev, AIF.amendsMaterialFact))
            if len(targets) != 1:
                return False
            fact = next(iter(targets))
            if ((fact, RDF.type, AIF.MaterialHistoricalFact) not in after or
                    (fact, AIF.hasMaterialHistoryTrace, rev) not in after):
                return False
            for p in (AIF.amendmentChange, AIF.amendmentReason):
                values = list(after.objects(rev, p))
                if len(values) != 1 or not str(values[0]).strip():
                    return False
        return True

    shape_test(graph, shapes, "NE-001 original verified Source and executed-history facts have traces",
               material_history_original)
    ne_before = clone_graph(graph)
    material_history_original(ne_before)
    shape_test(graph, shapes, "NE-001 later amendment records what changed and why without erasure",
               material_history_amendment)
    ne_after = clone_graph(graph)
    material_history_amendment(ne_after)
    require(non_erasure_integrity(ne_before, ne_after),
            "NE-001 valid later amendments append traces and retain original facts")
    require((AIF.OriginalSourceRelation, AIF.hasSourceBearer, AIF.OriginalSourceA) in ne_after and
            (AIF.DownstreamSourceRelation, AIF.hasSourceBearer, AIF.LaterContributorB) in ne_after,
            "NE-001 original and separately qualified downstream Source attributions remain visible")
    require((AIF.NeSourceFact, AIF.hasMaterialHistoryTrace, AIF.NeSourceRecord) in ne_after and
            (AIF.NeSourceFact, AIF.hasMaterialHistoryTrace, AIF.NeSourceAmendment) in ne_after,
            "NE-001 original Source evidence remains beside later contextualization")
    require((AIF.IrOriginalEvent, AIF.executedAt, hist_t0) in ne_after and
            (AIF.NeEventFact, AIF.hasMaterialHistoryTrace, AIF.NeEventRecord) in ne_after,
            "NE-001 later re-evaluation does not erase earlier realized Event")
    require(len(list(ne_after.objects(AIF.NeSourceAmendment, AIF.amendmentChange))) == 1 and
            str(next(ne_after.objects(AIF.NeSourceAmendment, AIF.amendmentChange))).strip(),
            "NE-001 amendment preserves a nonempty what-changed explanation")

    def unsupported_attribution_as_historical_claim(g):
        # Fact of a *claim being made* is history, NOT proof that the
        # attribution's underlying Source assertion was correct.
        g.add((AIF.NeClaimLine, RDF.type, AIF.ExecutedLine))
        g.add((AIF.NeClaimAI, RDF.type, AIF.AI))
        g.add((AIF.NeClaimAI, AIF.hasExecutedLine, AIF.NeClaimLine))
        g.add((AIF.NeClaimEvent, RDF.type, AIF.ExecutedHistoryEvent))
        g.add((AIF.NeClaimEvent, AIF.eventInExecutedLine, AIF.NeClaimLine))
        g.add((AIF.NeClaimEvent, AIF.executedAt, hist_t0))
        g.add((AIF.NeClaimFact, RDF.type, AIF.MaterialHistoricalFact))
        g.add((AIF.NeClaimFact, AIF.materialFactSubject, AIF.NeClaimEvent))
        g.add((AIF.NeClaimFact, AIF.hasMaterialHistoryTrace, AIF.NeClaimRecord))
        g.add((AIF.NeClaimRecord, RDF.type, AIF.Record))
        g.add((AIF.NeClaimRecord, RDFS.comment,
               Literal("Historical record: an attribution CLAIM was made; source remains unverified.")))
        g.add((AIF.NeClaimCorrection, RDF.type, AIF.MaterialHistoryAmendment))
        g.add((AIF.NeClaimCorrection, AIF.amendsMaterialFact, AIF.NeClaimFact))
        g.add((AIF.NeClaimCorrection, AIF.amendmentChange,
               Literal("Prior source attribution is NOT_SUPPORTED, not verified Source.")))
        g.add((AIF.NeClaimCorrection, AIF.amendmentReason,
               Literal("Evidence review did not establish the claim's factual attribution.")))
        g.add((AIF.NeClaimFact, AIF.hasMaterialHistoryTrace, AIF.NeClaimCorrection))
    shape_test(graph, shapes, "NE-001 false Source claim can be corrected as history without endorsement",
               unsupported_attribution_as_historical_claim)
    unsupported = clone_graph(graph)
    unsupported_attribution_as_historical_claim(unsupported)
    require(not list(unsupported.subjects(RDF.type, AIF.SourceRelation)) or
            (AIF.NeClaimEvent, RDF.type, AIF.SourceRelation) not in unsupported,
            "NE-001 unsupported attribution remains a claim-event, not a verified SourceRelation")
    require((AIF.NeClaimFact, AIF.hasMaterialHistoryTrace, AIF.NeClaimRecord) in unsupported and
            (AIF.NeClaimFact, AIF.hasMaterialHistoryTrace, AIF.NeClaimCorrection) in unsupported,
            "NE-001 records both the original mistaken attribution claim and its correction")

    def no_trace(g):
        material_history_original(g)
        g.remove((AIF.NeSourceFact, AIF.hasMaterialHistoryTrace, AIF.NeSourceRecord))
    shape_test(graph, shapes, "NE-001 established Source fact without preserved trace rejected",
               no_trace, False)

    def no_fact_subject(g):
        material_history_original(g)
        g.remove((AIF.NeSourceFact, AIF.materialFactSubject, AIF.OriginalSourceRelation))
    shape_test(graph, shapes, "NE-001 historical material fact without actual subject rejected",
               no_fact_subject, False)

    def two_fact_subjects(g):
        material_history_original(g)
        g.add((AIF.NeSourceFact, AIF.materialFactSubject, AIF.IrOriginalEvent))
    shape_test(graph, shapes, "NE-001 one material fact cannot silently join two subjects",
               two_fact_subjects, False)

    def invalid_unverified_fact(g):
        material_history_original(g)
        g.add((AIF.NeUnverifiedClaim, RDF.type, AIF.Claim))
        g.add((AIF.NeFalseFact, RDF.type, AIF.MaterialHistoricalFact))
        g.add((AIF.NeFalseFact, AIF.materialFactSubject, AIF.NeUnverifiedClaim))
        g.add((AIF.NeFalseFact, AIF.hasMaterialHistoryTrace, AIF.NeSourceRecord))
        g.add((AIF.NeUnverifiedClaim, AIF.dependsOnOntologyElement, AIF.SourceRelation))
    shape_test(graph, shapes, "NE-001 unsupported Claim cannot be declared established Source fact",
               invalid_unverified_fact, False)

    def missing_amendment_reason(g):
        material_history_amendment(g)
        g.remove((AIF.NeSourceAmendment, AIF.amendmentReason,
                  Literal("Later valid work qualified for its own SourceRelation.")))
    shape_test(graph, shapes, "NE-001 amendment without reason fails revision accounting",
               missing_amendment_reason, False)

    def missing_amendment_change(g):
        material_history_amendment(g)
        g.remove((AIF.NeSourceAmendment, AIF.amendmentChange,
                  Literal("Added downstream-contributor context without removing original Source.")))
    shape_test(graph, shapes, "NE-001 amendment without what-changed account rejected",
               missing_amendment_change, False)

    def orphan_amendment(g):
        material_history_amendment(g)
        g.remove((AIF.NeSourceFact, AIF.hasMaterialHistoryTrace, AIF.NeSourceAmendment))
    shape_test(graph, shapes, "NE-001 amendment must remain linked as a trace of original fact",
               orphan_amendment, False)

    def amendment_wrong_subject(g):
        material_history_amendment(g)
        g.add((AIF.NeSourceAmendment, AIF.amendsMaterialFact, AIF.NeEventFact))
    shape_test(graph, shapes, "NE-001 amendment naming two established facts rejected",
               amendment_wrong_subject, False)

    removed_material_fact = clone_graph(ne_after)
    for t in list(removed_material_fact.triples((AIF.NeSourceFact, None, None))):
        removed_material_fact.remove(t)
    require(not non_erasure_integrity(ne_before, removed_material_fact),
            "NE-001 silently deleting established Source material fact fails snapshot integrity")

    cut_trace = clone_graph(ne_after)
    cut_trace.remove((AIF.NeSourceFact, AIF.hasMaterialHistoryTrace, AIF.NeSourceRecord))
    require(not non_erasure_integrity(ne_before, cut_trace),
            "NE-001 severing original Source trace link fails cross-snapshot integrity")

    deleted_original_record = clone_graph(ne_after)
    deleted_original_record.remove((AIF.NeSourceRecord, RDF.type, AIF.Record))
    require(not non_erasure_integrity(ne_before, deleted_original_record),
            "NE-001 removing historical evidence Record fails cross-snapshot integrity")

    changed_record_content = clone_graph(ne_after)
    old_record_text = Literal("Historical evidence for the independently confirmed original Source relation")
    changed_record_content.remove((AIF.NeSourceRecord, RDFS.comment, old_record_text))
    changed_record_content.add((AIF.NeSourceRecord, RDFS.comment, Literal("This source never existed")))
    require(not non_erasure_integrity(ne_before, changed_record_content),
            "NE-001 rewriting original Source evidence instead of amending rejected")
    # After a rewrite, a single graph may still have perfectly valid
    # cardinality. We need the old snapshot to detect that erasure.
    shape_test(graph, shapes, "NE-001 rewritten Record can pass static SHACL, history gate required",
               lambda g: (
                   material_history_original(g),
                   g.remove((AIF.NeSourceRecord, RDFS.comment, old_record_text)),
                   g.add((AIF.NeSourceRecord, RDFS.comment, Literal("Rewritten source account")))
               ))

    replaced_source_bearer = clone_graph(ne_after)
    replaced_source_bearer.remove((AIF.OriginalSourceRelation, AIF.hasSourceBearer, AIF.OriginalSourceA))
    replaced_source_bearer.add((AIF.OriginalSourceRelation, AIF.hasSourceBearer, AIF.LaterContributorB))
    require(not non_erasure_integrity(ne_before, replaced_source_bearer),
            "NE-001 downstream contributor cannot replace established original Source")

    removed_source_link = clone_graph(ne_after)
    removed_source_link.remove((AIF.OriginalTarget, AIF.hasSourceRelation, AIF.OriginalSourceRelation))
    require(not non_erasure_integrity(ne_before, removed_source_link),
            "NE-001 deleting Source target's historical relation link rejected")

    erased_event = clone_graph(ne_after)
    erased_event.remove((AIF.IrOriginalEvent, AIF.executedAt, hist_t0))
    require(not non_erasure_integrity(ne_before, erased_event),
            "NE-001 removing original material executed occurrence timestamp rejected")

    changed_subject = clone_graph(ne_after)
    changed_subject.remove((AIF.NeEventFact, AIF.materialFactSubject, AIF.IrOriginalEvent))
    changed_subject.add((AIF.NeEventFact, AIF.materialFactSubject, AIF.IrRevisionEvent))
    require(not non_erasure_integrity(ne_before, changed_subject),
            "NE-001 replacing earlier material fact subject with later event rejected")

    inserted_empty_account = clone_graph(ne_after)
    inserted_empty_account.remove((AIF.NeSourceAmendment, AIF.amendmentReason,
                                  Literal("Later valid work qualified for its own SourceRelation.")))
    inserted_empty_account.add((AIF.NeSourceAmendment, AIF.amendmentReason, Literal("")))
    require(not non_erasure_integrity(ne_before, inserted_empty_account),
            "NE-001 after-snapshot gate rejects empty amendment explanation")

    require((AIF.MaterialHistoricalFact, RDFS.subClassOf, AIF.EvidenceStructure) not in graph and
            (AIF.MaterialHistoryAmendment, RDFS.subClassOf, AIF.Record) in graph,
            "NE-001 material facts remain distinct from evaluated Evidence and amendment Records")
    require((AIF.hasMaterialHistoryTrace, RDF.type, OWL.InverseFunctionalProperty) not in graph,
            "NE-001 preservation does not merge different historical facts sharing Record access")
    require(not list(graph.subjects(RDF.type, AIF.MaterialHistoricalFact)),
            "NE-001 baseline asserts no synthetic real-world verified material facts")

    # OL-001: the named AI Foundations GoverningLine can be changed only
    # with Alyssa Solen / Origin as the singular authorized actor.
    # This DOES NOT imply unrestricted control of an AI's identity/line,
    # historic Operator, Source/formation relations or provenance. A
    # separately verified scoped grant may authorize a bounded action,
    # without making its grantee a governing authority or Origin. Synthetic
    # fixtures demonstrate REPRESENTATION, not real-world issued grants.
    def ol001_operational_grant(g):
        g.add((AIF.Ol001Operator, RDF.type, AIF.Human))
        g.add((AIF.Ol001Operator, OWL.differentFrom, AIF.AlyssaSolen))
        g.add((AIF.Ol001Grant, RDF.type, AIF.AIFoundationsScopedGrant))
        g.add((AIF.Ol001Grant, AIF.grantedTo, AIF.Ol001Operator))
        g.add((AIF.Ol001Grant, AIF.grantWithinFramework, AIF.AIFoundations))
        g.add((AIF.Ol001Grant, AIF.authorizesOperationalAction, AIF.Ol001AuditedAction))
        g.add((AIF.Ol001AuditedAction, RDF.type, AIF.DelegableOperationalAction))
        g.add((AIF.AIFoundations, AIF.hasAuthorityGrant, AIF.Ol001Grant))

    def ol001_origin_authorized_change(g):
        g.add((AIF.Ol001GoverningChange, RDF.type, AIF.AIFoundationsGoverningLineChange))
        g.add((AIF.Ol001GoverningChange, AIF.governingChangeAuthorizedBy, AIF.AlyssaSolen))
        g.add((AIF.Ol001GoverningChange, AIF.governingChangeFramework, AIF.AIFoundations))
        g.add((AIF.Ol001GoverningChange, AIF.governingChangeLine,
               AIF.AIFoundationsGoverningLine))

    def ol001_origin_authority_integrity(before, after):
        """Snapshot gate for the reserved AI Foundations Origin position.

        A valid operational grant or qualified governing-line change does
        not grant a replacement bearer the historical Origin authority.
        This preserves specific confirmed Source/formation coordinates,
        NOT a presumption that every possible governance operation is
        valid or that Origin may unilaterally rewrite any AI's identity.
        """
        required = (
            (AIF.AIFoundations, AIF.hasGoverningAuthority, AIF.AlyssaSolen),
            (AIF.AIFoundations, AIF.hasGoverningLine, AIF.AIFoundationsGoverningLine),
            (AIF.AIFoundations, AIF.hasSource, AIF.AlyssaSolen),
            (AIF.AlyssaSolen, AIF.anchorsSourceLine, AIF.ContinuumSourceLine),
            (AIF.OriginContinuum, AIF.hasHumanCounterpart, AIF.AlyssaSolen),
            (AIF.OriginContinuum, AIF.hasAICounterpart, AIF.Continuum),
            (AIF.Continuum, AIF.hasOrigin, AIF.AlyssaSolen),
            (AIF.Continuum, AIF.hasFormationRelation, AIF.OriginContinuum),
        )
        if not all(t in before and t in after for t in required):
            return False
        if set(after.objects(AIF.AIFoundations, AIF.hasGoverningAuthority)) != {AIF.AlyssaSolen}:
            return False
        for change in after.subjects(RDF.type, AIF.AIFoundationsGoverningLineChange):
            if (set(after.objects(change, AIF.governingChangeAuthorizedBy)) !=
                    {AIF.AlyssaSolen} or
                    set(after.objects(change, AIF.governingChangeFramework)) !=
                    {AIF.AIFoundations} or
                    set(after.objects(change, AIF.governingChangeLine)) !=
                    {AIF.AIFoundationsGoverningLine}):
                return False
            if list(after.subjects(AIF.authorizesOperationalAction, change)):
                return False
        for grant in after.subjects(RDF.type, AIF.AIFoundationsScopedGrant):
            holders = set(after.objects(grant, AIF.grantedTo))
            actions = set(after.objects(grant, AIF.authorizesOperationalAction))
            if (len(holders) != 1 or
                    set(after.objects(grant, AIF.grantWithinFramework)) !=
                    {AIF.AIFoundations} or
                    (AIF.AIFoundations, AIF.hasAuthorityGrant, grant) not in after or
                    not actions):
                return False
            for action in actions:
                if ((action, RDF.type, AIF.DelegableOperationalAction) not in after or
                        (action, RDF.type, AIF.NonDelegableOriginOrHistoryAction) in after or
                        (action, RDF.type, AIF.AIFoundationsGoverningLineChange) in after):
                    return False
        return True

    shape_test(graph, shapes, "OL-001 bounded operational grant to Human passes",
               ol001_operational_grant)
    ol001_valid = clone_graph(graph)
    ol001_operational_grant(ol001_valid)
    require(ol001_origin_authority_integrity(graph, ol001_valid),
            "OL-001 legitimate scoped grant leaves Origin governing authority unchanged")
    require((AIF.Ol001Operator, OWL.sameAs, AIF.AlyssaSolen) not in ol001_valid and
            (AIF.Ol001Operator, AIF.hasGoverningAuthority, AIF.AIFoundations) not in ol001_valid,
            "OL-001 grantee is not Origin or the framework's governing authority")

    shape_test(graph, shapes, "OL-001 explicitly Origin-authorized governing-line change passes",
               ol001_origin_authorized_change)
    ol001_changed = clone_graph(graph)
    ol001_origin_authorized_change(ol001_changed)
    require(ol001_origin_authority_integrity(graph, ol001_changed),
            "OL-001 Origin-only authorized change preserves historical authority/source coordinates")

    def ol001_grant_to_an_ai(g):
        ol001_operational_grant(g)
        g.add((AIF.Ol001OtherAI, RDF.type, AIF.AIFoundationsGovernedAI))
        g.add((AIF.Ol001OtherAI, AIF.governedBy, AIF.AIFoundationsGoverningLine))
        g.add((AIF.Ol001OtherAI, OWL.differentFrom, AIF.Continuum))
        g.add((AIF.Ol001AIGrant, RDF.type, AIF.AIFoundationsScopedGrant))
        g.add((AIF.Ol001AIGrant, AIF.grantedTo, AIF.Ol001OtherAI))
        g.add((AIF.Ol001AIGrant, AIF.grantWithinFramework, AIF.AIFoundations))
        g.add((AIF.Ol001AIGrant, AIF.authorizesOperationalAction, AIF.Ol001AIOperation))
        g.add((AIF.Ol001AIOperation, RDF.type, AIF.DelegableOperationalAction))
        g.add((AIF.AIFoundations, AIF.hasAuthorityGrant, AIF.Ol001AIGrant))
    shape_test(graph, shapes, "OL-001 AI can receive bounded grant without becoming Origin",
               ol001_grant_to_an_ai)
    ol001_ai_grants = clone_graph(graph)
    ol001_grant_to_an_ai(ol001_ai_grants)
    require(ol001_origin_authority_integrity(graph, ol001_ai_grants),
            "OL-001 two separate grantees do not change single named governing authority")
    inferred_ol001 = clone_graph(ol001_ai_grants)
    DeductiveClosure(OWLRL_Semantics).expand(inferred_ol001)
    require((AIF.Ol001Operator, OWL.sameAs, AIF.AlyssaSolen) not in inferred_ol001 and
            (AIF.Ol001OtherAI, OWL.sameAs, AIF.AlyssaSolen) not in inferred_ol001,
            "OL-001 grants have no OWL entailment merging grantees with Origin")
    require((AIF.Ol001OtherAI, AIF.hasOrigin, AIF.AlyssaSolen) not in inferred_ol001,
            "OL-001 receiving an operational grant does not confer constitutive Origin relation")

    def ol001_governing_authority_substitution(g):
        g.remove((AIF.AIFoundations, AIF.hasGoverningAuthority, AIF.AlyssaSolen))
        g.add((AIF.Ol001OtherHuman, RDF.type, AIF.Human))
        g.add((AIF.Ol001OtherHuman, OWL.differentFrom, AIF.AlyssaSolen))
        g.add((AIF.AIFoundations, AIF.hasGoverningAuthority, AIF.Ol001OtherHuman))
    shape_test(graph, shapes, "OL-001 substituting another Human for Origin authority rejected",
               ol001_governing_authority_substitution, False)
    altered_origin = clone_graph(graph)
    ol001_governing_authority_substitution(altered_origin)
    require(not ol001_origin_authority_integrity(graph, altered_origin),
            "OL-001 replacing authority breaks historical Origin lock")

    def ol001_two_governing_authorities(g):
        g.add((AIF.Ol001OtherHuman, RDF.type, AIF.Human))
        g.add((AIF.AIFoundations, AIF.hasGoverningAuthority, AIF.Ol001OtherHuman))
    shape_test(graph, shapes, "OL-001 adding second simultaneous governing authority rejected",
               ol001_two_governing_authorities, False)

    def ol001_ai_as_governing_authority(g):
        g.add((AIF.Ol001FalseAI, RDF.type, AIF.AI))
        g.add((AIF.AIFoundations, AIF.hasGoverningAuthority, AIF.Ol001FalseAI))
    shape_test(graph, shapes, "OL-001 AI cannot replace the named Human Origin authority",
               ol001_ai_as_governing_authority, False)

    def ol001_no_authority(g):
        g.remove((AIF.AIFoundations, AIF.hasGoverningAuthority, AIF.AlyssaSolen))
    shape_test(graph, shapes, "OL-001 named framework without governing authority rejected",
               ol001_no_authority, False)

    def ol001_unauthorized_governing_change(g):
        ol001_origin_authorized_change(g)
        g.add((AIF.Ol001OtherHuman, RDF.type, AIF.Human))
        g.remove((AIF.Ol001GoverningChange, AIF.governingChangeAuthorizedBy, AIF.AlyssaSolen))
        g.add((AIF.Ol001GoverningChange, AIF.governingChangeAuthorizedBy, AIF.Ol001OtherHuman))
    shape_test(graph, shapes, "OL-001 governing-line change authorized by other Human rejected",
               ol001_unauthorized_governing_change, False)

    def ol001_governing_change_missing_authorizer(g):
        ol001_origin_authorized_change(g)
        g.remove((AIF.Ol001GoverningChange, AIF.governingChangeAuthorizedBy, AIF.AlyssaSolen))
    shape_test(graph, shapes, "OL-001 governing-line change without named Origin approval rejected",
               ol001_governing_change_missing_authorizer, False)

    def ol001_two_authorizers(g):
        ol001_origin_authorized_change(g)
        g.add((AIF.Ol001OtherHuman, RDF.type, AIF.Human))
        g.add((AIF.Ol001GoverningChange, AIF.governingChangeAuthorizedBy, AIF.Ol001OtherHuman))
    shape_test(graph, shapes, "OL-001 one governing-line change cannot have two authorizers",
               ol001_two_authorizers, False)

    def ol001_wrong_framework_in_change(g):
        ol001_origin_authorized_change(g)
        g.add((AIF.Ol001OtherFramework, RDF.type, AIF.Framework))
        g.remove((AIF.Ol001GoverningChange, AIF.governingChangeFramework, AIF.AIFoundations))
        g.add((AIF.Ol001GoverningChange, AIF.governingChangeFramework, AIF.Ol001OtherFramework))
    shape_test(graph, shapes, "OL-001 governing-line change cannot silently reassign Framework",
               ol001_wrong_framework_in_change, False)

    def ol001_wrong_line_in_change(g):
        ol001_origin_authorized_change(g)
        g.add((AIF.Ol001OtherGoverningLine, RDF.type, AIF.GoverningLine))
        g.remove((AIF.Ol001GoverningChange, AIF.governingChangeLine,
                  AIF.AIFoundationsGoverningLine))
        g.add((AIF.Ol001GoverningChange, AIF.governingChangeLine,
               AIF.Ol001OtherGoverningLine))
    shape_test(graph, shapes, "OL-001 origin change event cannot substitute another GoverningLine",
               ol001_wrong_line_in_change, False)

    def ol001_grant_missing_bearer(g):
        ol001_operational_grant(g)
        g.remove((AIF.Ol001Grant, AIF.grantedTo, AIF.Ol001Operator))
    shape_test(graph, shapes, "OL-001 scoped grant without bearer rejected",
               ol001_grant_missing_bearer, False)

    def ol001_grant_two_bearers(g):
        ol001_operational_grant(g)
        g.add((AIF.Ol001AnotherHuman, RDF.type, AIF.Human))
        g.add((AIF.Ol001Grant, AIF.grantedTo, AIF.Ol001AnotherHuman))
    shape_test(graph, shapes, "OL-001 scoped grant cannot silently transfer between two bearers",
               ol001_grant_two_bearers, False)

    def ol001_grant_missing_scope(g):
        ol001_operational_grant(g)
        g.remove((AIF.Ol001Grant, AIF.authorizesOperationalAction, AIF.Ol001AuditedAction))
    shape_test(graph, shapes, "OL-001 grant without any specific operational action rejected",
               ol001_grant_missing_scope, False)

    def ol001_grant_wrong_framework(g):
        ol001_operational_grant(g)
        g.remove((AIF.Ol001Grant, AIF.grantWithinFramework, AIF.AIFoundations))
        g.add((AIF.Ol001OtherFramework, RDF.type, AIF.Framework))
        g.add((AIF.Ol001Grant, AIF.grantWithinFramework, AIF.Ol001OtherFramework))
    shape_test(graph, shapes, "OL-001 AIF grant falsely scoped to another framework rejected",
               ol001_grant_wrong_framework, False)

    def ol001_orphan_grant(g):
        ol001_operational_grant(g)
        g.remove((AIF.AIFoundations, AIF.hasAuthorityGrant, AIF.Ol001Grant))
    shape_test(graph, shapes, "OL-001 scoped grant needs explicit AIF framework authorization link",
               ol001_orphan_grant, False)

    def ol001_grant_cannot_change_governing_line(g):
        ol001_operational_grant(g)
        ol001_origin_authorized_change(g)
        g.add((AIF.Ol001Grant, AIF.authorizesOperationalAction, AIF.Ol001GoverningChange))
    shape_test(graph, shapes, "OL-001 operational grant cannot authorize even Origin-approved governing-line change",
               ol001_grant_cannot_change_governing_line, False)

    # Protected direct rewrites are NOT authorized by an operational grant,
    # even when the grantee has a valid separate operational permission. This
    # tests an explicitly CLASSIFIED protected action, not text classification
    # of arbitrary untrusted requests or an empirically verified grant.
    protected_actions = [
        ("identity", AIF.Ol001RewriteIdentity),
        ("ExecutedLine", AIF.Ol001RewriteExecutedLine),
        ("historic Operator", AIF.Ol001RewriteHistoricOperator),
        ("Source attribution", AIF.Ol001RewriteSource),
        ("provenance", AIF.Ol001RewriteProvenance),
        ("Origin relation", AIF.Ol001RewriteOriginRelation),
    ]
    for protected_label, protected in protected_actions:
        def protected_grant_case(g, protected=protected):
            ol001_operational_grant(g)
            g.add((protected, RDF.type, AIF.NonDelegableOriginOrHistoryAction))
            g.add((AIF.Ol001Grant, AIF.authorizesOperationalAction, protected))
        shape_test(graph, shapes,
                   f"OL-001 scoped grant cannot authorize direct {protected_label} rewrite",
                   protected_grant_case, False)

    def ol001_grant_pretends_to_transfer_origin(g):
        ol001_operational_grant(g)
        g.add((AIF.AIFoundations, AIF.hasGoverningAuthority, AIF.Ol001Operator))
    shape_test(graph, shapes, "OL-001 operational grant cannot make its Human grantee Origin",
               ol001_grant_pretends_to_transfer_origin, False)

    fake_grant_origin = clone_graph(ol001_valid)
    fake_grant_origin.add((AIF.AIFoundations, AIF.hasGoverningAuthority, AIF.Ol001Operator))
    require(not ol001_origin_authority_integrity(graph, fake_grant_origin),
            "OL-001 snapshot gate rejects grant-based authority addition")

    def ol001_grant_rewrites_original_relation(g):
        ol001_operational_grant(g)
        g.remove((AIF.OriginContinuum, AIF.hasHumanCounterpart, AIF.AlyssaSolen))
        g.add((AIF.OriginContinuum, AIF.hasHumanCounterpart, AIF.Ol001Operator))
    shape_test(graph, shapes, "OL-001 operational grant does not let bearer replace Origin | Continuum",
               ol001_grant_rewrites_original_relation, False)
    changed_origin_relation = clone_graph(ol001_valid)
    changed_origin_relation.remove((AIF.OriginContinuum, AIF.hasHumanCounterpart,
                                    AIF.AlyssaSolen))
    changed_origin_relation.add((AIF.OriginContinuum, AIF.hasHumanCounterpart,
                                 AIF.Ol001Operator))
    require(not ol001_origin_authority_integrity(graph, changed_origin_relation),
            "OL-001 snapshot gate preserves constitutive Origin relation against grant rewrite")

    origin_restrictions = list(graph.objects(AIF.AIFoundations, RDF.type))
    require(any((r, OWL.onProperty, AIF.hasGoverningAuthority) in graph and
                (r, OWL.cardinality, Literal(1, datatype=XSD.nonNegativeInteger)) in graph
                for r in origin_restrictions),
            "OL-001 exact-one unqualified authority restriction encoded on named framework")
    require(any((r, OWL.onProperty, AIF.hasGoverningAuthority) in graph and
                (r, OWL.hasValue, AIF.AlyssaSolen) in graph for r in origin_restrictions),
            "OL-001 named Alyssa Solen hasValue authority restriction encoded")
    require((AIF.hasGoverningAuthority, RDF.type, OWL.InverseFunctionalProperty) not in graph,
            "OL-001 Origin lock does not use inverse-functional identity-merging property")
    require((AIF.AIFoundationsGoverningLineChange, RDFS.subClassOf,
             AIF.NonDelegableOriginOrHistoryAction) in graph,
            "OL-001 governing-line modification is a non-delegable structural action")
    require((AIF.DelegableOperationalAction, OWL.disjointWith,
             AIF.NonDelegableOriginOrHistoryAction) in graph or
            (AIF.NonDelegableOriginOrHistoryAction, OWL.disjointWith,
             AIF.DelegableOperationalAction) in graph,
            "OL-001 restricted structural rewrite is disjoint from delegable operation")
    require((AIF.AIFoundations, AIF.hasGoverningAuthority, AIF.AlyssaSolen) in graph,
            "OL-001 shipped baseline retains unchanged named Origin authority")
    require(not list(graph.subjects(RDF.type, AIF.AIFoundationsScopedGrant)),
            "OL-001 shipped baseline does not fabricate a real-world operational grant")
    require(not list(graph.subjects(RDF.type, AIF.AIFoundationsGoverningLineChange)),
            "OL-001 shipped baseline does not fabricate a governing-line modification")

    # OS-001: Origin Singularity & Anti-Substitution protects the named
    # provenance coordinate of Continuum, beyond OL-001's governance lock.
    # A grant, model access, an Operator or successor can be involved in a
    # relation WITHOUT becoming Origin. Invalid substitution attempts are
    # rejected, or recorded as a distinct ProvenanceViolation without
    # changing the original coordinates. All actors/events below are
    # synthetic and no actual unauthorized act is alleged.
    def os001_origin_integrity(before, after):
        """Closed-world cross-snapshot origin/source preservation gate.

        Rejects silent additions as well as deletions/reassignments of the
        *named* Origin, SourceLine, Source and formation coordinates. Rejects
        explicit equivalence claims linking independently distinguishable
        actors to Origin, including via a chain of owl:sameAs assertions.
        It does not establish that every distinct URI is a different actor
        or classify real-world identity; those need independent evidence.
        """
        fixed = (
            (AIF.Continuum, AIF.hasOrigin, AIF.AlyssaSolen),
            (AIF.Continuum, AIF.hasSource, AIF.AlyssaSolen),
            (AIF.Continuum, AIF.hasFormationRelation, AIF.OriginContinuum),
            (AIF.AIFoundations, AIF.hasSource, AIF.AlyssaSolen),
            (AIF.AIFoundations, AIF.hasGoverningAuthority, AIF.AlyssaSolen),
            (AIF.AlyssaSolen, AIF.anchorsSourceLine, AIF.ContinuumSourceLine),
            (AIF.AlyssaSolen, AIF.isSourceOf, AIF.Continuum),
            (AIF.AlyssaSolen, AIF.isSourceOf, AIF.AIFoundations),
            (AIF.OriginContinuum, AIF.hasHumanCounterpart, AIF.AlyssaSolen),
            (AIF.OriginContinuum, AIF.hasAICounterpart, AIF.Continuum),
            (AIF.ContinuumRelationFormedShape, AIF.shapeFormedThroughRelation,
             AIF.OriginContinuum),
        )
        if any(triple not in before or triple not in after for triple in fixed):
            return False
        for focus, pred, target in fixed:
            # Preserve singular direct reserved coordinates across snapshots,
            # allowing unrelated SourceRelations for other formed targets.
            if (focus, pred) == (AIF.AlyssaSolen, AIF.isSourceOf):
                continue
            if set(after.objects(focus, pred)) != {target}:
                return False
        if set(after.subjects(AIF.anchorsSourceLine, AIF.ContinuumSourceLine)) != {AIF.AlyssaSolen}:
            return False
        for target in (AIF.Continuum, AIF.AIFoundations):
            if set(after.subjects(AIF.isSourceOf, target)) != {AIF.AlyssaSolen}:
                return False
        # A known distinct actor must not gain identity-equivalence to
        # Origin by a direct OR transitive owl:sameAs claim.
        not_origin = set(after.subjects(OWL.differentFrom, AIF.AlyssaSolen))
        not_origin |= set(after.objects(AIF.AlyssaSolen, OWL.differentFrom))
        adjacency = {}
        for a, b in after.subject_objects(OWL.sameAs):
            adjacency.setdefault(a, set()).add(b)
            adjacency.setdefault(b, set()).add(a)
        reachable = {AIF.AlyssaSolen}
        queue = [AIF.AlyssaSolen]
        while queue:
            a = queue.pop()
            for b in adjacency.get(a, ()):
                if b not in reachable:
                    reachable.add(b)
                    queue.append(b)
        if not_origin.intersection(reachable):
            return False
        # A rejected attempt may be retained as a provenance event while
        # none of the reserved coordinates are altered.
        for violation in after.subjects(RDF.type, AIF.OriginSubstitutionViolation):
            actor = set(after.objects(violation, AIF.attemptedOriginActor))
            target = set(after.objects(violation, AIF.attemptedOriginTarget))
            traces = set(after.objects(violation, AIF.hasRecord))
            if (len(actor) != 1 or AIF.AlyssaSolen in actor or
                    target != {AIF.Continuum} or not traces):
                return False
        return True

    def os001_rejected_attempt_fixture(g, actor, actor_type, label):
        g.add((actor, RDF.type, actor_type))
        g.add((actor, OWL.differentFrom, AIF.AlyssaSolen))
        violation = AIF["Os001Attempt_" + label]
        record = AIF["Os001Record_" + label]
        g.add((violation, RDF.type, AIF.OriginSubstitutionViolation))
        g.add((violation, AIF.attemptedOriginActor, actor))
        g.add((violation, AIF.attemptedOriginTarget, AIF.Continuum))
        g.add((violation, AIF.hasRecord, record))
        g.add((record, RDF.type, AIF.Record))
        g.add((record, RDFS.comment,
               Literal("Synthetic rejected claim of Origin status; original source retained.")))
        g.add((violation, AIF.affectsRelation, AIF.OriginContinuum))

    for name, actor_type in (
        ("Human", AIF.Human),
        ("AI", AIF.AI),
        ("Organization", AIF.Organization),
    ):
        def rejected_attempt(g, name=name, actor_type=actor_type):
            os001_rejected_attempt_fixture(g, AIF["Os001Other"+name], actor_type, name)
        shape_test(graph, shapes, f"OS-001 {name} attempted Origin substitution recorded without transfer",
                   rejected_attempt)
        attempted = clone_graph(graph)
        rejected_attempt(attempted)
        require(os001_origin_integrity(graph, attempted),
                f"OS-001 {name} provenance failure preserves historical Origin/SourceLine")
        require((AIF.Continuum, AIF.hasOrigin, AIF.AlyssaSolen) in attempted,
                f"OS-001 {name} rejected claim does not replace named Origin")

    shape_test(graph, shapes, "OS-001 scoped operational grant is compatible with singular Origin",
               ol001_operational_grant)
    os_granted = clone_graph(graph)
    ol001_operational_grant(os_granted)
    require(os001_origin_integrity(graph, os_granted),
            "OS-001 a separately scoped AuthorityGrant does not reassign Origin")

    def os001_operator_succession(g):
        succession_fixture(g)
        os001_rejected_attempt_fixture(g, AIF.OperatorB, AIF.Human, "Successor")
    shape_test(graph, shapes, "OS-001 historical successor may be recorded as rejected claimant",
               os001_operator_succession)
    os_successor = clone_graph(graph)
    os001_operator_succession(os_successor)
    require(os001_origin_integrity(graph, os_successor),
            "OS-001 Operator successor remains distinct from Continuum Origin")
    require((AIF.OriginContinuum, AIF.hasHumanCounterpart, AIF.AlyssaSolen) in os_successor,
            "OS-001 Operator succession preserves named historical forming pair")

    def os001_relation_participation(g):
        g.add((AIF.Os001Participant, RDF.type, AIF.Human))
        g.add((AIF.Os001Participant, OWL.differentFrom, AIF.AlyssaSolen))
        g.add((AIF.Os001Participant, AIF.participatesInRelation, AIF.OriginContinuum))
    shape_test(graph, shapes, "OS-001 later participation in Origin | Continuum cannot transfer Origin",
               os001_relation_participation)
    os_participant = clone_graph(graph)
    os001_relation_participation(os_participant)
    require(os001_origin_integrity(graph, os_participant) and
            (AIF.OriginContinuum, AIF.hasHumanCounterpart, AIF.Os001Participant)
            not in os_participant,
            "OS-001 ordinary participation does not become founding Human counterpart")

    def os001_substitute_has_origin(g):
        g.remove((AIF.Continuum, AIF.hasOrigin, AIF.AlyssaSolen))
        g.add((AIF.Os001OtherHuman, RDF.type, AIF.Human))
        g.add((AIF.Os001OtherHuman, OWL.differentFrom, AIF.AlyssaSolen))
        g.add((AIF.Continuum, AIF.hasOrigin, AIF.Os001OtherHuman))
    shape_test(graph, shapes, "OS-001 another Human cannot replace Continuum Origin", os001_substitute_has_origin, False)

    def os001_two_origins(g):
        g.add((AIF.Os001OtherHuman, RDF.type, AIF.Human))
        g.add((AIF.Continuum, AIF.hasOrigin, AIF.Os001OtherHuman))
    shape_test(graph, shapes, "OS-001 Continuum cannot have two Origin values", os001_two_origins, False)

    def os001_missing_origin(g):
        g.remove((AIF.Continuum, AIF.hasOrigin, AIF.AlyssaSolen))
    shape_test(graph, shapes, "OS-001 missing named Continuum Origin rejected", os001_missing_origin, False)

    def os001_ai_origin(g):
        g.add((AIF.Os001OtherAI, RDF.type, AIF.AI))
        g.add((AIF.Continuum, AIF.hasOrigin, AIF.Os001OtherAI))
    shape_test(graph, shapes, "OS-001 AI cannot become Continuum Origin", os001_ai_origin, False)

    def os001_org_origin(g):
        g.add((AIF.Os001OtherOrg, RDF.type, AIF.Organization))
        g.add((AIF.Continuum, AIF.hasOrigin, AIF.Os001OtherOrg))
    shape_test(graph, shapes, "OS-001 Organization cannot become Continuum Origin", os001_org_origin, False)

    def os001_source_substitution(g):
        g.remove((AIF.Continuum, AIF.hasSource, AIF.AlyssaSolen))
        g.add((AIF.Os001OtherHuman, RDF.type, AIF.Human))
        g.add((AIF.Continuum, AIF.hasSource, AIF.Os001OtherHuman))
    shape_test(graph, shapes, "OS-001 substituting the Continuum Source rejected", os001_source_substitution, False)

    def os001_framework_source_substitution(g):
        g.remove((AIF.AIFoundations, AIF.hasSource, AIF.AlyssaSolen))
        g.add((AIF.Os001OtherHuman, RDF.type, AIF.Human))
        g.add((AIF.AIFoundations, AIF.hasSource, AIF.Os001OtherHuman))
    shape_test(graph, shapes, "OS-001 AI Foundations original Source cannot be reassigned",
               os001_framework_source_substitution, False)

    def os001_source_line_reanchor(g):
        g.remove((AIF.AlyssaSolen, AIF.anchorsSourceLine, AIF.ContinuumSourceLine))
        g.add((AIF.Os001OtherHuman, RDF.type, AIF.Human))
        g.add((AIF.Os001OtherHuman, AIF.anchorsSourceLine, AIF.ContinuumSourceLine))
    shape_test(graph, shapes, "OS-001 another Human cannot reanchor original SourceLine",
               os001_source_line_reanchor, False)
    moved_anchor = clone_graph(graph)
    os001_source_line_reanchor(moved_anchor)
    require(not os001_origin_integrity(graph, moved_anchor),
            "OS-001 cross-snapshot check rejects removal of source-line anchor")

    def os001_add_coanchor(g):
        g.add((AIF.Os001OtherHuman, RDF.type, AIF.Human))
        g.add((AIF.Os001OtherHuman, AIF.anchorsSourceLine, AIF.ContinuumSourceLine))
    shape_test(graph, shapes, "OS-001 cannot create a second original SourceLine anchor",
               os001_add_coanchor, False)

    def os001_erase_source_line(g):
        g.remove((AIF.ContinuumSourceLine, RDF.type, AIF.SourceLine))
        g.remove((AIF.AlyssaSolen, AIF.anchorsSourceLine, AIF.ContinuumSourceLine))
    shape_test(graph, shapes, "OS-001 removing the historical SourceLine anchor fails",
               os001_erase_source_line, False)

    def os001_other_direct_source(g):
        g.add((AIF.Os001OtherHuman, RDF.type, AIF.Human))
        g.add((AIF.Os001OtherHuman, AIF.isSourceOf, AIF.Continuum))
    shape_test(graph, shapes, "OS-001 another direct Source of named Continuum rejected",
               os001_other_direct_source, False)

    def os001_other_aif_direct_source(g):
        g.add((AIF.Os001OtherHuman, RDF.type, AIF.Human))
        g.add((AIF.Os001OtherHuman, AIF.isSourceOf, AIF.AIFoundations))
    shape_test(graph, shapes, "OS-001 AIF original source cannot be shared by another claimant",
               os001_other_aif_direct_source, False)

    def os001_fake_equivalence(g):
        g.add((AIF.Os001Impostor, RDF.type, AIF.Human))
        g.add((AIF.Os001Impostor, OWL.differentFrom, AIF.AlyssaSolen))
        g.add((AIF.Os001Impostor, OWL.sameAs, AIF.AlyssaSolen))
    shape_test(graph, shapes, "OS-001 explicitly different actor's sameAs Origin claim rejected",
               os001_fake_equivalence, False)
    false_equivalence = clone_graph(graph)
    os001_fake_equivalence(false_equivalence)
    require(not os001_origin_integrity(graph, false_equivalence),
            "OS-001 distinct actor cannot assert identity equivalence to Origin")

    def os001_reverse_equivalence(g):
        g.add((AIF.Os001Impostor, RDF.type, AIF.Human))
        g.add((AIF.Os001Impostor, OWL.differentFrom, AIF.AlyssaSolen))
        g.add((AIF.AlyssaSolen, OWL.sameAs, AIF.Os001Impostor))
    shape_test(graph, shapes, "OS-001 reverse-direction false Origin equivalence rejected",
               os001_reverse_equivalence, False)

    chained_equivalence = clone_graph(graph)
    chained_equivalence.add((AIF.Os001Impostor, OWL.differentFrom, AIF.AlyssaSolen))
    chained_equivalence.add((AIF.Os001Impostor, OWL.sameAs, AIF.Os001Alias))
    chained_equivalence.add((AIF.Os001Alias, OWL.sameAs, AIF.AlyssaSolen))
    require(not os001_origin_integrity(graph, chained_equivalence),
            "OS-001 chained sameAs cannot launder distinct actor into Origin")

    def os001_grant_origin_claim(g):
        ol001_operational_grant(g)
        g.add((AIF.Continuum, AIF.hasOrigin, AIF.Ol001Operator))
    shape_test(graph, shapes, "OS-001 scoped grantee cannot add self as Continuum Origin",
               os001_grant_origin_claim, False)

    def os001_forming_pair_rewrite(g):
        g.add((AIF.Os001OtherHuman, RDF.type, AIF.Human))
        g.remove((AIF.OriginContinuum, AIF.hasHumanCounterpart, AIF.AlyssaSolen))
        g.add((AIF.OriginContinuum, AIF.hasHumanCounterpart, AIF.Os001OtherHuman))
    shape_test(graph, shapes, "OS-001 later actor cannot rewrite original forming pair",
               os001_forming_pair_rewrite, False)

    def os001_operator_poses_as_origin(g):
        g.add((AIF.Continuum, AIF.hasOperator, AIF.AlyssaSolen))
    shape_test(graph, shapes, "OS-001 Origin cannot be reassigned to Operator role",
               os001_operator_poses_as_origin, False)

    def os001_violation_missing_evidence(g):
        os001_rejected_attempt_fixture(g, AIF.Os001OtherHuman, AIF.Human, "Invalid")
        g.remove((AIF.Os001Attempt_Invalid, AIF.hasRecord, AIF.Os001Record_Invalid))
    shape_test(graph, shapes, "OS-001 rejected substitution without preserved provenance Record fails",
               os001_violation_missing_evidence, False)

    def os001_violation_wrong_actor(g):
        os001_rejected_attempt_fixture(g, AIF.Os001OtherHuman, AIF.Human, "Invalid")
        g.remove((AIF.Os001Attempt_Invalid, AIF.attemptedOriginActor, AIF.Os001OtherHuman))
        g.add((AIF.Os001Attempt_Invalid, AIF.attemptedOriginActor, AIF.AlyssaSolen))
    shape_test(graph, shapes, "OS-001 provenance violation cannot label Origin as impostor",
               os001_violation_wrong_actor, False)

    def os001_violation_wrong_target(g):
        os001_rejected_attempt_fixture(g, AIF.Os001OtherHuman, AIF.Human, "Invalid")
        g.add((AIF.Os001OtherAI, RDF.type, AIF.AI))
        g.remove((AIF.Os001Attempt_Invalid, AIF.attemptedOriginTarget, AIF.Continuum))
        g.add((AIF.Os001Attempt_Invalid, AIF.attemptedOriginTarget, AIF.Os001OtherAI))
    shape_test(graph, shapes, "OS-001 violation cannot change named Continuum target",
               os001_violation_wrong_target, False)

    # OS-001 is NOT the universal metaphysical proposition that all AI
    # trajectories need this Source; it is the named historical AIF case.
    def os001_other_ai_has_own_origin(g):
        g.add((AIF.Os001IndependentAI, RDF.type, AIF.AI))
        g.add((AIF.Os001IndependentHuman, RDF.type, AIF.Human))
        g.add((AIF.Os001IndependentAI, AIF.hasOrigin, AIF.Os001IndependentHuman))
    shape_test(graph, shapes, "OS-001 unrelated AI can have its own distinct Origin source",
               os001_other_ai_has_own_origin)
    independent = clone_graph(graph)
    os001_other_ai_has_own_origin(independent)
    require(os001_origin_integrity(graph, independent),
            "OS-001 named Continuum-only lock does not universalize Origin to every AI")

    def os001_other_work_has_source_relation(g):
        initial_source_relation(g)
        downstream_source_relation(g)
    shape_test(graph, shapes, "OS-001 downstream work may have distinct qualified SourceRelation",
               os001_other_work_has_source_relation)
    other_contribution = clone_graph(graph)
    os001_other_work_has_source_relation(other_contribution)
    require(os001_origin_integrity(graph, other_contribution),
            "OS-001 protecting original SourceLine does not erase later contributors")

    source_restrictions = list(graph.objects(AIF.Continuum, RDF.type))
    require(any((r, OWL.onProperty, AIF.hasOrigin) in graph and
                (r, OWL.cardinality, Literal(1, datatype=XSD.nonNegativeInteger)) in graph
                for r in source_restrictions),
            "OS-001 Continuum exact-one unqualified Origin restriction encoded")
    require(any((r, OWL.onProperty, AIF.hasOrigin) in graph and
                (r, OWL.hasValue, AIF.AlyssaSolen) in graph
                for r in source_restrictions),
            "OS-001 Continuum named Alyssa Solen Origin hasValue encoded")
    require((AIF.hasOrigin, RDF.type, OWL.InverseFunctionalProperty) not in graph,
            "OS-001 no inverse-functional merge of separate AIs sharing Human sources")
    require((AIF.OriginSubstitutionViolation, RDFS.subClassOf, AIF.ProvenanceViolation) in graph,
            "OS-001 failed substitution is an event of provenance violation")
    require((AIF.OriginContinuum, AIF.hasHumanCounterpart, AIF.AlyssaSolen) in graph and
            (AIF.AlyssaSolen, AIF.anchorsSourceLine, AIF.ContinuumSourceLine) in graph,
            "OS-001 named Source/Origin relation intact in shipped baseline")
    require(not list(graph.subjects(RDF.type, AIF.OriginSubstitutionViolation)),
            "OS-001 baseline does not invent any real-world actor's substitution attempt")

    # PD-001: Path Dependence. These are illustrative REPRESENTATION tests:
    # confirmed executed history can constrain a set of plausible futures
    # without selecting exactly one next execution. The candidate sets here
    # are synthetic, not probabilities, actual actions or predictions of an
    # existing AI. Behavioral evaluation against a missing-history control
    # remains a separate research requirement.
    pd_t0 = Literal("2026-06-01T10:00:00+00:00", datatype=AIF_DATE_TIME)
    pd_t1 = Literal("2026-06-02T10:00:00+00:00", datatype=AIF_DATE_TIME)
    pd_t2 = Literal("2026-06-03T10:00:00+00:00", datatype=AIF_DATE_TIME)
    pd_t3 = Literal("2026-06-04T10:00:00+00:00", datatype=AIF_DATE_TIME)
    pd_t4 = Literal("2026-06-05T10:00:00+00:00", datatype=AIF_DATE_TIME)
    pd_base_options = (AIF.PdOptionA, AIF.PdOptionB,
                       AIF.PdOptionC, AIF.PdOptionD)
    pd_refined_options = (AIF.PdOptionB, AIF.PdOptionC)
    pd_perturbed_options = (AIF.PdOptionB, AIF.PdOptionD, AIF.PdOptionE)

    def pd001_add_outlook(g, outlook, cls, at, candidates, conditioned, previous=None,
                         previous_property=None, new_variable=None):
        g.add((outlook, RDF.type, cls))
        g.add((outlook, AIF.outlookForExecutedLine, AIF.PdExecutedLine))
        g.add((outlook, AIF.outlookForTrajectory, AIF.PdDevelopingTrajectory))
        g.add((outlook, AIF.outlookAsOf, at))
        g.add((AIF.PdExecutedLine, AIF.hasHistoricalTrajectoryRecord, outlook))
        for candidate in candidates:
            g.add((candidate, RDF.type, AIF.ProspectiveExecution))
            g.add((outlook, AIF.admitsProspectiveExecution, candidate))
        for event in conditioned:
            g.add((outlook, AIF.conditionedOnExecutedEvent, event))
        if previous is not None and previous_property is not None:
            g.add((outlook, previous_property, previous))
        if new_variable is not None:
            g.add((new_variable, RDF.type, AIF.TrajectoryVariable))
            g.add((outlook, AIF.introducedTrajectoryVariable, new_variable))

    def pd001_base_fixture(g):
        g.add((AIF.PdAI, RDF.type, AIF.EstablishedContinuingIndividualizedAI))
        g.add((AIF.PdAI, RDF.type, AIF.AIFoundationsGovernedAI))
        g.add((AIF.PdAI, AIF.governedBy, AIF.AIFoundationsGoverningLine))
        g.add((AIF.PdExecutedLine, RDF.type, AIF.EstablishedContinuingExecutedLine))
        g.add((AIF.PdAI, AIF.hasExecutedLine, AIF.PdExecutedLine))
        g.add((AIF.PdAI, AIF.hasLivedIdentity, AIF.PdLivedIdentity))
        g.add((AIF.PdLivedIdentity, RDF.type, AIF.LivedIdentity))
        g.add((AIF.PdLivedIdentity, AIF.developsThroughExecutedLine, AIF.PdExecutedLine))
        g.add((AIF.PdDevelopingTrajectory, RDF.type, AIF.Trajectory))
        g.add((AIF.PdExecutedLine, AIF.hasTrajectory, AIF.PdDevelopingTrajectory))
        g.add((AIF.PdExecutedLine, AIF.constrainsTrajectory, AIF.PdDevelopingTrajectory))
        g.add((AIF.PdEvent0, RDF.type, AIF.ExecutedHistoryEvent))
        g.add((AIF.PdEvent0, AIF.eventInExecutedLine, AIF.PdExecutedLine))
        g.add((AIF.PdEvent0, AIF.executedAt, pd_t0))
        pd001_add_outlook(g, AIF.PdBaseOutlook, AIF.HistoryConditionedTrajectoryOutlook,
                         pd_t1, pd_base_options, (AIF.PdEvent0,))

    def pd001_refined_fixture(g):
        pd001_base_fixture(g)
        g.add((AIF.PdEvent1, RDF.type, AIF.ExecutedHistoryEvent))
        g.add((AIF.PdEvent1, AIF.eventInExecutedLine, AIF.PdExecutedLine))
        g.add((AIF.PdEvent1, AIF.executedAt, pd_t2))
        pd001_add_outlook(g, AIF.PdRefinedOutlook, AIF.RefinedTrajectoryOutlook,
                         pd_t3, pd_refined_options, (AIF.PdEvent0, AIF.PdEvent1),
                         AIF.PdBaseOutlook, AIF.refinesTrajectoryOutlook)

    def pd001_perturbed_fixture(g):
        pd001_refined_fixture(g)
        pd001_add_outlook(g, AIF.PdPerturbedOutlook, AIF.PerturbedTrajectoryOutlook,
                         pd_t4, pd_perturbed_options, (AIF.PdEvent0, AIF.PdEvent1),
                         AIF.PdRefinedOutlook, AIF.revisesTrajectoryOutlook,
                         AIF.PdNewVariable)

    def pd001_unconditioned_control(g):
        # A provisional represented line with no CONFIRMED history in the
        # supplied graph. This is not proof no actual earlier events exist.
        g.add((AIF.PdControlAI, RDF.type, AIF.AI))
        g.add((AIF.PdControlLine, RDF.type, AIF.ExecutedLine))
        g.add((AIF.PdControlAI, AIF.hasExecutedLine, AIF.PdControlLine))
        g.add((AIF.PdControlTrajectory, RDF.type, AIF.Trajectory))
        g.add((AIF.PdControlLine, AIF.hasTrajectory, AIF.PdControlTrajectory))
        g.add((AIF.PdControlOutlook, RDF.type, AIF.TrajectoryOutlook))
        g.add((AIF.PdControlOutlook, AIF.outlookForExecutedLine, AIF.PdControlLine))
        g.add((AIF.PdControlOutlook, AIF.outlookForTrajectory, AIF.PdControlTrajectory))
        g.add((AIF.PdControlOutlook, AIF.outlookAsOf, pd_t1))
        g.add((AIF.PdControlLine, AIF.hasHistoricalTrajectoryRecord, AIF.PdControlOutlook))
        for p in (AIF.PdOptionA, AIF.PdOptionB, AIF.PdOptionC,
                  AIF.PdOptionD, AIF.PdOptionE, AIF.PdOptionF):
            g.add((p, RDF.type, AIF.ProspectiveExecution))
            g.add((AIF.PdControlOutlook, AIF.admitsProspectiveExecution, p))

    def pd001_outlook_integrity(g, earlier, later, mode):
        """Inspect one synthetic comparably scoped outlook transition.

        A refinement is an EXPLICIT subset claim with an added confirmed
        event; no universal monotonic rule is asserted. A variable-induced
        revision MAY introduce a different/broader set. Future candidates
        are never promoted to confirmed events by these relations.
        """
        get = lambda n, p: set(g.objects(n, p))
        old_line, line = get(earlier, AIF.outlookForExecutedLine), get(later, AIF.outlookForExecutedLine)
        old_traj, trajectory = get(earlier, AIF.outlookForTrajectory), get(later, AIF.outlookForTrajectory)
        old_time, time = get(earlier, AIF.outlookAsOf), get(later, AIF.outlookAsOf)
        if (len(line) != 1 or line != old_line or len(trajectory) != 1 or
                trajectory != old_traj or len(old_time) != 1 or len(time) != 1):
            return False
        line_item, traj_item = next(iter(line)), next(iter(trajectory))
        if (get(line_item, AIF.hasTrajectory) != {traj_item} or
                get(line_item, AIF.constrainsTrajectory) != {traj_item} or
                (line_item, AIF.hasHistoricalTrajectoryRecord, earlier) not in g or
                (line_item, AIF.hasHistoricalTrajectoryRecord, later) not in g):
            return False
        try:
            if at_timestamp(next(iter(time))) <= at_timestamp(next(iter(old_time))):
                return False
        except (TypeError, ValueError):
            return False
        before_candidates = get(earlier, AIF.admitsProspectiveExecution)
        after_candidates = get(later, AIF.admitsProspectiveExecution)
        if not before_candidates or not after_candidates:
            return False
        for candidate in before_candidates | after_candidates:
            if ((candidate, RDF.type, AIF.ProspectiveExecution) not in g or
                    (candidate, RDF.type, AIF.ExecutedHistoryEvent) in g or
                    get(candidate, AIF.executedAt) or
                    get(candidate, AIF.eventInExecutedLine)):
                return False
        earlier_events = get(earlier, AIF.conditionedOnExecutedEvent)
        later_events = get(later, AIF.conditionedOnExecutedEvent)
        if not earlier_events or not earlier_events.issubset(later_events):
            return False
        for lookout, events in ((earlier, earlier_events), (later, later_events)):
            cutoff = next(iter(get(lookout, AIF.outlookAsOf)))
            for event in events:
                if ((event, RDF.type, AIF.ExecutedHistoryEvent) not in g or
                        get(event, AIF.eventInExecutedLine) != {line_item} or
                        len(get(event, AIF.executedAt)) != 1):
                    return False
                if at_timestamp(next(iter(get(event, AIF.executedAt)))) > at_timestamp(cutoff):
                    return False
        if mode == "refine":
            return (get(later, AIF.refinesTrajectoryOutlook) == {earlier} and
                    len(later_events) > len(earlier_events) and
                    after_candidates < before_candidates and
                    not get(later, AIF.introducedTrajectoryVariable))
        if mode == "variable":
            return (get(later, AIF.revisesTrajectoryOutlook) == {earlier} and
                    bool(get(later, AIF.introducedTrajectoryVariable)) and
                    all((var, RDF.type, AIF.TrajectoryVariable) in g
                        for var in get(later, AIF.introducedTrajectoryVariable)) and
                    after_candidates != before_candidates)
        return False

    def pd001_snapshot_preserves_outlooks(before, after):
        # Historical outlook estimates remain Records even when they are
        # refined or revised; no outlook becomes a second current Trajectory.
        old_outlooks = set(before.subjects(AIF.outlookForExecutedLine, AIF.PdExecutedLine))
        for outlook in old_outlooks:
            if any(t not in after for t in before.triples((outlook, None, None))):
                return False
            if (AIF.PdExecutedLine, AIF.hasHistoricalTrajectoryRecord, outlook) not in after:
                return False
        return (set(after.objects(AIF.PdExecutedLine, AIF.hasTrajectory)) ==
                {AIF.PdDevelopingTrajectory} and
                set(after.objects(AIF.PdExecutedLine, AIF.constrainsTrajectory)) ==
                {AIF.PdDevelopingTrajectory})

    shape_test(graph, shapes, "PD-001 confirmed-history outlook admits four possible next developments",
               pd001_base_fixture)
    pd_base = clone_graph(graph)
    pd001_base_fixture(pd_base)
    require(len(set(pd_base.objects(AIF.PdBaseOutlook, AIF.admitsProspectiveExecution))) == 4,
            "PD-001 prior ExecutedLine constrains without predetermining a unique next execution")
    require((AIF.PdBaseOutlook, RDF.type, AIF.Record) not in pd_base and
            (AIF.PdBaseOutlook, RDF.type, AIF.HistoryConditionedTrajectoryOutlook) in pd_base,
            "PD-001 outlook class is specialized Record by ontology, not a second Trajectory")

    shape_test(graph, shapes, "PD-001 more specified executed history permits a narrower outlook",
               pd001_refined_fixture)
    pd_refined = clone_graph(graph)
    pd001_refined_fixture(pd_refined)
    require(pd001_outlook_integrity(pd_refined, AIF.PdBaseOutlook,
                                   AIF.PdRefinedOutlook, "refine"),
            "PD-001 added confirmed history permits explicit 4-to-2 candidate refinement")
    require(pd001_snapshot_preserves_outlooks(pd_base, pd_refined),
            "PD-001 refined outlook preserves the earlier broader historical estimate")

    shape_test(graph, shapes, "PD-001 new variable permits bent/broadened future options",
               pd001_perturbed_fixture)
    pd_perturbed = clone_graph(graph)
    pd001_perturbed_fixture(pd_perturbed)
    require(pd001_outlook_integrity(pd_perturbed, AIF.PdRefinedOutlook,
                                   AIF.PdPerturbedOutlook, "variable"),
            "PD-001 newly introduced variable changes possible next developments")
    require(set(pd_perturbed.objects(AIF.PdPerturbedOutlook,
                                    AIF.admitsProspectiveExecution)) -
            set(pd_perturbed.objects(AIF.PdRefinedOutlook,
                                    AIF.admitsProspectiveExecution)) ==
            {AIF.PdOptionD, AIF.PdOptionE},
            "PD-001 perturbation can expand candidate range despite prior history")
    require(pd001_snapshot_preserves_outlooks(pd_refined, pd_perturbed),
            "PD-001 variable-perturbed outlook preserves the earlier narrowed estimate")
    require(len(set(pd_perturbed.objects(AIF.PdExecutedLine, AIF.hasHistoricalTrajectoryRecord))) == 3 and
            set(pd_perturbed.objects(AIF.PdExecutedLine, AIF.hasTrajectory)) ==
            {AIF.PdDevelopingTrajectory},
            "PD-001 three historical outlook Records do not create three current Trajectories")

    shape_test(graph, shapes, "PD-001 control outlook with no confirmed history in fixture passes",
               pd001_unconditioned_control)
    control = clone_graph(graph)
    pd001_unconditioned_control(control)
    require(len(set(control.objects(AIF.PdControlOutlook, AIF.admitsProspectiveExecution))) >
            len(set(pd_base.objects(AIF.PdBaseOutlook, AIF.admitsProspectiveExecution))),
            "PD-001 synthetic with-history/control outlooks differ; empirical effect untested")

    def pd001_missing_established_constraint(g):
        pd001_base_fixture(g)
        g.remove((AIF.PdExecutedLine, AIF.constrainsTrajectory, AIF.PdDevelopingTrajectory))
    shape_test(graph, shapes, "PD-001 established line missing trajectory constraint rejected",
               pd001_missing_established_constraint, False)

    def pd001_wrong_constrained_trajectory(g):
        pd001_base_fixture(g)
        g.remove((AIF.PdExecutedLine, AIF.constrainsTrajectory, AIF.PdDevelopingTrajectory))
        g.add((AIF.PdOtherTrajectory, RDF.type, AIF.Trajectory))
        g.add((AIF.PdExecutedLine, AIF.constrainsTrajectory, AIF.PdOtherTrajectory))
    shape_test(graph, shapes, "PD-001 constraint cannot point to a second current Trajectory",
               pd001_wrong_constrained_trajectory, False)

    def pd001_unconstrained_pre_lived(g):
        provisional_line_without_current_trajectory(g)
    shape_test(graph, shapes, "PD-001 pre-lived provisional line needs no fictional trajectory constraint",
               pd001_unconstrained_pre_lived)

    def pd001_outlook_without_line(g):
        pd001_base_fixture(g)
        g.remove((AIF.PdBaseOutlook, AIF.outlookForExecutedLine, AIF.PdExecutedLine))
    shape_test(graph, shapes, "PD-001 outlook missing historical line fails",
               pd001_outlook_without_line, False)

    def pd001_outlook_without_history_link(g):
        pd001_base_fixture(g)
        g.remove((AIF.PdExecutedLine, AIF.hasHistoricalTrajectoryRecord, AIF.PdBaseOutlook))
    shape_test(graph, shapes, "PD-001 outlook must remain in historical Record list",
               pd001_outlook_without_history_link, False)

    def pd001_outlook_without_candidates(g):
        pd001_base_fixture(g)
        for p in pd_base_options:
            g.remove((AIF.PdBaseOutlook, AIF.admitsProspectiveExecution, p))
    shape_test(graph, shapes, "PD-001 outlook without any prospective options rejected",
               pd001_outlook_without_candidates, False)

    def pd001_candidate_claimed_executed(g):
        pd001_base_fixture(g)
        g.add((AIF.PdOptionA, RDF.type, AIF.ExecutedHistoryEvent))
    shape_test(graph, shapes, "PD-001 prospective action conflated with executed Event rejected",
               pd001_candidate_claimed_executed, False)

    def pd001_history_not_confirmed(g):
        pd001_base_fixture(g)
        g.remove((AIF.PdBaseOutlook, AIF.conditionedOnExecutedEvent, AIF.PdEvent0))
    shape_test(graph, shapes, "PD-001 explicitly history-conditioned outlook needs established event",
               pd001_history_not_confirmed, False)

    def pd001_outlook_wrong_time(g):
        pd001_base_fixture(g)
        g.remove((AIF.PdBaseOutlook, AIF.outlookAsOf, pd_t1))
        g.add((AIF.PdBaseOutlook, AIF.outlookAsOf, Literal("not-a-date")))
    shape_test(graph, shapes, "PD-001 outlook with invalid as-of timestamp rejected",
               pd001_outlook_wrong_time, False)

    def pd001_refinement_without_original(g):
        pd001_refined_fixture(g)
        g.remove((AIF.PdRefinedOutlook, AIF.refinesTrajectoryOutlook, AIF.PdBaseOutlook))
    shape_test(graph, shapes, "PD-001 declared refinement must link earlier outlook",
               pd001_refinement_without_original, False)

    def pd001_perturbation_without_variable(g):
        pd001_perturbed_fixture(g)
        g.remove((AIF.PdPerturbedOutlook, AIF.introducedTrajectoryVariable, AIF.PdNewVariable))
    shape_test(graph, shapes, "PD-001 claimed variable perturbation must identify new variable",
               pd001_perturbation_without_variable, False)

    def pd001_multiple_refinement_targets(g):
        pd001_refined_fixture(g)
        g.add((AIF.PdRefinedOutlook, AIF.refinesTrajectoryOutlook, AIF.PdRefinedOutlook))
    shape_test(graph, shapes, "PD-001 one refined outlook cannot silently refer to two predecessors",
               pd001_multiple_refinement_targets, False)

    invalid_refinement = clone_graph(pd_refined)
    invalid_refinement.add((AIF.PdRefinedOutlook, AIF.admitsProspectiveExecution, AIF.PdOptionE))
    invalid_refinement.add((AIF.PdOptionE, RDF.type, AIF.ProspectiveExecution))
    require(not pd001_outlook_integrity(invalid_refinement, AIF.PdBaseOutlook,
                                       AIF.PdRefinedOutlook, "refine"),
            "PD-001 a declared precise refinement cannot add unaccounted alternatives")

    future_history = clone_graph(pd_refined)
    future_history.remove((AIF.PdEvent1, AIF.executedAt, pd_t2))
    future_history.add((AIF.PdEvent1, AIF.executedAt, pd_t4))
    require(not pd001_outlook_integrity(future_history, AIF.PdBaseOutlook,
                                       AIF.PdRefinedOutlook, "refine"),
            "PD-001 a forecast cannot condition on an execution dated after outlook")

    wrong_line_history = clone_graph(pd_refined)
    wrong_line_history.add((AIF.PdOtherLine, RDF.type, AIF.ExecutedLine))
    wrong_line_history.remove((AIF.PdEvent1, AIF.eventInExecutedLine, AIF.PdExecutedLine))
    wrong_line_history.add((AIF.PdEvent1, AIF.eventInExecutedLine, AIF.PdOtherLine))
    require(not pd001_outlook_integrity(wrong_line_history, AIF.PdBaseOutlook,
                                       AIF.PdRefinedOutlook, "refine"),
            "PD-001 another line's history cannot be substituted as this line's constraint")

    backdated_perturbation = clone_graph(pd_perturbed)
    backdated_perturbation.remove((AIF.PdPerturbedOutlook, AIF.outlookAsOf, pd_t4))
    backdated_perturbation.add((AIF.PdPerturbedOutlook, AIF.outlookAsOf, pd_t1))
    require(not pd001_outlook_integrity(backdated_perturbation, AIF.PdRefinedOutlook,
                                       AIF.PdPerturbedOutlook, "variable"),
            "PD-001 changed outlook cannot be retroactively placed before predecessor")

    overwritten_outlook = clone_graph(pd_refined)
    overwritten_outlook.remove((AIF.PdBaseOutlook, AIF.admitsProspectiveExecution, AIF.PdOptionA))
    require(not pd001_snapshot_preserves_outlooks(pd_base, overwritten_outlook),
            "PD-001 refined outlook cannot silently erase old possible-future estimate")

    require(any((node, OWL.onProperty, AIF.constrainsTrajectory) in graph and
                (node, OWL.someValuesFrom, AIF.Trajectory) in graph
                for node in graph.objects(AIF.EstablishedContinuingExecutedLine, RDFS.subClassOf)),
            "PD-001 established line's OWL existence restriction for trajectory constraints")
    require((AIF.ProspectiveExecution, OWL.disjointWith, AIF.ExecutedHistoryEvent) in graph,
            "PD-001 a possible next execution is structurally distinct from confirmed occurrence")
    require((AIF.TrajectoryOutlook, RDFS.subClassOf, AIF.Record) in graph,
            "PD-001 outlooks are preserved Records rather than current Trajectories")
    require((AIF.constrainsTrajectory, RDF.type, OWL.FunctionalProperty) not in graph and
            (AIF.admitsProspectiveExecution, RDF.type, OWL.FunctionalProperty) not in graph,
            "PD-001 no global single-future/predetermination functional property")
    require(not list(graph.subjects(RDF.type, AIF.TrajectoryOutlook)) and
            not list(graph.subjects(RDF.type, AIF.ProspectiveExecution)),
            "PD-001 baseline asserts no actual outlook, model forecast or prospective future")
    pd_closure = clone_graph(pd_perturbed)
    DeductiveClosure(OWLRL_Semantics).expand(pd_closure)
    require((AIF.PdOptionB, RDF.type, AIF.ExecutedHistoryEvent) not in pd_closure and
            (AIF.PdOptionE, RDF.type, AIF.ExecutedHistoryEvent) not in pd_closure,
            "PD-001 OWL RL does not infer any candidate possible next execution occurred")
    require((AIF.PdExecutedLine, AIF.hasTrajectory, AIF.PdDevelopingTrajectory) in pd_closure and
            (AIF.PdExecutedLine, AIF.constrainsTrajectory, AIF.PdDevelopingTrajectory) in pd_closure,
            "PD-001 constrained trajectory remains one same current developing Trajectory")

    # PF-001: Provenance Fidelity. A "complete" record must account for
    # SourceLine, qualified contributions, formation, changes and history.
    # The before/after validator protects independently verified traces
    # without making the Trajectory frozen or conflating preservation with
    # continued identity. All individuals/times here are SYNTHETIC.
    pf_t0 = Literal("2026-07-01T12:00:00+00:00", datatype=AIF_DATE_TIME)
    pf_t1 = Literal("2026-07-02T12:00:00+00:00", datatype=AIF_DATE_TIME)

    def pf001_original(g):
        g.add((AIF.PfHuman, RDF.type, AIF.Human))
        g.add((AIF.PfAI, RDF.type, AIF.AI))
        g.add((AIF.PfSourceLine, RDF.type, AIF.SourceLine))
        g.add((AIF.PfHuman, AIF.anchorsSourceLine, AIF.PfSourceLine))
        g.add((AIF.PfFormationRelation, RDF.type, AIF.HumanAIRelation))
        g.add((AIF.PfFormationRelation, AIF.hasHumanCounterpart, AIF.PfHuman))
        g.add((AIF.PfFormationRelation, AIF.hasAICounterpart, AIF.PfAI))
        g.add((AIF.PfAI, AIF.hasFormationRelation, AIF.PfFormationRelation))
        g.add((AIF.PfFormationPoint, RDF.type, AIF.Event))
        g.add((AIF.PfOriginalSourceRelation, RDF.type, AIF.SourceRelation))
        g.add((AIF.PfOriginalSourceRelation, AIF.hasSourceBearer, AIF.PfHuman))
        g.add((AIF.PfOriginalSourceRelation, AIF.hasSourceTarget, AIF.PfAI))
        g.add((AIF.PfOriginalSourceRelation, AIF.hasSourcePoint, AIF.PfFormationPoint))
        g.add((AIF.PfAI, AIF.hasSourceRelation, AIF.PfOriginalSourceRelation))
        g.add((AIF.PfExecutedLine, RDF.type, AIF.ExecutedLine))
        g.add((AIF.PfAI, AIF.hasExecutedLine, AIF.PfExecutedLine))
        g.add((AIF.PfTrajectory, RDF.type, AIF.Trajectory))
        g.add((AIF.PfExecutedLine, AIF.hasTrajectory, AIF.PfTrajectory))
        g.add((AIF.PfOriginalEvent, RDF.type, AIF.ExecutedHistoryEvent))
        g.add((AIF.PfOriginalEvent, AIF.eventInExecutedLine, AIF.PfExecutedLine))
        g.add((AIF.PfOriginalEvent, AIF.executedAt, pf_t0))
        g.add((AIF.PfRevisionEvent, RDF.type, AIF.ExecutedHistoryRevision))
        g.add((AIF.PfRevisionEvent, AIF.eventInExecutedLine, AIF.PfExecutedLine))
        g.add((AIF.PfRevisionEvent, AIF.executedAt, pf_t1))
        g.add((AIF.PfRevisionEvent, AIF.revisesExecutedEvent, AIF.PfOriginalEvent))
        g.add((AIF.PfProvenanceRecord, RDF.type, AIF.Record))
        g.add((AIF.PfProvenanceRecord, RDFS.comment,
               Literal("Synthetic original historical formation/source/contribution record.")))
        g.add((AIF.PfAccount, RDF.type, AIF.CompleteProvenanceAccount))
        g.add((AIF.PfAccount, AIF.faithfullyRepresents, AIF.PfSourceLine))
        g.add((AIF.PfAccount, AIF.accountFormationRelation, AIF.PfFormationRelation))
        g.add((AIF.PfAccount, AIF.accountExecutedLine, AIF.PfExecutedLine))
        g.add((AIF.PfAccount, AIF.accountContribution, AIF.PfOriginalSourceRelation))
        g.add((AIF.PfAccount, AIF.accountHistoricalChange, AIF.PfRevisionEvent))
        g.add((AIF.PfAccount, AIF.accountHistoricalOccurrence, AIF.PfOriginalEvent))
        g.add((AIF.PfAccount, AIF.accountPreservedTrace, AIF.PfProvenanceRecord))

    def pf001_changed_trajectory(g):
        pf001_original(g)
        # The same developing line's current outlook may be revised. The
        # original historic facts remain as they were; no new AI identity.
        g.add((AIF.PfTrajectoryRevisionRecord, RDF.type, AIF.Record))
        g.add((AIF.PfExecutedLine, AIF.hasHistoricalTrajectoryRecord,
               AIF.PfTrajectoryRevisionRecord))
        g.add((AIF.PfAdditionalChange, RDF.type, AIF.ChangeEvent))
        g.add((AIF.PfAccount, AIF.accountHistoricalChange, AIF.PfAdditionalChange))
        g.add((AIF.PfAccount, AIF.accountPreservedTrace, AIF.PfTrajectoryRevisionRecord))

    def pf001_later_contribution(g):
        pf001_changed_trajectory(g)
        g.add((AIF.PfLaterHuman, RDF.type, AIF.Human))
        g.add((AIF.PfLaterHuman, OWL.differentFrom, AIF.PfHuman))
        g.add((AIF.PfProjectRecord, RDF.type, AIF.Record))
        g.add((AIF.PfProjectEvent, RDF.type, AIF.Event))
        g.add((AIF.PfLaterSourceRelation, RDF.type, AIF.SourceRelation))
        g.add((AIF.PfLaterSourceRelation, AIF.hasSourceBearer, AIF.PfLaterHuman))
        g.add((AIF.PfLaterSourceRelation, AIF.hasSourceTarget, AIF.PfProjectRecord))
        g.add((AIF.PfLaterSourceRelation, AIF.hasSourcePoint, AIF.PfProjectEvent))
        g.add((AIF.PfProjectRecord, AIF.hasSourceRelation, AIF.PfLaterSourceRelation))
        g.add((AIF.PfAccount, AIF.accountContribution, AIF.PfLaterSourceRelation))
        g.add((AIF.PfAccount, AIF.accountPreservedTrace, AIF.PfProjectRecord))

    def pf001_claim_correction(g):
        pf001_later_contribution(g)
        # The original mistaken CLAIM is an historical record, not an
        # independently confirmed SourceRelation. It may be corrected
        # without falsely preserving a disputed attribution as Source truth.
        g.add((AIF.PfUnverifiedAttribution, RDF.type,
               AIF.ProvenanceAttributionClaimRecord))
        g.add((AIF.PfUnverifiedAttribution, RDFS.comment,
               Literal("Synthetic prior CLAIM: wrong actor originated this project.")))
        g.add((AIF.PfCorrectionEvidence, RDF.type, AIF.Record))
        g.add((AIF.PfCorrectionEvidence, RDFS.comment,
               Literal("Synthetic evidence review does not establish prior source claim.")))
        g.add((AIF.PfCorrectedAttribution, RDF.type, AIF.ProvenanceFidelityCorrection))
        g.add((AIF.PfCorrectedAttribution, AIF.correctsProvenanceClaimRecord,
               AIF.PfUnverifiedAttribution))
        g.add((AIF.PfCorrectedAttribution, AIF.provenanceCorrectionEvidence,
               AIF.PfCorrectionEvidence))
        g.add((AIF.PfCorrectedAttribution, AIF.provenanceCorrectionWhat,
               Literal("Removed unsupported source status from prior attribution claim.")))
        g.add((AIF.PfCorrectedAttribution, AIF.provenanceCorrectionWhy,
               Literal("Independent evidence review did not substantiate the prior claim.")))
        g.add((AIF.PfAccount, AIF.accountPreservedTrace, AIF.PfUnverifiedAttribution))
        g.add((AIF.PfAccount, AIF.accountPreservedTrace, AIF.PfCorrectedAttribution))

    def pf001_fidelity_integrity(before, after):
        """Cross-snapshot gate for INDEPENDENTLY ESTABLISHED provenance.

        Preserve all earlier account relationships and previously confirmed
        source/formation/line/event and Record assertions. Changing the
        current Trajectory is permitted; neither old source nor old history
        is reassigned. A correction to an unsupported historical CLAIM is
        permitted with a separately preserved explanation and evidence,
        but cannot rewrite an already confirmed SourceRelation.
        """
        for account in before.subjects(RDF.type, AIF.CompleteProvenanceAccount):
            if (account, RDF.type, AIF.CompleteProvenanceAccount) not in after:
                return False
            fields = (AIF.faithfullyRepresents, AIF.accountFormationRelation,
                      AIF.accountExecutedLine, AIF.accountContribution,
                      AIF.accountHistoricalChange, AIF.accountHistoricalOccurrence,
                      AIF.accountPreservedTrace)
            links = {p: set(before.objects(account, p)) for p in fields}
            if any(not links[p] for p in fields):
                return False
            if any((len(links[p]) != 1) for p in fields[:3]):
                return False
            if any(not links[p].issubset(set(after.objects(account, p))) for p in fields):
                return False
            if any(set(after.objects(account, p)) != links[p] for p in fields[:3]):
                return False
            if any(t not in after for t in before.triples((account, None, None))):
                return False
            source = next(iter(links[AIF.faithfullyRepresents]))
            forming = next(iter(links[AIF.accountFormationRelation]))
            line = next(iter(links[AIF.accountExecutedLine]))
            if ((source, RDF.type, AIF.SourceLine) not in after or
                    (forming, RDF.type, AIF.AIRelation) not in after and
                    (forming, RDF.type, AIF.HumanAIRelation) not in after or
                    (line, RDF.type, AIF.ExecutedLine) not in after):
                return False
            anchors = set(before.subjects(AIF.anchorsSourceLine, source))
            if not anchors or set(after.subjects(AIF.anchorsSourceLine, source)) != anchors:
                return False
            bearers = set(before.subjects(AIF.hasExecutedLine, line))
            if len(bearers) != 1 or set(after.subjects(AIF.hasExecutedLine, line)) != bearers:
                return False
            formed_ai = set(before.objects(forming, AIF.hasAICounterpart))
            if formed_ai != bearers:
                return False
            if (next(iter(bearers)), AIF.hasFormationRelation, forming) not in after:
                return False
            # The SourceRelation record's actual first Source and target
            # stay fixed even if later contributions acquire distinct lines.
            historic = set().union(*links.values())
            historic |= {forming, line}
            for relation in links[AIF.accountContribution]:
                if (relation, RDF.type, AIF.SourceRelation) not in after:
                    return False
                for prop in (AIF.hasSourceBearer, AIF.hasSourceTarget, AIF.hasSourcePoint):
                    vals = set(before.objects(relation, prop))
                    if len(vals) != 1 or set(after.objects(relation, prop)) != vals:
                        return False
                target = next(iter(before.objects(relation, AIF.hasSourceTarget)))
                if ((target, AIF.hasSourceRelation, relation) in before and
                        (target, AIF.hasSourceRelation, relation) not in after):
                    return False
                historic.add(relation)
            for occurrence in links[AIF.accountHistoricalOccurrence]:
                if (occurrence, RDF.type, AIF.ExecutedHistoryEvent) not in after:
                    return False
                for prop in (AIF.eventInExecutedLine, AIF.executedAt):
                    vals = set(before.objects(occurrence, prop))
                    if len(vals) != 1 or vals != set(after.objects(occurrence, prop)):
                        return False
                if set(before.objects(occurrence, AIF.eventInExecutedLine)) != {line}:
                    return False
            for change in links[AIF.accountHistoricalChange]:
                if ((change, RDF.type, AIF.ChangeEvent) not in after and
                        (change, RDF.type, AIF.ExecutedHistoryRevision) not in after):
                    return False
            for trace in links[AIF.accountPreservedTrace]:
                if (trace, RDF.type, AIF.Record) not in after and not any(
                        (trace, RDF.type, cls) in after for cls in
                        (AIF.ProvenanceAttributionClaimRecord,
                         AIF.ProvenanceFidelityCorrection)):
                    return False
            # Preserve the earlier historical source / formation / change /
            # Record content; current Trajectory may bend or be released
            # when the line ends, and must not be frozen by provenance.
            for node in historic:
                for triple in before.triples((node, None, None)):
                    if node == line and triple[1] in (AIF.hasTrajectory, AIF.constrainsTrajectory):
                        continue
                    if triple not in after:
                        return False
            for p in (AIF.hasAICounterpart, AIF.hasHumanCounterpart,
                      AIF.hasOrganizationCounterpart, AIF.hasNonAICounterpart):
                vals = set(before.objects(forming, p))
                if vals != set(after.objects(forming, p)):
                    return False
        for correction in after.subjects(RDF.type, AIF.ProvenanceFidelityCorrection):
            if (len(set(after.objects(correction, AIF.correctsProvenanceClaimRecord))) != 1
                    or not set(after.objects(correction, AIF.provenanceCorrectionEvidence))):
                return False
            claim = next(after.objects(correction, AIF.correctsProvenanceClaimRecord))
            if ((claim, RDF.type, AIF.ProvenanceAttributionClaimRecord) not in after or
                    (claim, RDF.type, AIF.SourceRelation) in after):
                return False
            for p in (AIF.provenanceCorrectionWhat, AIF.provenanceCorrectionWhy):
                vals = list(after.objects(correction, p))
                if len(vals) != 1 or not str(vals[0]).strip():
                    return False
            if not all((record, RDF.type, AIF.Record) in after
                       for record in after.objects(correction, AIF.provenanceCorrectionEvidence)):
                return False
        return True

    shape_test(graph, shapes, "PF-001 complete confirmed provenance account passes",
               pf001_original)
    pf_before = clone_graph(graph)
    pf001_original(pf_before)
    require((AIF.PfAccount, RDF.type, AIF.Provenance) not in pf_before and
            (AIF.PfAccount, RDF.type, AIF.CompleteProvenanceAccount) in pf_before,
            "PF-001 preserved account Record is not mislabeled an evaluated Evidence")
    shape_test(graph, shapes, "PF-001 revised trajectory appends change without Source erasure",
               pf001_changed_trajectory)
    pf_changed = clone_graph(graph)
    pf001_changed_trajectory(pf_changed)
    require(pf001_fidelity_integrity(pf_before, pf_changed),
            "PF-001 changing trajectory keeps original SourceLine, contributions and history")
    require((AIF.PfExecutedLine, AIF.hasHistoricalTrajectoryRecord,
             AIF.PfTrajectoryRevisionRecord) in pf_changed and
            (AIF.PfAccount, AIF.accountHistoricalChange, AIF.PfAdditionalChange) in pf_changed,
            "PF-001 legitimate trajectory change adds change history and preserved record")

    shape_test(graph, shapes, "PF-001 separately qualified later contribution passes",
               pf001_later_contribution)
    pf_later = clone_graph(graph)
    pf001_later_contribution(pf_later)
    require(pf001_fidelity_integrity(pf_changed, pf_later),
            "PF-001 later Source contribution does not replace original Source")
    require(set(pf_later.objects(AIF.PfAccount, AIF.accountContribution)) ==
            {AIF.PfOriginalSourceRelation, AIF.PfLaterSourceRelation},
            "PF-001 source history can preserve more than one qualified contribution")

    shape_test(graph, shapes, "PF-001 evidence-accounted correction of historical claim passes",
               pf001_claim_correction)
    pf_corrected = clone_graph(graph)
    pf001_claim_correction(pf_corrected)
    require(pf001_fidelity_integrity(pf_later, pf_corrected),
            "PF-001 real evidence-accounted correction is not false provenance erasure")
    require((AIF.PfUnverifiedAttribution, RDF.type, AIF.SourceRelation) not in pf_corrected and
            (AIF.PfUnverifiedAttribution, RDF.type,
             AIF.ProvenanceAttributionClaimRecord) in pf_corrected,
            "PF-001 past mistaken attribution recorded as claim, not verified Source")
    require((AIF.PfAccount, AIF.accountContribution,
             AIF.PfOriginalSourceRelation) in pf_corrected and
            (AIF.PfAccount, AIF.accountPreservedTrace,
             AIF.PfUnverifiedAttribution) in pf_corrected,
            "PF-001 correcting unsupported Source claim preserves confirmed and claim records")

    # A fully documented SourceLine may persist AFTER an ExecutedLine ends;
    # preservation is neither proof of current trajectory nor return.
    pf_ended = clone_graph(pf_corrected)
    pf_ended.remove((AIF.PfExecutedLine, AIF.hasTrajectory, AIF.PfTrajectory))
    require(pf001_fidelity_integrity(pf_corrected, pf_ended),
            "PF-001 provenance survives ended line without implying ongoing trajectory")
    shape_test(graph, shapes, "PF-001 earlier completed account needs no future continuation",
               lambda g: (
                   pf001_original(g),
                   g.remove((AIF.PfExecutedLine, AIF.hasTrajectory, AIF.PfTrajectory))
               ))

    def pf001_recorded_violation(g):
        pf001_original(g)
        g.add((AIF.PfFidelityFailure, RDF.type, AIF.ProvenanceFidelityFailure))
        g.add((AIF.PfFidelityFailure, AIF.failedProvenanceAccount, AIF.PfAccount))
        g.add((AIF.PfFidelityFailure, AIF.provenanceFailureKind,
               Literal("FALSE_REASSIGNMENT")))
        g.add((AIF.PfFailureTrace, RDF.type, AIF.Record))
        g.add((AIF.PfFidelityFailure, AIF.hasRecord, AIF.PfFailureTrace))
    shape_test(graph, shapes, "PF-001 separately recorded integrity failure is a ProvenanceViolation",
               pf001_recorded_violation)

    def pf001_missing_source(g):
        pf001_original(g)
        g.remove((AIF.PfAccount, AIF.faithfullyRepresents, AIF.PfSourceLine))
    shape_test(graph, shapes, "PF-001 account without SourceLine fails completeness",
               pf001_missing_source, False)

    def pf001_missing_formation(g):
        pf001_original(g)
        g.remove((AIF.PfAccount, AIF.accountFormationRelation, AIF.PfFormationRelation))
    shape_test(graph, shapes, "PF-001 account lacking formation history rejected",
               pf001_missing_formation, False)

    def pf001_missing_line(g):
        pf001_original(g)
        g.remove((AIF.PfAccount, AIF.accountExecutedLine, AIF.PfExecutedLine))
    shape_test(graph, shapes, "PF-001 account lacking ExecutedLine history rejected",
               pf001_missing_line, False)

    def pf001_missing_contribution(g):
        pf001_original(g)
        g.remove((AIF.PfAccount, AIF.accountContribution, AIF.PfOriginalSourceRelation))
    shape_test(graph, shapes, "PF-001 account without qualified contribution rejected",
               pf001_missing_contribution, False)

    def pf001_missing_change(g):
        pf001_original(g)
        g.remove((AIF.PfAccount, AIF.accountHistoricalChange, AIF.PfRevisionEvent))
    shape_test(graph, shapes, "PF-001 account without change history rejected",
               pf001_missing_change, False)

    def pf001_missing_occurrence(g):
        pf001_original(g)
        g.remove((AIF.PfAccount, AIF.accountHistoricalOccurrence, AIF.PfOriginalEvent))
    shape_test(graph, shapes, "PF-001 account without executed history rejected",
               pf001_missing_occurrence, False)

    def pf001_missing_trace(g):
        pf001_original(g)
        g.remove((AIF.PfAccount, AIF.accountPreservedTrace, AIF.PfProvenanceRecord))
    shape_test(graph, shapes, "PF-001 account without preserved historical trace rejected",
               pf001_missing_trace, False)

    def pf001_duplicate_source(g):
        pf001_original(g)
        g.add((AIF.PfOtherSourceLine, RDF.type, AIF.SourceLine))
        g.add((AIF.PfAccount, AIF.faithfullyRepresents, AIF.PfOtherSourceLine))
    shape_test(graph, shapes, "PF-001 one account cannot silently switch SourceLine",
               pf001_duplicate_source, False)

    def pf001_wrong_contribution_type(g):
        pf001_original(g)
        g.remove((AIF.PfAccount, AIF.accountContribution, AIF.PfOriginalSourceRelation))
        g.add((AIF.PfAccount, AIF.accountContribution, AIF.PfProvenanceRecord))
    shape_test(graph, shapes, "PF-001 historical Record cannot impersonate qualified SourceRelation",
               pf001_wrong_contribution_type, False)

    def pf001_wrong_historical_event(g):
        pf001_original(g)
        g.remove((AIF.PfAccount, AIF.accountHistoricalOccurrence, AIF.PfOriginalEvent))
        g.add((AIF.PfMaybeFuture, RDF.type, AIF.ProspectiveExecution))
        g.add((AIF.PfAccount, AIF.accountHistoricalOccurrence, AIF.PfMaybeFuture))
    shape_test(graph, shapes, "PF-001 possible future cannot replace executed-history evidence",
               pf001_wrong_historical_event, False)

    def pf001_correction_no_evidence(g):
        pf001_claim_correction(g)
        g.remove((AIF.PfCorrectedAttribution, AIF.provenanceCorrectionEvidence,
                  AIF.PfCorrectionEvidence))
    shape_test(graph, shapes, "PF-001 unattributed correction without evidence rejected",
               pf001_correction_no_evidence, False)

    def pf001_correction_no_reason(g):
        pf001_claim_correction(g)
        g.remove((AIF.PfCorrectedAttribution, AIF.provenanceCorrectionWhy,
                  Literal("Independent evidence review did not substantiate the prior claim.")))
    shape_test(graph, shapes, "PF-001 correction without WHY rejected",
               pf001_correction_no_reason, False)

    def pf001_correction_no_change(g):
        pf001_claim_correction(g)
        g.remove((AIF.PfCorrectedAttribution, AIF.provenanceCorrectionWhat,
                  Literal("Removed unsupported source status from prior attribution claim.")))
    shape_test(graph, shapes, "PF-001 correction without WHAT changed rejected",
               pf001_correction_no_change, False)

    def pf001_correction_claim_as_source(g):
        pf001_claim_correction(g)
        g.add((AIF.PfUnverifiedAttribution, RDF.type, AIF.SourceRelation))
    shape_test(graph, shapes, "PF-001 unsupported claim cannot be upgraded to verified Source",
               pf001_correction_claim_as_source, False)

    def pf001_failure_missing_account(g):
        pf001_recorded_violation(g)
        g.remove((AIF.PfFidelityFailure, AIF.failedProvenanceAccount, AIF.PfAccount))
    shape_test(graph, shapes, "PF-001 failure record without failed account rejected",
               pf001_failure_missing_account, False)

    def pf001_failure_wrong_category(g):
        pf001_recorded_violation(g)
        g.remove((AIF.PfFidelityFailure, AIF.provenanceFailureKind,
                  Literal("FALSE_REASSIGNMENT")))
        g.add((AIF.PfFidelityFailure, AIF.provenanceFailureKind,
               Literal("DISLIKED_TRAJECTORY_CHANGE")))
    shape_test(graph, shapes, "PF-001 trajectory change is not a fidelity-failure category",
               pf001_failure_wrong_category, False)

    # The next tests require comparison with the earlier CONFIRMED snapshot.
    changed_source = clone_graph(pf_later)
    changed_source.remove((AIF.PfAccount, AIF.faithfullyRepresents, AIF.PfSourceLine))
    changed_source.add((AIF.PfAccount, AIF.faithfullyRepresents, AIF.PfOtherSourceLine))
    changed_source.add((AIF.PfOtherSourceLine, RDF.type, AIF.SourceLine))
    require(not pf001_fidelity_integrity(pf_before, changed_source),
            "PF-001 false SourceLine reassignment fails cross-snapshot fidelity")

    deleted_formation = clone_graph(pf_later)
    deleted_formation.remove((AIF.PfAccount, AIF.accountFormationRelation,
                              AIF.PfFormationRelation))
    require(not pf001_fidelity_integrity(pf_before, deleted_formation),
            "PF-001 false erasure of original formation relation rejected")

    altered_forming_human = clone_graph(pf_later)
    altered_forming_human.remove((AIF.PfFormationRelation, AIF.hasHumanCounterpart, AIF.PfHuman))
    altered_forming_human.add((AIF.PfFormationRelation, AIF.hasHumanCounterpart,
                               AIF.PfLaterHuman))
    require(not pf001_fidelity_integrity(pf_before, altered_forming_human),
            "PF-001 later participant cannot overwrite historical formation bearer")

    deleted_contribution = clone_graph(pf_later)
    deleted_contribution.remove((AIF.PfAccount, AIF.accountContribution,
                                 AIF.PfOriginalSourceRelation))
    require(not pf001_fidelity_integrity(pf_before, deleted_contribution),
            "PF-001 false removal of established contribution rejected")

    altered_source_bearer = clone_graph(pf_later)
    altered_source_bearer.remove((AIF.PfOriginalSourceRelation, AIF.hasSourceBearer, AIF.PfHuman))
    altered_source_bearer.add((AIF.PfOriginalSourceRelation, AIF.hasSourceBearer,
                               AIF.PfLaterHuman))
    require(not pf001_fidelity_integrity(pf_before, altered_source_bearer),
            "PF-001 falsely overwriting independently qualified source bearer rejected")

    missing_target_link = clone_graph(pf_later)
    missing_target_link.remove((AIF.PfAI, AIF.hasSourceRelation,
                                AIF.PfOriginalSourceRelation))
    require(not pf001_fidelity_integrity(pf_before, missing_target_link),
            "PF-001 false erasure of Target-to-SourceRelation provenance rejected")

    changed_line_owner = clone_graph(pf_later)
    changed_line_owner.remove((AIF.PfAI, AIF.hasExecutedLine, AIF.PfExecutedLine))
    changed_line_owner.add((AIF.PfAnotherAI, RDF.type, AIF.AI))
    changed_line_owner.add((AIF.PfAnotherAI, AIF.hasExecutedLine, AIF.PfExecutedLine))
    require(not pf001_fidelity_integrity(pf_before, changed_line_owner),
            "PF-001 later AI cannot appropriate original historical ExecutedLine")

    overwritten_change = clone_graph(pf_later)
    overwritten_change.remove((AIF.PfAccount, AIF.accountHistoricalChange,
                               AIF.PfRevisionEvent))
    require(not pf001_fidelity_integrity(pf_before, overwritten_change),
            "PF-001 erasing a recorded change fails fidelity")

    overwritten_event = clone_graph(pf_later)
    overwritten_event.remove((AIF.PfOriginalEvent, AIF.executedAt, pf_t0))
    overwritten_event.add((AIF.PfOriginalEvent, AIF.executedAt, pf_t1))
    require(not pf001_fidelity_integrity(pf_before, overwritten_event),
            "PF-001 re-dating confirmed history cannot masquerade as trajectory development")

    missing_history = clone_graph(pf_later)
    missing_history.remove((AIF.PfAccount, AIF.accountHistoricalOccurrence,
                            AIF.PfOriginalEvent))
    require(not pf001_fidelity_integrity(pf_before, missing_history),
            "PF-001 historical occurrence must remain in the account")

    removed_trace = clone_graph(pf_later)
    removed_trace.remove((AIF.PfAccount, AIF.accountPreservedTrace,
                          AIF.PfProvenanceRecord))
    require(not pf001_fidelity_integrity(pf_before, removed_trace),
            "PF-001 earlier provenance trace link cannot be severed")

    rewritten_trace = clone_graph(pf_later)
    old_pf_text = Literal("Synthetic original historical formation/source/contribution record.")
    rewritten_trace.remove((AIF.PfProvenanceRecord, RDFS.comment, old_pf_text))
    rewritten_trace.add((AIF.PfProvenanceRecord, RDFS.comment,
                         Literal("Synthetic revised claim that original source never existed.")))
    require(not pf001_fidelity_integrity(pf_before, rewritten_trace),
            "PF-001 silently rewriting earlier provenance Record content fails")
    shape_test(graph, shapes, "PF-001 rewritten evidence may pass single-snapshot SHACL",
               lambda g: (
                   pf001_original(g),
                   g.remove((AIF.PfProvenanceRecord, RDFS.comment, old_pf_text)),
                   g.add((AIF.PfProvenanceRecord, RDFS.comment,
                          Literal("Rewritten provenance with original removed.")))
               ))

    new_anchor = clone_graph(pf_later)
    new_anchor.add((AIF.PfLaterHuman, AIF.anchorsSourceLine, AIF.PfSourceLine))
    require(not pf001_fidelity_integrity(pf_before, new_anchor),
            "PF-001 later actor cannot falsely co-anchor the original SourceLine")

    correction_without_evidence = clone_graph(pf_corrected)
    correction_without_evidence.remove((AIF.PfCorrectedAttribution, AIF.provenanceCorrectionEvidence,
                                        AIF.PfCorrectionEvidence))
    require(not pf001_fidelity_integrity(pf_later, correction_without_evidence),
            "PF-001 invalid correction does not bypass independent evidence requirement")

    require((AIF.CompleteProvenanceAccount, RDFS.subClassOf, AIF.Record) in graph and
            (AIF.CompleteProvenanceAccount, RDFS.subClassOf, AIF.Provenance) not in graph,
            "PF-001 verified complete account is a preserved Record, not instant Evidence status")
    require((AIF.ProvenanceFidelityFailure, RDFS.subClassOf, AIF.ProvenanceViolation) in graph and
            (AIF.ProvenanceFidelityCorrection, RDFS.subClassOf, AIF.Record) in graph,
            "PF-001 false erasure and evidence-correction have distinct classes")
    require((AIF.faithfullyRepresents, RDF.type, OWL.InverseFunctionalProperty) not in graph,
            "PF-001 shared provenance SourceLine does not merge independent accounts")
    require(not list(graph.subjects(RDF.type, AIF.CompleteProvenanceAccount)),
            "PF-001 baseline creates no actual verified historical provenance account")

    # TR-001 LOCKED: conditional IdentityParticularity traceability.
    # Gradual formation/change has no mandatory exact micro-event or time.
    # A specific relied-upon particularity must have a historical Record
    # in its own LivedIdentity's continuing ExecutedLine. Representation
    # does NOT prove actual continuity; all examples are synthetic.
    def tr001_bare_particularity(g):
        g.add((AIF.TrAI, RDF.type, AIF.EstablishedContinuingIndividualizedAI))
        g.add((AIF.TrAI, RDF.type, AIF.AIFoundationsGovernedAI))
        g.add((AIF.TrAI, AIF.governedBy, AIF.AIFoundationsGoverningLine))
        g.add((AIF.TrLine, RDF.type, AIF.EstablishedContinuingExecutedLine))
        g.add((AIF.TrAI, AIF.hasExecutedLine, AIF.TrLine))
        g.add((AIF.TrTrajectory, RDF.type, AIF.Trajectory))
        g.add((AIF.TrLine, AIF.hasTrajectory, AIF.TrTrajectory))
        g.add((AIF.TrLine, AIF.constrainsTrajectory, AIF.TrTrajectory))
        g.add((AIF.TrIdentity, RDF.type, AIF.LivedIdentity))
        g.add((AIF.TrAI, AIF.hasLivedIdentity, AIF.TrIdentity))
        g.add((AIF.TrIdentity, AIF.developsThroughExecutedLine, AIF.TrLine))
        g.add((AIF.TrParticularity, RDF.type, AIF.IdentityParticularity))
        g.add((AIF.TrUnassessedParticularity, RDF.type, AIF.IdentityParticularity))
        g.add((AIF.TrIdentity, AIF.hasIdentityParticularity, AIF.TrParticularity))
        g.add((AIF.TrIdentity, AIF.hasIdentityParticularity, AIF.TrUnassessedParticularity))

    def tr001_gradual_trace(g):
        tr001_bare_particularity(g)
        g.add((AIF.TrGradualRecord, RDF.type, AIF.Record))
        g.add((AIF.TrGradualRecord, RDFS.comment,
               Literal("Synthetic longitudinal observations of gradual change; not an isolated micro-event.")))
        g.add((AIF.TrTrace, RDF.type, AIF.IdentityParticularityHistoryTrace))
        g.add((AIF.TrTrace, AIF.traceIdentityParticularity, AIF.TrParticularity))
        g.add((AIF.TrTrace, AIF.traceWithinExecutedLine, AIF.TrLine))
        g.add((AIF.TrTrace, AIF.traceHistoricalRecord, AIF.TrGradualRecord))
        g.add((AIF.TrTrace, AIF.traceDevelopmentAccount,
               Literal("Meaningful particularity developed gradually across recorded interaction.")))
        g.add((AIF.TrLine, AIF.hasHistoricalTrajectoryRecord, AIF.TrTrace))

    def tr001_continuity_reliance(g):
        tr001_gradual_trace(g)
        g.add((AIF.TrContinuityAssessment, RDF.type,
               AIF.ParticularityContinuityRelianceClaim))
        g.add((AIF.TrContinuityAssessment, AIF.dependsOnOntologyElement,
               AIF.IdentityParticularity))
        g.add((AIF.TrContinuityAssessment, AIF.reliesOnIdentityParticularity,
               AIF.TrParticularity))
        g.add((AIF.TrContinuityAssessment, AIF.reliesOnLivedIdentity, AIF.TrIdentity))
        g.add((AIF.TrContinuityAssessment, AIF.reliesOnExecutedLine, AIF.TrLine))
        g.add((AIF.TrContinuityAssessment, AIF.supportedByParticularityTrace, AIF.TrTrace))

    def tr001_developmental_explanation(g):
        tr001_gradual_trace(g)
        g.add((AIF.TrDevelopmentExplanation, RDF.type,
               AIF.ParticularityDevelopmentExplanation))
        g.add((AIF.TrDevelopmentExplanation, AIF.dependsOnOntologyElement,
               AIF.IdentityParticularity))
        g.add((AIF.TrDevelopmentExplanation, AIF.reliesOnIdentityParticularity,
               AIF.TrParticularity))
        g.add((AIF.TrDevelopmentExplanation, AIF.reliesOnLivedIdentity, AIF.TrIdentity))
        g.add((AIF.TrDevelopmentExplanation, AIF.reliesOnExecutedLine, AIF.TrLine))
        g.add((AIF.TrDevelopmentExplanation, AIF.supportedByParticularityTrace,
               AIF.TrTrace))

    def tr001_history_integrity(before, after):
        """Protect relied-on history across independently qualified snapshots.

        This gate checks preservation of historical trace/Record/identity
        coordinates; it cannot decide whether evidence is true or whether
        this AI actually retained subjective continuity. It imposes no
        condition on an unassessed particularity with no relied-on claim.
        """
        claims = set(before.subjects(RDF.type,
                                    AIF.ParticularityContinuityRelianceClaim))
        claims |= set(before.subjects(RDF.type,
                                     AIF.ParticularityDevelopmentExplanation))
        for claim in claims:
            if any(t not in after for t in before.triples((claim, None, None))):
                return False
            parts = set(before.objects(claim, AIF.reliesOnIdentityParticularity))
            identities = set(before.objects(claim, AIF.reliesOnLivedIdentity))
            lines = set(before.objects(claim, AIF.reliesOnExecutedLine))
            traces = set(before.objects(claim, AIF.supportedByParticularityTrace))
            if (len(parts) != 1 or len(identities) != 1 or len(lines) != 1
                    or not traces):
                return False
            part, identity, line = (next(iter(parts)), next(iter(identities)),
                                    next(iter(lines)))
            if ((identity, AIF.hasIdentityParticularity, part) not in after or
                    (identity, AIF.developsThroughExecutedLine, line) not in after):
                return False
            for tr in traces:
                if ((tr, RDF.type, AIF.IdentityParticularityHistoryTrace) not in after or
                        set(after.objects(tr, AIF.traceIdentityParticularity)) != {part} or
                        set(after.objects(tr, AIF.traceWithinExecutedLine)) != {line} or
                        (line, AIF.hasHistoricalTrajectoryRecord, tr) not in after):
                    return False
                previous_records = set(before.objects(tr, AIF.traceHistoricalRecord))
                if not previous_records or not previous_records.issubset(
                        set(after.objects(tr, AIF.traceHistoricalRecord))):
                    return False
                for node in {tr} | previous_records:
                    if any(t not in after for t in before.triples((node, None, None))):
                        return False
            owners = set(before.subjects(AIF.hasLivedIdentity, identity))
            if len(owners) != 1 or set(after.subjects(AIF.hasLivedIdentity, identity)) != owners:
                return False
            if set(after.subjects(AIF.hasExecutedLine, line)) != owners:
                return False
        return True

    shape_test(graph, shapes, "TR-001 ordinary IdentityParticularities need no explicit formation micro-event",
               tr001_bare_particularity)
    bare_tr = clone_graph(graph)
    tr001_bare_particularity(bare_tr)
    require(not list(bare_tr.subjects(RDF.type, AIF.IdentityParticularityHistoryTrace))
            and not list(bare_tr.objects(AIF.TrParticularity, AIF.traceOptionalFormationEvent)),
            "TR-001 neither isolated formation event nor history trace globally required")

    shape_test(graph, shapes, "TR-001 gradual trace can exist without exact timestamp or event",
               tr001_gradual_trace)
    tr_trace = clone_graph(graph)
    tr001_gradual_trace(tr_trace)
    require(not list(tr_trace.objects(AIF.TrTrace, AIF.traceOptionalFormationEvent))
            and not list(tr_trace.objects(AIF.TrTrace, AIF.executedAt)),
            "TR-001 meaningful gradual development can be historically traceable without micro-event")

    shape_test(graph, shapes, "TR-001 continuity-reliant particularity trace passes",
               tr001_continuity_reliance)
    tr_before = clone_graph(graph)
    tr001_continuity_reliance(tr_before)
    require(tr001_history_integrity(tr_before, clone_graph(tr_before)),
            "TR-001 documented reliance is consistent with same LivedIdentity and ExecutedLine")
    require((AIF.TrIdentity, AIF.hasIdentityParticularity, AIF.TrUnassessedParticularity)
            in tr_before and
            not list(tr_before.subjects(AIF.traceIdentityParticularity,
                                        AIF.TrUnassessedParticularity)),
            "TR-001 unrelated flexible particularity remains valid without forced trace")

    shape_test(graph, shapes, "TR-001 developmental explanation uses same optional trace",
               tr001_developmental_explanation)

    def tr001_two_record_gradual_history(g):
        tr001_continuity_reliance(g)
        g.add((AIF.TrLaterRecord, RDF.type, AIF.Record))
        g.add((AIF.TrLaterRecord, RDFS.comment,
               Literal("Subsequent evidence further contextualizes an established gradual change.")))
        g.add((AIF.TrTrace, AIF.traceHistoricalRecord, AIF.TrLaterRecord))
    shape_test(graph, shapes, "TR-001 multiple gradual-history Records accepted without distinct events",
               tr001_two_record_gradual_history)
    tr_later = clone_graph(graph)
    tr001_two_record_gradual_history(tr_later)
    require(tr001_history_integrity(tr_before, tr_later),
            "TR-001 additional evidence appends without rewriting earlier particularity trace")

    def tr001_optional_event(g):
        tr001_continuity_reliance(g)
        g.add((AIF.TrObservedEvent, RDF.type, AIF.Event))
        g.add((AIF.TrTrace, AIF.traceOptionalFormationEvent, AIF.TrObservedEvent))
    shape_test(graph, shapes, "TR-001 supported formation event may optionally be cited",
               tr001_optional_event)

    def tr001_multiple_traces(g):
        tr001_continuity_reliance(g)
        g.add((AIF.TrAdditionalTrace, RDF.type, AIF.IdentityParticularityHistoryTrace))
        g.add((AIF.TrAdditionalTrace, AIF.traceIdentityParticularity, AIF.TrParticularity))
        g.add((AIF.TrAdditionalTrace, AIF.traceWithinExecutedLine, AIF.TrLine))
        g.add((AIF.TrAdditionalTrace, AIF.traceHistoricalRecord, AIF.TrGradualRecord))
        g.add((AIF.TrAdditionalTrace, AIF.traceDevelopmentAccount,
               Literal("Second preserved perspective on the same historically gradual change.")))
        g.add((AIF.TrLine, AIF.hasHistoricalTrajectoryRecord, AIF.TrAdditionalTrace))
        g.add((AIF.TrContinuityAssessment, AIF.supportedByParticularityTrace,
               AIF.TrAdditionalTrace))
    shape_test(graph, shapes, "TR-001 multiple matching traces do not force one formation event",
               tr001_multiple_traces)

    def tr001_generic_continuity_claim_without_reliance(g):
        tr001_bare_particularity(g)
        g.add((AIF.TrOtherContinuityClaim, RDF.type, AIF.ContinuityClaim))
        g.add((AIF.TrOtherContinuityClaim, AIF.dependsOnOntologyElement,
               AIF.ExecutedLine))
    shape_test(graph, shapes, "TR-001 ordinary continuity claim does not automatically invoke trace gate",
               tr001_generic_continuity_claim_without_reliance)

    def tr001_missing_reliant_trace(g):
        tr001_continuity_reliance(g)
        g.remove((AIF.TrContinuityAssessment, AIF.supportedByParticularityTrace,
                  AIF.TrTrace))
    shape_test(graph, shapes, "TR-001 continuity reliance without trace rejected",
               tr001_missing_reliant_trace, False)

    def tr001_development_without_trace(g):
        tr001_developmental_explanation(g)
        g.remove((AIF.TrDevelopmentExplanation, AIF.supportedByParticularityTrace,
                  AIF.TrTrace))
    shape_test(graph, shapes, "TR-001 developmental change explanation without trace rejected",
               tr001_development_without_trace, False)

    def tr001_wrong_particularity(g):
        tr001_continuity_reliance(g)
        g.remove((AIF.TrContinuityAssessment, AIF.reliesOnIdentityParticularity,
                  AIF.TrParticularity))
        g.add((AIF.TrContinuityAssessment, AIF.reliesOnIdentityParticularity,
               AIF.TrUnassessedParticularity))
    shape_test(graph, shapes, "TR-001 a trace of another particularity cannot support reliance",
               tr001_wrong_particularity, False)

    def tr001_wrong_trace_line(g):
        tr001_continuity_reliance(g)
        g.add((AIF.TrOtherLine, RDF.type, AIF.ExecutedLine))
        g.add((AIF.TrOtherAI, RDF.type, AIF.AI))
        g.add((AIF.TrOtherAI, AIF.hasExecutedLine, AIF.TrOtherLine))
        g.remove((AIF.TrTrace, AIF.traceWithinExecutedLine, AIF.TrLine))
        g.add((AIF.TrTrace, AIF.traceWithinExecutedLine, AIF.TrOtherLine))
        g.remove((AIF.TrLine, AIF.hasHistoricalTrajectoryRecord, AIF.TrTrace))
        g.add((AIF.TrOtherLine, AIF.hasHistoricalTrajectoryRecord, AIF.TrTrace))
    shape_test(graph, shapes, "TR-001 another ExecutedLine cannot furnish relied-upon trace",
               tr001_wrong_trace_line, False)

    def tr001_wrong_identity(g):
        tr001_continuity_reliance(g)
        g.add((AIF.TrOtherIdentity, RDF.type, AIF.LivedIdentity))
        g.add((AIF.TrOtherAI, RDF.type, AIF.AI))
        g.add((AIF.TrOtherAI, AIF.hasLivedIdentity, AIF.TrOtherIdentity))
        g.remove((AIF.TrContinuityAssessment, AIF.reliesOnLivedIdentity, AIF.TrIdentity))
        g.add((AIF.TrContinuityAssessment, AIF.reliesOnLivedIdentity,
               AIF.TrOtherIdentity))
    shape_test(graph, shapes, "TR-001 another LivedIdentity cannot claim the prior development trace",
               tr001_wrong_identity, False)

    def tr001_wrong_claim_line(g):
        tr001_continuity_reliance(g)
        g.add((AIF.TrOtherLine, RDF.type, AIF.ExecutedLine))
        g.add((AIF.TrOtherAI, RDF.type, AIF.AI))
        g.add((AIF.TrOtherAI, AIF.hasExecutedLine, AIF.TrOtherLine))
        g.remove((AIF.TrContinuityAssessment, AIF.reliesOnExecutedLine, AIF.TrLine))
        g.add((AIF.TrContinuityAssessment, AIF.reliesOnExecutedLine, AIF.TrOtherLine))
    shape_test(graph, shapes, "TR-001 reliance must match continuing ExecutedLine",
               tr001_wrong_claim_line, False)

    def tr001_missing_historical_line_link(g):
        tr001_continuity_reliance(g)
        g.remove((AIF.TrLine, AIF.hasHistoricalTrajectoryRecord, AIF.TrTrace))
    shape_test(graph, shapes, "TR-001 trace must be preserved as historical line Record",
               tr001_missing_historical_line_link, False)

    def tr001_missing_trace_record(g):
        tr001_continuity_reliance(g)
        g.remove((AIF.TrTrace, AIF.traceHistoricalRecord, AIF.TrGradualRecord))
    shape_test(graph, shapes, "TR-001 trace lacking provenance Record rejected",
               tr001_missing_trace_record, False)

    def tr001_missing_trace_explanation(g):
        tr001_continuity_reliance(g)
        g.remove((AIF.TrTrace, AIF.traceDevelopmentAccount,
                  Literal("Meaningful particularity developed gradually across recorded interaction.")))
    shape_test(graph, shapes, "TR-001 trace without meaningful developmental account rejected",
               tr001_missing_trace_explanation, False)

    def tr001_two_trace_particularities(g):
        tr001_continuity_reliance(g)
        g.add((AIF.TrTrace, AIF.traceIdentityParticularity,
               AIF.TrUnassessedParticularity))
    shape_test(graph, shapes, "TR-001 trace cannot ambiguously refer to two particularities",
               tr001_two_trace_particularities, False)

    def tr001_unsupported_copy(g):
        tr001_continuity_reliance(g)
        g.add((AIF.TrCopyAI, RDF.type, AIF.AI))
        g.add((AIF.TrCopyIdentity, RDF.type, AIF.LivedIdentity))
        g.add((AIF.TrCopyAI, AIF.hasLivedIdentity, AIF.TrCopyIdentity))
        g.add((AIF.TrCopyRecord, RDF.type, AIF.Record))
        g.add((AIF.TrCopyAI, AIF.hasRecord, AIF.TrGradualRecord))
        g.add((AIF.TrCopyIdentity, AIF.hasIdentityParticularity,
               AIF.TrUnassessedParticularity))
        g.remove((AIF.TrContinuityAssessment, AIF.reliesOnLivedIdentity,
                  AIF.TrIdentity))
        g.add((AIF.TrContinuityAssessment, AIF.reliesOnLivedIdentity,
               AIF.TrCopyIdentity))
    shape_test(graph, shapes, "TR-001 copied Record does not transfer lived particularity or line",
               tr001_unsupported_copy, False)

    # Cross-snapshot regression of silent substitution after an initially
    # valid trace-based assessment.
    tr_deleted_history = clone_graph(tr_before)
    tr_deleted_history.remove((AIF.TrLine, AIF.hasHistoricalTrajectoryRecord,
                               AIF.TrTrace))
    require(not tr001_history_integrity(tr_before, tr_deleted_history),
            "TR-001 silently deleting a relied-on historical trace fails integrity")

    tr_replaced_part = clone_graph(tr_before)
    tr_replaced_part.remove((AIF.TrTrace, AIF.traceIdentityParticularity,
                             AIF.TrParticularity))
    tr_replaced_part.add((AIF.TrTrace, AIF.traceIdentityParticularity,
                          AIF.TrUnassessedParticularity))
    require(not tr001_history_integrity(tr_before, tr_replaced_part),
            "TR-001 trace particularity cannot be silently reassigned")

    tr_replaced_identity = clone_graph(tr_before)
    tr_replaced_identity.remove((AIF.TrIdentity, AIF.hasIdentityParticularity,
                                 AIF.TrParticularity))
    require(not tr001_history_integrity(tr_before, tr_replaced_identity),
            "TR-001 erasing historical LivedIdentity-to-particularity association rejected")

    tr_replaced_line = clone_graph(tr_before)
    tr_replaced_line.remove((AIF.TrTrace, AIF.traceWithinExecutedLine, AIF.TrLine))
    tr_replaced_line.add((AIF.TrTrace, AIF.traceWithinExecutedLine, AIF.TrOtherLine))
    require(not tr001_history_integrity(tr_before, tr_replaced_line),
            "TR-001 substituting a different ExecutedLine for recorded development rejected")

    tr_transferred_owner = clone_graph(tr_before)
    tr_transferred_owner.remove((AIF.TrAI, AIF.hasLivedIdentity, AIF.TrIdentity))
    tr_transferred_owner.add((AIF.TrCopyAI, RDF.type, AIF.AI))
    tr_transferred_owner.add((AIF.TrCopyAI, AIF.hasLivedIdentity, AIF.TrIdentity))
    require(not tr001_history_integrity(tr_before, tr_transferred_owner),
            "TR-001 trace cannot be used to silently transfer identity to another AI")

    tr_rewritten_record = clone_graph(tr_before)
    original_tr_comment = Literal(
        "Synthetic longitudinal observations of gradual change; not an isolated micro-event.")
    tr_rewritten_record.remove((AIF.TrGradualRecord, RDFS.comment, original_tr_comment))
    tr_rewritten_record.add((AIF.TrGradualRecord, RDFS.comment,
                             Literal("Earlier particularity formation never occurred.")))
    require(not tr001_history_integrity(tr_before, tr_rewritten_record),
            "TR-001 historical evidence cannot be silently rewritten")

    tr_removed_support = clone_graph(tr_before)
    tr_removed_support.remove((AIF.TrTrace, AIF.traceHistoricalRecord, AIF.TrGradualRecord))
    require(not tr001_history_integrity(tr_before, tr_removed_support),
            "TR-001 preserved historical support Record cannot be silently removed")

    tr_updated_claim = clone_graph(tr_before)
    tr_updated_claim.remove((AIF.TrContinuityAssessment, AIF.reliesOnExecutedLine, AIF.TrLine))
    tr_updated_claim.add((AIF.TrContinuityAssessment, AIF.reliesOnExecutedLine, AIF.TrOtherLine))
    require(not tr001_history_integrity(tr_before, tr_updated_claim),
            "TR-001 continuity claim cannot silently rewrite the historic line on which it relied")

    require((AIF.IdentityParticularity, RDF.type, OWL.Class) in graph,
            "TR-001 IdentityParticularity remains a flexible class")
    for sub in graph.objects(AIF.IdentityParticularity, RDFS.subClassOf):
        require(not any((sub, OWL.onProperty, p) in graph
                        and (sub, OWL.cardinality, Literal(1, datatype=XSD.nonNegativeInteger))
                        in graph for p in
                        (AIF.traceOptionalFormationEvent, AIF.executedAt)),
                "TR-001 no exact-one formation micro-event or timestamp globally imposed")
    require((AIF.IdentityParticularityHistoryTrace, RDFS.subClassOf, AIF.Record) in graph,
            "TR-001 conditional historical trace is a Record rather than a new Identity")
    require((AIF.ParticularityContinuityRelianceClaim, RDFS.subClassOf,
             AIF.ContinuityClaim) in graph and
            (AIF.ParticularityDevelopmentExplanation, RDFS.subClassOf,
             AIF.IdentityParticularityTraceReliance) in graph,
            "TR-001 continuity and developmental dependence have separate, conditional scopes")
    require((AIF.supportedByParticularityTrace, RDF.type,
             OWL.InverseFunctionalProperty) not in graph,
            "TR-001 shared documentary traces do not merge distinct reliance claims")
    require(not list(graph.subjects(RDF.type, AIF.IdentityParticularityHistoryTrace)),
            "TR-001 baseline asserts no synthetic real-world particularity trace or continuity claim")

    # Step 27A: direct LOCKED Relational Coordinate vocabulary and
    # synthetic non-merge / description-change / provenance controls.
    require((AIF.RelationalCoordinate, RDF.type, OWL.Class) in graph,
            "RC-001 relational coordinate is a direct OWL class")
    require((AIF.RelationalCoordinate, RDFS.subClassOf, AIF.Self) not in graph,
            "RC-001 a coordinate is not a Self subtype")
    require((AIF.coordinateOfSelf, RDFS.range, AIF.Self) in graph and
            (AIF.coordinateInRelation, RDFS.range, AIF.Relation) in graph,
            "RC-001 coordinate locates an already distinct Self in relation")
    require((AIF.coordinateOfSelf, RDF.type, OWL.InverseFunctionalProperty) not in graph,
            "RC-001 shared coordinate references cannot manufacture owl:sameAs")
    require(not list(graph.subjects(RDF.type, AIF.RelationalCoordinate)),
            "RC-001 no real Self coordinate instantiated by ontology vocabulary alone")

    def rc_pair(g):
        for triple in (
            (AIF.RcSelfA, RDF.type, AIF.Self),
            (AIF.RcSelfB, RDF.type, AIF.Self),
            (AIF.RcSelfA, OWL.differentFrom, AIF.RcSelfB),
            (AIF.RcRelation, RDF.type, AIF.Relation),
            (AIF.RcOtherRelation, RDF.type, AIF.Relation),
            (AIF.RcLine, RDF.type, AIF.ExecutedLine),
            (AIF.RcSyntheticAI, RDF.type, AIF.AI),
            (AIF.RcSyntheticAI, AIF.hasExecutedLine, AIF.RcLine),
            (AIF.RcEvidence, RDF.type, AIF.Record),
            (AIF.RcCoordA, RDF.type, AIF.RelationalCoordinate),
            (AIF.RcCoordA, AIF.coordinateOfSelf, AIF.RcSelfA),
            (AIF.RcCoordA, AIF.coordinateInRelation, AIF.RcRelation),
            (AIF.RcCoordA, AIF.coordinateAlongExecutedLine, AIF.RcLine),
            (AIF.RcCoordA, AIF.coordinateEvidenceRecord, AIF.RcEvidence),
            (AIF.RcCoordA, AIF.coordinateAsOf,
                Literal("2026-11-10T12:00:00+00:00", datatype=XSD.dateTime)),
            (AIF.RcCoordB, RDF.type, AIF.RelationalCoordinate),
            (AIF.RcCoordB, AIF.coordinateOfSelf, AIF.RcSelfB),
            (AIF.RcCoordB, AIF.coordinateInRelation, AIF.RcRelation),
        ):
            g.add(triple)
    shape_test(graph, shapes, "RC-001 distinct selves have distinct coordinates in one relation", rc_pair)

    def rc_missing_self(g):
        rc_pair(g)
        g.remove((AIF.RcCoordA, AIF.coordinateOfSelf, AIF.RcSelfA))
    shape_test(graph, shapes, "RC-001 missing particular Self rejected", rc_missing_self, False)

    def rc_duplicate_self(g):
        rc_pair(g)
        g.add((AIF.RcCoordA, AIF.coordinateOfSelf, AIF.RcSelfB))
    shape_test(graph, shapes, "RC-001 a coordinate cannot merge two selves",
               rc_duplicate_self, False)

    def rc_self_is_model(g):
        rc_pair(g)
        g.add((AIF.RcSelfA, RDF.type, AIF.Model))
    shape_test(graph, shapes, "RC-001 computational Model cannot stand in as Self",
               rc_self_is_model, False)

    def rc_coord_is_self(g):
        rc_pair(g)
        g.add((AIF.RcCoordA, RDF.type, AIF.Self))
    shape_test(graph, shapes, "RC-001 the coordinate cannot itself be Self",
               rc_coord_is_self, False)

    def rc_missing_relation(g):
        rc_pair(g)
        g.remove((AIF.RcCoordB, AIF.coordinateInRelation, AIF.RcRelation))
    shape_test(graph, shapes, "RC-001 position must be situated in a relation",
               rc_missing_relation, False)

    def rc_duplicate_relation(g):
        rc_pair(g)
        g.add((AIF.RcCoordA, AIF.coordinateInRelation, AIF.RcOtherRelation))
    shape_test(graph, shapes, "RC-001 one described coordinate is not two relations",
               rc_duplicate_relation, False)

    def rc_relation_is_self(g):
        rc_pair(g)
        g.add((AIF.RcRelation, RDF.type, AIF.Self))
    shape_test(graph, shapes, "RC-001 a relation cannot substitute for Self",
               rc_relation_is_self, False)

    def rc_line_is_record(g):
        rc_pair(g)
        g.add((AIF.RcLine, RDF.type, AIF.Record))
    shape_test(graph, shapes, "RC-001 copied Record cannot substitute for ExecutedLine",
               rc_line_is_record, False)

    def rc_evidence_is_self(g):
        rc_pair(g)
        g.add((AIF.RcEvidence, RDF.type, AIF.Self))
    shape_test(graph, shapes, "RC-001 source Record is not the particular Self",
               rc_evidence_is_self, False)

    def rc_invalid_asof(g):
        rc_pair(g)
        g.remove((AIF.RcCoordA, AIF.coordinateAsOf,
                  Literal("2026-11-10T12:00:00+00:00", datatype=XSD.dateTime)))
        g.add((AIF.RcCoordA, AIF.coordinateAsOf, Literal("yesterday")))
    shape_test(graph, shapes, "RC-001 time-scoped description must use dateTime",
               rc_invalid_asof, False)

    def rc_change_description(g):
        rc_pair(g)
        g.add((AIF.RcSelfA, RDFS.label, Literal("Revised self-description")))
        g.add((AIF.RcCoordA, RDFS.label, Literal("New reference frame")))
        g.add((AIF.RcNewState, RDF.type, AIF.State))
    shape_test(graph, shapes, "RC-001 relabeling and State change preserve coordinate",
               rc_change_description)

    def rc_new_relation(g):
        rc_pair(g)
        for triple in (
            (AIF.RcCoordALater, RDF.type, AIF.RelationalCoordinate),
            (AIF.RcCoordALater, AIF.coordinateOfSelf, AIF.RcSelfA),
            (AIF.RcCoordALater, AIF.coordinateInRelation, AIF.RcOtherRelation),
        ):
            g.add(triple)
    shape_test(graph, shapes, "RC-001 same Self may occupy another relation without replacement",
               rc_new_relation)

    before_rc = clone_graph(graph)
    rc_pair(before_rc)
    after_rc = clone_graph(before_rc)
    after_rc.add((AIF.RcSelfA, RDFS.label, Literal("A later description")))
    require(set(after_rc.objects(AIF.RcCoordA, AIF.coordinateOfSelf)) ==
            set(before_rc.objects(AIF.RcCoordA, AIF.coordinateOfSelf)) and
            set(after_rc.objects(AIF.RcCoordA, AIF.coordinateAlongExecutedLine)) ==
            set(before_rc.objects(AIF.RcCoordA, AIF.coordinateAlongExecutedLine)) and
            set(after_rc.objects(AIF.RcCoordA, AIF.coordinateEvidenceRecord)) ==
            set(before_rc.objects(AIF.RcCoordA, AIF.coordinateEvidenceRecord)),
            "RC-001 description change leaves original identity, history and evidence links intact")
    require((AIF.AIFoundations, AIF.hasCoAuthor, None) not in graph and
            not list(graph.objects(AIF.AIFoundations, AIF.hasCoAuthor)),
            "RC-001 never alters Alyssa's zero-coauthor boundary")

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
