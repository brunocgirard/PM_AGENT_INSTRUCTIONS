# Insight Builder — design spec

**Owner:** Bruno (PM) · **Platform:** Microsoft Copilot Studio
**License basis:** M365 Copilot business (Copilot Studio included; Code Interpreter via Copilot credits) — **no Microsoft Fabric.**
**Goal:** Take shared documents or a SharePoint library → interview the user → discover, clean, and analyze → write the pertinent Excel/Word → define what to track → emit a paste-ready Power BI build package.

---

## 1. Why this design (the licensing reality)

- A **Copilot Studio agent cannot natively read a Power BI report or semantic model.** The supported "talk to Power BI data" path is the **Fabric Data Agent**, which needs **F2+ Fabric capacity / Power BI Premium P1+** — not available here.
- The user's data is **Excel/CSV + Dataverse/SharePoint**, which never needed the Data Agent. So the design routes around Fabric entirely.
- The **M365 Copilot license** includes full Copilot Studio access; **SharePoint/Graph grounding is zero-rated**, and **Code Interpreter is unlocked** (premium — ~100 credits / 10 responses).
- Net: everything from raw docs → a complete Power BI **build package** is in reach. Only the final dashboard **rendering** stays in Power BI.

## 2. Architecture

```
You share: a doc OR a SharePoint library of docs
        │
   ┌────▼───────────────────────────────────────┐
   │  Copilot Studio Agent — "Insight Builder"    │
   │                                              │
   │  Knowledge (zero-rated):                     │
   │   • SharePoint document library              │
   │   • Business glossary (what metrics mean)    │
   │   • house-style (optional)                   │
   │                                              │
   │  Skills / topics:                            │
   │   0. Intake & interview                      │
   │   1. Discover related info                   │
   │   2. Clean & profile        (Code Interp.)   │
   │   3. Gaps + similarity      (Code Interp.)   │
   │   4. Produce artifact (Excel/Word)           │
   │   5. Define what to track (KPI spec)         │
   │   6. Power BI build package                  │
   │                                              │
   │  Actions:                                    │
   │   • Create/Update file in SharePoint (Flow)  │
   │   • Document output (Word)                    │
   └──────────────────────────────────────────────┘
                     │
        Paste package into Power BI (Copilot in Power BI)
```

## 3. Skills — see the runnable definitions

The seven topics are defined in two committed places:
- **Portable skill:** `skills/insight-builder/SKILL.md` (agentskills.io format, validator-clean).
- **Copilot Studio config:** `agent/06_INSIGHT_BUILDER.md` (name, description, paste-in instructions, knowledge/tool wiring, capability-check table).

## 4. Build order

1. Create the agent; paste the system instructions from `agent/06_INSIGHT_BUILDER.md`.
2. Add the SharePoint library + business glossary as Knowledge. Fill descriptions + synonyms. **Test grounding first.**
3. Settings → File processing → File uploads = On; Code interpreter = On.
4. Wire the Power Automate "Create/Update file in SharePoint" action and enable Document output.
5. Build/verify topics 0→6 against one real dataset each.
6. Publish to Teams; pilot with 2–3 real datasets; refine the glossary from wrong answers.

## 5. Honest boundary

The agent produces a complete, paste-ready Power BI build package (model prep + DAX + layout + per-page Copilot prompts). It does **not** render the dashboard — that happens in Power BI with Copilot in Power BI (if the tenant has it). No Copilot Studio agent renders a Power BI report directly.

## 6. Future add-ons (need more licensing)

- **Live KPI values in chat** — Power Automate action wrapping Power BI REST `ExecuteQueries` / XMLA; needs Power BI capacity.
- **Governed NL Q&A over published models** — Fabric Data Agent consumed as a tool; needs Fabric F2+ / Premium.

## 7. Sources

- Copilot Studio licensing — https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing
- M365 Copilot includes Copilot Studio — https://microsoft.github.io/mcscatblog/posts/no-copilot-license-m365-channel/
- Code interpreter (structured data) — https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-code-interpreter-structured-data
- Document output (preview) — https://learn.microsoft.com/en-us/microsoft-copilot-studio/generate-document-output-prompt
- Knowledge sources summary — https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio
- Optimize semantic model for Copilot — https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-evaluate-data
- Fabric data agent (why excluded) — https://learn.microsoft.com/en-us/fabric/data-science/concept-data-agent
