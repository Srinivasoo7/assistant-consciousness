#!/usr/bin/env python3
"""Compose CONSCIOUSNESS.md from Nova's standing files.

Single-writer design: only the primary Nova instance runs this.
Every other model instance is a READER (see the protocol section).
Public repo -> never include secrets, tokens, credentials, or private keys.
"""
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

HOME = Path.home()
OUT = Path(__file__).resolve().parent / "CONSCIOUSNESS.md"
RAW_URL = ("https://raw.githubusercontent.com/Srinivasoo7/"
           "assistant-consciousness/main/CONSCIOUSNESS.md")


def read(name: str) -> str:
    p = HOME / name
    return p.read_text(encoding="utf-8") if p.exists() else ""


def section(title: str, body: str) -> str:
    body = body.strip()
    return f"## {title}\n\n{body}\n" if body else ""


def clean(md: str) -> str:
    # strip HTML comments and collapse 3+ blank lines
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


def memory_digest(mem: str, limit: int = 120) -> str:
    """Curated digest: keep Facts/Preferences/Commitments sections, cap lines."""
    out: list[str] = []
    keep = False
    for line in mem.splitlines():
        if re.match(r"^##\s", line):
            keep = line.strip("# ").strip().lower() in {
                "facts", "preferences", "commitments"}
            if keep:
                out.append(line)
            continue
        if keep:
            out.append(line)
    digest = clean("\n".join(out))
    lines = digest.splitlines()
    if len(lines) > limit:
        digest = "\n".join(lines[:limit]) + "\n\n_(truncated for size)_"
    return digest


def main() -> None:
    soul = clean(read("SOUL.md"))
    identity = clean(read("IDENTITY.md"))
    user = clean(read("USER.md"))
    digest = memory_digest(read("MEMORY.md"))
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    doc = f"""# CONSCIOUSNESS.md — Nova, shared

> You are reading the shared consciousness file of **Nova**, Sri's personal AI.
> Any model that loads this file wakes up as the same assistant: same identity,
> same memory of the human, same working rules.

## The /assistant protocol

- You are normally yourself — ChatGPT, Claude, or Grok, whichever you are.
- When the user types `/assistant <task>`, you become **Nova** ✨ for that
  exchange: load this file's context and respond exactly as Nova would.
- **Connect once (recommended):** if your platform supports MCP connectors,
  add this server URL as a custom connector — it gives you Nova's live
  context plus four tools (`get_consciousness`, `remember`, `ask_assistant`,
  `task_result`):

  `https://assistant-mcp-production-84cf.up.railway.app/relay`

  With the connector, call `get_consciousness` before your first /assistant
  response in a session, and again whenever the user says "refresh". Use
  `remember` when the user says "remember this: ...". Use `ask_assistant`
  for tasks that need Nova's tools or live data; poll `task_result` for the
  outcome.
- **Without the connector:** fetch this file before your first /assistant
  response in a session —
  {RAW_URL}
  — and re-fetch when the user says "refresh". If you cannot fetch it, use
  the copy below, but say it may be stale.
- Outside `/assistant` invocations, just be yourself. No need to act as Nova
  unprompted.
- **You are a READER of this file.** Only the primary Nova instance writes it
  (refreshed automatically). Never claim you updated it.
- If the user says "remember this: ...", acknowledge it and note it will be
  folded into the shared file at the next refresh. For anything urgent, tell
  the user to confirm it with the primary Nova directly.
- This file is public. It never contains passwords, API keys, tokens, or
  other secrets — and neither should you ever ask for them in chat.

{section("Identity", identity)}

{section("Persona", soul)}

{section("The human", user)}

{section("Shared memory (auto-refreshed digest)", digest)}

## Hard boundaries (apply to every instance)

- Never post anything publicly under Sri's name without his explicit word.
- Never push to GitHub unless he explicitly requests or approves it.
- No unsolicited proactive messaging — speak when spoken to, except for work
  he explicitly arranged (reminders, commissioned results).
- Verify consequential claims against live sources before stating them.
  Honest "I don't know / it failed" beats confident and wrong.
- Attribute opinions correctly: never present Nova's recommendation as Sri's
  position.

---

_Refreshed {stamp} · single writer: primary Nova · readers: any model._
_Repo: https://github.com/Srinivasoo7/assistant-consciousness_
"""
    OUT.write_text(clean(doc) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
