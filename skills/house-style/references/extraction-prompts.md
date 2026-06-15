# Extraction prompts
Three copy-paste meta-prompts to run on uploaded (redacted) senior-PM documents.
Run each prompt in sequence; feed outputs to `improve.py` after ratification.

---

## 1 — Style-guide extraction

> Here are [N] documents written by one author. Reverse-engineer their writing style into reusable, TESTABLE rules covering tone, sentence structure, vocabulary choices, rhetorical moves, and formatting conventions. State each rule in the form "A reviewer can mark this PASS or FAIL by checking: [explicit criterion]." Support each rule with a short quoted example pulled from the text. Where the samples are inconsistent with each other, flag the inconsistency explicitly rather than averaging it away — note which doc shows which pattern so a human can decide which to enshrine.

Deliver output as a numbered list. For each rule include:
- **Rule** (the testable statement)
- **Example** (verbatim quote, doc reference in brackets)
- **Confidence** (HIGH = consistent across all samples; MEDIUM = majority; LOW = seen once or in tension with another sample)
- **Conflict note** (if any)

---

## 2 — Structural-template extraction

> Across these [N] documents of type [X — e.g. weekly status report / project charter / risk register], infer the common document skeleton. Deliver:
> 1. An ordered section list with the exact heading label used most often.
> 2. For each section: its purpose (one sentence), the data fields it contains, and — where the section includes a table — the column schema (column names in order, unit or format per column).
> 3. A "always present / optional / rare" classification for each section.
> 4. Any sequencing rules (e.g. "Summary always precedes Detail", "Risks section always follows Schedule").
>
> Note deviations across samples and flag sections where authors disagree on placement or naming.

Deliver as a structured outline. Use consistent indentation: Section > Purpose > Fields > Table schema > Presence flag > Deviations.

---

## 3 — Analysis-rubric extraction

> These documents are the OUTPUT of an expert PM's thinking. Your task is to reconstruct the analytical process that produced them — not what they say, but how the author reasoned before writing.
>
> Reconstruct:
> 1. What the author checked (the checklist of inputs/signals they verified).
> 2. The order in which they checked things (sequence matters — earlier checks gate later ones).
> 3. The criteria or thresholds they applied at each step (what made something cross a line — quantitative where possible, qualitative where not).
> 4. The decision rules (what pattern of findings led to what conclusion or escalation).
> 5. What they chose NOT to include — and why (revealed by what is consistently omitted despite being available).
>
> Output format:
> - Ordered checklist (Step N → what is checked → threshold → output if met / not met)
> - Decision thresholds table (Signal | Threshold | Interpretation | PM Action)
> - "What gets cut" note at the end

Flag any steps where the reasoning is inferred vs. explicitly evidenced in the text.
