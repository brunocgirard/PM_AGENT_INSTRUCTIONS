# Setup Guide — Building "Senior PM Coach" in Microsoft 365 Copilot

This guide takes you from the files in this folder to a working agent inside
M365 Copilot. Total time: about 20–30 minutes.

---

## What you have

```
Agent_PMI/
├── agent/
│   ├── 01_AGENT_INSTRUCTIONS.md   → the agent's system prompt
│   └── 02_AGENT_PROFILE.md        → name, description, starter prompts
├── knowledge/
│   ├── K1_PMBOK7_Reference.md         → upload as knowledge
│   ├── K2_Artifacts_Playbook.md       → upload as knowledge
│   ├── K3_PMP_Exam_Study_Guide.md     → upload as knowledge
│   ├── K4_Coaching_and_Blind_Spots.md → upload as knowledge
│   ├── K5_Calculations.md             → upload as knowledge
│   ├── K6_Agile_Mechanics.md          → upload as knowledge
│   └── K7_PM_Theory.md                → upload as knowledge
└── SETUP_GUIDE.md                     → this file
```

The seven `K` files become the agent's **knowledge**. The two `agent` files
hold text you **paste into fields** — they are not uploaded.

> These knowledge files are original reference material written for you. Do
> NOT upload the PMBOK book itself — it is copyrighted, and anything uploaded
> as knowledge becomes visible to everyone you share the agent with.

---

> Already done for you: the `.docx` versions of all seven `K` files are already
> in the `knowledge/` folder. You can skip Step 1 and go straight to Step 2.

## Step 1 — Convert the knowledge files to .docx (already done)

M365 Copilot **does not accept `.md` files** as knowledge. It accepts `.docx`
(best), `.pdf`, or `.txt`. Use `.docx` — it keeps the headings and tables,
which makes the agent's search work better.

**Easiest conversion (using Word):**
1. Open Microsoft Word.
2. File → Open → pick `K1_PMBOK7_Reference.md` (set the file-type filter to
   "All Files" so `.md` shows). Word imports the text.
3. File → Save As → choose **Word Document (.docx)** → save as
   `K1_PMBOK7_Reference.docx`.
4. Repeat for `K2` through `K7`.

If the Markdown symbols (`#`, `|`, `-`) look messy after import, that is fine —
the agent still reads the text. If you want them clean, paste the content into
a blank Word document and apply Heading styles, but this is optional.

**Alternative:** if these files are already on a machine with `pandoc`
installed, run for each file:
`pandoc K1_PMBOK7_Reference.md -o K1_PMBOK7_Reference.docx`

You should end with seven `.docx` files: `K1_PMBOK7_Reference`,
`K2_Artifacts_Playbook`, `K3_PMP_Exam_Study_Guide`,
`K4_Coaching_and_Blind_Spots`, `K5_Calculations`, `K6_Agile_Mechanics`,
`K7_PM_Theory`.

---

## Step 2 — Move the files to your work computer

Copy to your work machine (USB drive, or email them to your work address —
they contain no confidential project data, only PM reference material):
- The 7 `.docx` knowledge files.
- `01_AGENT_INSTRUCTIONS.md` and `02_AGENT_PROFILE.md` (just to read the text
  from — you will copy-paste out of them).

---

## Step 3 — Open the Agent Builder

On your work computer:
1. Open **Microsoft 365 Copilot** (in Teams, the Microsoft 365 app, or
   m365.cloud.microsoft — wherever you normally use Copilot).
2. In the left-hand pane, click **New agent** (sometimes shown as
   "Create agent" or a "+" near Agents).
3. When asked how to start, choose **Skip to configure** (manual control).

If you do not see "New agent", your tenant admin may have disabled agent
creation — ask your IT/Copilot admin to enable it.

---

## Step 4 — Fill in the configuration fields

Open `agent/02_AGENT_PROFILE.md` and `agent/01_AGENT_INSTRUCTIONS.md` and copy
the values into these fields:

| Field | What to enter |
|---|---|
| **Name** | `Senior PM Coach` (from 02_AGENT_PROFILE.md) |
| **Description** | The description block from 02_AGENT_PROFILE.md |
| **Instructions** | Everything below the line in 01_AGENT_INSTRUCTIONS.md |
| **Starter prompts** | The 6 prompts from the table in 02_AGENT_PROFILE.md |

For Instructions: copy only the text **below** the `---` divider in
`01_AGENT_INSTRUCTIONS.md` (starts with `# Role`). It is within the 8,000
character limit.

---

## Step 5 — Add the knowledge files

1. In the **Knowledge** section of the builder, choose to upload files.
2. Upload all seven `.docx` files: `K1` through `K7`.
3. Wait until each shows as ready (uploaded files take a few minutes to index —
   a "Preparing" label clears when done).

Optional: if you keep your real project documents in a SharePoint site, you can
also add that site as a knowledge source so the agent can reference your actual
project files. Add the SharePoint URL in the Knowledge section. Only do this if
you are comfortable with anyone you share the agent with seeing those files.

---

## Step 6 — Test the agent

Use the **Try it** panel (available once Name, Description, and Instructions
are filled in). Test both modes:

- Project advisor: type *"What's next on my project?"* — it should ask which
  phase you are in, then recommend an artifact.
- Document review: paste a short fake charter — it should return Strengths,
  Gaps/Risks, Recommended fixes.
- Tutor: type *"Quiz me on risk management"* — it should ask one
  scenario-based question and wait.

If answers ignore the knowledge files, confirm the files finished indexing and
that the instructions were pasted in full.

---

## Step 7 — Create and share

1. Click **Create** (or Save). The agent is now private to you.
2. To share: use the **Share** button or the `...` menu next to the agent.
   Options: only you, specific people/teams, or anyone in your organization.
3. After any later edit, click **Update** so changes reach users. If you used
   SharePoint knowledge, re-share after updating so permissions propagate.

---

## Maintaining the agent

- To improve behavior: edit the **Instructions** text and click Update.
- To refresh reference content: edit a `K` file here, re-convert to `.docx`,
  and re-upload it in the Knowledge section (remove the old version first).
- If you later get **Copilot Studio**, you can import this agent and gain
  stricter knowledge-only grounding and multi-channel publishing — but the
  in-Copilot Agent Builder is enough for everything described here.

---

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

---

## Quick troubleshooting

| Symptom | Fix |
|---|---|
| `.md` file rejected as knowledge | Convert to `.docx` (Step 1) |
| Agent answers from general knowledge, ignores files | Wait for indexing to finish; if your builder shows an "only use specified sources" toggle, enable it; re-check the instructions were pasted in full |
| "New agent" button missing | Tenant admin must enable agent creation |
| Can't share org-wide | Admin disabled it; share with specific people instead |
| Instructions won't fit | They are ~7,900 chars — make sure you pasted only the part below the divider, not the note above it |
