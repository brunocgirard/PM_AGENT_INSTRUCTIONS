# Planner AI Report Prompt Library — Design

**Date:** 2026-05-29
**Author:** Bruno C. Girard
**Status:** Approved for build (pending spec review)

## Goal

A reusable library of copy-paste prompts that drive Microsoft Planner's
**Status Reports** feature (the *Planner Agent*, formerly "Project Manager
agent") to produce executive-grade project reports. Each report is generated
into a Microsoft **Loop** page. The prompts give executives and stakeholders
visibility into status, risk, schedule health, and weekly progress, and are
designed to be **reused across any project** with little or no editing.

## How the target feature actually works (verified)

- **Where:** Microsoft Teams **desktop** Planner app → open a **Premium** plan →
  **Reports** tab → **Get Started**. (The Reports tab does *not* appear in the
  browser version.)
- **Flow:** pick a **reporting period** from the dropdown → type instructions
  into the **"Provide more details"** free-text box → **Generate** → the report
  is written into a **Loop page** (a `.loop` file in the creator's
  OneDrive/SharePoint), shareable into Teams/Outlook or "as a newsletter."
- **Critical design consequence:** the "Provide more details" box is an
  **instructions** field, *not* a data field. The agent reads the plan's data
  itself via Microsoft Graph. **We never paste task data into the prompt.**
  This makes every prompt **inherently project-agnostic** — the same text works
  on any plan, because the agent reads whatever plan is open.
- **Prerequisites:** Planner Premium plan; M365 Copilot license (to generate);
  Loop enabled by admin; plan shared with a group; **≥10 tasks** in the plan.

### Plan data the agent can read

- **Confirmed:** task names, due dates, % complete / progress, assignments,
  milestones, overdue items, recent activity, buckets, labels, and **Priority**
  (this plan uses Planner's **Urgent / Important / Medium / Low** values).
- **Priority is a first-class risk signal:** Urgent/Important tasks that are
  overdue, due-soon, or on the critical path are weighted up in risk derivation
  and "top risks" ranking.
- **Unconfirmed by Microsoft:** task **dependencies** and **critical path**
  (they exist in the Premium Timeline view, but MS has not documented that the
  report agent reads them); sprints; effort/duration; custom fields.
- **Design response:** prompts *use* critical path / dependencies **when
  present** and **gracefully fall back** to overdue / slipping / due-soon tasks,
  emitting an explicit note rather than inventing a critical path.

### Loop rendering

- **Supported:** headings (H1–H3, collapsible), tables (named columns; no cell
  merge/sort), bulleted & numbered lists, checklists, callouts, dividers, quote
  blocks, emoji, code blocks — and **Mermaid** (via `/mermaid` or a
  ```` ```mermaid ```` code block): flowcharts, **gantt**, **quadrantChart**,
  mindmaps.
- **Mermaid caveats:** (1) it is **static** — no live link to plan data, so a
  chart is a point-in-time **snapshot**; (2) whether the *report agent itself*
  emits Mermaid on request is **unverified** — so every chart instruction is
  best-effort with a **table fallback**, and the user may need to drop in a
  `/mermaid` block manually after generation. If a Mermaid preview greys out,
  clearing browser cache is the known fix.
- **No native Gantt/chart component** exists in Loop — Mermaid is the only route.

## Deliverable

A `planner-reports/` folder at the project root containing:

| File | Purpose | Primary audience |
|---|---|---|
| `00_README.md` | How/where to use, prerequisites, RAG legend + thresholds, Mermaid notes, review-before-send | The PM (you) |
| `01_executive_status_onepager.txt` | Plan-on-a-page RAG status | Steering committee / executives |
| `02_risk_criticalpath_analysis.txt` | Schedule-derived risk + risk register + heat-map | PM + sponsor |
| `03_weekly_update.txt` | Weekly progress (lean, operational) | Project team / delivery lead |
| `04_milestone_schedule_health.txt` | Milestone tracker + variance + Gantt | PM + PMO |

Each `.txt` is the exact block to paste into "Provide more details." A short
HTML-comment header at the top of each file (version, date, audience, usage)
sits *outside* the prompt body so it can be left in or trimmed.

## Shared prompt skeleton (every report follows this order)

1. **Role / persona** — "senior project analyst producing a [report] for [AUDIENCE]."
2. **Source-of-truth rule** — use **only this plan's data**; never invent dates,
   owners, %s, or risks; if a field is missing write **"Not available in plan."**
3. **Exact output structure** — numbered sections, named **verbatim**, in order;
   **do not add/remove/rename**; if a section has no data keep the heading and
   write "Not available in plan" (prevents layout drift on reuse).
4. **RAG legend (emoji-only)** — 🟢 On track · 🟡 At risk · 🔴 Off track ·
   ⬜ Not available. "Use these only; no other symbols."
5. **Loop formatting rules** — `##` title, `###` sections; callout (`>`) for the
   header block; tables with the **exact named columns** given; checklists for
   task lists; em dashes; no invented sections/columns.
6. **Mermaid rule (where applicable)** — emit the specified chart in a
   ```` ```mermaid ```` block with caption **"Snapshot as of [date]"**; **if you
   cannot render a diagram, output the equivalent table instead.**
7. **Tone & length caps** — formal, factual; no filler/praise/hedging; explicit
   bullet/word caps per section.
8. **Closing reminder** — output is a **draft to be reviewed** before distribution.

**Placeholders:** kept minimal because the agent reads the active plan. Standard
ones: `[AUDIENCE]` (+ short audience description) and optional `[SPONSOR]` in the
asks section. `[REPORTING PERIOD]` is also chosen in the UI dropdown; it appears
in the prompt only as a reinforcing label.

## Per-report section maps

### 01 — Executive status one-pager (RAG plan-on-a-page)
1. **Header callout** — Project · Reporting period · PM · Date · **Overall RAG**.
2. **Status dashboard** — table `Dimension | Status | Note (≤10 words)`; rows:
   **Schedule, Scope, Resources, Risk**. (No Budget row — Planner has no cost
   field, so budget can't be read from any plan; omitted by design.) Schedule
   and Risk are the strongest signals; Scope and Resources are best-effort from
   plan data (added/removed tasks; assignments/unassigned/over-concentration) —
   ⬜ if not inferable.
3. **Executive summary** — ≤3 bullets: current state · top risk · key ask.
4. **Milestone timeline** — Mermaid **gantt** of milestones (status-coded),
   caption "Snapshot as of [date]"; fallback table
   `Milestone | Baseline | Forecast | Status | Owner`.
5. **Top risks (3–5)** — table `Risk | Impact | Owner | Mitigation | RAG`.
6. **Decisions / asks** — numbered: decision · from whom · by when.
7. **Accomplished / Next period** — two bullet lists, ≤5 each.

### 02 — Risk & critical-path analysis
1. **Header callout** — Project · Period · **Overall Risk RAG** · Date.
2. **Schedule-derived risk signals** — derived from the plan: critical-path
   tasks (if available), overdue tasks, slipping milestones, near-term
   dependencies, and **high-priority (Urgent/Important) tasks at risk**. If
   critical path is unavailable, state so explicitly and derive from due dates /
   overdue / dependencies / priority.
3. **Risk register** — table `ID | Risk | Category | Probability (H/M/L) |
   Impact (H/M/L) | Score | Response (Avoid/Transfer/Mitigate/Accept/Escalate) |
   Owner | Trigger | Status`. Risks are built **from the schedule signals above
   plus task Priority (Urgent/Important first) plus any tasks/labels explicitly
   flagged as risks**; each row must cite its **basis** (e.g., "Urgent task, 12
   days overdue on critical path") and be marked **"recorded"** (from the plan)
   or **"derived"** (inferred from schedule/priority). Qualitative scoring is
   analysis, not fabrication — but it must trace to a concrete plan fact.
4. **Risk heat-map** — Mermaid **quadrantChart** (x = Probability, y = Impact)
   plotting the top risks; caption "Snapshot as of [date]"; fallback: a
   Probability×Impact table.
5. **Recommended actions** — for red/amber risks: action · owner · by when.
6. **Watch list** — lower-severity risks to monitor.

### 03 — Weekly update (lean, tables only — no Mermaid)
1. **Header callout** — Project · Week of [period] · PM · **Overall RAG** + one-sentence comment.
2. **Status pills** — Schedule / Scope / Resources / Risk (no Budget).
3. **Accomplished this week** — bullets (tasks completed in period).
4. **Planned next week** — bullets (upcoming tasks).
5. **Milestone tracker (compact)** — `Milestone | Forecast | Status`.
6. **Blockers & issues** — issue · owner · what's needed.
7. **Decisions needed** — numbered: what · from whom · by when.
8. **Top risks** — top 3, one line each.

### 04 — Milestone / schedule health
1. **Header callout** — Project · Period · **Overall Schedule RAG** · % complete · Date.
2. **Milestone Gantt** — Mermaid **gantt** (done/active/crit coding), caption
   "Snapshot as of [date]"; fallback to the tracker table below.
3. **Milestone tracker** — table `ID | Milestone | Phase | Baseline | Forecast |
   Actual | Variance (days) | Status | Owner | Recovery (if amber/red)`.
4. **Overdue tasks** — `Task | Owner | Days late`.
5. **Critical path / at-risk** — critical-path tasks with float **if available**;
   else due-soon + dependency-driven, with the limitation noted.
6. **Next 30 / 60 / 90-day milestones** — grouped, RAG-coded.
7. **Schedule commentary** — 2–3 sentences on trend, within plan data only.

## README contents (00)

- What it is; where the feature lives (step-by-step); prerequisites.
- Why the prompts are reusable across projects (agent reads the active plan).
- How to fill `[AUDIENCE]` / `[SPONSOR]`.
- **RAG legend + threshold reference** (schedule / scope / resources / risk —
  Green/Amber/Red definitions) so status is consistent and defensible.
- **Mermaid notes:** static snapshot; may need a manual `/mermaid` paste if the
  agent omits it; clear browser cache if the preview greys out.
- **Review-before-send** warning (MS treats output as a draft).
- Operating tips: generate fresh each period; be specific; min 10 tasks.
- Short "sources / further reading" list.

## Anti-goals (YAGNI)

- No data-paste workflow (the agent reads the plan).
- **No EVM/SPI/CPI math** (recommended and accepted): Planner lacks baseline
  cost/effort, so any index would be fabricated/misleading. Schedule health uses
  milestone variance, % complete, overdue, and critical-path/priority signals.
- **No Budget reporting** anywhere: Planner has no cost field; budget can't be
  read from any plan, so the Budget pill is omitted (not shown as "unavailable").
- No single mega-prompt with conditional logic — one standalone file per report.
- No Power BI / Charts-view integration — out of scope for the Loop report.

## Success criteria

- Pasting any prompt into a real Premium plan produces a one-page, consistently
  structured Loop report with stable section order across runs and projects.
- Missing data degrades gracefully ("Not available in plan") instead of being
  invented.
- Charts render when the agent supports them and fall back to tables when not.
- The prompts require no per-project editing beyond `[AUDIENCE]`.

## Sources

- MS Support — *Generate automatic status reports with Planner agent*
- MS — *FAQ about Planner agent*; TechCommunity Planner blog
- Loop + Mermaid: MS Q&A (static, no live data link), mspoweruser, MS Learn
- Reporting standards: ProjectManager.com, Mastt, Rebel's Guide to PM (RAG),
  RAIDlog / U. Waterloo PMO (RAID), Praxis (milestone slip chart), PMI (EVM &
  critical path), PMBOK 7 performance domains (Measurement, Uncertainty).
