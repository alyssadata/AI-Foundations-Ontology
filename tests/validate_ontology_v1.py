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
    conforms, report, _ = validate(
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
