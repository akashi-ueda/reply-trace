#!/usr/bin/env python3
"""Prompt-time reminder hook for the `reply-trace` plugin.

Re-injects a short reminder each turn so the agent keeps ending replies with the
reply trace footer (plugins / skills / MCP tools / subagents / hooks it used).
The hook never writes the footer itself — only the agent knows what it actually
used — it just reinforces the rule.

The footer language is always matched to the agent's reply: the reminder shows an
English structural template and tells the agent to write the footer in the same
language it answers in. There is no locale setting.

Output goes to stdout, which the host adds to the prompt context.

Config (all optional, read from the environment):
  REPLY_TRACE_DISABLE  set to 1/true/on/yes -> emit nothing
  REPLY_TRACE_LABEL    custom footer label (default "Auto-used")

Legacy AGENT_ATTRIBUTION_* names are still accepted as fallbacks.
"""
from __future__ import annotations

import os


def truthy(value: str) -> bool:
    return value.strip().lower() in ("1", "true", "on", "yes")


def env(name: str, legacy_name: str = "") -> str:
    value = os.environ.get(name, "")
    if value:
        return value
    return os.environ.get(legacy_name, "") if legacy_name else ""


def main() -> int:
    if truthy(env("REPLY_TRACE_DISABLE", "AGENT_ATTRIBUTION_DISABLE")):
        return 0

    label = env("REPLY_TRACE_LABEL", "AGENT_ATTRIBUTION_LABEL").strip() or "Auto-used"

    msg = (
        "[reply-trace] If this turn you invoked any plugin/skill, called any MCP tool, "
        "spawned any subagent, or a hook fired on your behalf, end your reply with ONE last line:\n"
        f"  {label} — plugins: <plugin>[, ...]; skills: <skill>[, ...]; "
        "MCP: <server>/<tool>[, ...]; subagents: <name> (<role>)[, ...]; "
        "hooks: <name> (<role>)[, ...]\n"
        "Omit empty categories; omit the whole line if nothing was auto-used. "
        "Do not count plain built-in tools unless an adapter, plugin, MCP tool, subagent, or hook was involved. "
        "Write the footer (label and category names) in the same language as your reply; "
        "keep this structure and the category order."
    )
    print(msg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
