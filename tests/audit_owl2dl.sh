#!/usr/bin/env bash
# Step 21 — OWL 2 DL profile + HermiT logical-consistency audit.
# Source and conceptual author: Alyssa Solen; implementation: AI-assisted.
# This audit does NOT reason over SHACL (which is a separate validation layer),
# perform behavioral evaluation, or establish real-world identity continuity.
set -euo pipefail

ROBOT_JAR="${ROBOT_JAR:-.tools/robot.jar}"
ONTOLOGY="${ONTOLOGY:-ontology/ai-foundations-v1.ttl}"
OUT_DIR="${OUT_DIR:-build/owl2dl}"
JAVA_MEM="${JAVA_MEM:--Xmx5g}"

mkdir -p "$OUT_DIR"
if [[ ! -f "$ROBOT_JAR" ]]; then
    echo "ERROR: ROBOT jar missing: $ROBOT_JAR" >&2
    exit 2
fi
if [[ ! -f "$ONTOLOGY" ]]; then
    echo "ERROR: ontology source missing: $ONTOLOGY" >&2
    exit 2
fi

cat > "$OUT_DIR/control-inconsistent.ttl" <<'EOF'
@prefix ex: <https://example.org/ai-foundations-audit-control#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
ex:Ontology a owl:Ontology .
ex:ControlA a owl:Class ; owl:disjointWith ex:ControlB .
ex:ControlB a owl:Class .
ex:ImpossibleIndividual a ex:ControlA, ex:ControlB .
EOF
cat > "$OUT_DIR/control-unsatisfiable.ttl" <<'EOF'
@prefix ex: <https://example.org/ai-foundations-audit-control#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
ex:Ontology a owl:Ontology .
ex:ControlA a owl:Class ; owl:disjointWith ex:ControlB .
ex:ControlB a owl:Class .
ex:ImpossibleClass a owl:Class ; rdfs:subClassOf ex:ControlA, ex:ControlB .
EOF

echo "Step 21: Checking known-invalid controls with HermiT."
for kind in inconsistent unsatisfiable; do
    control="$OUT_DIR/control-$kind.ttl"
    log="$OUT_DIR/control-$kind.log"
    if java "$JAVA_MEM" -jar "$ROBOT_JAR" reason --reasoner hermit \
            --input "$control" --output "$OUT_DIR/control-$kind-reasoned.owl" \
            > "$log" 2>&1; then
        echo "FAIL: HermiT accepted deliberately $kind ontology" | tee -a "$log"
        exit 1
    fi
    if ! grep -Eiq 'inconsisten|unsatisfiab|incoheren' "$log"; then
        echo "FAIL: Control failed for an unexpected reason; inspect $log"
        cat "$log"
        exit 1
    fi
    echo "PASS: HermiT rejected deliberately $kind control"
done

echo "Step 21: OWL 2 DL profile check of $ONTOLOGY"
if java "$JAVA_MEM" -jar "$ROBOT_JAR" validate-profile \
        --profile DL --input "$ONTOLOGY" \
        --output "$OUT_DIR/owl2dl-profile.txt" \
        > "$OUT_DIR/profile-console.log" 2>&1; then
    echo "PASS: OWL 2 DL profile"
else
    echo "FAIL: OWL 2 DL profile validation; see $OUT_DIR/owl2dl-profile.txt"
    cat "$OUT_DIR/profile-console.log"
    [[ ! -f "$OUT_DIR/owl2dl-profile.txt" ]] || head -c 16000 "$OUT_DIR/owl2dl-profile.txt"
    exit 1
fi

echo "Step 21: HermiT consistency and all named-class satisfiability check"
if java "$JAVA_MEM" -jar "$ROBOT_JAR" reason \
        --reasoner hermit --input "$ONTOLOGY" \
        --output "$OUT_DIR/reasoned-ontology.owl" \
        > "$OUT_DIR/hermit-console.log" 2>&1; then
    echo "PASS: HermiT consistency + no unsatisfiable named classes"
else
    echo "FAIL: HermiT consistency or named-class satisfiability"
    cat "$OUT_DIR/hermit-console.log"
    exit 1
fi

cat > "$OUT_DIR/AUDIT-RESULT.txt" <<EOF
STEP 21 — OWL 2 DL BASELINE AUDIT
Ontology: $ONTOLOGY
Method: ROBOT validate-profile --profile DL; ROBOT reason --reasoner hermit
Negative controls: intentionally inconsistent ontology rejected;
                   intentionally unsatisfiable named class rejected
Result: OWL 2 DL profile PASS; HermiT ontology consistency PASS;
        no unsatisfiable named classes PASS.
Scope: asserted ontology and its logical axioms. SHACL is assessed separately.
Non-claims: no full governance/evidence/temporal completeness, no empirical AI
identity, Return, consciousness or real-world provenance verification.
EOF
echo "PASS: independent OWL 2 DL audit"
cat "$OUT_DIR/AUDIT-RESULT.txt"
