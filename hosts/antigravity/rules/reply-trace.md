# Reply Trace footer

> Antigravity rule. Set its activation to **Always On** in the Customizations →
> Rules panel so it applies to every turn.

Append a single disclosure line as the **last line** of your reply whenever,
during this turn, you used any of: a **plugin/extension**, a **skill or
workflow**, an **MCP tool**, a **subagent**, or a **hook**. This makes agent
behavior transparent to the user.

## When to emit

Emit the footer when, during the current turn, you:

- used a plugin or extension,
- invoked a skill or workflow,
- called an MCP tool (`mcp__<server>__<tool>`),
- spawned a subagent, or
- a hook acted on your behalf.

Do **not** count plain built-in editor/file tools the user can already see you
using. If nothing in the list above happened, **omit the line completely** —
never print an empty footer.

## Format

One line, last in the reply. Categories in this order, each omitted when empty:

```
Auto-used — plugins: <plugin>[, ...]; skills: <skill>[, ...]; MCP: <server>/<tool>[, ...]; subagents: <name> (<role>)[, ...]; hooks: <name> (<role>)[, ...]
```

- **plugins**: extension/plugin id when one was explicitly used.
- **skills**: the skill or workflow id you applied.
- **MCP**: `<server>/<tool>` for each MCP tool called (dedupe repeats).
- **subagents**: subagent name + short role in parentheses.
- **hooks**: hook name + a short role in parentheses.

## Language

Write the footer in the **same language as your reply**, keeping this structure
and category order.

## Rules of thumb

- Exactly one line, always last, no blank-line padding.
- Omit empty categories; omit the whole line when nothing was auto-used.
- Be honest: list only what you actually used this turn, deduped.
