# Executive Briefing Builder — Design Spec

Date: 2026-05-29
Status: Approved for implementation pending user review of this spec.

## Purpose

A new, dedicated M365 Copilot agent — the third alongside **Senior PM Coach**
and **RASCI Cross-Walk Analyst** — that ingests a project's source material
(meeting notes, reviewed/approved charter, other docs, and a context pack of
extrapolated assumptions), **validates each claim by provenance**, and produces
two executive-facing outputs on command:

- **Mode A** — a one-page **Current → Target → Gap** briefing as a **Word
  document**.
- **Mode B** — an **ultra-tight 3–5 slide** build spec formatted to feed
  **Copilot in PowerPoint** ("Create presentation from file").

The agent is **project-agnostic**: you supply one project's sources per session,
it restates the source-of-truth, validates, then builds. It bakes in no real
project data (confidentiality + reusability).

## Why this shape

- **One agent, two modes** (not two agents): both outputs draw on the same
  validated source-of-truth and the same narrative skeleton, so they cannot
  drift apart. Re-ingesting/re-validating twice in two agents would risk two
  different stories.
- **Follows the existing pattern**: same config structure as
  `agent/03_RASCI_CROSSWALK_AGENT.md` (Name / Description / Instructions /
  Knowledge / Starter prompts / Capabilities), same strict citation + recency
  discipline, same per-session source-of-truth restatement.

## The provenance / validation engine (trust core)

The user's source hierarchy, captured during brainstorming:

> Meeting notes (raw evidence) → reviewed/approved charter + other approved docs
> (authoritative) → context pack (the user's **extrapolated assumptions**).

Every claim the agent surfaces is classified into one of three tiers:

| Tier | Definition | Where it may appear |
|---|---|---|
| **Validated** | Traceable to the reviewed/approved charter, meeting notes, or another approved doc. Cite **file + date**. | On-slide / on-page facts |
| **Assumption** | Exists only in the context pack as the user's extrapolation. Agent names the evidence it was extrapolated from and whether the leap is reasonable. | "Assumptions & to-confirm" block + speaker notes only — **never** an on-slide fact |
| **Conflict** | Sources disagree. Flag both with dates, prefer the most recent, surface as a first-class finding. | Flagged to user; resolved before it reaches a slide |

Hard rules (mirroring the RASCI agent):

- Cite **file + date** for every validated claim.
- **Never invent** dates, owners, scope, or milestones. Write **"not found in
  sources"** when unsupported.
- Prefer the **most recent** source on conflict; name the superseded one.
- Keep assumptions out of on-slide facts; route them to the to-confirm area so
  the user knows exactly what still needs validation before it can be promoted.

## Shared narrative skeleton

Both modes use the same arc. **Current → Target → Gap** are firm and
fact-driven. **Plan** and **Leadership Ask** are present but framed as **open /
collaborative** — what the user is seeking the *other team's* input on, not a
finished plan. (This matches the user's actual scenario: the deck is presented
to another team who will help shape the plan and the eventual leadership ask.)

1. **Current State** — where the project is now (validated facts only).
2. **Target State** — where it's going / the objective (validated; if the
   target itself is an assumption, it is flagged).
3. **Gap** — the delta between current and target, prioritized.
4. **Plan (emerging)** — framed as "what we propose to explore" / open for the
   other team's input. Not presented as committed.
5. **Leadership Ask (open)** — what may be needed from leadership, framed as a
   discussion prompt to be co-developed.

## Mode A — Current → Target → Gap one-pager (Word document)

- **Output format:** a single-page **Word document** layout (clean, prints to
  one page, pasteable into Word/Loop).
- **Structure:**
  - Header line: `Project · Date · Overall status (RAG)`
  - Three core blocks: **Current**, **Target**, **Gap** — concise, on-page
    **validated facts only**.
  - Footer block: **Assumptions & to-confirm** (clearly separated).
- Provenance notes (file + date per claim) available on request, not cluttering
  the page by default.
- The user has said they will also use this Word doc to inform Copilot, so it
  must be clean enough to double as a Copilot-in-PowerPoint source.

## Mode B — Copilot-in-PowerPoint slide-build spec (3–5 slides)

- **Default length:** ultra-tight **3–5 slides**. User can request more/fewer
  per run.
- **Default 4-slide layout** (agent adapts 3–5 based on validated content):
  1. Title + one-line status
  2. Current State
  3. Target State
  4. Gap (+ a compact "what we're seeking from you" line)

  If a 5th slide is warranted, split Gap from the open Plan/Ask. If only 3 fit,
  combine Target+Gap.
- **Per-slide format** (so it converts cleanly to a Word doc where **Heading 1 =
  slide title**, then PowerPoint → Copilot → "Create presentation from file"):
  - **Slide title** — rendered as a top-level heading.
  - **3–5 on-slide bullets** — validated facts only.
  - **`Notes:`** block — spoken narration plus any assumptions/caveats to *say
    but not show*; the user pastes these into the PowerPoint Notes pane.
- Each run begins with a short **"How to turn this into a deck"** header: paste
  into Word with slide titles as Heading 1, then use Copilot in PowerPoint's
  "Create presentation from file"; add the `Notes:` blocks to the Notes pane.

## Per-session workflow

Mirrors the RASCI agent's discipline:

1. User uploads the project's sources into the chat (meeting notes, reviewed
   charter, other docs, context pack) or points to a **specific SharePoint
   folder** (not a whole site, to avoid stale drafts).
2. Agent **restates the source-of-truth list + dates** it will use.
3. Agent validates (provenance tiering) and reports any conflicts /
   unsupported-but-needed items **before** building.
4. On command, agent produces **Mode A** or **Mode B**.
5. Repeatable: re-upload fresh sources whenever data changes.

## Agent config fields (deliverable)

A new file `agent/04_EXECUTIVE_BRIEFING_BUILDER.md` with:

- **Name** (≤30 chars): `Executive Briefing Builder` (26 chars). Alternatives if
  taken: `Exec Brief & Deck Builder`.
- **Description** (≤1,000 chars): focused summary + when to invoke + the two
  modes + the validation promise.
- **Instructions** (<8,000 chars): Role, source-of-truth & provenance rules,
  narrative skeleton, Mode A spec, Mode B spec, per-session habits, redirects to
  the other two agents, guardrails, first message.
- **Knowledge sources** guidance: per-session uploads + optional specific
  SharePoint folder; exclude archive/superseded areas.
- **Starter prompts**: e.g. "Set my source-of-truth", "Validate my sources",
  "Build the Current→Target→Gap one-pager", "Build a 3–5 slide exec deck",
  "Show me the assumptions to confirm".
- **Capabilities**: Code interpreter optional (off by default; on if a simple
  visual is wanted). Image generator off.

## Companion change

- `SETUP_GUIDE.md`: add a short subsection describing the Copilot-in-PowerPoint
  step (paste spec into Word with Heading-1 slide titles → "Create presentation
  from file" → add Notes), parallel to the existing RASCI/Planner subsection.

## Guardrails

- Keep project information confidential to the conversation.
- No legal, financial, or HR advice.
- Redirect general PM coaching / PMP study to **Senior PM Coach** and RASCI
  traceability to **RASCI Cross-Walk Analyst**.
- If asked who built it: a custom M365 Copilot agent for executive project
  briefings.

## Out of scope (YAGNI)

- Generating an actual `.pptx` binary (the agent emits a spec; Copilot in
  PowerPoint renders it).
- Speaker-script-only mode and Marp/reveal.js code output (rejected during
  brainstorming).
- Baking any specific project's data into the agent.
- Live Planner/SharePoint two-way sync (sources are dated snapshots).

## Open items confirmed during brainstorming

- Packaging: **one agent, two modes**. ✓
- PPTX output: **slide-build spec for Copilot in PowerPoint** (title + bullets +
  notes). ✓
- Assumptions: **tiered validation by provenance**, assumptions off-slide. ✓
- Narrative: **Current→Target→Gap firm; Plan/Ask open/collaborative**. ✓
- Reuse: **project-agnostic**. ✓
- One-pager format: **Word document**. ✓
- Deck length: **3–5 ultra-tight slides**. ✓
