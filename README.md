# agent-attribution

A small agent plugin that ends each reply with a **one-line disclosure** of the
skills, MCP tools, and hooks the agent auto-used that turn — for transparency.

```
Auto-used — skills: caveman:caveman; MCP: anthropicDocs/search_docs; hooks: pre_tool_use (checks command policy)
```

The line is omitted entirely when nothing was auto-used, and empty categories are
dropped. The label and language are configurable.

## What's inside

One plugin (`attribution`) with exactly **one skill** and **one hook**:

- **Skill** (`skills/attribution`) — defines the rule, the footer format, the
  categories (skills / MCP / hooks), and locale/label configuration with examples.
- **Hook** (`hooks/`, `UserPromptSubmit`) — re-injects a short reminder every turn
  so the rule does not drift over a long session. It only reminds; the agent writes
  the actual line, because only the agent knows what it really used.

This mirrors how persistent-style plugins (e.g. caveman) stay active: a skill
carries the spec, a per-turn hook keeps it from being forgotten.

## Install (Claude Code)

```bash
claude plugin marketplace add akashi-ueda/agent-attribution
claude plugin install attribution@agent-attribution
```

Restart Claude Code so the hook loads.

## Configuration

All optional, via environment variables:

| Variable | Effect |
|----------|--------|
| `AGENT_ATTRIBUTION_LABEL` | Replace the `Auto-used` label (e.g. `사용한 자동 트리거`). |
| `AGENT_ATTRIBUTION_LOCALE` | `en` (default) or another locale. Built-in: `ko`. Non-`en` writes category names/roles in that language, same structure. |
| `AGENT_ATTRIBUTION_DISABLE` | Set `1`/`true` to suppress the footer in that environment. |

Korean example:

```
사용한 자동 트리거 — 스킬: caveman:caveman; MCP: anthropicDocs/search_docs; 훅: pre_tool_use (명령 정책 확인)
```

## Why "agent", not "claude"

The format and rule are host-agnostic. The shipped hook targets Claude Code's
`UserPromptSubmit` event, but the skill spec applies to any agent that can load a
skill and run a prompt-time hook. Ports for other agents (Codex, etc.) can add a
sibling hook without changing the skill.

## How it works

1. On every prompt, the `UserPromptSubmit` hook runs `hooks/reminder.py`, which
   prints a short reminder (respecting your config) into the prompt context.
2. The agent, guided by the skill, ends its reply with the footer line listing
   what it auto-used this turn.
3. If nothing was auto-used, no line is printed.

The hook resolves its own path via `${CLAUDE_PLUGIN_ROOT}` and needs `python3` on
PATH (no third-party dependencies).

## Repository layout

```
.claude-plugin/marketplace.json     # marketplace manifest (lists the plugin)
plugins/attribution/
  .claude-plugin/plugin.json         # plugin manifest
  skills/attribution/SKILL.md        # the rule + format + config + examples
  hooks/hooks.json                   # UserPromptSubmit -> reminder.py
  hooks/reminder.py                  # prints the per-turn reminder
LICENSE                              # MIT
```

## License

MIT — see [LICENSE](LICENSE).
