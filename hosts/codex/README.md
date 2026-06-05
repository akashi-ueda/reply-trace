# Codex host adapter

The `reply-trace` rule and reminder hook are agent-agnostic. Claude Code
loads them as a plugin (see repo root). Codex uses the same core through a
personal plugin package plus a `UserPromptSubmit` hook adapter.

## What Codex needs

1. **Personal plugin package** — copy the plugin into Codex's personal plugin
   source directory:

   ```bash
   mkdir -p ~/.codex/plugins
   rm -rf ~/.codex/plugins/reply-trace
   mkdir -p ~/.codex/plugins/reply-trace
   cp -R hosts/codex/.codex-plugin ~/.codex/plugins/reply-trace/
   cp -R plugins/reply-trace/skills ~/.codex/plugins/reply-trace/
   ```

   The package includes `.codex-plugin/plugin.json` and the shared
   `skills/reply-trace/SKILL.md`.

   Do not copy `plugins/reply-trace/hooks/hooks.json` into the Codex plugin
   package. That file is the Claude Code hook adapter.

2. **Personal marketplace entry** — add this plugin to
   `~/.agents/plugins/marketplace.json`. You can copy the example:

   ```bash
   mkdir -p ~/.agents/plugins
   test -f ~/.agents/plugins/marketplace.json || \
     cp hosts/codex/personal-marketplace.example.json ~/.agents/plugins/marketplace.json
   ```

   If you already have a personal marketplace file, merge only the
   `reply-trace` entry from the example. Codex resolves `source.path` relative
   to the marketplace root, so the example uses:

   ```json
   {
     "source": {
       "source": "local",
       "path": "./.codex/plugins/reply-trace"
     }
   }
   ```

3. **Hook adapter** — copy the same `reminder.py` and wire it into Codex hooks:

   ```bash
   mkdir -p ~/.codex/hooks
   cp plugins/reply-trace/hooks/reminder.py ~/.codex/hooks/reply_trace.py
   ```

   Then merge the `UserPromptSubmit` entry from
   [`hooks.fragment.json`](./hooks.fragment.json) into `~/.codex/hooks.json`.

4. Restart Codex. Open the plugin directory, select the personal marketplace,
   install `reply-trace`, start a new thread, and approve the hook trust prompt
   if Codex asks.

## Notes

- Codex plugins use `.codex-plugin/plugin.json`.
- Codex personal marketplaces can live at `~/.agents/plugins/marketplace.json`.
- Codex can discover hooks bundled with enabled plugins, but this adapter keeps
  the prompt-time reminder explicit in the active Codex hook layer.
- `reminder.py` is identical to the Claude hook script. It only reads env config
  and prints a reminder to stdout, which Codex adds to the prompt context.
- Configuration env vars (`REPLY_TRACE_LABEL`, `REPLY_TRACE_LOCALE`,
  `REPLY_TRACE_DISABLE`) work the same on both hosts. Legacy
  `AGENT_ATTRIBUTION_*` names are accepted as fallbacks.
- Other agents can use the same model: durable instruction plus prompt-time
  reminder/middleware, with host concepts mapped to `plugins`, `skills`, `MCP`,
  `subagents`, and `hooks`.

## 한국어

Codex는 `reply-trace`를 personal plugin package와 `UserPromptSubmit` hook
adapter로 사용합니다.

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

기존 `~/.agents/plugins/marketplace.json`이 있으면 example 파일 전체를 덮지
말고 `reply-trace` entry만 병합합니다. 그 다음 `hooks.fragment.json`을
`~/.codex/hooks.json`에 병합하고 Codex를 재시작합니다. personal marketplace에서
`reply-trace`를 설치하고, hook trust 확인이 나오면 승인합니다.

`plugins/reply-trace/hooks/hooks.json`은 Claude Code 전용 hook adapter이므로
Codex plugin package에는 복사하지 않습니다.

## 日本語

Codex では `reply-trace` を personal plugin package と
`UserPromptSubmit` hook adapter として使います。

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

既存の `~/.agents/plugins/marketplace.json` がある場合は example 全体で
上書きせず、`reply-trace` entry だけをマージします。次に
`hooks.fragment.json` を `~/.codex/hooks.json` にマージし、Codex を再起動します。
personal marketplace から `reply-trace` をインストールし、hook trust の確認が
出たら承認します。

`plugins/reply-trace/hooks/hooks.json` は Claude Code 専用 hook adapter なので、
Codex plugin package にはコピーしません。
