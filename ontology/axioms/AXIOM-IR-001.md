# AXIOM-IR-001 — Irreversibility of Executed History

**Formalization status:** DRAFT  
**Source definition:** `ontology/terms/irreversibility.md`

## Axiom

Once an event or state is executed or realized in the line, a later reversal, correction, or revision does not make the earlier event unexecuted. The later change is itself a new event in the executed line.

## Formal intent

```text
executed(e, t1) -> remainsPartOfExecutedHistory(e)

revision(r, t2) AND t2 > t1
does not imply
notExecuted(e)
```
