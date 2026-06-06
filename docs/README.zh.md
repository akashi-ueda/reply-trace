# reply-trace (中文)

> 让 AI 智能体的行为可见：在每次回复中公开所用的插件、技能、MCP 工具、
> 子代理和钩子。

语言：[English](../README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [Español](README.es.md) · **中文**

当智能体在幕后使用自动化时，`reply-trace` 会在回复末尾追加一行透明度页脚：

```text
自动使用 — 插件: Browser; 技能: browser:control-in-app-browser; MCP: anthropicDocs/search_docs; 子代理: reviewer (检查 diff); 钩子: pre_tool_use (检查命令策略)
```

- 如果什么都没用到，则不输出该行。
- 空的类别会被省略。

## 为什么

现代编码智能体可能会悄悄引入插件、技能、MCP 服务器、子代理和钩子。这很强大，
但会让回答难以审计。本插件让这种公开保持简短、一致，并始终位于回复末尾。

## 亮点

| 功能 | 作用 |
|------|------|
| 单行页脚 | 仅在需要时添加一行紧凑的归属信息。 |
| 智能体无关核心 | 同一规则适用于 Claude Code、Codex、Cursor、Antigravity 等。 |
| 插件或规则 | 在 Claude Code/Codex 上是插件包；在 Cursor/Antigravity 上是常驻规则。 |
| 多语言支持 | 默认英文，并提供 es、ko、ja、zh 的页脚标签/类别。 |
| 零依赖 | 钩子是仅使用标准库的小型 Python 脚本。 |

## 安装

### Claude Code

```bash
claude plugin marketplace add akashi-ueda/reply-trace
claude plugin install reply-trace@reply-trace
```

重启 Claude Code 以加载钩子。

### Codex

与 Claude Code 相同的两条命令：

```bash
codex plugin marketplace add akashi-ueda/reply-trace
codex plugin install reply-trace@reply-trace
```

重启 Codex，运行 `/hooks` 并一次性信任 `reply-trace` 钩子（插件钩子是
non-managed，因此 Codex 在运行前会请求批准）。

同一个插件包同时服务两个 host：Codex 读取兼容的
`.claude-plugin/marketplace.json`，从 `.codex-plugin/plugin.json` 安装，并自动
发现内置的 `hooks/hooks.json`。钩子命令使用 `${CLAUDE_PLUGIN_ROOT}`，Codex 为
兼容性设置该变量——无需手动接线。本地开发安装见
[hosts/codex/README.md](../hosts/codex/README.md)。

### Cursor

Cursor 没有插件包，但其 **Rules** 是每轮都会重新注入的常驻指令——等同于插件中
持久指令的那一半。作为 always-apply 规则安装：

```bash
mkdir -p .cursor/rules
cp hosts/cursor/rules/reply-trace.mdc .cursor/rules/reply-trace.mdc
```

该规则设置了 `alwaysApply: true`，因此 Cursor 每轮都会包含它。Cursor 的
`beforeSubmitPrompt` 钩子无法注入上下文（只能拦截），所以由常驻规则（而非钩子）
承担提醒。全局/用户规则选项与细节见
[hosts/cursor/README.md](../hosts/cursor/README.md)。

### Google Antigravity

Antigravity 同样使用常驻 **Rules**，且没有 prompt 阶段的钩子，因此规则即全部
适配器：

```bash
mkdir -p .agents/rules
cp hosts/antigravity/rules/reply-trace.md .agents/rules/reply-trace.md
```

然后打开 **Customizations → Rules**，将 `reply-trace` 规则的激活方式设为
**Always On**。如需全局规则，请追加到 `~/.gemini/GEMINI.md`。细节见
[hosts/antigravity/README.md](../hosts/antigravity/README.md)。

## 配置

所有选项均通过环境变量控制。

| 变量 | 默认 | 作用 |
|------|------|------|
| `REPLY_TRACE_LABEL` | locale 默认值 | 替换页脚标签。 |
| `REPLY_TRACE_LOCALE` | `auto` | `auto` 让页脚匹配你回复的语言；设为 `en`/`ko`/`ja`/`es`/`zh`/其他以固定。 |
| `REPLY_TRACE_DISABLE` | 未设置 | 设为 `1`、`true`、`on` 或 `yes` 以抑制页脚。 |

仍接受旧版 `AGENT_ATTRIBUTION_*` 变量作为回退。

## Locale

默认情况下（`REPLY_TRACE_LOCALE=auto`），页脚语言跟随回复语言——中文回复得到
中文页脚，无需配置。设置明确的 locale 可固定为某一语言并使用规范的类别词。

```bash
# 固定为中文（auto 时，中文回复会自动使用）
export REPLY_TRACE_LOCALE=zh
```

```text
自动使用 — 插件: Browser; 技能: browser:control-in-app-browser; MCP: anthropicDocs/search_docs; 子代理: reviewer (检查 diff); 钩子: pre_tool_use (检查命令策略)
```

## 智能体无关核心

插件由两部分组成：

| 部分 | 职责 |
|------|------|
| `skills/reply-trace/SKILL.md` | 定义何时输出页脚以及如何格式化。 |
| `hooks/reminder.py` | 每个 prompt 重新注入简短提醒，防止规则漂移。 |

钩子不写页脚。页脚由智能体编写，因为只有它确切知道这一轮用了哪些插件、工具、
子代理和钩子。

这是一种透明度约定，而非防篡改的审计日志。它依赖宿主智能体遵循已加载的指令和
prompt 阶段的提醒。

移植到其他智能体宿主：

1. 通过该宿主的持久指令、skill、规则或扩展机制加载 `SKILL.md`（或等效规则）。
2. 若宿主支持 prompt 阶段钩子，在每个 prompt 前运行 `reminder.py` 或等效中间件；
   若不支持（如 Cursor、Antigravity），常驻规则已在每轮重新应用。
3. 将宿主概念映射到这些类别：`plugins`、`skills`、`MCP`、`subagents`、`hooks`。
4. 将最终公开保持为回复末尾的一行。

## 许可证

MIT —— 见 [LICENSE](../LICENSE)。
