# reply-trace

> Make AI agent behavior visible: disclose the plugins, skills, MCP tools,
> subagents, and hooks used for each reply.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Plugin](https://img.shields.io/badge/plugin-Claude%20Code%20%2B%20Codex-blue)](#install)
[![Agent agnostic](https://img.shields.io/badge/design-agent--agnostic-purple)](#agent-agnostic-core)
[![Locales](https://img.shields.io/badge/locales-en%20%7C%20ko%20%7C%20ja-orange)](#locales)

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
| Agent-agnostic core | Same rule works across Claude Code, Codex, and other agent hosts. |
| Host adapters | Claude Code plugin included; Codex personal plugin package and hook adapter included. |
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

Codex support has two parts:

1. A personal plugin package with `.codex-plugin/plugin.json` and the shared
   `reply-trace` skill.
2. A `UserPromptSubmit` hook adapter that re-injects the reminder each turn.

See [hosts/codex/README.md](hosts/codex/README.md).

Short version:

```bash
mkdir -p ~/.codex/plugins ~/.agents/plugins ~/.codex/hooks
rm -rf ~/.codex/plugins/reply-trace
mkdir -p ~/.codex/plugins/reply-trace
cp -R hosts/codex/.codex-plugin ~/.codex/plugins/reply-trace/
cp -R plugins/reply-trace/skills ~/.codex/plugins/reply-trace/
test -f ~/.agents/plugins/marketplace.json || \
  cp hosts/codex/personal-marketplace.example.json ~/.agents/plugins/marketplace.json
cp plugins/reply-trace/hooks/reminder.py ~/.codex/hooks/reply_trace.py
```

If `~/.agents/plugins/marketplace.json` already exists, merge only the
`reply-trace` entry from
[hosts/codex/personal-marketplace.example.json](hosts/codex/personal-marketplace.example.json).
Then merge [hosts/codex/hooks.fragment.json](hosts/codex/hooks.fragment.json)
into `~/.codex/hooks.json`, restart Codex, install `reply-trace` from the
personal marketplace, and approve the hook trust prompt if Codex asks.

Do not copy `plugins/reply-trace/hooks/hooks.json` into the Codex plugin
package. That file is the Claude Code hook adapter. Codex uses
`hosts/codex/hooks.fragment.json` instead.

Official Codex behavior this package relies on:

- Codex plugins use `.codex-plugin/plugin.json`.
- Personal marketplaces live at `~/.agents/plugins/marketplace.json`.
- Personal plugin folders are commonly stored under `~/.codex/plugins/`.
- Codex discovers plugin-bundled hooks, but this project still ships a host
  hook adapter because the reminder must run at `UserPromptSubmit` in the
  active Codex hook layer.

## Configuration

All options use environment variables.

| Variable | Default | Effect |
|----------|---------|--------|
| `REPLY_TRACE_LABEL` | locale default | Replaces the footer label. |
| `REPLY_TRACE_LOCALE` | `en` | Selects category names. Built in: `en`, `ko`, `ja`. |
| `REPLY_TRACE_DISABLE` | unset | Set `1`, `true`, `on`, or `yes` to suppress the footer. |

Legacy `AGENT_ATTRIBUTION_*` variables are still accepted as fallbacks.

## Locales

### English

```text
Auto-used — plugins: Browser; skills: browser:control-in-app-browser; MCP: anthropicDocs/search_docs; subagents: reviewer (checks diff); hooks: pre_tool_use (checks command policy)
```

### Korean

```bash
export REPLY_TRACE_LOCALE=ko
```

```text
사용한 자동 트리거 — 플러그인: Browser; 스킬: browser:control-in-app-browser; MCP: anthropicDocs/search_docs; 서브에이전트: reviewer (diff 검토); 훅: pre_tool_use (명령 정책 확인)
```

### Japanese

```bash
export REPLY_TRACE_LOCALE=ja
```

```text
使用した自動トリガー — プラグイン: Browser; スキル: browser:control-in-app-browser; MCP: anthropicDocs/search_docs; サブエージェント: reviewer (diff確認); フック: pre_tool_use (コマンドポリシー確認)
```

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

1. Load `SKILL.md` through that host's durable instruction, skill, or extension
   mechanism.
2. Run `reminder.py`, or equivalent middleware, before each user prompt.
3. Map host concepts into these categories:
   `plugins`, `skills`, `MCP`, `subagents`, `hooks`.
4. Keep the final disclosure as one line at the end of the reply.

## Repository Layout

```text
.claude-plugin/marketplace.json
docs/
  README.ko.md
  README.ja.md
hosts/
  codex/
    .codex-plugin/plugin.json
    README.md
    hooks.fragment.json
    personal-marketplace.example.json
plugins/
  reply-trace/
    .claude-plugin/plugin.json
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
