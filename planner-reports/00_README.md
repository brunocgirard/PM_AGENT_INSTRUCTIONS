# Planner AI Report Prompts — Reusable Library

Copy-paste prompts that drive **Microsoft Planner's Status Reports** feature (the
*Planner Agent*) to produce executive-grade reports in a **Loop** page. The same
prompts work on **any project** — you never paste task data, so just open the
plan you want and paste the prompt.

## The four reports

| File | Report | Use it for | Audience |
|---|---|---|---|
| `01_executive_status_onepager.txt` | Plan-on-a-page RAG status | Monthly/steering visibility | Executives / sponsors |
| `02_risk_criticalpath_analysis.txt` | Risk + critical-path analysis | Risk reviews, governance | Sponsor + PM |
| `03_weekly_update.txt` | Weekly progress (lean) | Team cadence | Project team / delivery lead |
| `04_milestone_schedule_health.txt` | Milestone tracker + variance | Schedule deep-dive | PM + PMO |

## How to generate a report

1. Open **Microsoft Teams (desktop app)** → **Planner** → open your **Premium**
   plan. *(The Reports tab does not appear in the browser version of Planner.)*
2. Go to the **Reports** tab → **Get Started**.
3. Choose the **reporting period** in the dropdown.
4. Open the prompt file, fill the `[PLACEHOLDERS]` (see below), and copy
   **everything below the `PASTE BELOW THIS LINE` divider** into the
   **"Provide more details"** box.
5. Click **Generate**. The report opens as a **Loop page** you can share into
   Teams/Outlook or "as a newsletter."
6. **Review and correct the draft before distributing.** Microsoft treats the
   output as a draft — the agent reads real task data but can misframe it.

### Prerequisites (one-time)

- A **Planner Premium** plan (the new Planner; formerly Project for the web).
- A **Microsoft 365 Copilot** license (needed to *generate*; viewing/editing the
  Loop page does not).
- **Loop** enabled by your admin.
- The plan is **shared with a group** (Teams-created plans already are).
- The plan has at least **10 tasks**.

## Placeholders

The prompts are project-agnostic because the agent reads whatever plan is open.
The only things you fill in are:

| Placeholder | What to put | Example |
|---|---|---|
| `[AUDIENCE]` | Who the report is for + what they need | `Executive Steering Committee — non-technical sponsors who need health, risks, and decisions in 90 seconds` |
| `[REPORTING PERIOD]` | The period label (also set in the dropdown) | `week of 26–30 May 2026` |
| `[SPONSOR]` *(optional)* | Named decision-maker for the asks section | `Maria Lopez, VP Operations` |

Tip: keep one filled-in copy per project if your audience wording is stable, so
you don't re-type it each period.

## RAG legend & thresholds (keep these consistent)

The prompts tell the agent to use **these emoji only**:

> 🟢 On track · 🟡 At risk, monitor · 🔴 Off track, action required · ⬜ Not available in plan

Suggested thresholds (edit to match your PMO's published standard):

| Dimension | 🟢 Green | 🟡 Amber | 🔴 Red |
|---|---|---|---|
| **Schedule** | No milestone slip; critical path intact | Slip ≤ ~1 reporting period; buffer shrinking | Slip > 1 period **or** critical-path milestone late |
| **Scope** | Baseline scope holding | Change requests pending / unapproved adds | Scope changed without approval |
| **Resources** | Work assigned & balanced | Key tasks unassigned or over-concentrated | High-priority work blocked by resource gaps |
| **Risk** | No high risks open | One or more mediums need active mitigation | A high risk likely to materialize / no mitigation |

> **Why no Budget pill?** Planner has no cost field, so budget can't be read from
> any plan. It's omitted by design rather than always showing "Not available."
> If you track budget elsewhere, add a Budget line to the Loop page manually.

## Mermaid charts (read this)

Reports `01` and `04` request a **Mermaid Gantt**, and `02` a **Mermaid
quadrantChart** (risk heat-map). Important caveats:

- **Static snapshot.** Mermaid in Loop has *no live link* to the plan — a chart
  is frozen at generation time. Each prompt adds a *"Snapshot as of [date]"*
  caption so readers know.
- **Best-effort.** Whether the Planner Agent emits Mermaid on request is not
  guaranteed. Each prompt instructs a **table fallback** if it can't. If the
  chart is missing and you want it, add it manually: in the Loop page type
  `/mermaid` (or a ` ```mermaid ` code block) and paste a diagram.
- If a Mermaid **preview greys out** in Loop, clearing the browser cache fixes it.

## Notes & known limits

- **Critical path / dependencies:** they exist in the Premium Timeline view, but
  Microsoft hasn't documented that the report agent reads them. The prompts use
  them *if present* and otherwise fall back to due-soon / overdue / dependency /
  **priority** signals, stating the limitation — never inventing a critical path.
- **Priority** (Urgent / Important / Medium / Low) is used as a risk-weighting
  signal across reports.
- **No EVM/SPI/CPI** — Planner has no cost/effort baseline, so those indices
  would be misleading. Schedule health uses milestone variance, % complete,
  overdue, and critical-path/priority instead.
- Start a **fresh report each period** so prior context doesn't bleed in.

## Sources / further reading

- Microsoft Support — *Generate automatic status reports with Planner agent*; *FAQ about Planner agent*.
- Loop + Mermaid (static, no live link): Microsoft Q&A; MS Learn; mspoweruser.
- Reporting standards: ProjectManager.com (exec status), Mastt (plan-on-a-page, RAG),
  Rebel's Guide to PM (RAG/BRAG), RAIDlog & U. Waterloo PMO (RAID), Praxis
  (milestone slip chart), PMI (EVM & critical path), PMBOK 7 (Measurement &
  Uncertainty performance domains).
