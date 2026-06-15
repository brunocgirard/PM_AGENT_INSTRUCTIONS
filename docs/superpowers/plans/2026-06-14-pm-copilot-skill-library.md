# PM Copilot Skill Library Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author a portable `skills/` library of `agentskills.io` SKILL.md bundles — five first-party PM skills (converted from the existing `agent/*.md` configs) plus vendored, well-rated community skills — ready to import into the rebuilt Microsoft Copilot Studio as one "PM Copilot" agent.

**Architecture:** Each skill is a folder under `skills/` with a `SKILL.md` (YAML frontmatter + markdown body) and optional `references/`, `scripts/`, `assets/`. A Python validator enforces the format contract (folder name = `name`, `description` ≤1024 chars, body ≤8000 chars, valid YAML, required fields). `house-style` is a living skill with an ingest loop (observe→reconcile→write-back) modeled on jzOcb/writing-style-skill. Knowledge files move into each skill's `references/`.

**Tech Stack:** Markdown + YAML frontmatter (agentskills.io standard); Python 3.14 (validator); git; PowerShell 7 / bash for commands.

---

## Implementation note (2026-06-14, applied during execution)

Mid-execution design change to **Task 6 (house-style)**, per user direction: house-style is **not** a runtime ingest-loop skill. It is a **knowledge/reference file the agent grounds on**, added to Copilot Studio as a Knowledge source, and **grown offline** (run the extraction prompts on redacted senior-PM docs, update the file, re-upload). Consequences vs. the original Task 6 below:
- `scripts/observe.py` and `scripts/improve.py` were **removed** (no runtime loop).
- `references/inbox/` was **removed**.
- `references/ingest-log.md` was **renamed to `references/change-log.md`** (a manual, append-by-hand changelog).
- The SKILL.md "Ingest loop" section became a `## How this file is grown (offline)` workflow.
The `house-style/references/extraction-prompts.md`, `glossary.md`, `templates/`, and `exemplars/` were kept. Task 6 steps below describing scripts/inbox/ingest-log are superseded by this note.

---

## Format contract (the rules every SKILL.md must satisfy)

- Folder per skill under `skills/<name>/`, containing `SKILL.md`.
- YAML frontmatter, required fields:
  - `name`: lowercase, hyphen-separated, ≤64 chars, **equals the folder name**.
  - `description`: ≤1024 chars, trigger-rich (verbs + nouns the user will say).
- Markdown body ≤8,000 chars.
- Optional subfolders: `references/`, `scripts/`, `assets/`.

## File Structure

```
skills/
├── README.md                         # library index + Copilot Studio import steps
├── validate_skills.py                # format-contract validator (the "test runner")
├── house-style/
│   ├── SKILL.md
│   ├── scripts/{observe.py,improve.py}
│   └── references/{extraction-prompts.md,glossary.md,ingest-log.md,
│                   inbox/.gitkeep,templates/.gitkeep,exemplars/.gitkeep}
├── pm-coach/
│   ├── SKILL.md
│   └── references/  (K1,K3,K4,K5,K6,K7 .md)
├── rasci-crosswalk/
│   ├── SKILL.md
│   └── references/{rasci-variants.md,gap-taxonomy.md,output-schema.json}
├── exec-briefing/
│   ├── SKILL.md
│   └── references/{current-target-gap-template.md,provenance-gate.md}
├── ol-kpi-architect/
│   ├── SKILL.md
│   └── references/{kirkpatrick-backward.md,adkar.md}
└── vendor/                            # vendored community skills (license + provenance preserved)
    ├── docx/  pptx/  xlsx/  pdf/  internal-comms/   (from anthropics/skills)
    ├── humanizer/                      (from blader/humanizer)
    ├── writing-style-skill/            (from jzOcb/writing-style-skill — reference for house-style)
    ├── data-analytics-skills/          (from nimrodfisher)
    └── mermaid-skill/                  (from WH-2099)
```

Source mapping (existing → new):
- `agent/01_AGENT_INSTRUCTIONS_PLAN_V2.md` → `skills/pm-coach/SKILL.md`
- `agent/03_RASCI_CROSSWALK_AGENT.md` → `skills/rasci-crosswalk/SKILL.md`
- `agent/04_EXECUTIVE_BRIEFING_BUILDER.md` → `skills/exec-briefing/SKILL.md`
- `agent/05_OL_KPI_ARCHITECT.md` → `skills/ol-kpi-architect/SKILL.md`
- `knowledge/K*.md` → copied into the relevant skill's `references/`

---

## Task 1: Validator (the test runner)

**Files:**
- Create: `skills/validate_skills.py`

- [ ] **Step 1: Write the validator**

```python
#!/usr/bin/env python3
"""Validate agentskills.io SKILL.md bundles under skills/."""
import sys, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME, MAX_DESC, MAX_BODY = 64, 1024, 8000

def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, text, "missing YAML frontmatter (must start with '---')"
    end = text.find("\n---", 3)
    if end == -1:
        return None, text, "unterminated YAML frontmatter"
    fm_raw, body = text[3:end].strip(), text[end+4:].lstrip("\n")
    fm = {}
    for line in fm_raw.splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#")):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body, None

def validate(skill_dir):
    errs = []
    md = skill_dir / "SKILL.md"
    if not md.exists():
        return [f"{skill_dir.name}: no SKILL.md"]
    fm, body, ferr = parse_frontmatter(md.read_text(encoding="utf-8"))
    if ferr:
        return [f"{skill_dir.name}: {ferr}"]
    name = fm.get("name", "")
    desc = fm.get("description", "")
    if not name: errs.append(f"{skill_dir.name}: missing 'name'")
    if name and not NAME_RE.match(name):
        errs.append(f"{skill_dir.name}: name '{name}' not lowercase-hyphen")
    if len(name) > MAX_NAME: errs.append(f"{skill_dir.name}: name >{MAX_NAME} chars")
    if name and name != skill_dir.name:
        errs.append(f"{skill_dir.name}: name '{name}' != folder '{skill_dir.name}'")
    if not desc: errs.append(f"{skill_dir.name}: missing 'description'")
    if len(desc) > MAX_DESC:
        errs.append(f"{skill_dir.name}: description {len(desc)}>{MAX_DESC} chars")
    if len(body) > MAX_BODY:
        errs.append(f"{skill_dir.name}: body {len(body)}>{MAX_BODY} chars")
    return errs

def main():
    targets = sys.argv[1:] or [str(p) for p in sorted(ROOT.iterdir())
                               if p.is_dir() and (p / "SKILL.md").exists()]
    all_errs = []
    for t in targets:
        d = Path(t) if Path(t).is_absolute() else ROOT / t
        all_errs += validate(d)
    if all_errs:
        print("FAIL:"); [print("  -", e) for e in all_errs]; sys.exit(1)
    print(f"PASS: {len(targets)} skill(s) valid"); sys.exit(0)

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run it to verify it passes with zero skills (no false failures)**

Run: `python skills/validate_skills.py`
Expected: `PASS: 0 skill(s) valid` (no skill dirs yet)

- [ ] **Step 3: Commit**

```bash
git add skills/validate_skills.py
git commit -m "feat(skills): add SKILL.md format validator"
```

---

## Task 2: pm-coach skill (simplest conversion — establishes the pattern)

**Files:**
- Create: `skills/pm-coach/SKILL.md`
- Create: `skills/pm-coach/references/` (copy K1,K3,K4,K5,K6,K7)
- Source: `agent/01_AGENT_INSTRUCTIONS_PLAN_V2.md`

- [ ] **Step 1: Create folder + copy knowledge references**

```bash
mkdir -p skills/pm-coach/references
cp knowledge/K1_PMBOK7_Reference.md knowledge/K3_PMP_Exam_Study_Guide.md \
   knowledge/K4_Coaching_and_Blind_Spots.md knowledge/K5_Calculations.md \
   knowledge/K6_Agile_Mechanics.md knowledge/K7_PM_Theory.md \
   skills/pm-coach/references/
```

- [ ] **Step 2: Write `skills/pm-coach/SKILL.md`**

Take the instructions body from `agent/01_AGENT_INSTRUCTIONS_PLAN_V2.md` (everything below its `---` divider) and prepend this frontmatter. Apply three edits to the body: (a) change "Ground every answer in: ... attached" to "Ground every answer in the files in `references/`"; (b) insert the house-style hook line (shown below) right after the Role section; (c) trim to ≤8,000 chars if needed.

```markdown
---
name: pm-coach
description: Senior PM mentor and PMP tutor for hybrid (predictive+agile) projects. Use when the user wants coaching on a live project (what to do next in their current phase, reviewing a document they paste, surfacing blind spots/gaps, walking through a mistake) OR PMP exam prep (drilling questions, explaining a formula, quizzing on ECO domains, study planning). Speaks first-person as an invested senior PM. Grounds answers in PMBOK 7, the Artifacts Playbook, Calculations, Agile Mechanics, PM Theory, and the PMP Exam Guide. Triggers: "coach me", "what should I do next", "review this", "what am I missing", "quiz me", "explain EVM/PERT/float", "study plan".
---
```

House-style hook to insert after the Role section:

```markdown
# House voice
When drafting any document or artifact for the user, first load the
`house-style` skill and apply it: its style guide governs voice, its templates
govern structure, its analysis rubric governs what you check and in what order.
```

- [ ] **Step 3: Run the validator**

Run: `python skills/validate_skills.py pm-coach`
Expected: `PASS: 1 skill(s) valid`
If FAIL on body length, trim the body (the V2 source is already near 8k) until it passes.

- [ ] **Step 4: Commit**

```bash
git add skills/pm-coach
git commit -m "feat(skills): add pm-coach skill (from PLAN_V2)"
```

---

## Task 3: rasci-crosswalk skill (+ borrowed gap taxonomy & output schema)

**Files:**
- Create: `skills/rasci-crosswalk/SKILL.md` (source: `agent/03_RASCI_CROSSWALK_AGENT.md`)
- Create: `skills/rasci-crosswalk/references/rasci-variants.md`
- Create: `skills/rasci-crosswalk/references/gap-taxonomy.md`
- Create: `skills/rasci-crosswalk/references/output-schema.json`

- [ ] **Step 1: Create folder**

```bash
mkdir -p skills/rasci-crosswalk/references
```

- [ ] **Step 2: Write the gap taxonomy reference** (borrowed pattern from shtracer)

Create `skills/rasci-crosswalk/references/gap-taxonomy.md`:

```markdown
# Traceability gap taxonomy (borrowed from shtracer)
Use these gap categories when cross-checking the RASCI against OCM sources:
- **Orphan activity** — RASCI activity with no matching OCM timeline/plan item.
- **Dangling item** — OCM timeline/plan item with no RASCI owner.
- **Coverage gap** — phase/workstream with < expected activity density.
- **Owner conflict** — same activity, different owners across sources.
- **Date conflict** — same activity, different dates; prefer the most recent source.
- **Sequence conflict** — dependency order disagrees between RASCI and timeline.
Report each finding with: id, category, the two sources + dates, and a coverage %
for the affected phase (covered items / expected items).
```

- [ ] **Step 3: Write the output schema reference**

Create `skills/rasci-crosswalk/references/output-schema.json`:

```json
{
  "traceability_matrix": [
    {"activity_id": "", "rasci_owner": "", "ocm_match": "", "status": "matched|orphan|dangling", "source": "", "source_date": ""}
  ],
  "gaps": [
    {"id": "", "category": "orphan|dangling|coverage|owner_conflict|date_conflict|sequence_conflict", "detail": "", "sources": [], "priority": "high|med|low"}
  ],
  "coverage_by_phase": [{"phase": "", "covered": 0, "expected": 0, "coverage_pct": 0}]
}
```

- [ ] **Step 4: Write the RASCI variants reference**

Create `skills/rasci-crosswalk/references/rasci-variants.md` with the RACI/RASCI/RASIC/DACI/CAIRO letter meanings so the agent recognizes any client notation. (Content: list each variant and what each letter means.)

- [ ] **Step 5: Write `skills/rasci-crosswalk/SKILL.md`**

Take the body from `agent/03_RASCI_CROSSWALK_AGENT.md` (below its Instructions `---` divider), prepend the frontmatter below, and add a line in the method telling it to use `references/gap-taxonomy.md` and emit results matching `references/output-schema.json`. Add the house-style hook (same block as Task 2 Step 2) before any drafting. For timeline visuals, add: "To render a timeline, emit Mermaid `gantt` syntax (the mermaid-skill renders it)."

```markdown
---
name: rasci-crosswalk
description: Traceability analyst for a training team inside a larger OCM (change management) workstream. Use when the user wants to cross-check a RASCI against the OCM timeline/plan, SWOT, notes, and SharePoint to find what is missing. Produces a traceability matrix, a prioritized gap/conflict list (orphans, dangling items, coverage gaps, owner/date/sequence conflicts), a proposed revised baseline timeline, a reconciliation against a Microsoft Planner export, and a plan-health/risk-readiness audit. Cites file + date for every claim, prefers the most recent source, never invents dates or dependencies. Triggers: "start the matrix", "cross-walk my RASCI", "reconcile my Planner", "check my plan health", "what's missing from my timeline".
---
```

- [ ] **Step 6: Run the validator**

Run: `python skills/validate_skills.py rasci-crosswalk`
Expected: `PASS: 1 skill(s) valid`

- [ ] **Step 7: Commit**

```bash
git add skills/rasci-crosswalk
git commit -m "feat(skills): add rasci-crosswalk skill with gap taxonomy + output schema"
```

---

## Task 4: ol-kpi-architect skill (+ Kirkpatrick backward-design reference)

**Files:**
- Create: `skills/ol-kpi-architect/SKILL.md` (source: `agent/05_OL_KPI_ARCHITECT.md`)
- Create: `skills/ol-kpi-architect/references/kirkpatrick-backward.md`
- Create: `skills/ol-kpi-architect/references/adkar.md`

- [ ] **Step 1: Create folder**

```bash
mkdir -p skills/ol-kpi-architect/references
```

- [ ] **Step 2: Write the Kirkpatrick backward-design reference** (borrowed from Devlin Peck template)

Create `skills/ol-kpi-architect/references/kirkpatrick-backward.md`:

```markdown
# Kirkpatrick backward design (Level 4 → 1)
Derive KPIs by starting from the desired business result and working backward:
- **Level 4 — Results:** the business outcome the training must move. Define first.
- **Level 3 — Behavior:** the on-the-job behavior change that drives Level 4.
- **Level 2 — Learning:** the knowledge/skill that enables the Level 3 behavior.
- **Level 1 — Reaction:** learner engagement/relevance signals (leading input).
For each level, propose a metric only if the project actually captures the data.
Tag each metric Leading (input) or Lagging (outcome).
```

- [ ] **Step 3: Write the ADKAR reference**

Create `skills/ol-kpi-architect/references/adkar.md` with the five ADKAR stages (Awareness, Desire, Knowledge, Ability, Reinforcement) and one adoption signal per stage.

- [ ] **Step 4: Write `skills/ol-kpi-architect/SKILL.md`**

Take the body from `agent/05_OL_KPI_ARCHITECT.md` (below its Instructions `---` divider), prepend the frontmatter below, add a line pointing the KPI derivation at `references/kirkpatrick-backward.md` and `references/adkar.md`, and add the house-style hook (Task 2 block) before drafting outputs.

```markdown
---
name: ol-kpi-architect
description: Designs a defensible measurement system for a training team (Organizational Learning) inside a larger OCM change workstream. Use when the user wants KPIs that are realistic given their actual RASCI, OCM plan/timeline, and Microsoft Planner export. Grounded in Kirkpatrick (learning effectiveness), ADKAR/Prosci (adoption), and PMBOK Measurement (control points). Runs an internal panel of four lenses (Learning-Effectiveness, Adoption, Project-Controls, Feasibility Skeptic), tags every KPI as OL / OCM / Shared, separates leading inputs from lagging outcomes, and builds a KPI catalog, an OL Implementation Health scorecard, and a control-point register. Never invents baselines or targets; prefers the most recent source. Triggers: "frame my sources", "propose OL KPIs", "build my OL scorecard", "control points".
---
```

- [ ] **Step 5: Run the validator**

Run: `python skills/validate_skills.py ol-kpi-architect`
Expected: `PASS: 1 skill(s) valid`

- [ ] **Step 6: Commit**

```bash
git add skills/ol-kpi-architect
git commit -m "feat(skills): add ol-kpi-architect skill with Kirkpatrick/ADKAR refs"
```

---

## Task 5: Vendor the borrowed community skills

**Files:**
- Create: `skills/vendor/<skill>/...` for each borrowed skill, each with its upstream `LICENSE` + a `PROVENANCE.md`.

- [ ] **Step 1: Clone sources to a temp dir and copy the needed skill folders**

```bash
mkdir -p skills/vendor
tmp=$(mktemp -d)
git clone --depth 1 https://github.com/anthropics/skills "$tmp/anthropic"
git clone --depth 1 https://github.com/blader/humanizer "$tmp/humanizer"
git clone --depth 1 https://github.com/jzOcb/writing-style-skill "$tmp/wss"
git clone --depth 1 https://github.com/nimrodfisher/data-analytics-skills "$tmp/das"
git clone --depth 1 https://github.com/WH-2099/mermaid-skill "$tmp/mermaid"
# Anthropic: copy the five skills we use
for s in docx pptx xlsx pdf internal-comms; do
  cp -r "$tmp/anthropic/skills/$s" "skills/vendor/$s" 2>/dev/null || \
  cp -r "$tmp/anthropic/$s" "skills/vendor/$s"
done
cp -r "$tmp/humanizer" skills/vendor/humanizer
cp -r "$tmp/wss" skills/vendor/writing-style-skill
cp -r "$tmp/das" skills/vendor/data-analytics-skills
cp -r "$tmp/mermaid" skills/vendor/mermaid-skill
```

- [ ] **Step 2: Preserve each LICENSE and remove nested .git**

```bash
find skills/vendor -name ".git" -type d -prune -exec rm -rf {} +
# Ensure each anthropic skill carries the repo LICENSE
for s in docx pptx xlsx pdf internal-comms; do
  cp "$tmp/anthropic/LICENSE"* "skills/vendor/$s/" 2>/dev/null || true
done
```

- [ ] **Step 3: Write a PROVENANCE.md in each vendored skill**

For each `skills/vendor/<x>/`, create `PROVENANCE.md`:

```markdown
# Provenance
- Source: <upstream repo URL>
- Vendored: 2026-06-14
- Commit/version: <record `git rev-parse HEAD` from the clone>
- License: see LICENSE in this folder (Anthropic skills are source-available — internal use only, do not redistribute without re-checking terms)
- Use in PM Copilot: <one line, e.g. "exec-briefing Word output">
```

Record the actual commit hashes: before deleting `$tmp`, run `git -C "$tmp/anthropic" rev-parse HEAD` (repeat per repo) and paste into each PROVENANCE.

- [ ] **Step 4: Validate vendored skills don't break the validator**

Run: `python skills/validate_skills.py`
Expected: `PASS` for all first-party skills. Vendored skills live under `skills/vendor/` (not a direct child of `skills/`), so the validator's top-level scan ignores them — confirm output lists only first-party skills. If any vendored skill violates the contract that's upstream's concern, not ours.

- [ ] **Step 5: Commit**

```bash
rm -rf "$tmp"
git add skills/vendor
git commit -m "chore(skills): vendor borrowed community skills with license + provenance"
```

---

## Task 6: house-style living skill (SKILL.md + scripts + references scaffold)

**Files:**
- Create: `skills/house-style/SKILL.md`
- Create: `skills/house-style/scripts/observe.py`, `skills/house-style/scripts/improve.py`
- Create: `skills/house-style/references/extraction-prompts.md`, `glossary.md`, `ingest-log.md`, and `.gitkeep` in `inbox/`, `templates/`, `exemplars/`

- [ ] **Step 1: Scaffold folders**

```bash
mkdir -p skills/house-style/scripts skills/house-style/references/inbox \
         skills/house-style/references/templates skills/house-style/references/exemplars
touch skills/house-style/references/inbox/.gitkeep \
      skills/house-style/references/templates/.gitkeep \
      skills/house-style/references/exemplars/.gitkeep
```

- [ ] **Step 2: Write the seed references**

Create `skills/house-style/references/glossary.md`:

```markdown
# House glossary (living — grows on ingest)
| Preferred term | Avoid | Note |
|---|---|---|
| (seeded on first ingest) | | |
```

Create `skills/house-style/references/ingest-log.md`:

```markdown
# Ingest log (append-only)
Each upload appends one entry: date, file (redacted name), rules added/reinforced/conflicted, confidence notes.

<!-- entries below, newest last -->
```

Create `skills/house-style/references/extraction-prompts.md` with three copy-paste meta-prompts (style-guide extraction, structural-template extraction, analysis-rubric extraction) — the prompts from the design spec's extraction method.

- [ ] **Step 3: Write `scripts/observe.py`** (extract candidate rules from inbox docs)

```python
#!/usr/bin/env python3
"""observe.py — read redacted docs in references/inbox/, emit candidate style rules.
Usage: python observe.py            (lists inbox files + extraction checklist)
This is a helper scaffold: it prepares the material; the LLM (Copilot/Claude) does
the extraction using references/extraction-prompts.md, then improve.py records it."""
from pathlib import Path
INBOX = Path(__file__).resolve().parent.parent / "references" / "inbox"
docs = [p for p in INBOX.glob("*") if p.is_file() and p.name != ".gitkeep"]
if not docs:
    print("Inbox empty. Drop redacted senior-PM docs into references/inbox/ first.")
else:
    print(f"{len(docs)} doc(s) to observe:")
    for d in docs: print("  -", d.name)
    print("\nNext: run each through the prompts in references/extraction-prompts.md,")
    print("then record accepted rules with improve.py.")
```

- [ ] **Step 4: Write `scripts/improve.py`** (append a ratified change to the ingest log)

```python
#!/usr/bin/env python3
"""improve.py — append a ratified ingest entry to references/ingest-log.md.
Usage: python improve.py "2026-06-14" "status-report-A (redacted)" "added: lead with RAG verdict; reinforced: <=1 page" """
import sys
from pathlib import Path
LOG = Path(__file__).resolve().parent.parent / "references" / "ingest-log.md"
if len(sys.argv) < 4:
    print("Usage: improve.py <date> <file> <changes>"); sys.exit(1)
date, fname, changes = sys.argv[1], sys.argv[2], sys.argv[3]
entry = f"\n- **{date}** — {fname}: {changes}\n"
with LOG.open("a", encoding="utf-8") as f:
    f.write(entry)
print("Appended to ingest-log.md:", entry.strip())
```

- [ ] **Step 5: Write `skills/house-style/SKILL.md`**

Body must contain: the Style Guide (seeded, "grows on ingest"), Do/Don't list, Analysis Rubric, and the **ingest loop** procedure (drop file → redact → observe → reconcile add/reinforce/conflict preferring recent → write back + log → promote exemplars ≤3/type), plus the triangulation (≥3 docs) and ratification gates. Keep ≤8,000 chars. Prepend:

```markdown
---
name: house-style
description: The company's living house style — how a senior PM writes, structures documents, and reasons. Other skills load this before drafting so every output matches the senior PM's voice, structure, and analytical rigor. Also runs the INGEST LOOP: when the user uploads a senior-PM document, it redacts it, extracts voice/structure/reasoning patterns, reconciles them against the existing kit (add new, reinforce, or flag conflicts preferring the most recent source), updates the style guide/templates/glossary, and appends an ingest-log entry. Grows and sharpens over time. Triggers: "apply house style", "learn from this doc", "ingest this", "update my style guide", "make it sound like us".
---
```

- [ ] **Step 6: Run the validator**

Run: `python skills/validate_skills.py house-style`
Expected: `PASS: 1 skill(s) valid`

- [ ] **Step 7: Smoke-test the scripts**

Run: `python skills/house-style/scripts/observe.py`
Expected: `Inbox empty. Drop redacted senior-PM docs into references/inbox/ first.`
Run: `python skills/house-style/scripts/improve.py 2026-06-14 "seed" "initialized kit"`
Expected: `Appended to ingest-log.md: ...` and the line appears in `ingest-log.md`.

- [ ] **Step 8: Commit**

```bash
git add skills/house-style
git commit -m "feat(skills): add living house-style skill with ingest loop + scripts"
```

---

## Task 7: exec-briefing skill (wires house-style + vendored docx/pptx)

**Files:**
- Create: `skills/exec-briefing/SKILL.md` (source: `agent/04_EXECUTIVE_BRIEFING_BUILDER.md`)
- Create: `skills/exec-briefing/references/current-target-gap-template.md`
- Create: `skills/exec-briefing/references/provenance-gate.md`

- [ ] **Step 1: Create folder**

```bash
mkdir -p skills/exec-briefing/references
```

- [ ] **Step 2: Write the Current→Target→Gap template**

Create `skills/exec-briefing/references/current-target-gap-template.md` with the one-page skeleton: Source-of-truth restatement → Current → Target → Gap → Plan (open for discussion) → Leadership ask. Note which sections hold Validated facts vs Assumptions (kept off-slide).

- [ ] **Step 3: Write the provenance gate** (borrowed Ragas "faithfulness" idea)

Create `skills/exec-briefing/references/provenance-gate.md`:

```markdown
# Provenance gate (faithfulness check before rendering)
Classify every claim before it goes on the page:
- **Validated** — traceable to meeting notes or the approved charter; cite file + date.
- **Assumption** — from the user's context pack; keep OFF-slide / in an appendix.
- **Conflict** — sources disagree; flag it and prefer the most recent source.
Do not render a document until every on-slide fact is Validated. Never invent
dates, owners, or scope.
```

- [ ] **Step 4: Write `skills/exec-briefing/SKILL.md`**

Take the body from `agent/04_EXECUTIVE_BRIEFING_BUILDER.md` (below its Instructions `---` divider), prepend the frontmatter below, and wire in: (a) house-style hook (Task 2 block) before drafting; (b) "apply `references/provenance-gate.md` before rendering"; (c) "for the Word one-pager use the vendored `docx` skill; for the 3–5 slide deck use the vendored `pptx` skill (or emit the PowerPoint 'Create presentation from file' build spec if those skills are unavailable in the host)."

```markdown
---
name: exec-briefing
description: Turns a project's sources into trustworthy executive communication. Use when the user wants a one-page Current→Target→Gap briefing (Word) or a 3–5 slide executive deck. Restates the source-of-truth, then validates every claim by provenance — Validated (traceable to notes/approved charter, cited by file+date), Assumption (kept off-slide), or Conflict (prefer most recent). Builds on a Current→Target→Gap skeleton with Plan and the leadership ask framed as open for discussion. Renders Word via the docx skill and slides via the pptx skill. Never invents dates, owners, or scope. Triggers: "set my source-of-truth", "build the one-pager", "build a 3–5 slide exec deck", "validate these claims".
---
```

- [ ] **Step 5: Run the validator**

Run: `python skills/validate_skills.py exec-briefing`
Expected: `PASS: 1 skill(s) valid`

- [ ] **Step 6: Commit**

```bash
git add skills/exec-briefing
git commit -m "feat(skills): add exec-briefing skill with provenance gate + docx/pptx wiring"
```

---

## Task 8: Library README + Copilot Studio import guide + full validation

**Files:**
- Create: `skills/README.md`

- [ ] **Step 1: Write `skills/README.md`**

Contents:
- One-line purpose of the library.
- Table: each first-party skill, its trigger summary, and source `agent/` file.
- List of vendored skills + their PROVENANCE pointers.
- "How house-style stays living": drop docs in `house-style/references/inbox/`, run observe/improve locally, re-import.
- **Copilot Studio import steps** (fill in exact UI clicks when verified against the rebuilt UI; until then, record the assumption that skills import as folder/zip bundles and that `observe`/`improve` run locally — not inside Copilot Studio — then the updated SKILL.md is re-imported).
- The format contract (name=folder, desc ≤1024, body ≤8000) and how to run `validate_skills.py`.

- [ ] **Step 2: Run the full validation across all first-party skills**

Run: `python skills/validate_skills.py`
Expected: `PASS: 5 skill(s) valid` (house-style, pm-coach, rasci-crosswalk, exec-briefing, ol-kpi-architect)

- [ ] **Step 3: Commit**

```bash
git add skills/README.md
git commit -m "docs(skills): add library README + Copilot Studio import guide"
```

---

## Self-review notes (coverage check)

- Spec's 5 first-party skills → Tasks 2,3,4,6,7. ✓
- Vendored community skills with license+provenance → Task 5. ✓
- Living house-style ingest loop + scripts → Task 6. ✓
- Format contract enforced → Task 1 validator, run in every skill task. ✓
- Knowledge files relocated to references/ → Task 2 (and per-skill refs in 3,4,7). ✓
- Copilot Studio import + the two open questions (folder/zip import, scripts run locally) → Task 8 README, recorded as assumptions to verify against the rebuilt UI. ✓
- Borrowed patterns (shtracer gap taxonomy, Kirkpatrick backward, Ragas faithfulness, mermaid render) → Tasks 3,4,7. ✓
- Out of scope (MCP wiring, real ingest run, validation harness) — correctly omitted.
