# PM Copilot — Skill Library

## Purpose

This directory is the portable SKILL.md (agentskills.io standard) skill library for the **PM Copilot** agent built in Microsoft Copilot Studio. It contains five first-party skills converted from the user's original M365 Copilot agent instruction files, plus nine vendored community skills imported from public repositories. Together they give the agent its specialist capabilities — from PMP coaching and RASCI cross-walking to document rendering and prose humanizing.

---

## First-party skills

| Skill | What it does | Converted from |
|---|---|---|
| `pm-coach` | Senior PM mentor and PMP tutor for hybrid (predictive+agile) projects; drills exam questions, coaches live project work, grounds in PMBOK 7 | `agent/01_AGENT_INSTRUCTIONS_PLAN_V2.md` |
| `rasci-crosswalk` | Traceability analyst for a training team inside an OCM workstream; produces a matrix, prioritized gap/conflict list, revised baseline timeline, and plan-health audit | `agent/03_RASCI_CROSSWALK_AGENT.md` |
| `exec-briefing` | Turns a project's sources into trustworthy executive communication (one-page Word briefing or 3–5 slide deck), validating every claim by provenance | `agent/04_EXECUTIVE_BRIEFING_BUILDER.md` |
| `ol-kpi-architect` | Designs a defensible measurement system for an OL team inside an OCM workstream; runs a four-lens panel, tags KPIs as OL/OCM/Shared, builds a scorecard and control-point register | `agent/05_OL_KPI_ARCHITECT.md` |
| `house-style` | The company's house-style reference — voice, tone, formatting rules, an analysis rubric, and a glossary — that other skills ground on before drafting | NEW (grown from a knowledge/reference file; see section below) |

---

## house-style — special: knowledge file, grown offline

`house-style` is **not a runtime loop**. It is a style/voice/rigor reference — the accumulated learnings of what "good" looks like for this PM — that the agent grounds on. In Copilot Studio it is added as a **Knowledge source** (not as an active skill/tool). Other skills carry a `# House voice` hook that instructs them to apply this guidance whenever it is present.

**How it is maintained (offline process):**

1. Gather (redacted) senior-PM documents you want to learn from.
2. Run the prompts in `skills/house-style/references/extraction-prompts.md` against those documents.
3. Update `skills/house-style/SKILL.md` (style guide + confidence tiers), its `references/templates/`, and `glossary.md` with the new learnings.
4. Record the change in `references/change-log.md`.
5. Re-upload the updated `SKILL.md` (and any template files) to the agent's Knowledge in Copilot Studio.

The agent itself does **not** ingest documents or run any update loop at runtime. All growth happens offline and is committed back to this repo before re-upload.

---

## Vendored community skills

All vendor files live under `skills/vendor/`. Each subfolder contains a `PROVENANCE.md` recording the upstream source, commit, and license.

| Folder | Upstream source | Use in PM Copilot |
|---|---|---|
| `docx` | https://github.com/anthropics/skills | `exec-briefing` Word output |
| `pptx` | https://github.com/anthropics/skills | `exec-briefing` slide deck |
| `xlsx` | https://github.com/anthropics/skills | Spreadsheet output |
| `pdf` | https://github.com/anthropics/skills | PDF extract/fill |
| `internal-comms` | https://github.com/anthropics/skills | Status-report formatting |
| `humanizer` | https://github.com/blader/humanizer | De-AI prose pass |
| `writing-style-skill` | https://github.com/jzOcb/writing-style-skill | Reference architecture for house-style ingest loop |
| `data-analytics-skills` | https://github.com/nimrodfisher/data-analytics-skills | Exec-summary/dashboard-spec helpers |
| `mermaid-skill` | https://github.com/WH-2099/mermaid-skill | Render RASCI/timeline Gantt visuals |

**License notes:**

- The five Anthropic skills (`docx`, `pptx`, `xlsx`, `pdf`, `internal-comms`) are **source-available, not open source** — internal use only; do not redistribute without re-checking terms. See `LICENSE.txt` in each folder.
- The remaining four skills carry their own upstream licenses; see the `LICENSE` file in each folder.
- `mermaid-skill` keeps its SKILL.md nested at `.claude/skills/mermaid/SKILL.md` per its upstream layout.

The validator intentionally does **not** auto-scan `skills/vendor/*` — those files follow their own upstream conventions and are not required to pass the format contract below.

---

## Format contract and validation

Every first-party skill folder must satisfy the following rules:

- Folder name must exactly equal the YAML `name` field in `SKILL.md`.
- `description` must be 1,024 characters or fewer.
- Body (everything after the closing `---`) must be 8,000 characters or fewer.
- The file must open with valid `---` YAML frontmatter (at minimum `name` and `description`).

**Run the validator:**

```bash
# Validate all first-party skills
python skills/validate_skills.py

# Validate a single skill
python skills/validate_skills.py pm-coach
```

The validator scans only the immediate child directories of `skills/` (excluding `vendor/`). A clean run reports:

```
PASS: 5 skill(s) valid
```

---

## Copilot Studio import — VERIFY IN UI

> **VERIFY IN UI** — The import flow below is based on working assumptions about how Copilot Studio handles SKILL.md bundles and the agent's generative orchestration. Confirm each point against the rebuilt Copilot Studio UI before relying on it.

**Working assumptions to confirm:**

- Skills import as folder or ZIP bundles containing `SKILL.md`; the exact upload mechanism (UI panel, API, CLI) needs verification in the current Copilot Studio release.
- The agent uses **generative orchestration** — the orchestrator selects skills by matching the user's message against each skill's `description`. Keep descriptions precise and trigger-phrase-rich to ensure correct routing.
- `house-style` and any associated templates or exemplars are added as **Knowledge sources** (not as active tools/skills), so the agent can ground on them without triggering them as a callable action.
- The offline house-style extraction and update process runs locally on the maintainer's machine, not inside Copilot Studio.

**Capacity guidelines (confirm limits in current UI):**

- Keep total active tools/skills in the 25–30 range for predictable orchestration; the hard cap is reported as 128.
- Respect the 8,000-character instruction body limit (enforced by the validator above) and the 500-file Knowledge source limit.

Treat these as items to confirm against the live UI, not settled facts.
