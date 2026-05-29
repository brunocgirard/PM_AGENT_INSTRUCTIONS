# Planner Reconciliation & Plan-Health — Phases 4 & 5 for RASCI Cross-Walk Analyst

**Date:** 2026-05-29
**Status:** Design — pending user review
**Affects:** `agent/03_RASCI_CROSSWALK_AGENT.md` (existing M365 Copilot Agent Builder config)

---

## Problem

The RASCI Cross-Walk Analyst already produces Phases 1–3: a traceability matrix,
a gap/conflict list, and a proposed revised baseline timeline. The user acts on
that output inside **Microsoft Planner**. But the project is mid-management-change,
so new data keeps arriving and decisions get revisited. The Planner plan and the
agent's analysis drift apart over time.

Two needs follow from that:

1. **Reconciliation (the delta).** After new data lands, compare the analysis
   against the *live* Planner state and surface exactly what changed and what to
   update — in either direction.
2. **Plan health (the audit).** Assess whether the Planner plan is actually fit to
   run the project: does it cover the RASCI, are tasks well described, and is there
   enough sequencing to derive a critical path for risk analysis?

## Decision

Extend the **existing** agent (Approach C), not build a separate one. The work is
the same domain (RASCI ↔ timeline traceability) and reuses the agent's existing
recency machinery ("prefer the most recent source, cite file + date, flag
superseded, never invent"). Add two new, self-contained phases that can each run
standalone when only Planner — or only the sources — changed.

Planner data reaches the agent via **Planner's built-in "Export plan to Excel"**,
uploaded (or dropped in the SharePoint folder) each cycle. No Copilot Studio, no
admin lift. The agent compares against that dated snapshot.

## Shared prerequisite — the RASCI-ID tag

Planner has no stable IDs or native dependencies that line up with the RASCI.
Without a shared key the agent must fuzzy-match on task title, which is where it
could guess wrong. **Convention:** tag each Planner task with its RASCI ID — as a
title prefix (e.g. `R-014 — Draft training comms`) or a Planner **Label**. The
agent matches on that tag first; absent a tag it falls back to title similarity and
marks the match **"unconfirmed — verify."** It never silently guesses a match.

This convention is documented in the agent config and in the operating notes so the
user maintains it going forward.

---

## Phase 4 — Planner reconciliation (the delta)

**Trigger.** Run any time new data has landed — a fresh Planner export, a revised
source doc, or both. Does NOT re-run Phases 1–3; consumes their output plus the new
Planner snapshot.

**Inputs each cycle.**
- Latest **Planner Excel export** (Task Name, Bucket, Assigned To, Start/Due dates,
  Progress, Labels).
- The agent's **Phase 3 revised baseline** (in-session, or re-pasted in a new session).
- Optionally, **new/updated source docs** since the last run.

**Matching.** RASCI-ID tag first; title-similarity fallback marked "unconfirmed —
verify." Unmatched-but-expected items are reported, never dropped.

**Output — four-bucket delta report** (clean, paste-ready tables):

| Bucket | Meaning | Proposed action |
|---|---|---|
| **① To add** | In the analysis (gap list / Phase 3) but no matching Planner task | Insert task: bucket, assignee = R from RASCI, due date, predecessor |
| **② Now unsupported / superseded** | Exists in Planner, but latest sources changed or removed it | Flag for review/removal — cite newer source + date |
| **③ Mismatch** | Task in both, but date, owner, or sequence differs | Show both values, cite which is newer, propose the correction |
| **④ Aligned** | Confirmed match | Listed briefly so coverage is visible |

Plus a one-line **"what changed since last reconciliation"** note explaining *why*
the delta moved.

**Bucket ③ — mismatch handling, made precise.** For any task matched in both,
compare three fields; each disagreement is its own line:

| Field | Analysis source | Planner source | Resolution rule |
|---|---|---|---|
| **Due / start date** | Phase 3 / sources | Planner export | Prefer the value backed by the most recent dated source; if Planner is newer truth, say so and propose updating the *analysis* |
| **Owner (R)** | R from RASCI | Assigned To | Flag; cite which is newer; never auto-pick — present both |
| **Sequence / predecessor** | Phase 3 | (none native in Planner) | Note Planner can't hold dependencies; recommend capturing in Description or checklist |

**Direction-awareness is mandatory.** A mismatch does not always mean "fix Planner."
If the Planner task was edited more recently than the source, the *analysis* may be
stale. The agent states which way the correction should flow, citing dated evidence.

Every row obeys the existing rules: cite file + date, prefer most recent, flag
superseded, never invent dates/owners.

---

## Phase 5 — Planner plan health & risk-readiness check (the audit)

A periodic assessment (not a delta) of whether the Planner plan is fit to run the
project and support risk analysis. Three lenses, ending in a short scorecard.

**Lens 1 — RASCI coverage.** For every RASCI activity where the user is **R, A, or
S**, is there a corresponding Planner task? Report covered vs. uncovered and a simple
coverage ratio, grouped by role so R/A gaps (where the user is on the hook) read as
higher-priority than S gaps. (Distinct from Phase 4 ①: that bucket is new gaps from
the latest analysis; this is a standing audit of the whole plan against the whole
RASCI.)

**Lens 2 — Task description quality.** Score each task against a rubric:
- Clear outcome/deliverable (not just a bare verb in the title)
- Owner assigned (Assigned To populated)
- Due date set (and start date where relevant)
- Enough Description/checklist to be actionable

Flag "thin" tasks (title-only, no owner, or no date) as **not execution-ready**, with
a one-line suggested rewrite.

**Lens 3 — Critical-path & risk readiness.** Planner has **no native dependency or
critical-path feature**, so:
- Derive likely critical-path candidates from the predecessor/successor info the
  agent already holds in Phase 3.
- Flag tasks with no sequencing info as **blind spots for risk analysis** — you
  cannot assess schedule risk on work you cannot sequence.
- Recommend a lightweight way to capture dependencies in Planner so a critical path
  and risk register can actually be built (e.g. a `Depends-on: <RASCI ID>` line in
  Description, or a dependency Label).

**Output — scorecard + prioritized fix list:**
- RASCI coverage: `X of Y` activities have tasks, broken out by R / A / S (R/A gaps ranked above S)
- Thin tasks: count + list
- Tasks missing sequencing: count + list (the risk-analysis blind spots)
- Prioritized fixes, highest-leverage first

---

## Changes to `03_RASCI_CROSSWALK_AGENT.md`

1. **Instructions** — add `# Phase 4 — Planner reconciliation` and `# Phase 5 —
   Planner plan health & risk-readiness check` after the existing Phase 3 section,
   each written as a self-contained pass.
2. **Shared prerequisite** — add the RASCI-ID tag convention (a short subsection the
   two phases reference).
3. **Description (≤1,000 chars)** — add one clause noting the agent now reconciles
   against a Planner export and audits plan health. Re-check the character count.
4. **Working habits** — at the start of a Phase 4/5 run, restate which Planner export
   (filename + export date) and which analysis version is being reconciled.
5. **Starter prompts** — add two rows: "Reconcile against my Planner export" and
   "Check my Planner plan health."
6. **Knowledge sources note** — mention uploading the current Planner Excel export
   each cycle.
7. **Guardrails / recency rules** — reused as-is, no duplication.

Watch the **8,000-character Instructions limit**. Phases 4–5 add an estimated
~1,800–2,200 chars to the current instructions; if the total would exceed the limit,
tighten wording (the phase bodies, not the recency rules) rather than dropping a phase.

## Out of scope

- Live Planner/Graph connection (Copilot Studio) — explicitly deferred.
- Auto-writing changes back into Planner — the agent proposes; the user applies.
- Any change to the Senior PM Coach agent.

## Success criteria

- Given a Planner export + the Phase 1–3 output, Phase 4 returns the four-bucket
  delta with direction-aware mismatch resolution, every row citing file + date.
- Phase 5 returns the three-lens scorecard, flagging thin tasks and sequencing blind
  spots, and recommending how to capture dependencies for critical-path/risk work.
- Both phases run standalone and never invent dates, owners, or matches.
- The edited config stays within the 8,000-character Instructions limit.
