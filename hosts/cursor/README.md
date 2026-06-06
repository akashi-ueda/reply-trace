# Cursor host

Cursor has no Claude/Codex-style plugin package, but it has **Rules** —
always-on instructions re-sent with every request. `reply-trace` ships as an
always-apply rule, which is equivalent to the durable-instruction half of the
plugin on other hosts.

## Install (project rule)

Copy the rule into your project's `.cursor/rules/` folder and commit it:

```bash
mkdir -p .cursor/rules
cp hosts/cursor/rules/reply-trace.mdc .cursor/rules/reply-trace.mdc
```

The rule sets `alwaysApply: true`, so Cursor includes it in every chat and Agent
turn — no further setup. Restart or reload the Cursor window to pick it up.

## Install (global / user rule)

To apply it across all projects, open **Cursor Settings → Rules → User Rules**
and paste the body of [`rules/reply-trace.mdc`](rules/reply-trace.mdc) (the text
below the frontmatter).

## Why a rule, not a hook

Cursor supports hooks via `.cursor/hooks.json`, but the per-turn
`beforeSubmitPrompt` hook **cannot inject context** — it can only read or block
the prompt. Only `sessionStart` (and a few post-events) can add context, and
`sessionStart` fires once per session, not per turn. Since an `alwaysApply` rule
is already re-sent every turn, the rule alone covers the per-turn reminder that
the hook provides on Claude Code and Codex. No hook is required.

If you still want a once-per-session nudge, add a `sessionStart` hook in
`.cursor/hooks.json` whose script prints `{"additional_context": "<reminder>"}`
on stdout.

## Concept mapping

| reply-trace category | Cursor concept |
|----------------------|----------------|
| plugins | extensions |
| skills | rules / workflows |
| MCP | MCP tools (`mcp__<server>__<tool>`) |
| subagents | background agents |
| hooks | `.cursor/hooks.json` hooks |

## References

- [Cursor — Rules](https://cursor.com/docs/context/rules) (`.mdc` format, `alwaysApply`, AGENTS.md)
- [Cursor — Hooks](https://cursor.com/docs/hooks) (event list, context-injection limits)
