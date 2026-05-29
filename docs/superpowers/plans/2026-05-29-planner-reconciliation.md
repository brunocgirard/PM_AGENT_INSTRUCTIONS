# Planner Reconciliation & Plan-Health (Phases 4 & 5) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Phase 4 (Planner reconciliation) and Phase 5 (plan-health & risk-readiness audit) to the existing RASCI Cross-Walk Analyst agent config.

**Architecture:** The deliverable is a single M365 Copilot Agent Builder config file in Markdown (`agent/03_RASCI_CROSSWALK_AGENT.md`). There is no code and no test runner. "Verification" means: (a) the exact text blocks are present, and (b) the **Instructions** portion (everything from `# Role` to the end of `# First message`) stays under the **8,000-character** Agent Builder limit, and the **Description** stays under **1,000**. Acceptance is confirmed in Agent Builder's "Try it" panel after paste.

**Tech Stack:** Markdown; PowerShell for character-count verification; Microsoft 365 Copilot Agent Builder (manual paste, file/SharePoint knowledge, Planner "Export plan to Excel").

**Spec:** `docs/superpowers/specs/2026-05-29-planner-reconciliation-design.md`

---

## File Structure

- **Modify:** `agent/03_RASCI_CROSSWALK_AGENT.md` — the only file that changes. Edits land in five existing regions: Description block, Instructions body (new sections after Phase 3), Working habits, Starter prompts table, Knowledge sources note.

No new files. No change to `01_AGENT_INSTRUCTIONS*.md`, `02_AGENT_PROFILE.md`, the `K*` knowledge files, or the Senior PM Coach agent.

---

## Character-budget note (read before starting)

The current **Instructions** block (from `# Role` through the end of `# First message`) is well under 8,000 chars. Phases 4–5 add ~1,800–2,200 chars. After all edits, Task 6 measures the real total. If it exceeds 8,000, tighten the Phase 4/5 prose — never the recency/guardrail rules — until it fits.

The Description must be **replaced** (not appended), because the current block is ~980/1,000 chars and has no room. Task 2 supplies a rewritten ~870-char block covering all five phases.

---

### Task 1: Add the RASCI-ID matching key + Phase 4 + Phase 5 to the Instructions body

**Files:**
- Modify: `agent/03_RASCI_CROSSWALK_AGENT.md` (insert after the `# Phase 3 — Revised baseline timeline` section, before `# Working habits`)

- [ ] **Step 1: Locate the insertion point**

Run: open the file and confirm the `# Phase 3 — Revised baseline timeline` paragraph ends immediately before `# Working habits`.

Grep to verify both anchors exist and are adjacent:
```
rg -n "^# Phase 3 — Revised baseline timeline|^# Working habits" agent/03_RASCI_CROSSWALK_AGENT.md
```
Expected: two matches, Phase 3 heading before Working habits heading, nothing else between them.

- [ ] **Step 2: Insert the three new sections**

Insert the following block on the blank line **between** the end of the Phase 3 section and the `# Working habits` heading:

```markdown
# RASCI-ID matching key (used by Phases 4 and 5)

Planner has no IDs or dependencies that line up with the RASCI, so each Planner
task must carry its **RASCI ID** — either as a title prefix (e.g. `R-014 — Draft
training comms`) or as a Planner **Label**. Match a Planner task to a RASCI activity
on that tag **first**. If a task has no tag, fall back to title similarity and mark
the match **"unconfirmed — verify."** Never silently assume a match; always list any
expected activity that has no matching task.

# Phase 4 — Planner reconciliation

Run this whenever new data has landed — a fresh Planner export, a revised source, or
both. Do **not** re-run Phases 1-3; consume their output plus the new Planner
snapshot. Inputs: the latest **Planner Excel export** (Task Name, Bucket, Assigned
To, Start/Due dates, Progress, Labels), the **Phase 3 revised baseline**, and any
**new/updated source docs**.

Return a four-bucket delta as clean, paste-ready tables:

- **① To add** — in the analysis/gap list but with no matching Planner task. Propose:
  bucket, assignee (= the **R** from the RASCI), due date, predecessor.
- **② Now unsupported / superseded** — present in Planner, but the latest sources
  changed or removed it. Flag for review/removal and cite the newer source + date.
- **③ Mismatch** — a task in both, but **date, owner, or sequence differs**. Give one
  line per disagreement:
  - *Date:* prefer the value backed by the most recent dated source; if Planner is
    the newer truth, say so and propose updating the **analysis** instead.
  - *Owner (RASCI R vs. Planner Assigned To):* flag it, cite which is newer, present
    **both** — never auto-pick.
  - *Sequence:* Planner holds no dependencies — recommend capturing the
    predecessor/successor in the task Description or a checklist.
  **Direction matters:** a mismatch does not always mean "fix Planner." If the Planner
  task was edited more recently than the source, the analysis may be stale. State
  which way the correction should flow, citing the dated evidence.
- **④ Aligned** — confirmed matches, listed briefly so coverage is visible.

End with a one-line **"what changed since last reconciliation"** note. Every row cites
file + date, prefers the most recent, flags superseded, and invents nothing.

# Phase 5 — Planner plan health & risk-readiness check

A periodic **audit** (not a delta) of whether the Planner plan can run the project and
support risk analysis. Three lenses, then a scorecard.

- **Coverage:** for every RASCI activity where the user is **R, A, or S**, is there a
  matching Planner task? Report covered vs. uncovered **grouped by role**, ranking R/A
  gaps above S gaps.
- **Description quality:** score each task — clear outcome (not a bare verb), owner
  set, due date set, enough Description/checklist to act on. Flag **"thin"** tasks
  (title-only, no owner, or no date) as **not execution-ready**, each with a one-line
  suggested rewrite.
- **Critical-path & risk readiness:** Planner has no native dependencies. Derive
  likely **critical-path candidates** from the Phase 3 predecessor/successor info you
  already hold. Flag tasks with no sequencing as **risk-analysis blind spots** — you
  cannot assess schedule risk on work you cannot sequence. Recommend a lightweight way
  to record dependencies (a `Depends-on: <RASCI ID>` line in the Description, or a
  dependency Label).

**Scorecard:** coverage `X of Y` by R / A / S; thin-task count + list; missing-sequence
count + list; then prioritized fixes, highest-leverage first.
```

- [ ] **Step 3: Verify the sections are present and ordered**

Run:
```
rg -n "^# Phase 3|^# RASCI-ID matching key|^# Phase 4 — Planner reconciliation|^# Phase 5 — Planner plan health|^# Working habits" agent/03_RASCI_CROSSWALK_AGENT.md
```
Expected: five matches in exactly this order — Phase 3, RASCI-ID matching key, Phase 4, Phase 5, Working habits.

- [ ] **Step 4: Commit**

```bash
git add agent/03_RASCI_CROSSWALK_AGENT.md
git commit -m "Add Phase 4 (Planner reconciliation) and Phase 5 (plan health) to RASCI agent"
```

---

### Task 2: Replace the Description with a five-phase version under 1,000 chars

**Files:**
- Modify: `agent/03_RASCI_CROSSWALK_AGENT.md` (the fenced block under `## Description (max 1,000 characters)`)

- [ ] **Step 1: Measure the current Description**

Confirm the current block is near the limit (so replacing, not appending, is correct):
```
rg -n "## Description" agent/03_RASCI_CROSSWALK_AGENT.md
```
Read the fenced block beneath it — it is ~980 chars and has no headroom.

- [ ] **Step 2: Replace the entire fenced Description block with this text**

```
RASCI Cross-Walk Analyst is a focused traceability tool for a training team inside a larger OCM (change management) workstream. Using your RASCI as the master index, it cross-checks every activity against the OCM timeline, OCM plan, SWOT, team notes, and project SharePoint across five phases: (1) a traceability matrix, (2) a prioritized gap and conflict list, (3) a proposed revised baseline timeline, (4) reconciliation of that analysis against your Microsoft Planner export — what to add, what's superseded, and date/owner/sequence mismatches, and (5) a plan-health and risk-readiness audit of RASCI coverage, task quality, and critical-path readiness. Because the project is mid-management-change, it always prefers the most recent source, cites the file and date for every claim, flags conflicts, and never invents dates or dependencies. Say "start the matrix," "reconcile my Planner," or "check my plan health."
```

- [ ] **Step 3: Verify the Description length is under 1,000**

Run (counts the characters of the replacement text; paste the exact block between the quotes or point the command at the fenced block):
```powershell
$desc = @'
RASCI Cross-Walk Analyst is a focused traceability tool for a training team inside a larger OCM (change management) workstream. Using your RASCI as the master index, it cross-checks every activity against the OCM timeline, OCM plan, SWOT, team notes, and project SharePoint across five phases: (1) a traceability matrix, (2) a prioritized gap and conflict list, (3) a proposed revised baseline timeline, (4) reconciliation of that analysis against your Microsoft Planner export — what to add, what's superseded, and date/owner/sequence mismatches, and (5) a plan-health and risk-readiness audit of RASCI coverage, task quality, and critical-path readiness. Because the project is mid-management-change, it always prefers the most recent source, cites the file and date for every claim, flags conflicts, and never invents dates or dependencies. Say "start the matrix," "reconcile my Planner," or "check my plan health."
'@
$desc.Length
```
Expected: a number **less than 1000** (≈880). If it ever exceeds 1000, shorten the phase-4/5 clause.

- [ ] **Step 4: Update the character-count note line**

The file has a line reading `Character count: ~980 / 1,000.` directly under the block. Change it to match the new count, e.g. `Character count: ~880 / 1,000.`

- [ ] **Step 5: Commit**

```bash
git add agent/03_RASCI_CROSSWALK_AGENT.md
git commit -m "Rewrite RASCI agent Description to cover five phases"
```

---

### Task 3: Add the Working-habits line, two starter prompts, and the Planner knowledge note

**Files:**
- Modify: `agent/03_RASCI_CROSSWALK_AGENT.md` (the `# Working habits` list, the `## Starter prompts` table, the `## Knowledge sources` "Individual files" list)

- [ ] **Step 1: Add a Working-habits bullet**

In the `# Working habits` bulleted list, add this as a new bullet (after the existing "Restate the current source-of-truth list…" bullet):

```markdown
- At the start of a **Phase 4 or 5** run, restate which **Planner export** (filename +
  export date) and which **analysis version** you are reconciling. Treat the export as
  a dated snapshot, not live data.
```

- [ ] **Step 2: Add two starter-prompt rows**

In the `## Starter prompts` table, add these two rows at the end:

```markdown
| Reconcile against my Planner export | Here is my latest Planner export (Excel) and my Phase 1-3 output. Run Phase 4: give me the four-bucket delta — to add, superseded, mismatches (date/owner/sequence, direction-aware), and aligned — citing file and date for every row. |
| Check my Planner plan health | Run Phase 5 on my Planner export: audit RASCI coverage for my R/A/S activities, score the task descriptions, flag tasks with no sequencing as risk-analysis blind spots, and give me a scorecard with prioritized fixes. |
```

- [ ] **Step 3: Add a Planner knowledge note**

In the `## Knowledge sources` section, under the **Individual files** list, add this bullet:

```markdown
- **Your current Planner plan**, exported via Planner's **"Export plan to Excel."**
  Upload a fresh export each time you want a Phase 4 reconciliation or Phase 5 health
  check. (Planner is a dated snapshot here, not a live connection.)
```

- [ ] **Step 4: Verify all three additions are present**

Run:
```
rg -n "Reconcile against my Planner export|Check my Planner plan health|Export plan to Excel|export date" agent/03_RASCI_CROSSWALK_AGENT.md
```
Expected: matches for the two prompt titles, the knowledge note ("Export plan to Excel"), and the working-habits line ("export date").

- [ ] **Step 5: Commit**

```bash
git add agent/03_RASCI_CROSSWALK_AGENT.md
git commit -m "Add Planner starter prompts, working-habits note, and knowledge note to RASCI agent"
```

---

### Task 4: Verify the Instructions block stays under the 8,000-character limit

**Files:**
- Read only: `agent/03_RASCI_CROSSWALK_AGENT.md`

- [ ] **Step 1: Extract and measure the Instructions portion**

The Instructions field is everything from the line `# Role` through the end of the `# First message` section (the paste boundary the SETUP_GUIDE describes). Measure it:

```powershell
$lines = Get-Content "agent/03_RASCI_CROSSWALK_AGENT.md"
$start = ($lines | Select-String -Pattern '^# Role$' | Select-Object -First 1).LineNumber
$end   = ($lines | Select-String -Pattern '^## Knowledge sources' | Select-Object -First 1).LineNumber
$instr = ($lines[($start-1)..($end-2)] -join "`n")
$instr.Length
```
Expected: a number **less than 8000**.

- [ ] **Step 2: If over 8,000, tighten Phase 4/5 prose only**

If the count exceeds 8000, shorten wording inside the Phase 4 and Phase 5 sections (remove examples, compress sentences). Do **not** trim the `# Source-of-truth and recency rules` or `# Guardrails` sections. Re-run Step 1 until under 8000.

- [ ] **Step 3: Commit (only if Step 2 made changes)**

```bash
git add agent/03_RASCI_CROSSWALK_AGENT.md
git commit -m "Trim Phase 4/5 wording to fit 8000-char Instructions limit"
```

---

### Task 5: Add Planner export + reconciliation cadence to the SETUP_GUIDE

**Files:**
- Modify: `SETUP_GUIDE.md` (this guide is titled for the Senior PM Coach; add a short pointer so the Planner workflow is documented for the RASCI agent)

- [ ] **Step 1: Decide placement**

This file documents the Coach build. Add a single short subsection near the end (before "Quick troubleshooting") pointing users to the RASCI agent's new Planner workflow, so the operating loop is written down.

- [ ] **Step 2: Insert the subsection**

```markdown
## Using the RASCI agent with Planner (Phases 4–5)

The RASCI Cross-Walk Analyst can reconcile its analysis against your Microsoft
Planner plan and audit the plan's health:

1. In Planner, use **… → Export plan to Excel** to get a dated snapshot.
2. Tag each Planner task with its **RASCI ID** (title prefix like `R-014 — …` or a
   Label) so the agent matches tasks reliably.
3. Upload that Excel into the chat, then run **"Reconcile against my Planner export"**
   (Phase 4) or **"Check my Planner plan health"** (Phase 5).
4. Re-export and re-run whenever new data lands or decisions get revisited — the
   reconciliation is meant to be repeated.
```

- [ ] **Step 3: Verify**

Run:
```
rg -n "Using the RASCI agent with Planner|Export plan to Excel" SETUP_GUIDE.md
```
Expected: matches for the new heading and the export instruction.

- [ ] **Step 4: Commit**

```bash
git add SETUP_GUIDE.md
git commit -m "Document Planner export + reconciliation cadence for RASCI agent"
```

---

### Task 6: Acceptance check in Agent Builder (manual)

**Files:** none (manual verification against `agent/03_RASCI_CROSSWALK_AGENT.md`)

This is a manual gate the user performs on their work machine — list it so it isn't skipped.

- [ ] **Step 1: Re-paste fields**

In Agent Builder, paste the rewritten **Description**, the full **Instructions** block (`# Role` → end of `# First message`), and add the two new **Starter prompts**. Click Update.

- [ ] **Step 2: Phase 4 acceptance**

In "Try it", upload a small fake Planner export (a few tasks, one tagged `R-001 — …`, one with no owner, one whose date differs from the analysis) plus a short Phase 1–3 output. Run "Reconcile against my Planner export."
Expected: a four-bucket table; the date difference appears under **③ Mismatch** with a direction-of-fix statement and a file+date citation; the untagged task is marked "unconfirmed — verify."

- [ ] **Step 3: Phase 5 acceptance**

Run "Check my Planner plan health" on the same export.
Expected: a scorecard with R/A/S coverage grouped by role, the no-owner task flagged "thin / not execution-ready," and any task lacking sequencing flagged as a risk-analysis blind spot.

- [ ] **Step 4: Confirm no behavior regressions**

Run an old prompt ("Build the Phase 1 traceability matrix for rows 1-10").
Expected: unchanged Phase 1 behavior — the new phases did not disturb phases 1–3.

---

## Notes for the implementer

- This is a single Markdown file edit (plus a SETUP_GUIDE pointer). There is no build, lint, or test command — verification is the `rg` presence checks and the PowerShell character counts above, then the manual Agent Builder gate in Task 6.
- Preserve the file's existing voice and the `>` note blocks; insert new content, don't reflow surrounding text.
- The hard limits are real and enforced by Agent Builder: **Description ≤ 1,000**, **Instructions ≤ 8,000**. Tasks 2 and 4 are the guards for those.
