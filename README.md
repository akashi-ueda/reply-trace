# reply-trace

> Make AI agent behavior visible: disclose the plugins, skills, MCP tools,
> subagents, and hooks used for each reply.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Hosts](https://img.shields.io/badge/hosts-Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20Cursor%20%C2%B7%20Antigravity-blue)](#install)
[![Agent agnostic](https://img.shields.io/badge/design-agent--agnostic-purple)](#agent-agnostic-core)
[![Language](https://img.shields.io/badge/language-en%20%7C%20ko%20%7C%20ja-orange)](#language)

Languages: **English** · [한국어](docs/README.ko.md) · [日本語](docs/README.ja.md)

`reply-trace` adds a final one-line transparency footer when an agent
uses automation behind the scenes:

```text
Auto-used — plugins: Browser; skills: browser:control-in-app-browser; MCP: anthropicDocs/search_docs; subagents: reviewer (checks diff); hooks: pre_tool_use (checks command policy)
```

Empty categories are dropped. If nothing was used, the footer is omitted.

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
| Locale support | English default, with Korean and Japanese footer labels/categories. |
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
cp hosts/cursor/rules/reply-trace.mdc .cursor/rules/reply-trace.mdc
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
| `REPLY_TRACE_LABEL` | locale default | Replaces the footer label. |
| `REPLY_TRACE_LOCALE` | `auto` | `auto` matches the footer to your reply's language; set `en`/`ko`/`ja`/other to pin one. |
| `REPLY_TRACE_DISABLE` | unset | Set `1`, `true`, `on`, or `yes` to suppress the footer. |

Legacy `AGENT_ATTRIBUTION_*` variables are still accepted as fallbacks.

## Language

By default (`REPLY_TRACE_LOCALE=auto`) the footer language follows the reply — a
Korean reply gets a Korean footer, a Japanese reply a Japanese one, with no
configuration. Set an explicit `REPLY_TRACE_LOCALE` to pin one language with
canonical category words. Localized footer examples live in the
[Korean](docs/README.ko.md) and [Japanese](docs/README.ja.md) docs.

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

Bundled host adapters: Claude Code & Codex (plugin package), Cursor & Antigravity
(always-on rule under [`hosts/`](hosts/)).

## Repository Layout

```text
.claude-plugin/marketplace.json
docs/
  README.ko.md
  README.ja.md
hosts/
  codex/
    README.md
  cursor/
    README.md
    rules/
      reply-trace.mdc
  antigravity/
    README.md
    rules/
      reply-trace.md
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
