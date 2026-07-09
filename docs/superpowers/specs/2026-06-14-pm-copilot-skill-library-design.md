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
| `house-style` | NEW — **living/self-learning** (modeled on jzOcb/writing-style-skill) | Voice + structure + rigor every output follows; grows each time a senior-PM doc is uploaded | jzOcb observe→improve loop; distilled-rules + annotated-exemplars | style-guide, templates, exemplars, glossary, analysis-rubric, ingest log |
| `pm-coach` | `01..PLAN_V2.md` | Coach live hybrid projects + PMP tutor | ECO-weighting; tag-question-to-PMBOK-principle; Socratic ask-before-tell | K1,K3,K4,K5,K6,K7 |
| `rasci-crosswalk` | `03..md` | RASCI ↔ OCM timeline traceability + gap analysis + Planner reconcile | `shtracer` gap taxonomy + JSON output schema; completeness-% scoring | RASCI variants glossary |
| `exec-briefing` | `04..md` | Current→Target→Gap one-pager (Word) + 3–5 slide deck spec | Ragas "faithfulness" as provenance gate model | (calls docx/pptx skills) |
| `ol-kpi-architect` | `05..md` | KPI catalog + scorecard + control-point register | Kirkpatrick backward-from-Level-4 design | Kirkpatrick/ADKAR refs |
| `docx-builder` | Anthropic skill | Generate .docx | — | — |
| `pptx-builder` | Anthropic skill | Generate .pptx | — | — |

### Borrowed community skills (well-rated, agentskills.io format)

Vendored into the library (license-checked) or used as templates. Star counts ≈ June 2026.

| Capability | Borrow | How used |
|---|---|---|
| Word / PPT / Excel / PDF generation | [anthropics/skills](https://github.com/anthropics/skills) — docx, pptx, xlsx, pdf, **internal-comms** | `exec-briefing` output; status-report formatting. *Source-available — internal use OK, check before redistributing.* |
| "Write like me" self-learning loop | [jzOcb/writing-style-skill](https://github.com/jzOcb/writing-style-skill) | **Architecture base for `house-style`** (observe→improve scripts) |
| De-AI / tone cleanup | [blader/humanizer](https://github.com/blader/humanizer) (~24k) | Final pass on any drafted prose |
| Exec-summary / dashboard-spec / tech→business translation | [nimrodfisher/data-analytics-skills](https://github.com/nimrodfisher/data-analytics-skills) | Cherry-pick into `exec-briefing` / `ol-kpi-architect` |
| Status notes / meeting notes / weekly report | [claude-office-skills/skills](https://github.com/claude-office-skills/skills) | Templates for `pm-coach` drafting |
| Gantt / timeline / flowchart render | [WH-2099/mermaid-skill](https://github.com/WH-2099/mermaid-skill) · [Agents365-ai/mermaid-skill](https://github.com/Agents365-ai/mermaid-skill) | Render backend for `rasci-crosswalk` timeline + RASCI visuals |
| Ongoing discovery | [ComposioHQ](https://github.com/ComposioHQ/awesome-claude-skills) · [alirezarezvani](https://github.com/alirezarezvani/claude-skills) · [travisvn](https://github.com/travisvn/awesome-claude-skills) curated lists | Browse for new skills over time |

**Gap:** no well-rated RASCI/RACI-matrix skill exists → `rasci-crosswalk` stays a custom build.

### How `house-style` plugs into the others

Each output-producing skill (`exec-briefing`, `ol-kpi-architect`, and any drafting
in `pm-coach`/`rasci-crosswalk`) opens with: *"Before drafting, load and apply the
`house-style` skill: its style guide governs voice, its template governs structure,
its analysis rubric governs what you check and in what order."* The `house-style`
body stays generic; document-type specifics live in its `references/` (one template
+ exemplars per type).

## The House Style "Voice & Rigor" kit — a LIVING, self-learning skill

`house-style` is **not** a one-shot extraction. It is a living document that gets
**molded by every senior-PM file uploaded**: each upload runs an ingest loop that
extracts patterns and *appends/refines* the kit, so the agent's sense of "our house
voice" sharpens over time. Architecture is modeled on
[jzOcb/writing-style-skill](https://github.com/jzOcb/writing-style-skill)
(observe → extract → write-back → improve).

### Layered kit (what grows)

| Artifact | Contains | Where it lives | Grows on upload? |
|---|---|---|---|
| Style Guide | Testable voice/tone/formatting rules ("open with a one-line RAG verdict") | `SKILL.md` body | Yes — rules added/refined |
| Do / Don't list | Sharp positive + negative constraints | `SKILL.md` body | Yes |
| Analysis Rubric | Ordered analytical steps + decision thresholds (how they *reason*) | `SKILL.md` body | Yes |
| Structural Templates | Section order + section intents + table schemas, per doc type | `references/templates/` | Yes — new type → new template |
| Annotated Exemplars | 2–3 gold docs per type, margin notes on *why* a passage works | `references/exemplars/` | Yes — best example per type kept |
| Glossary | Preferred terms, acronyms, banned phrases | `references/glossary.md` | Yes |
| **Ingest log** | What each upload changed, with date + confidence | `references/ingest-log.md` | Yes — append-only audit trail |

### The ingest loop (runs each time you upload a doc)

1. **Drop the file** into `house-style/references/inbox/` (or paste it).
2. **Redact** — strip names, dollar figures, client identifiers **before** anything is
   stored or sent to a model.
3. **Observe** — extract this doc's patterns (voice, structure, table schemas, reasoning
   cues) into a candidate rule set.
4. **Reconcile against the existing kit** — for each candidate:
   - *New, consistent* → add it.
   - *Reinforces an existing rule* → bump its confidence.
   - *Conflicts with an existing rule* → flag in the ingest log, prefer the **more recent**
     doc, and keep both until a human ratifies (do not silently overwrite).
5. **Write back** — update the Style Guide / templates / glossary; record the change +
   date + confidence in `ingest-log.md`.
6. **Promote exemplars** — if the doc is a *gold* example of its type, keep it (redacted,
   annotated) and retire a weaker one so exemplar count stays ≤3 per type.

Rules carry a **confidence** that rises as more docs reinforce them; low-confidence rules
are applied tentatively and surfaced for review. This is what makes it "living" rather than
a static prompt — and the ingest log makes every change auditable and reversible.

### Quality gates (kept from the extraction method)

- **Triangulate** — a pattern becomes a firm rule only after it recurs across ≥3 docs;
  single-doc patterns stay low-confidence (defense against overfitting to one doc's quirks).
- **Expert interview (optional, high-value)** — a 30–60 min talk with the senior PM captures
  tacit reasoning the documents hide ("what's the first thing you look at when a milestone
  slips?"). Feed answers in as a high-confidence upload. This is what separates rigor from mimicry.
- **Human ratification** — periodically the senior PM (or you) reviews the ingest log and
  confirms/rejects flagged conflicts and low-confidence rules; never enshrine patterns from
  low-rated docs.
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

**In scope (first build):** author the 5 first-party skills (`house-style`, `pm-coach`,
`rasci-crosswalk`, `exec-briefing`, `ol-kpi-architect`) as SKILL.md bundles with
`references/` populated from existing knowledge files; scaffold `house-style` as a
**living skill** — ingest-loop instructions, empty `references/` slots (inbox, templates,
exemplars, glossary, ingest-log), and the observe/improve scripts adapted from
jzOcb/writing-style-skill; document the Copilot Studio import steps; identify which
borrowed community skills to vendor; **vendor them into `skills/` with each one's
LICENSE + a provenance note** (source repo URL, commit/version, date vendored).

**Out of scope (later):** MCP wiring; running the actual senior-PM ingest (needs real docs);
validation harness.

## Open questions

- Borrowed skills are *source-available* (Anthropic) / various community licenses — **decision:
  vendor them**, preserving each skill's LICENSE file + a `PROVENANCE.md` per vendored skill;
  internal use only, do not redistribute the repo publicly without re-checking terms.
- House-style ingest scripts (`observe`/`improve`): runnable inside Copilot Studio, or run
  locally (Claude Code / editor) to update the SKILL.md, then re-import? Likely the latter —
  confirm what the rebuilt Copilot Studio executes.
- Confirm whether Copilot Studio imports a skill **folder/zip** or points at a repo path
  (affects packaging) — verify in the rebuilt UI when we build.

## Success criteria

- All 5 first-party skills load in PM Copilot and trigger on natural phrasing (description-driven).
- `house-style` ingests an uploaded doc and visibly updates its rules + ingest log.
- An exec briefing generated through `exec-briefing` + `house-style` is judged
  "sounds like our senior PM" on a hold-out test.
- Each skill body is ≤8,000 chars; descriptions ≤1024 chars; folder names match `name`.
