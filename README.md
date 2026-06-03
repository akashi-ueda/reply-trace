# reply-trace

> Make AI agent behavior visible: disclose the plugins, skills, MCP tools,
> subagents, and hooks used for each reply.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Plugin](https://img.shields.io/badge/plugin-Claude%20Code%20%2B%20Codex-blue)](#install)
[![Agent agnostic](https://img.shields.io/badge/design-agent--agnostic-purple)](#agent-agnostic-core)
[![Locales](https://img.shields.io/badge/locales-en%20%7C%20ko%20%7C%20ja-orange)](#locales)

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
cp -R plugins/reply-trace/.codex-plugin ~/.codex/plugins/reply-trace/
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
hosts/
  codex/
    README.md
    hooks.fragment.json
    personal-marketplace.example.json
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

## 한국어

`reply-trace`는 에이전트가 플러그인, 스킬, MCP 도구, 서브에이전트,
훅을 사용했을 때 응답 마지막에 한 줄 disclosure를 추가합니다.

```text
사용한 자동 트리거 — 플러그인: Browser; 스킬: browser:control-in-app-browser; MCP: anthropicDocs/search_docs; 서브에이전트: reviewer (diff 검토); 훅: pre_tool_use (명령 정책 확인)
```

- 아무것도 사용하지 않으면 줄을 출력하지 않습니다.
- 빈 category는 생략합니다.
- Claude Code 플러그인으로 바로 설치할 수 있고, Codex는 `hosts/codex/`
  adapter와 personal plugin package를 사용합니다.
- 다른 AI 에이전트도 durable instruction + prompt-time reminder 방식으로
  붙일 수 있습니다.

### 설치

Claude Code:

```bash
claude plugin marketplace add akashi-ueda/reply-trace
claude plugin install reply-trace@reply-trace
```

Codex:

```bash
mkdir -p ~/.codex/plugins ~/.agents/plugins ~/.codex/hooks
rm -rf ~/.codex/plugins/reply-trace
mkdir -p ~/.codex/plugins/reply-trace
cp -R plugins/reply-trace/.codex-plugin ~/.codex/plugins/reply-trace/
cp -R plugins/reply-trace/skills ~/.codex/plugins/reply-trace/
test -f ~/.agents/plugins/marketplace.json || \
  cp hosts/codex/personal-marketplace.example.json ~/.agents/plugins/marketplace.json
cp plugins/reply-trace/hooks/reminder.py ~/.codex/hooks/reply_trace.py
```

기존 `~/.agents/plugins/marketplace.json`이 있으면 example 파일 전체를 덮지
말고 `reply-trace` entry만 병합합니다. 그 다음
`hosts/codex/hooks.fragment.json`의 `UserPromptSubmit` 항목을
`~/.codex/hooks.json`에 병합하고, Codex를 재시작한 뒤 personal marketplace에서
`reply-trace`를 설치합니다.

`plugins/reply-trace/hooks/hooks.json`은 Claude Code 전용 hook adapter이므로
Codex plugin package에는 복사하지 않습니다.

주의: 이 프로젝트는 자동 감사 로그가 아닙니다. 에이전트가 로드된 지침과
prompt-time reminder를 따르도록 돕는 transparency convention입니다.

## 日本語

`reply-trace` は、エージェントがプラグイン、スキル、MCP ツール、
サブエージェント、フックを使ったときに、返信の最後へ 1 行の disclosure を
追加します。

```text
使用した自動トリガー — プラグイン: Browser; スキル: browser:control-in-app-browser; MCP: anthropicDocs/search_docs; サブエージェント: reviewer (diff確認); フック: pre_tool_use (コマンドポリシー確認)
```

- 何も使っていない場合は出力しません。
- 空の category は省略します。
- Claude Code plugin として使えます。Codex は `hosts/codex/` adapter を
  使い、personal plugin package としても配布できます。
- 他の AI エージェントにも durable instruction + prompt-time reminder で
  移植できます。

### インストール

Claude Code:

```bash
claude plugin marketplace add akashi-ueda/reply-trace
claude plugin install reply-trace@reply-trace
```

Codex:

```bash
mkdir -p ~/.codex/plugins ~/.agents/plugins ~/.codex/hooks
rm -rf ~/.codex/plugins/reply-trace
mkdir -p ~/.codex/plugins/reply-trace
cp -R plugins/reply-trace/.codex-plugin ~/.codex/plugins/reply-trace/
cp -R plugins/reply-trace/skills ~/.codex/plugins/reply-trace/
test -f ~/.agents/plugins/marketplace.json || \
  cp hosts/codex/personal-marketplace.example.json ~/.agents/plugins/marketplace.json
cp plugins/reply-trace/hooks/reminder.py ~/.codex/hooks/reply_trace.py
```

既存の `~/.agents/plugins/marketplace.json` がある場合は example 全体で
上書きせず、`reply-trace` entry だけをマージします。その後、
`hosts/codex/hooks.fragment.json` の `UserPromptSubmit` 設定を
`~/.codex/hooks.json` にマージし、Codex を再起動して personal marketplace
から `reply-trace` をインストールします。

`plugins/reply-trace/hooks/hooks.json` は Claude Code 専用 hook adapter なので、
Codex plugin package にはコピーしません。

注意: これは改ざん不能な監査ログではありません。エージェントが読み込んだ
指示と prompt-time reminder に従って disclosure を書くための transparency
convention です。
