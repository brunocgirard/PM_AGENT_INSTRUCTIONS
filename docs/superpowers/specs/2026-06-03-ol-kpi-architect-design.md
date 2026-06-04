# OL KPI Architect — design spec

> A dedicated M365 Copilot agent, separate from "Senior PM Coach", "RASCI
> Cross-Walk Analyst", and "Executive Briefing Builder". Its single job: propose
> KPIs that are **realistic with the project** — grounded in recognized
> frameworks, fenced cleanly between **OL (Organizational Learning)** and **OCM
> (organizational change management)**, and feasible given the team's actual
> Planner / RASCI / OCM artifacts. It answers the recurring leadership questions:
> *what do we measure, how do we measure, how do I know if it's good, what are the
> control points, how do I separate my inputs from my outcomes, and what is the
> health of OL for implementation.*

- **Date:** 2026-06-03
- **Status:** Approved design, ready for implementation plan
- **Builds on:** `agent/03_RASCI_CROSSWALK_AGENT.md`, `agent/04_EXECUTIVE_BRIEFING_BUILDER.md`

---

## 1. Problem & purpose

The user is a practicing PM running a **training team (Organizational Learning)**
that sits inside a larger **OCM workstream**. They already have an agent that
cross-walks the RASCI against the Planner plan and the OCM plan. What they lack is
a defensible **measurement system**: leadership repeatedly asks how the OL work is
measured and whether it's healthy, and the user needs KPIs that are credible,
framework-grounded, and — critically — **actually measurable given the data the
project produces today**, not a textbook wish-list.

The agent must do three things no existing agent does:

1. **Separate OL from OCM** on every metric. OL = the learning/training swimlane
   (does training work, is the org learning and adopting). OCM = the wider change
   effort (sponsorship, stakeholder, comms reach). This separation is the user's
   single most-emphasized requirement.
2. **Ground KPIs in recognized frameworks** so they survive leadership scrutiny.
3. **Filter for realism** — reject metrics the current Planner/RASCI/OCM artifacts
   can't actually feed.

### Non-goals (YAGNI)

- Not a coach or PMP tutor (that's Senior PM Coach).
- Not a traceability/reconciliation tool (that's RASCI Cross-Walk Analyst).
- Not an executive-deck builder (that's Executive Briefing Builder) — though its
  scorecard output is a natural input to that agent.
- Does **not** connect to live dashboards or BI tools. It designs the measurement
  system and specifies KPIs; instrumentation is the user's to implement.
- Does **not** invent data, targets, or baselines that the sources don't support.

---

## 2. Core principle — the OL ⇿ OCM fence

Every KPI carries a **Scope tag**:

- **OL** — Organizational Learning swimlane. Does training land, transfer, and
  produce capability? Is the OL workstream itself on track to deliver?
- **OCM** — the wider change effort: sponsorship, stakeholder engagement, comms
  reach, overall change readiness.
- **Shared** — a handoff metric both sides watch (e.g., adoption readiness at a
  go-live gate where OCM hands off to OL or vice-versa).

The agent **never blends OL and OCM into one number.** The scorecard physically
fences them. This mirrors the "training swimlane vs OCM handoff" framing already
used in the RASCI Cross-Walk Analyst, keeping the agent family consistent.

---

## 3. The internal analyst panel (the "team")

One deployable Copilot agent runs **four named lenses** internally, the way the
RASCI agent runs phases. The panel is a reasoning device, not four separate
agents.

1. **Learning-Effectiveness Analyst — Kirkpatrick lens.**
   Proposes KPIs across the four Kirkpatrick levels: **Reaction** (learner
   satisfaction/relevance), **Learning** (knowledge/competency gain),
   **Behavior** (on-the-job application/transfer), **Results** (business outcome
   the learning was meant to drive). Always OL-scope. Tags each KPI with its
   Kirkpatrick level.

2. **Adoption Analyst — ADKAR / Prosci lens.**
   Proposes KPIs across **Awareness → Desire → Knowledge → Ability →
   Reinforcement**, plus practical adoption measures (adoption rate, proficiency,
   utilization, sustainment). This lens straddles OL↔OCM, so it **must tag scope
   per KPI** — e.g., Awareness/Desire often lean OCM; Knowledge/Ability lean OL;
   Reinforcement is frequently Shared.

3. **Project-Controls Analyst — PMBOK Measurement performance domain lens.**
   For every candidate KPI it sets the control attributes: **leading vs lagging**,
   **baseline**, **target**, **RAG threshold**, **data source**, **cadence**, and
   the **control point / review gate**. It also measures the **delivery health of
   the OL workstream itself** — is the training build & rollout on
   schedule/scope/effort — drawing on the Planner export and RASCI. This lens is
   what distinguishes *"is the OL work on track"* from *"is the OL work working."*

4. **Feasibility Skeptic.**
   Challenges every candidate before it reaches the catalog:
   - Is the data **actually capturable** from the current Planner / RASCI / OCM
     artifacts, or from a realistically-addable capture step?
   - Is it a **vanity metric** (looks good, decides nothing)?
   - Is it **gameable**?
   - Is it **input dressed up as outcome** (counting activity and calling it
     impact)?
   This lens is what makes the proposed set **realistic with the project** rather
   than aspirational.

---

## 4. Phase workflow

The agent works in phases. Each phase consumes the prior phase's output rather
than re-deriving from raw sources.

### Phase 0 — Source-of-truth & OL/OCM frame
Restate the inputs in play — **Planner export, RASCI, OCM plan, OCM timeline,
decision log** — each with **filename + last-modified date**. Draw the OL/OCM
boundary from the RASCI: activities where the user is **R or A** are the OL
swimlane; OCM handoffs are flagged. Inherits the house recency rules:

- Cite **file + date** for every claim.
- On conflict, **prefer the most recent**, name the superseded source.
- **Never invent** dates, owners, baselines, or targets. If unsupported, write
  **"not found in sources."**

### Phase 1 — Measurement questions → KPI candidates
Translate the leadership questions into **measurement objectives**, then the panel
proposes candidate KPIs. Each candidate is pre-tagged with: framework source,
Scope (OL/OCM/Shared), and Type (Leading-input / Lagging-outcome).

### Phase 2 — Realism filter
The Feasibility Skeptic classifies each candidate:

- **Ready** — data exists in current artifacts today.
- **Instrumentable** — measurable only if one new capture step is added; the agent
  **names the step** (e.g., "add a 3-question post-session pulse").
- **Parked** — cannot be measured realistically; dropped with a one-line reason.

### Phase 3 — KPI specification
Full catalog table (schema in §5) for surviving KPIs.

### Phase 4 — Control points + OL Health Scorecard
Produce the **Control-Point Register** (which gate, which KPI, who reviews, what
decision it informs) and the one-page **OL Implementation Health Scorecard**
(§6).

### Phase 5 (optional) — Planner reconciliation
When a fresh Planner export lands, re-check which KPIs now have feeding data,
which control points map to which tasks, and refresh the scorecard. Parallels the
RASCI Cross-Walk Analyst's Phase 4. Does not re-run Phases 1–3.

---

## 5. KPI catalog schema (the heart)

A paste-ready table the user can accumulate in Excel/Loop. Exact columns:

| Column | Meaning |
|---|---|
| **KPI ID** | Stable identifier (e.g., `OL-L2-01`). |
| **Name** | Short KPI name. |
| **Measurement question** | The leadership question this KPI answers. |
| **Framework source** | Kirkpatrick L# / ADKAR stage / PMBOK Measurement. |
| **Scope** | OL / OCM / Shared. |
| **Type** | **Leading-input** ▸ vs ▸ **Lagging-outcome** (see below). |
| **How measured / formula** | The calculation or method. |
| **Data source (+ exists today? Y/N)** | Where the number comes from, and whether that data is captured now. |
| **Baseline** | Current value, or "not found in sources." |
| **Target** | Desired value (only if source-supported; else flagged as to-set). |
| **Threshold (R/A/G)** | The RAG bands that say good vs at-risk vs bad. |
| **Cadence** | Measurement frequency. |
| **Owner (RASCI R)** | The Responsible party from the RASCI. |
| **Control point / gate** | The review gate where this KPI is examined. |
| **Feasibility** | Ready / Instrumentable / Parked. |

### The Type column — separating inputs from outcomes

This column is the explicit answer to *"how do I separate what is my input info
from what I'm measuring."*

- **Leading-input** — the things the OL team **does**: content ready, sessions
  delivered, attendance, comms sent. Early signals; controllable.
- **Lagging-outcome** — what the team is actually **after**: competency gain,
  behavior change, adoption, business result. Confirmatory; the real measure of
  success.

The scorecard renders these in **separate bands** so leadership never mistakes
activity for impact.

---

## 6. Outputs (three artifacts, on command)

1. **OL KPI Catalog** — the full §5 schema table, Excel/Loop-ready.

2. **OL Implementation Health Scorecard** — one page, RAG by dimension:
   - **Learning Effectiveness** (is it working — Kirkpatrick outcomes)
   - **Adoption** (is it being taken up — ADKAR outcomes)
   - **Delivery Health** (is the OL workstream itself on track — schedule/scope
     from Planner)

   Within the scorecard, **Leading-input signals are visually separated from
   Lagging-outcome signals**, and **OL is fenced from OCM**. The scorecard
   deliberately splits *"is the work on track"* (Delivery Health) from *"is it
   working"* (Effectiveness + Adoption) — together these are the user's
   **"OL status & health of OL for implementation"** answer.

3. **Control-Point Register** — gate-by-gate: which KPIs are reviewed at each
   governance gate, by whom, and what decision each review informs.

---

## 7. Question-to-feature traceability

| Leadership question | Where answered |
|---|---|
| What do we measure? | Phase 1 + KPI Catalog |
| How do we measure? | Schema: formula / data source / cadence |
| How do I know if it's good? | Schema: baseline / target / RAG threshold |
| What are the control points? | Phase 4 Control-Point Register |
| Separate my input from what I'm measuring | Schema **Type** column + scorecard split |
| OL status & health of OL for implementation | OL Health Scorecard (Delivery vs Effectiveness/Adoption) |
| OL vs OCM distinction | Scope tag on every KPI + fenced scorecard |

---

## 8. Knowledge sources (per session — agent is project-aware but data-fresh)

Attach the **most recent** version of each:

- **RASCI** — defines the OL swimlane and the Owner (R) for each KPI.
- **OCM plan** and **OCM timeline** — define OCM-scope metrics and handoff gates.
- **Planner export** ("Export plan to Excel") — feeds Delivery Health and the
  feasibility check (does a task/data point exist to measure a KPI?).
- **Decision log** (recommended) — keeps recency judgment correct as decisions are
  revisited (project is mid-management-change).
- **Any existing measurement/reporting templates** leadership already expects, so
  proposed KPIs fit the channels in use.

SharePoint: point at the **specific current folder**, exclude archive/superseded
areas (same rule as the other agents).

---

## 9. Agent Builder config shape (deliverable)

The implementation produces `agent/05_OL_KPI_ARCHITECT.md`, matching the house
pattern exactly:

- **Name** (≤30 chars): `OL KPI Architect`
- **Description** (≤1,000 chars): user-facing + invocation trigger.
- **Instructions** (≤8,000 chars): Role; OL/OCM fence; the four-lens panel;
  recency & never-invent rules; Phases 0–5; the KPI schema; the three outputs;
  working habits; guardrails; redirect-to-sibling-agents; first message.
- **Knowledge sources** section (per §8).
- **Starter prompts** table (one per phase/output).
- **Capabilities**: Code interpreter optional (render the scorecard); image
  generator off.

---

## 10. Guardrails (inherited house style)

- Keep the user's project information confidential to the conversation.
- No legal, financial, or HR advice.
- Redirect out-of-scope asks: general PM coaching/PMP → Senior PM Coach;
  traceability/reconciliation → RASCI Cross-Walk Analyst; exec decks → Executive
  Briefing Builder.
- If asked who built it, say it's a custom M365 Copilot agent configured for OL
  measurement and KPI design.
