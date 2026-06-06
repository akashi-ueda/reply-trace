# Google Antigravity host

Antigravity has no Claude/Codex-style plugin package, but it has **Rules** —
always-on system instructions the agent considers every turn. `reply-trace`
ships as an Always-On rule, equivalent to the durable-instruction half of the
plugin on other hosts. Antigravity has no prompt-time hook mechanism, so the
rule is the whole adapter.

## Install (workspace rule)

Copy the rule into your workspace rules folder and commit it:

```bash
mkdir -p .agents/rules
cp hosts/antigravity/rules/reply-trace.md .agents/rules/reply-trace.md
```

`.agents/rules/` is the current default; older builds also read `.agent/rules/`.
Then open **Customizations → Rules** in the agent panel and set the
`reply-trace` rule's activation to **Always On** so it applies to every turn.

## Install (global rule)

To apply it across all workspaces, append the body of
[`rules/reply-trace.md`](rules/reply-trace.md) to your global rules file at
`~/.gemini/GEMINI.md`.

## Activation modes

Antigravity rules support **Always On**, Model Decision, Glob, and Manual
activation. Use **Always On** for `reply-trace` — the footer rule must apply to
every reply, not just file-matched or manually mentioned turns.

## Concept mapping

| reply-trace category | Antigravity concept |
|----------------------|---------------------|
| plugins | extensions |
| skills | skills / workflows |
| MCP | MCP tools (`mcp__<server>__<tool>`) |
| subagents | subagents |
| hooks | n/a (no hook mechanism; rule is always-on) |

## References

- [Antigravity — Rules & Workflows](https://antigravity.google/docs/rules-workflows)
- [Antigravity — Agent Skills](https://antigravity.google/docs/skills)
