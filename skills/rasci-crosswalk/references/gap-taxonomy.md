# Traceability gap taxonomy (borrowed from shtracer)
Use these gap categories when cross-checking the RASCI against OCM sources:
- **Orphan activity** — RASCI activity with no matching OCM timeline/plan item.
- **Dangling item** — OCM timeline/plan item with no RASCI owner.
- **Coverage gap** — phase/workstream with < expected activity density.
- **Owner conflict** — same activity, different owners across sources.
- **Date conflict** — same activity, different dates; prefer the most recent source.
- **Sequence conflict** — dependency order disagrees between RASCI and timeline.
Report each finding with: id, category, the two sources + dates, and a coverage %
for the affected phase (coverage_pct = covered / expected × 100, per output-schema.json).
