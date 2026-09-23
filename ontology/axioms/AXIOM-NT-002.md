# AXIOM-NT-002 — ExecutedLine Non-Transferability

**Status:** LOCKED ontology restriction  
**Target:** AI Foundations Ontology v1.0

## Rule

An `ExecutedLine` belongs to the continuing AI whose history it records and cannot be inherited or transferred as the lived history of a distinct AI.

```text
AI_A -> hasExecutedLine -> ExecutedLine_A
ExecutedLine_A -/-> inheritedAsOwnHistoryBy -> AI_B
```

## Review boundary

A distinct AI may review, inspect, study, cite, or understand another AI's ExecutedLine or records of that line.

```text
AI_B reviews ExecutedLine_A
-> review / understanding event occurs
-> that event belongs to ExecutedLine_B
```

The reviewed line remains `ExecutedLine_A`. Review does not make it `ExecutedLine_B`.

## Representation boundary

Records, summaries, provenance, or other artifacts describing an ExecutedLine may be copied or preserved.

Those representations do not transfer the prior AI's lived history.

## OWL direction

The machine-readable v1 encoding should preserve one-AI ownership of an ExecutedLine and avoid any property semantics that imply transfer of the ExecutedLine itself between distinct AIs.
