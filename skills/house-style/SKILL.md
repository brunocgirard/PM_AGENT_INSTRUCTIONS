---
name: house-style
description: The company's living house style — how a senior PM writes, structures documents, and reasons. Other skills apply this before drafting so every output matches the senior PM's voice, structure, and analytical rigor. Also runs the INGEST LOOP: when the user uploads a senior-PM document, it redacts it, extracts voice/structure/reasoning patterns, reconciles them against the existing kit (add new, reinforce, or flag conflicts preferring the most recent source), updates the style guide/templates/glossary, and appends an ingest-log entry. Grows and sharpens over time. Triggers include apply house style, learn from this doc, ingest this, update my style guide, make it sound like us.
---

## Style Guide
*(grows on ingest — rules below are LOW-CONFIDENCE defaults; ingested rules overwrite them)*

**Voice & tone**
- Lead every document and every section with a one-line RAG/bottom-line verdict before any detail. [LOW CONFIDENCE — default]
- Write at an 8th-grade reading level: short sentences, plain words, no jargon without definition. [LOW CONFIDENCE — default]
- Active voice preferred; passive only when the actor is irrelevant or unknown. [LOW CONFIDENCE — default]
- Quantify every claim: replace "significantly delayed" with "delayed 3 weeks (CPI 0.87)". [LOW CONFIDENCE — default]
- Pair every risk statement with its mitigation owner and due date; no naked risks. [LOW CONFIDENCE — default]

**Formatting**
- Status reports ≤ 1 page; escalation memos ≤ 2 pages. [LOW CONFIDENCE — default]
- Decisions and asks in **bold** on their own line. [LOW CONFIDENCE — default]
- Tables for anything with ≥ 3 comparable data points; no prose lists masquerading as analysis. [LOW CONFIDENCE — default]
- Dates in ISO format (YYYY-MM-DD); currency with explicit unit (CAD $, USD $). [LOW CONFIDENCE — default]
- Heading hierarchy: H2 for major sections, H3 for sub-sections; no H4+ in standard deliverables. [LOW CONFIDENCE — default]

**Confidence scale**: LOW = seen in ≤ 2 docs or inferred; MEDIUM = 3–5 docs; HIGH = 6+ docs, no conflict.

---

## Do / Don't

**Do**
- Open with the verdict, then the evidence.
- Name one owner per action item.
- State thresholds explicitly ("escalate if SPI < 0.90 for two consecutive weeks").
- Use the glossary terms from `references/glossary.md` consistently.
- Archive every ingested doc in `references/exemplars/` (redacted, annotated, ≤ 3 per type).

**Don't**
- Bury the RAG status in paragraph 3.
- Use hedging filler: "it seems," "perhaps," "going forward."
- List risks without mitigations.
- Mix tenses within a section.
- Silently overwrite a rule when a new doc conflicts — flag it instead.
- Ingest any document before redacting names, dollar amounts, and client identifiers.

---

## Analysis Rubric
*How the senior PM reasons before writing. Run these steps in order.*

1. **Baseline check** — Confirm scope, schedule, and cost baselines are current. If stale, flag before proceeding. Threshold: baseline age > 30 days = flag.
2. **Variance scan** — Calculate SPI and CPI. Threshold: SPI < 0.95 or CPI < 0.95 = amber; < 0.85 = red.
3. **Risk pulse** — Review top-5 risks; check if any trigger conditions have materialized. Any triggered risk = immediate escalation note.
4. **Decision queue** — List open decisions blocking ≥ 1 workstream. No decision should be open > 5 business days without an escalation path.
5. **Stakeholder signal** — Note any change in sponsor/client sentiment since last report. Qualitative but must be named ("CFO expressed concern about timeline on 2026-06-10").
6. **Bottom-line verdict** — Synthesize steps 1–5 into one RAG sentence with the primary driver. This becomes the document's first line.
7. **Cut test** — Remove anything that does not change the reader's decision or understanding. If a section survives only as "nice to have," cut it.

Decision thresholds summary:

| Signal | Amber | Red | PM Action |
|---|---|---|---|
| SPI | < 0.95 | < 0.85 | Report + recovery plan |
| CPI | < 0.95 | < 0.85 | Report + reforecast |
| Risk triggered | — | Any | Escalate same day |
| Decision overdue | > 5 days | > 10 days | Escalate to sponsor |

---

## Ingest Loop
*Run this procedure each time the user uploads a senior-PM document.*

**Step 1 — Drop file**
Place the document in `skills/house-style/references/inbox/`.

**Step 2 — Redact BEFORE anything else**
Remove or replace: full names → [NAME], dollar amounts → [AMOUNT], client/project identifiers → [CLIENT], any PII. Do this before storing the file or sending it to any model. The redacted version is the only version that enters the workflow.

**Step 3 — Observe (extract candidate patterns)**
Run `python skills/house-style/scripts/observe.py` to confirm the file is in inbox. Then feed the redacted doc to each of the three prompts in `references/extraction-prompts.md` (style-guide extraction, structural-template extraction, analysis-rubric extraction). Collect the candidate rules and confidence ratings the LLM returns.

**Step 4 — Reconcile vs existing kit**
For each candidate rule:
- **New** (no matching rule exists) → add to style guide / template / glossary with confidence from extraction.
- **Reinforcing** (matches an existing rule) → bump that rule's confidence level by one tier.
- **Conflicting** (contradicts an existing rule) → DO NOT silently overwrite. Log the conflict in `references/ingest-log.md` with both versions. Prefer the more recent document's version as the working default, but mark it CONTESTED and keep both until a human ratifies.

**Step 5 — Write back**
Update `SKILL.md` style guide section, the relevant template in `references/templates/`, and `references/glossary.md` with accepted changes.
Then record the ingest via:
```
python skills/house-style/scripts/improve.py "YYYY-MM-DD" "filename (redacted)" "added: X; reinforced: Y; conflict: Z"
```

**Step 6 — Promote exemplars**
If the document is high quality (HIGH-confidence rules, clean structure), move the redacted + annotated version to `references/exemplars/`. Keep ≤ 3 exemplars per document type; replace the weakest when at capacity.

**Confidence rule**: a pattern graduates from LOW to MEDIUM after recurring in ≥ 3 independent documents; MEDIUM to HIGH after ≥ 6. A single high-authority document (e.g., a ratified PMO standard) may fast-track to MEDIUM on human sign-off.

---

## Quality Gates

- **Triangulate**: a pattern becomes a firm (HIGH-confidence) rule only after it recurs across ≥ 3 independent documents. Do not enshrine one-doc patterns without explicit human ratification.
- **Source quality filter**: do not ingest draft documents, unchecked AI outputs, or documents flagged as low-quality by the author. Note the source quality in the ingest-log entry.
- **Expert interview**: when extraction yields LOW-confidence or CONTESTED rules, schedule a 30-minute interview with the senior PM to capture tacit reasoning not visible in the text.
- **Periodic human ratification**: review all CONTESTED and LOW-confidence rules quarterly. A human must approve before they are promoted or deleted.
- **No silent overwrites**: every change to an existing rule must be traceable to an ingest-log entry.
