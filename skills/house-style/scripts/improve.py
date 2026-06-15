#!/usr/bin/env python3
"""improve.py — append a ratified ingest entry to references/ingest-log.md.
Usage: python improve.py "2026-06-14" "status-report-A (redacted)" "added: lead with RAG verdict; reinforced: <=1 page" """
import sys
from pathlib import Path
LOG = Path(__file__).resolve().parent.parent / "references" / "ingest-log.md"
if len(sys.argv) < 4:
    print("Usage: improve.py <date> <file> <changes>"); sys.exit(1)
date, fname, changes = sys.argv[1], sys.argv[2], sys.argv[3]
entry = f"\n- **{date}** — {fname}: {changes}\n"
with LOG.open("a", encoding="utf-8") as f:
    f.write(entry)
print("Appended to ingest-log.md:", entry.strip())
