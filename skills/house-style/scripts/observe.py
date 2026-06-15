#!/usr/bin/env python3
"""observe.py — read redacted docs in references/inbox/, emit candidate style rules.
Usage: python observe.py            (lists inbox files + extraction checklist)
This is a helper scaffold: it prepares the material; the LLM (Copilot/Claude) does
the extraction using references/extraction-prompts.md, then improve.py records it."""
from pathlib import Path
INBOX = Path(__file__).resolve().parent.parent / "references" / "inbox"
docs = [p for p in INBOX.glob("*") if p.is_file() and p.name != ".gitkeep"]
if not docs:
    print("Inbox empty. Drop redacted senior-PM docs into references/inbox/ first.")
else:
    print(f"{len(docs)} doc(s) to observe:")
    for d in docs: print("  -", d.name)
    print("\nNext: run each through the prompts in references/extraction-prompts.md,")
    print("then record accepted rules with improve.py.")
