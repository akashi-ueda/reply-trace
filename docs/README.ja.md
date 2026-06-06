# reply-trace (日本語)

> AI エージェントの動作を可視化: 返信ごとに使ったプラグイン、スキル、
> MCP ツール、サブエージェント、フックを disclosure として公開。

言語: [English](../README.md) · [한국어](README.ko.md) · **日本語** · [Español](README.es.md) · [中文](README.zh.md)

`reply-trace` は、エージェントが裏で自動化を使ったときに、返信の最後へ
1 行の transparency footer を追加します:

```text
使用した自動トリガー — プラグイン: Browser; スキル: browser:control-in-app-browser; MCP: anthropicDocs/search_docs; サブエージェント: reviewer (diff確認); フック: pre_tool_use (コマンドポリシー確認)
```

- 何も使っていない場合は出力しません。
- 空の category は省略します。

## なぜ

最近のコーディングエージェントは、プラグイン、スキル、MCP サーバー、
サブエージェント、フックを静かに取り込みます。強力ですが、回答の監査を
難しくします。このプラグインは disclosure を小さく一貫させ、常に返信の
最後に置きます。

## 特徴

| 機能 | 説明 |
|------|------|
| 1 行 footer | 必要なときだけ簡潔な attribution 行を追加。 |
| Agent-agnostic core | 同じルールが Claude Code、Codex、Cursor、Antigravity などで動作。 |
| プラグインまたは rule | Claude Code/Codex はプラグインパッケージ、Cursor/Antigravity は always-on rule。 |
| 自動言語 | footer は各返信と同じ言語で書かれる — locale 設定なし。 |
| 依存なし | フックは標準ライブラリのみの小さな Python スクリプト。 |

## インストール

### Claude Code

```bash
claude plugin marketplace add akashi-ueda/reply-trace
claude plugin install reply-trace@reply-trace
```

フックが読み込まれるよう Claude Code を再起動します。

### Codex

Claude Code と同じ 2 コマンド:

```bash
codex plugin marketplace add akashi-ueda/reply-trace
codex plugin install reply-trace@reply-trace
```

Codex を再起動し、`/hooks` で `reply-trace` フックを一度 trust します（プラグイン
フックは non-managed なので実行前に承認が必要）。

同じプラグインパッケージが両ホストに対応します: Codex は legacy 互換の
`.claude-plugin/marketplace.json` を読み、`.codex-plugin/plugin.json` から
インストールし、同梱の `hooks/hooks.json` を自動検出します。フックコマンドは
`${CLAUDE_PLUGIN_ROOT}` を使い、Codex がプラグインフック互換のためこの変数を
設定するので、手動のフック配線は不要です。ローカル開発インストールは
[hosts/codex/README.md](../hosts/codex/README.md) を参照。

### Cursor

Cursor にはプラグインパッケージがありませんが、**Rules** が毎ターン再注入される
always-on 指示なので、プラグインの durable-instruction の役割と同等です。
always-apply rule としてインストール:

```bash
mkdir -p .cursor/rules
cp rules/reply-trace.mdc .cursor/rules/reply-trace.mdc
```

rule は `alwaysApply: true` なので Cursor が毎ターン含めます。Cursor の per-turn
`beforeSubmitPrompt` フックは context を注入できない（ブロックのみ）ため、フック
ではなく always-on rule が reminder を担います。global/user-rule オプションと詳細:
[hosts/cursor/README.md](../hosts/cursor/README.md)。

### Google Antigravity

Antigravity も always-on **Rules** を使い、prompt-time フックがないため rule が
アダプターのすべてです:

```bash
mkdir -p .agents/rules
cp hosts/antigravity/rules/reply-trace.md .agents/rules/reply-trace.md
```

その後 **Customizations → Rules** で `reply-trace` rule の有効化を **Always On**
に設定します。グローバル rule は `~/.gemini/GEMINI.md` に追記します。詳細:
[hosts/antigravity/README.md](../hosts/antigravity/README.md)。

## 設定

すべてのオプションは環境変数で制御します。

| 変数 | デフォルト | 効果 |
|------|-----------|------|
| `REPLY_TRACE_LABEL` | `Auto-used` | footer ラベルを置換。 |
| `REPLY_TRACE_DISABLE` | unset | `1`, `true`, `on`, `yes` で footer を抑制。 |

レガシーの `AGENT_ATTRIBUTION_*` 変数も fallback として受け付けます。

## 言語

footer の言語は常に返信の言語に従います — 日本語で答えれば日本語 footer、
韓国語なら韓国語 footer、設定不要です。locale 設定はなく、言語は会話に従います。
例えば日本語の返信は次で終わります。

```text
使用した自動トリガー — プラグイン: Browser; スキル: browser:control-in-app-browser; MCP: anthropicDocs/search_docs; サブエージェント: reviewer (diff確認); フック: pre_tool_use (コマンドポリシー確認)
```

## Agent-Agnostic Core

プラグインは 2 つの部品から成ります:

| 部品 | 役割 |
|------|------|
| `skills/reply-trace/SKILL.md` | footer をいつ・どう出力するかを定義。 |
| `hooks/reminder.py` | ルールがぶれないよう prompt-time reminder を再注入。 |

フックは footer を書きません。そのターンでどのプラグイン・ツール・
サブエージェント・フックが使われたかはエージェントだけが知っているため、
footer はエージェントが書きます。

これは transparency convention であり、改ざん不能な監査ログではありません。
ホストエージェントが読み込んだ指示と prompt-time reminder に従うことを前提に
します。

他のエージェントホストへの移植:

1. そのホストの durable instruction・skill・extension の仕組みで `SKILL.md` を読み込む。
2. 各 user prompt の前に `reminder.py` または同等のミドルウェアを実行。
3. ホスト概念を `plugins`, `skills`, `MCP`, `subagents`, `hooks` の category に対応付け。
4. 最終 disclosure を返信末尾の 1 行として維持。

## ライセンス

MIT — [LICENSE](../LICENSE) を参照。
