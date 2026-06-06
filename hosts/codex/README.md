# Codex host

`reply-trace` ships a single plugin package that works on both Claude Code and
Codex. The skill (`SKILL.md`) and the `UserPromptSubmit` reminder
(`hooks/hooks.json` + `hooks/reminder.py`) are agent-agnostic, so Codex loads
the same files Claude Code does.

## Install (marketplace)

```bash
codex plugin marketplace add akashi-ueda/reply-trace
codex plugin install reply-trace@reply-trace
```

Restart Codex, then run `/hooks` and trust the `reply-trace` hook. Plugin-bundled
hooks are non-managed, so Codex skips them until you review and trust the current
definition once.

That's it — no manual hook wiring. Codex auto-discovers the bundled
`hooks/hooks.json` and sets `CLAUDE_PLUGIN_ROOT` for the reminder command, so the
same hook file runs on both hosts.

## Install (local / development)

To test a local checkout without the public marketplace, add a personal
marketplace entry pointing at this repo's plugin folder:

`~/.agents/plugins/marketplace.json`

```json
{
  "name": "personal",
  "plugins": [
    {
      "name": "reply-trace",
      "source": { "source": "local", "path": "./plugins/reply-trace" },
      "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
      "interface": { "displayName": "Reply Trace" },
      "category": "Productivity"
    }
  ]
}
```

Codex resolves `source.path` relative to the marketplace root. Point it at wherever
this repo's `plugins/reply-trace` lives, restart Codex, install from your personal
marketplace, and trust the hook via `/hooks`.

## How it works on Codex

- Plugin manifest: `.codex-plugin/plugin.json` (Codex), `.claude-plugin/plugin.json` (Claude Code). Both sit in the same plugin folder.
- Skill: `skills/reply-trace/SKILL.md`, shared.
- Hook: `hooks/hooks.json` runs `reminder.py` at `UserPromptSubmit`. Codex
  auto-discovers this default file; no `hooks` entry in the manifest is required.
- Env: the hook command uses `${CLAUDE_PLUGIN_ROOT}`, which Codex sets for
  plugin-hook compatibility (alongside its own `PLUGIN_ROOT`).
- Config env vars (`REPLY_TRACE_LABEL`, `REPLY_TRACE_DISABLE`) work the same on
  both hosts. Legacy `AGENT_ATTRIBUTION_*` names are accepted as fallbacks. The
  footer language always matches the reply — there is no locale setting.

## References

- [Codex — Build plugins](https://developers.openai.com/codex/plugins/build) (plugin structure, bundled hooks)
- [Codex — Hooks](https://developers.openai.com/codex/hooks) (`UserPromptSubmit` event, trust review)
