<div align="center">

# reply-trace

### See what your AI agent actually used — one transparency footer per reply.

Plugins, skills, MCP tools, subagents, and hooks an agent pulled in behind the
scenes, disclosed in a single line at the end of every answer.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Hosts](https://img.shields.io/badge/hosts-Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20Cursor%20%C2%B7%20Antigravity-blue)](#install)
[![No deps](https://img.shields.io/badge/deps-zero%20(stdlib)-brightgreen)](#agent-agnostic-core)

[**Install**](#install) · [Configuration](#configuration) · [How it works](#agent-agnostic-core)

[한국어](docs/README.ko.md) · [日本語](docs/README.ja.md) · [Español](docs/README.es.md) · [中文](docs/README.zh.md)

<!--
  DEMO GIF placeholder. Record a ~5s clip of an agent reply gaining the footer,
  save it to docs/assets/demo.gif (see docs/assets/README.md), then uncomment the
  <img> below. Kept commented so the hero never shows a broken image.
  <img src="docs/assets/demo.gif" alt="reply-trace footer appended to an agent reply" width="720">
-->

</div>

`reply-trace` adds a final one-line transparency footer when an agent uses
automation behind the scenes:

```text
Auto-used — plugins: Browser; skills: browser:control-in-app-browser; MCP: anthropicDocs/search_docs; subagents: reviewer (checks diff); hooks: pre_tool_use (checks command policy)
```

Empty categories are dropped. If nothing was used, the footer is omitted.

## Quick start

```bash
# Claude Code
claude plugin marketplace add akashi-ueda/reply-trace
claude plugin install reply-trace@reply-trace
```

One package covers Claude Code and Codex; an always-on rule covers Cursor and
Antigravity. See [Install](#install) for all four hosts.

## Why

Modern coding agents can silently pull in plugins, skills, MCP servers,
subagents, and hooks. That is powerful, but it can make an answer hard to audit.

This plugin keeps the disclosure small, consistent, and always at the end of the
reply.

## Highlights

| Feature | What it does |
|---------|--------------|
| One-line footer | Adds a compact attribution line only when needed. |
| Agent-agnostic core | Same rule works across Claude Code, Codex, Cursor, Antigravity, and other hosts. |
| Plugin or rule | Plugin package on Claude Code / Codex; always-on rule on Cursor / Antigravity. |
| Auto language | The footer is written in the same language as each reply — no locale setting. |
| No dependencies | Hook is a small Python script using only the standard library. |

## Install

### Claude Code

```bash
claude plugin marketplace add akashi-ueda/reply-trace
claude plugin install reply-trace@reply-trace
```

Restart Claude Code so the hook loads.

### Codex

Same two-command flow as Claude Code:

```bash
codex plugin marketplace add akashi-ueda/reply-trace
codex plugin install reply-trace@reply-trace
```

Restart Codex, run `/hooks`, and trust the `reply-trace` hook once (plugin
hooks are non-managed, so Codex asks before running them).

The same plugin package serves both hosts: Codex reads the legacy-compatible
`.claude-plugin/marketplace.json`, installs from `.codex-plugin/plugin.json`,
and auto-discovers the bundled `hooks/hooks.json`. The hook command uses
`${CLAUDE_PLUGIN_ROOT}`, which Codex sets for plugin-hook compatibility — so no
manual hook wiring is needed. For local development install, see
[hosts/codex/README.md](hosts/codex/README.md).

### Cursor

Cursor has no plugin package, but its **Rules** are always-on instructions
re-sent every turn — equivalent to the plugin's durable-instruction half. Ship
`reply-trace` as an always-apply rule:

```bash
mkdir -p .cursor/rules
cp rules/reply-trace.mdc .cursor/rules/reply-trace.mdc
```

The rule sets `alwaysApply: true`, so Cursor includes it in every turn with no
further setup. Cursor's per-turn `beforeSubmitPrompt` hook can't inject context,
so the always-on rule (not a hook) carries the reminder here. Details and a
global/user-rule option: [hosts/cursor/README.md](hosts/cursor/README.md).

### Google Antigravity

Antigravity also uses always-on **Rules** and has no prompt-time hook, so the
rule is the whole adapter:

```bash
mkdir -p .agents/rules
cp hosts/antigravity/rules/reply-trace.md .agents/rules/reply-trace.md
```

Then open **Customizations → Rules** and set the `reply-trace` rule to **Always
On**. For a global rule, append it to `~/.gemini/GEMINI.md`. Details:
[hosts/antigravity/README.md](hosts/antigravity/README.md).

## Configuration

All options use environment variables.

| Variable | Default | Effect |
|----------|---------|--------|
| `REPLY_TRACE_LABEL` | `Auto-used` | Replaces the footer label. |
| `REPLY_TRACE_DISABLE` | unset | Set `1`, `true`, `on`, or `yes` to suppress the footer. |

Legacy `AGENT_ATTRIBUTION_*` variables are still accepted as fallbacks.

## Language

The footer language always follows your reply — a Korean reply gets a Korean
footer, a Japanese reply a Japanese one, and so on, with no configuration. There
is no locale setting; the language matches the conversation. The README itself is
translated into [Korean](docs/README.ko.md), [Japanese](docs/README.ja.md),
[Spanish](docs/README.es.md), and [Chinese](docs/README.zh.md).

## Agent-Agnostic Core

The plugin has two pieces:

| Piece | Role |
|-------|------|
| `skills/reply-trace/SKILL.md` | Defines when to emit the footer and how to format it. |
| `hooks/reminder.py` | Re-injects a short prompt-time reminder so the rule does not drift. |

The hook does not write the footer. The agent writes it, because only the agent
knows exactly which plugins, tools, subagents, and hooks were used in that turn.

This is a transparency convention, not a tamper-proof audit log. It relies on
the host agent following the loaded instruction and prompt-time reminder.

Porting to another agent host:

1. Load `SKILL.md` (or an equivalent rule) through that host's durable
   instruction, skill, rule, or extension mechanism.
2. If the host supports prompt-time hooks, run `reminder.py` or equivalent
   middleware before each user prompt. If it doesn't (e.g. Cursor, Antigravity),
   an always-on rule already re-applies every turn, so the rule alone suffices.
3. Map host concepts into these categories:
   `plugins`, `skills`, `MCP`, `subagents`, `hooks`.
4. Keep the final disclosure as one line at the end of the reply.

Bundled host adapters: Claude Code & Codex (plugin package under
[`plugins/`](plugins/)), Cursor ([`rules/reply-trace.mdc`](rules/reply-trace.mdc)),
and Antigravity ([`hosts/antigravity/`](hosts/antigravity/)).

## Repository Layout

```text
.claude-plugin/marketplace.json
_config.yml                      # GitHub Pages: renders README as the site
rules/
  reply-trace.mdc                # Cursor rule (root = cursor.directory auto-detect)
docs/
  README.ko.md
  README.ja.md
  README.es.md
  README.zh.md
  assets/                        # demo.gif + recording notes
hosts/
  codex/README.md
  cursor/README.md
  antigravity/
    README.md
    rules/reply-trace.md
plugins/
  reply-trace/
    .claude-plugin/plugin.json
    .codex-plugin/plugin.json
    hooks/
      hooks.json
      reminder.py
    skills/
      reply-trace/
        SKILL.md
LICENSE
```

## License

MIT — see [LICENSE](LICENSE).

## Other Languages

- [한국어 (Korean)](docs/README.ko.md)
- [日本語 (Japanese)](docs/README.ja.md)
- [Español (Spanish)](docs/README.es.md)
- [中文 (Chinese)](docs/README.zh.md)
