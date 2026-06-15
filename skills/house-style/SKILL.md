---
name: house-style
description: The company's house style — how a senior PM writes, structures documents, and reasons. This is a reference/knowledge file the agent grounds on: other skills apply it before drafting so every output matches the senior PM's voice, structure, and analytical rigor. It captures voice/tone/formatting rules, a do/don't list, an analysis rubric, and a glossary. It is grown OFFLINE (a maintainer runs the extraction prompts on senior-PM documents, then re-uploads the updated file to the agent's Knowledge) — the agent does not run any ingest loop at runtime. Triggers include apply house style, review for style, rewrite in our style, does this match our voice, make it sound like us, match our house style.
---

This file is the company's house-style reference. The agent grounds on it; other skills apply it before drafting. It is not a procedure the agent runs — it is the learnings other outputs conform to.

## Style Guide
*(seeded — rules below are LOW-CONFIDENCE defaults; replace them with real learnings extracted from senior-PM documents)*

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

Each rule carries a confidence tier — see the canonical `## Confidence scale` below.

---

## Confidence scale
*(canonical — both the Style Guide and the offline update process reference this; do not duplicate elsewhere)*

- **LOW** — seen in ≤ 2 docs, or inferred. Working default only; never enshrined without ratification.
- **MEDIUM** — recurs across 3–5 independent docs. A single high-authority document (e.g. a ratified PMO standard) may fast-track straight to MEDIUM on human sign-off.
- **HIGH** — recurs across 6+ independent docs with no unresolved conflict.

---

## Do / Don't

**Do**
- Open with the verdict, then the evidence.
- Name one owner per action item.
- State thresholds explicitly ("escalate if SPI < 0.90 for two consecutive weeks").
- Use the glossary terms from `references/glossary.md` consistently.

**Don't**
- Bury the RAG status in paragraph 3.
- Use hedging filler: "it seems," "perhaps," "going forward."
- List risks without mitigations.
- Mix tenses within a section.

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

## How this file is grown (offline)
*This is a maintainer workflow, run offline (locally or in a chat) — NOT something the agent executes at runtime.*

1. **Collect & redact** — Gather senior-PM documents. Before anything else, redact names, dollar amounts, and client/project IDs. Work only from the redacted copies; do not retain unredacted originals.
2. **Extract** — Run the three prompts in `references/extraction-prompts.md` (style-guide, structural-template, analysis-rubric extraction) on each redacted document. Process one document at a time so candidate rules stay tied to a known source.
3. **Triangulate** — A pattern becomes a firm rule only after it recurs across ≥ 3 independent documents (see `## Confidence scale`; a ratified PMO standard may fast-track to MEDIUM on sign-off). Do not enshrine patterns from draft or low-quality documents.
4. **Reconcile** — Add new rules, reinforce matching ones, and on conflict prefer the version from the more recently AUTHORED document (compare by document date, not by when you processed it). Keep both versions noted until ratified; never silently overwrite.
5. **Write back** — Update this file's Style Guide / Do-Don't / Analysis Rubric, `references/glossary.md`, and any document templates (markdown files named `references/templates/<doc-type>.md` with an ordered section list + per-section fields + table column schemas). Keep ≤ 3 gold exemplars per document type in `references/exemplars/` (redacted, annotated). Record each change by hand in `references/change-log.md`.
6. **Re-upload** — Re-upload this file (plus any updated templates/exemplars) to the agent's Knowledge so the agent grounds on the latest house style.
