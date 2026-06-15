# PM Copilot — Skill Library Design

**Date:** 2026-06-14
**Owner:** Bruno (practicing PM, studying for PMP)
**Status:** Draft for review

## Goal

Convert the existing M365 Copilot agents into a single **PM Copilot** agent in the
rebuilt **Microsoft Copilot Studio**, powered by a library of portable
**`SKILL.md`** skills (open `agentskills.io` standard). Add a **House Style**
skill that captures how a senior PM at the company analyzes, structures, and
writes — so every output reflects that voice and rigor. Borrow proven open skills
where they beat building from scratch.

## Key facts that shape this design

- **Skills format (locked):** rebuilt Copilot Studio accepts skills in the open
  `agentskills.io` SKILL.md standard — the same format used by Claude Code,
  VS Code, Visual Studio 2026, GitHub Copilot, and `microsoft/skills-for-copilot-studio`.
  - One **folder per skill**; folder contains a **`SKILL.md`**.
  - **YAML frontmatter**, two required fields:
    - `name` — lowercase, hyphen-separated, ≤64 chars, **must match folder name**.
    - `description` — ≤1024 chars; the agent reads this to decide *when* to load
      the skill. Must be trigger-rich (verbs + nouns the user will actually say).
  - **Markdown body** = the instructions (the "what to do").
  - Optional `references/`, `scripts/`, `assets/` subfolders for supporting files.
- **Why a skill library (not 4 agents, not 1 mega-prompt):** skills auto-load by
  `description`, giving modularity without separate agents or A2A wiring. Each skill
  stays small and focused; the 8,000-char instruction limit applies per skill body,
  not to the whole system.
- **No drop-in replacement exists** for any of the four agents — each fills a real
  gap. Strategy is **convert + borrow patterns + equip**, never wholesale replace.
- **Knowledge files** (PMBOK7, Artifacts Playbook, Calculations, Agile Mechanics,
  PM Theory, Coaching & Blind Spots, PMP Exam Guide) move into each skill's
  `references/` and/or stay as Copilot Studio knowledge sources.

## Architecture

```
PM Copilot  (one Copilot Studio agent, generative orchestration ON)
│
├── skills/
│   ├── house-style/            ← Voice & Rigor kit; referenced by all output skills
│   ├── pm-coach/               ← from 01_AGENT_INSTRUCTIONS_PLAN_V2.md
│   ├── rasci-crosswalk/        ← from 03_RASCI_CROSSWALK_AGENT.md
│   ├── exec-briefing/          ← from 04_EXECUTIVE_BRIEFING_BUILDER.md
│   ├── ol-kpi-architect/       ← from 05_OL_KPI_ARCHITECT.md
│   ├── docx-builder/           ← borrowed (Anthropic docx skill), used by exec-briefing
│   └── pptx-builder/           ← borrowed (Anthropic pptx skill), used by exec-briefing
│
├── knowledge sources           ← PMBOK7, Artifacts Playbook, Calculations, etc.
└── (later phase) MCP tools      ← ms-365-mcp-server: live Planner / Excel / SharePoint
```

### Skill inventory

| Skill | Source | Job | Borrows | references/ |
|---|---|---|---|---|
| `house-style` | NEW (from senior-PM docs) | Voice + structure + rigor every output follows | distilled-rules + annotated-exemplars pattern | style-guide, templates, exemplars, glossary, analysis-rubric |
| `pm-coach` | `01..PLAN_V2.md` | Coach live hybrid projects + PMP tutor | ECO-weighting; tag-question-to-PMBOK-principle; Socratic ask-before-tell | K1,K3,K4,K5,K6,K7 |
| `rasci-crosswalk` | `03..md` | RASCI ↔ OCM timeline traceability + gap analysis + Planner reconcile | `shtracer` gap taxonomy + JSON output schema; completeness-% scoring | RASCI variants glossary |
| `exec-briefing` | `04..md` | Current→Target→Gap one-pager (Word) + 3–5 slide deck spec | Ragas "faithfulness" as provenance gate model | (calls docx/pptx skills) |
| `ol-kpi-architect` | `05..md` | KPI catalog + scorecard + control-point register | Kirkpatrick backward-from-Level-4 design | Kirkpatrick/ADKAR refs |
| `docx-builder` | Anthropic skill | Generate .docx | — | — |
| `pptx-builder` | Anthropic skill | Generate .pptx | — | — |

### How `house-style` plugs into the others

Each output-producing skill (`exec-briefing`, `ol-kpi-architect`, and any drafting
in `pm-coach`/`rasci-crosswalk`) opens with: *"Before drafting, load and apply the
`house-style` skill: its style guide governs voice, its template governs structure,
its analysis rubric governs what you check and in what order."* The `house-style`
body stays generic; document-type specifics live in its `references/` (one template
+ exemplars per type).

## The House Style "Voice & Rigor" kit (senior-PM extraction)

Layered kit — **distilled testable rules** (always-on, in SKILL.md body) +
**templates/exemplars/glossary** (retrieved, in `references/`).

| Artifact | Contains | Where it lives |
|---|---|---|
| Style Guide | Testable voice/tone/formatting rules ("open with a one-line RAG verdict") | `SKILL.md` body |
| Do / Don't list | Sharp positive + negative constraints | `SKILL.md` body |
| Analysis Rubric | Ordered analytical steps + decision thresholds (how they *reason*) | `SKILL.md` body |
| Structural Templates | Section order + section intents + table schemas, per doc type | `references/templates/` |
| Annotated Exemplars | 2–3 gold docs per type, with margin notes on *why* a passage works | `references/exemplars/` |
| Glossary | Preferred terms, acronyms, banned phrases | `references/glossary.md` |

### Extraction workflow (run when real docs arrive)

1. **Curate & redact** — 5–15 docs *per type*; tag type/audience/phase/date/quality;
   strip names, dollar figures, client identifiers **before** any text enters a prompt.
2. **Meta-prompt the LLM per type** to draft style guide, template, rubric. (Spec ships
   copy-paste prompts in `house-style/references/extraction-prompts.md`.)
3. **Triangulate** — extract only patterns recurring across ≥3 docs; flag inconsistencies
   (defense against overfitting to one doc's quirks).
4. **Expert interview (30–60 min)** — capture the tacit reasoning docs hide ("what's the
   first thing you look at when a milestone slips?"). This is what separates rigor from mimicry.
5. **Human ratification** — senior PM marks which patterns are intentional vs accidental;
   never extract from low-rated docs.
6. **Validate** — hold-out test (generate against a brief whose real output you have but the
   agent hasn't seen); pairwise LLM-as-judge ("which sounds more like the author?"); rubric-graded
   human review. Failures point to a missing/wrong rule → fix the artifact.

### Pitfalls + counters

- **Overfitting** → distilled rules over raw exemplars; ≤3 diverse exemplars; "imitate
  structure/voice, never copy content."
- **Confidential leakage** → redact at corpus-build time; review the knowledge base as if exposable.
- **Cargo-culting errors** → expert ratification pass; skip low-quality docs.
- **Mimicry without rigor** → keep the analysis rubric separate from the style guide; validate
  rigor independently from voice.
- **Drift** → versioned changelog of the kit; re-validate when the underlying model updates.

## Equipping with live data (later phase — out of scope for first build)

- **`softeria/ms-365-mcp-server`** — live Planner + Excel + SharePoint read. Turns
  `rasci-crosswalk` and `ol-kpi-architect` from "paste me an export" into "read my plan."
- Office-generation MCP only if the borrowed docx/pptx skills prove insufficient.
- Microsoft **Project** has no MCP server anywhere → manual export remains the path.

## Scope

**In scope (first build):** author the 6 first-party skills (`house-style`, `pm-coach`,
`rasci-crosswalk`, `exec-briefing`, `ol-kpi-architect`) as SKILL.md bundles with
`references/` populated from existing knowledge files; scaffold `house-style` with
extraction prompts and empty `references/` slots; document the Copilot Studio import steps.

**Out of scope (later):** borrowing/vendoring the Anthropic docx/pptx skills (evaluate
licenses first); MCP wiring; running the actual senior-PM extraction (needs real docs);
validation harness.

## Open questions

- Borrowed docx/pptx skills are *source-available*, not OSI open — license check before vendoring.
- Confirm whether Copilot Studio imports a skill **folder/zip** or points at a repo path
  (affects packaging) — verify in the rebuilt UI when we build.

## Success criteria

- All 6 skills load in PM Copilot and trigger on natural phrasing (description-driven).
- An exec briefing generated through `exec-briefing` + `house-style` is judged
  "sounds like our senior PM" on a hold-out test.
- Each skill body is ≤8,000 chars; descriptions ≤1024 chars; folder names match `name`.
