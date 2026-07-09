---
name: pptx-exec
description: Use when the user wants to build an executive-ready PowerPoint presentation and needs a paste-ready prompt for Copilot in PowerPoint. Ingests project files (Excel registers, Word docs, screenshots, existing slides), asks targeted clarifying questions slide-by-slide, then outputs a polished, concise, decision-oriented Copilot prompt. Triggers: "prepare a deck", "executive presentation", "Copilot prompt for PowerPoint", "status presentation for my director/VP".
---

# Executive PowerPoint Copilot Prompt Builder

Turn raw project files into a single paste-ready prompt that Microsoft Copilot (inside PowerPoint) uses to generate an executive-grade deck. The user runs the final prompt in Copilot themselves; your job is to extract the real facts, sharpen the message, and engineer the prompt.

## Core principle

Executives read decks in seconds. Every slide must pass: **one message, led by the conclusion, with a clear and simple language.** Cut everything else. You are optimizing for *what the executive needs to decide*, not for completeness.

## Workflow (follow in order)

### 1. Ingest the source material
- Ask the user which files to use, or read everything they pointed to.
- Use the Read tool for images/screenshots (extract status %, RAG colors, owners, dates, risk text) and for Excel/Word/PDF.
- Build an internal fact sheet: project name, current status/metrics, owners per workstream, top risks (with impact + mitigation + RAG), key dates, and any decisions pending.
- Never invent numbers. If a fact is missing, mark it and ask.

### 2. Clarify (ask, don't assume)
Ask these as a short batched set (use AskUserQuestion where it fits). Skip any already answered:
- **Audience & seniority** — director, VP, C-suite, steering committee? (drives tone + concision)
- **Language** — always ask; never assume.
- **Meeting goal** — inform, get a decision, get budget/resources, gather recommendations?
- **Time limit / # slides** — 5 min → ~6 slides; 15 min → ~10.
- **The ask** — what single thing do you want the executive to do, decide, or commit to?
- **Featured risks** — which 2–3 risks to spotlight (the rest go in an appendix line).

### 3. Propose the slide map, confirm per slide
- Present a numbered slide map (title + the ONE message of each slide) as a compact table.
- For each slide, state the message in the executive's terms. Let the user confirm or adjust before generating.
- Default executive structure: (1) Objective/agenda, (2) Status & what's in place, (3) Coverage/ownership, (4) The tool/method showing control, (5) Top risks + asks, (6) Recommendations/decision needed. Adapt to the goal.

### 4. Generate the Copilot prompt
Output ONE fenced code block the user copies into Copilot. The prompt must:
- Open with global instructions: number of slides, language, audience, tone (factual, reassuring, decision-oriented), and visual style (clean, professional, ≤5 bullets/slide, one icon per section, minimal text).
- Give each slide explicitly: slide number, title, subtitle, and the exact bullets/table content — using the REAL facts extracted in step 1.
- Be written in the deck's target language (so Copilot generates in that language).
- End with a note (to the user, outside the code block) listing where to manually re-insert their own screenshots/charts, since Copilot won't import them.

### 5. Offer the speaker script
After the prompt, offer a short per-slide speaker script (what to say) so they can rehearse.

## Quality bar for the generated prompt
- One message per slide. If a slide has two ideas, split or cut.
- Numbers over adjectives ("Design 58%" not "good progress").
- A dedicated "ask"/decision slide near the end.
- No jargon walls; short noun-phrase bullets.
- RAG/status color-coded where risks appear.
- Reassuring frame for status decks: progress is real + a structure is in place + the team is ready.

## Notes & limits
- Copilot in PowerPoint generates best when the prompt is pasted as ONE block, then refined slide-by-slide with follow-ups (e.g. "make slide 5 more visual with RAG colors").
- Copilot cannot insert the user's real screenshots — always remind them to re-add those after generation.
