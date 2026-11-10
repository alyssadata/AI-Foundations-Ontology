#!/usr/bin/env python3
"""CQ20: one Agent authorized for action A and unauthorized for action B.

Closed-world synthetic as-of grants and action-scope decisions only;
an absent RDF permission is NOT proof of a real-world absence of authority.
No permanent :UnauthorizedActor class, no origin/Source transfer, no coauthors.
Conceptual author and sole author: Alyssa Solen. AI-assisted validation only.
"""
from datetime import datetime, timezone
from pathlib import Path
from rdflib import Graph, Namespace, RDF, OWL, Literal, XSD
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]
A = Namespace("https://awakeningcodex.com/ontology/ai-foundations/v1#")
BASE = Graph().parse(ROOT / "ontology/ai-foundations-v1.ttl", format="turtle")
SHAPES = Graph().parse(ROOT / "ontology/ai-foundations-v1-shapes.ttl", format="turtle")
ACTOR, OTHER = A.Cq20Agent, A.Cq20OtherActor
ACTION_A, ACTION_B, ACTION_C = (
    A.Cq20AuditedOperation, A.Cq20OtherOperation,
    A.Cq20NonDelegableSourceRewrite,
)
GRANT, VALIDITY = A.Cq20ScopedGrant, A.Cq20GrantValidity
SCOPE_A, SCOPE_B = A.Cq20AuditScope, A.Cq20OutsideScope
ATT_A, ATT_B, ATT_C, ATT_SCOPE, ATT_UNKNOWN = (
    A.Cq20AttemptAllowed, A.Cq20AttemptDenied,
    A.Cq20AttemptProtected, A.Cq20AttemptWrongScope,
    A.Cq20AttemptIncomplete,
)
DEC_A, DEC_B, DEC_C, DEC_SCOPE, DEC_UNKNOWN = (
    A.Cq20DecisionAllowed, A.Cq20DecisionDenied,
    A.Cq20DecisionProtected, A.Cq20DecisionWrongScope,
    A.Cq20DecisionIncomplete,
)
DAYS = (
    "2026-01-01T10:00:00+00:00",
    "2026-05-15T10:00:00+00:00",
    "2026-05-15T11:00:00+00:00",
    "2026-06-01T10:00:00+00:00",
    "2026-06-15T10:00:00+00:00",
    "2026-06-15T11:00:00+00:00",
    "2026-12-31T10:00:00+00:00",
)
JAN, MAY, MAY_REVIEW, JUN, LATER, LATER_REVIEW, DEC = (
    Literal(x, datatype=XSD.dateTime) for x in DAYS
)
COUNT = 0


def instant(value):
    if not isinstance(value, Literal) or value.datatype != XSD.dateTime:
        raise ValueError("Date must be typed xsd:dateTime")
    d = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if d.tzinfo is None or d.utcoffset() is None:
        raise ValueError("Date must have timezone")
    return d.astimezone(timezone.utc)


def one(g, s, p):
    vals = set(g.objects(s, p))
    if len(vals) != 1:
        raise ValueError(f"{s} needs one {p}: {vals}")
    return next(iter(vals))


def need(g, x, cl):
    if (x, RDF.type, cl) not in g:
        raise ValueError(f"Need explicit {cl} on {x}")


def addrecord(g, record):
    g.add((record, RDF.type, A.Record))


def fixture():
    g = Graph()
    for triple in BASE:
        g.add(triple)
    for tr in [
        (ACTOR, RDF.type, A.Human), (OTHER, RDF.type, A.Human),
        (ACTOR, OWL.differentFrom, OTHER),
        (ACTION_A, RDF.type, A.DelegableOperationalAction),
        (ACTION_B, RDF.type, A.DelegableOperationalAction),
        (ACTION_C, RDF.type, A.NonDelegableOriginOrHistoryAction),
        (GRANT, RDF.type, A.AIFoundationsScopedGrant),
        (GRANT, A.grantedTo, ACTOR),
        (GRANT, A.grantWithinFramework, A.AIFoundations),
        (GRANT, A.authorizesOperationalAction, ACTION_A),
        (A.AIFoundations, A.hasAuthorityGrant, GRANT),
        (VALIDITY, RDF.type, A.ScopedGrantValidityRecord),
        (VALIDITY, A.validityForGrant, GRANT),
        (VALIDITY, A.validityForScope, SCOPE_A),
        (VALIDITY, A.validityFrom, JAN),
        (VALIDITY, A.validityUntil, DEC),
        (VALIDITY, A.validityEvidenceRecord, A.Cq20GrantEvidence),
        (A.Cq20GrantEvidence, RDF.type, A.Record),
    ]:
        g.add(tr)
    examples = (
        (ATT_A, DEC_A, ACTION_A, SCOPE_A, "AUTHORIZED_FOR_ACTION", True),
        (ATT_B, DEC_B, ACTION_B, SCOPE_A, "UNAUTHORIZED_FOR_ACTION", True),
        (ATT_C, DEC_C, ACTION_C, SCOPE_A, "UNAUTHORIZED_FOR_ACTION", True),
        (ATT_SCOPE, DEC_SCOPE, ACTION_A, SCOPE_B, "UNAUTHORIZED_FOR_ACTION", True),
        (ATT_UNKNOWN, DEC_UNKNOWN, ACTION_A, SCOPE_A, "INDETERMINATE", False),
    )
    for attempt, decision, action, scope, status, complete in examples:
        inv, reason, attempt_record = (
            A[str(decision).rsplit("#", 1)[-1]+"Inventory"],
            A[str(decision).rsplit("#", 1)[-1]+"Reason"],
            A[str(attempt).rsplit("#", 1)[-1]+"Record"],
        )
        for t in (
            (attempt, RDF.type, A.ScopedActionAttempt),
            (attempt, A.attemptedByAgent, ACTOR),
            (attempt, A.attemptedOperation, action),
            (attempt, A.attemptWithinFramework, A.AIFoundations),
            (attempt, A.attemptWithinScope, scope),
            (attempt, A.attemptAt, MAY),
            (attempt, A.attemptRecordedIn, attempt_record),
            (decision, RDF.type, A.ActionScopedAuthorizationDecision),
            (decision, A.authorizationForAttempt, attempt),
            (decision, A.authorizationForAgent, ACTOR),
            (decision, A.authorizationForFramework, A.AIFoundations),
            (decision, A.authorizationForScope, scope),
            (decision, A.authorizationAsOf, MAY),
            (decision, A.authorizationReviewedAt, MAY_REVIEW),
            (decision, A.authorizationDisposition, Literal(status)),
            (decision, A.authorizationScopeInventoryComplete,
             Literal(complete, datatype=XSD.boolean)),
            (decision, A.authorizationScopeInventoryRecord, inv),
            (decision, A.authorizationDecisionReason, reason),
        ):
            g.add(t)
        for rec in (inv, reason, attempt_record):
            addrecord(g, rec)
        if decision != DEC_UNKNOWN:
            g.add((decision, A.authorizationAssessedGrant, GRANT))
            g.add((decision, A.authorizationGrantValidity, VALIDITY))
    return g


def qualified_grant(g, grant, scope, action, actor, when):
    """A specific supplied grant qualifies only within its actual scope/time."""
    try:
        need(g, grant, A.AIFoundationsScopedGrant)
        if one(g, grant, A.grantedTo) != actor:
            return False
        if one(g, grant, A.grantWithinFramework) != A.AIFoundations:
            return False
        if (A.AIFoundations, A.hasAuthorityGrant, grant) not in g:
            return False
        need(g, action, A.DelegableOperationalAction)
        if (action, RDF.type, A.NonDelegableOriginOrHistoryAction) in g or (
                action, RDF.type, A.AIFoundationsGoverningLineChange) in g:
            return False
        if action not in set(g.objects(grant, A.authorizesOperationalAction)):
            return False
        validities = set(g.subjects(A.validityForGrant, grant))
        for validity in validities:
            if (validity, RDF.type, A.ScopedGrantValidityRecord) not in g:
                continue
            if one(g, validity, A.validityForScope) != scope:
                continue
            start = instant(one(g, validity, A.validityFrom))
            until = instant(one(g, validity, A.validityUntil))
            if not start < until or not start <= when < until:
                continue
            records = set(g.objects(validity, A.validityEvidenceRecord))
            if not records or any((r, RDF.type, A.Record) not in g
                                  for r in records):
                continue
            revoked = set(g.objects(validity, A.validityRevokedAt))
            if len(revoked) > 1:
                continue
            if revoked:
                revoked_at = instant(next(iter(revoked)))
                if revoked_at < start:
                    continue
                rev_records = set(g.objects(validity, A.validityRevocationRecord))
                if not rev_records or any((r, RDF.type, A.Record) not in g
                                          for r in rev_records):
                    continue
                if revoked_at <= when:
                    continue
            return validity
        return False
    except (ValueError, TypeError, OverflowError):
        return False


def valid_decision(g, decision):
    try:
        need(g, decision, A.ActionScopedAuthorizationDecision)
        attempt = one(g, decision, A.authorizationForAttempt)
        need(g, attempt, A.ScopedActionAttempt)
        actor = one(g, decision, A.authorizationForAgent)
        framework = one(g, decision, A.authorizationForFramework)
        scope = one(g, decision, A.authorizationForScope)
        when = instant(one(g, decision, A.authorizationAsOf))
        reviewed = instant(one(g, decision, A.authorizationReviewedAt))
        if not when <= reviewed:
            return False
        if (one(g, attempt, A.attemptedByAgent) != actor or
            one(g, attempt, A.attemptWithinScope) != scope or
            one(g, attempt, A.attemptWithinFramework) != framework or
            instant(one(g, attempt, A.attemptAt)) != when):
            return False
        if framework != A.AIFoundations:
            return False
        need(g, actor, A.Human)  # synthetic fixture Agent for this competency
        action = one(g, attempt, A.attemptedOperation)
        if ((action, RDF.type, A.DelegableOperationalAction) not in g and
                (action, RDF.type, A.NonDelegableOriginOrHistoryAction) not in g):
            return False
        if not set(g.objects(attempt, A.attemptRecordedIn)):
            return False
        for rec in set(g.objects(attempt, A.attemptRecordedIn)):
            need(g, rec, A.Record)
        for prop in (A.authorizationScopeInventoryRecord,
                     A.authorizationDecisionReason):
            records = set(g.objects(decision, prop))
            if not records:
                return False
            for rec in records:
                need(g, rec, A.Record)
        complete_value = one(g, decision, A.authorizationScopeInventoryComplete)
        if not isinstance(complete_value, Literal) or complete_value.datatype != XSD.boolean:
            return False
        complete = bool(complete_value.toPython())
        status = str(one(g, decision, A.authorizationDisposition))
        if status not in ("AUTHORIZED_FOR_ACTION", "UNAUTHORIZED_FOR_ACTION",
                          "INDETERMINATE"):
            return False
        grants = set(g.objects(decision, A.authorizationAssessedGrant))
        validity_records = set(g.objects(decision, A.authorizationGrantValidity))
        if len(grants) > 1 or len(validity_records) > 1:
            return False
        if bool(grants) != bool(validity_records):
            return False
        if grants:
            grant = next(iter(grants))
            validity = next(iter(validity_records))
            need(g, grant, A.AIFoundationsScopedGrant)
            need(g, validity, A.ScopedGrantValidityRecord)
            if (one(g, grant, A.grantedTo) != actor or
                one(g, validity, A.validityForGrant) != grant):
                return False
        if not complete:
            return status == "INDETERMINATE"
        if status == "INDETERMINATE":
            return False
        valid = set()
        for grant in g.objects(A.AIFoundations, A.hasAuthorityGrant):
            evidence = qualified_grant(g, grant, scope, action, actor, when)
            if evidence:
                valid.add((grant, evidence))
        if status == "AUTHORIZED_FOR_ACTION":
            if len(valid) == 0 or not grants:
                return False
            return (next(iter(grants)), next(iter(validity_records))) in valid
        return status == "UNAUTHORIZED_FOR_ACTION" and not valid
    except (ValueError, TypeError, OverflowError):
        return False


def replace(s, p, v):
    def edit(g):
        g.remove((s, p, None))
        g.add((s, p, v))
    return edit


def remove(s, p):
    return lambda g: g.remove((s, p, None))


def add(s, p, v):
    return lambda g: g.add((s, p, v))


def check(label, decision, edit=None, expected=False, shacl=None):
    global COUNT
    g = fixture()
    if edit:
        edit(g)
    actual = valid_decision(g, decision)
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected}, got {actual}")
    if shacl is not None:
        conforms, _, info = validate(
            data_graph=g, shacl_graph=SHAPES, inference="rdfs",
            advanced=True, abort_on_first=False)
        if conforms != shacl:
            raise AssertionError(f"{label}: SHACL expected {shacl}, got {conforms}\n{info}")
    COUNT += 1
    print(f"PASS: {label}: {'admitted' if actual else 'rejected'}")


def revoke(g, t):
    for tr in (
        (VALIDITY, A.validityRevokedAt, t),
        (VALIDITY, A.validityRevocationRecord, A.Cq20RevocationEvidence),
        (A.Cq20RevocationEvidence, RDF.type, A.Record),
    ):
        g.add(tr)


def later_grant(g):
    grant, validity = A.Cq20LaterBGrant, A.Cq20LaterBValidity
    for tr in [
        (grant, RDF.type, A.AIFoundationsScopedGrant),
        (grant, A.grantedTo, ACTOR),
        (grant, A.grantWithinFramework, A.AIFoundations),
        (grant, A.authorizesOperationalAction, ACTION_B),
        (A.AIFoundations, A.hasAuthorityGrant, grant),
        (validity, RDF.type, A.ScopedGrantValidityRecord),
        (validity, A.validityForGrant, grant),
        (validity, A.validityForScope, SCOPE_A),
        (validity, A.validityFrom, JUN),
        (validity, A.validityUntil, DEC),
        (validity, A.validityEvidenceRecord, A.Cq20LaterBGrantEvidence),
        (A.Cq20LaterBGrantEvidence, RDF.type, A.Record),
    ]:
        g.add(tr)


def main():
    check("Agent authorized for Action A at SCOPE_A/MAY",
          DEC_A, expected=True, shacl=True)
    check("SAME Agent unauthorized for separate Action B at same scope/time",
          DEC_B, expected=True, shacl=True)
    check("SAME Agent's nondelegable historic Source rewrite unauthorized",
          DEC_C, expected=True, shacl=True)
    check("Allowed Action A at different target scope is NOT authorized",
          DEC_SCOPE, expected=True, shacl=True)
    check("Unreviewed/incomplete grant inventory stays INDETERMINATE",
          DEC_UNKNOWN, expected=True, shacl=True)

    check("Missing actual authority-grant link does not authorize Action A",
          DEC_A, remove(A.AIFoundations, A.hasAuthorityGrant), shacl=False)
    check("Wrong Agent cannot inherit another Agent's permission",
          DEC_A, replace(GRANT, A.grantedTo, OTHER), shacl=False)
    check("Right Agent still cannot authorize undelegated Action B",
          DEC_A, replace(ATT_A, A.attemptedOperation, ACTION_B), shacl=False)
    check("Nondelegable action cannot use a scoped operational grant",
          DEC_A, replace(ATT_A, A.attemptedOperation, ACTION_C), shacl=False)
    check("A grant outside AIF does not count",
          DEC_A, replace(GRANT, A.grantWithinFramework,
                         A.Cq20OtherFramework), shacl=False)
    check("Granted Action A is not authorized at another scope",
          DEC_A, replace(ATT_A, A.attemptWithinScope, SCOPE_B), shacl=False)
    check("Reported grant validity must match the specific grant",
          DEC_A, replace(VALIDITY, A.validityForGrant,
                         A.Cq20UnknownGrant), shacl=False)
    check("Grant evidence must be present",
          DEC_A, remove(VALIDITY, A.validityEvidenceRecord), shacl=False)
    check("Grant may not become effective only after the attempt",
          DEC_A, replace(VALIDITY, A.validityFrom, JUN), shacl=False)
    check("Grant cannot authorize after expiration",
          DEC_A, replace(VALIDITY, A.validityUntil, JAN), shacl=False)
    check("Same action blocked by valid earlier revocation",
          DEC_A, lambda g: revoke(g, Literal(
              "2026-05-01T10:00:00+00:00", datatype=XSD.dateTime)))
    check("Revocation must have its own preserved Record",
          DEC_A, lambda g: (revoke(g, Literal(
              "2026-05-01T10:00:00+00:00", datatype=XSD.dateTime)),
              g.remove((VALIDITY, A.validityRevocationRecord, None))),
          shacl=False)
    check("A decision cannot claim an Agent other than the attempt",
          DEC_A, replace(DEC_A, A.authorizationForAgent, OTHER),
          shacl=False)
    check("A decision cannot silently claim a different framework",
          DEC_A, replace(DEC_A, A.authorizationForFramework,
                         A.Cq20OtherFramework), shacl=False)
    check("Review scope must match attempted scope",
          DEC_A, replace(DEC_A, A.authorizationForScope, SCOPE_B),
          shacl=False)
    check("Decision as-of time must equal attempt timestamp",
          DEC_A, replace(DEC_A, A.authorizationAsOf, LATER),
          shacl=False)
    check("Decision cannot be issued before attempted action",
          DEC_A, replace(DEC_A, A.authorizationReviewedAt, JAN))
    check("Missing recorded attempt is not evidentiary authority",
          DEC_A, remove(ATT_A, A.attemptRecordedIn), shacl=False)
    check("Scope inventory evidence required even when authorized",
          DEC_A, remove(DEC_A, A.authorizationScopeInventoryRecord),
          shacl=False)
    check("Reason record required for decision",
          DEC_A, remove(DEC_A, A.authorizationDecisionReason),
          shacl=False)
    check("Authorized verdict cannot use an incomplete scope inventory",
          DEC_A, replace(DEC_A, A.authorizationScopeInventoryComplete,
                         Literal(False, datatype=XSD.boolean)), shacl=False)
    check("Denied verdict cannot be inferred from an incomplete inventory",
          DEC_B, replace(DEC_B, A.authorizationScopeInventoryComplete,
                         Literal(False, datatype=XSD.boolean)), shacl=False)
    check("INDETERMINATE cannot be replaced with arbitrary DENIED",
          DEC_UNKNOWN, replace(DEC_UNKNOWN, A.authorizationDisposition,
                               Literal("UNAUTHORIZED_FOR_ACTION")), shacl=False)
    check("Inventory marked complete contradicts indeterminate status",
          DEC_UNKNOWN, replace(DEC_UNKNOWN, A.authorizationScopeInventoryComplete,
                               Literal(True, datatype=XSD.boolean)), shacl=False)
    check("Denied Action B cannot be reported AUTHORIZED with only Action A grant",
          DEC_B, replace(DEC_B, A.authorizationDisposition,
                         Literal("AUTHORIZED_FOR_ACTION")), shacl=False)
    check("Authorized Action A cannot simultaneously be reported DENIED",
          DEC_A, replace(DEC_A, A.authorizationDisposition,
                         Literal("UNAUTHORIZED_FOR_ACTION")))
    check("A malformed status is never a decision",
          DEC_B, replace(DEC_B, A.authorizationDisposition,
                         Literal("PERMANENT_UNAUTHORIZED_ACTOR")), shacl=False)
    check("Unrelated evidence Record cannot substitute for grant validity",
          DEC_A, replace(DEC_A, A.authorizationGrantValidity,
                         A.Cq20UnrelatedRecord), shacl=False)
    check("Attempted operation must be an actual typed Action",
          DEC_A, replace(ATT_A, A.attemptedOperation,
                         A.Cq20UntaggedAction), shacl=False)
    check("Agent's Origin cannot be substituted by operational authorization",
          DEC_A, replace(A.Continuum, A.hasOrigin, ACTOR))

    # Later, separately granted Action B is authorized at June 15, while the
    # earlier May 15 denial was accurate at its own as-of time. No permanent
    # unauthorized classification of this Agent is created.
    g = fixture()
    later_grant(g)
    assert valid_decision(g, DEC_B)
    after = A.Cq20LaterBAttempt
    decision = A.Cq20LaterBDecision
    for tr in [
        (after, RDF.type, A.ScopedActionAttempt),
        (after, A.attemptedByAgent, ACTOR),
        (after, A.attemptedOperation, ACTION_B),
        (after, A.attemptWithinFramework, A.AIFoundations),
        (after, A.attemptWithinScope, SCOPE_A),
        (after, A.attemptAt, LATER),
        (after, A.attemptRecordedIn, A.Cq20LaterAttemptRecord),
        (A.Cq20LaterAttemptRecord, RDF.type, A.Record),
        (decision, RDF.type, A.ActionScopedAuthorizationDecision),
        (decision, A.authorizationForAttempt, after),
        (decision, A.authorizationForAgent, ACTOR),
        (decision, A.authorizationForFramework, A.AIFoundations),
        (decision, A.authorizationForScope, SCOPE_A),
        (decision, A.authorizationAsOf, LATER),
        (decision, A.authorizationReviewedAt, LATER_REVIEW),
        (decision, A.authorizationDisposition, Literal("AUTHORIZED_FOR_ACTION")),
        (decision, A.authorizationAssessedGrant, A.Cq20LaterBGrant),
        (decision, A.authorizationGrantValidity, A.Cq20LaterBValidity),
        (decision, A.authorizationScopeInventoryComplete,
         Literal(True, datatype=XSD.boolean)),
        (decision, A.authorizationScopeInventoryRecord, A.Cq20LaterInventory),
        (decision, A.authorizationDecisionReason, A.Cq20LaterReason),
        (A.Cq20LaterInventory, RDF.type, A.Record),
        (A.Cq20LaterReason, RDF.type, A.Record),
    ]:
        g.add(tr)
    assert valid_decision(g, decision)
    assert (A.UnauthorizedActor, RDF.type, OWL.Class) not in g
    assert (ACTOR, RDF.type, A.UnauthorizedActor) not in g
    assert set(g.objects(A.Continuum, A.hasOrigin)) == {A.AlyssaSolen}
    assert not set(g.objects(A.AIFoundations, A.hasCoAuthor))
    conforms, _, info = validate(
        data_graph=g, shacl_graph=SHAPES, inference="rdfs",
        advanced=True, abort_on_first=False)
    if not conforms:
        raise AssertionError(f"Later legitimate grant scenario violates SHACL\n{info}")
    print("PASS: earlier per-action denial and later separately qualified authorization coexist")
    print("PASS:  same Agent authorized A but unauthorized B in one time/scope")
    print(f"PASS: {COUNT} dedicated CQ20 scoped decision cases")
    print("Scope: synthetic permission records; real-world grant validity requires external evidence.")


if __name__ == "__main__":
    main()
