# reply-trace (日本語)

> AI エージェントの動作を可視化: 返信ごとに使ったプラグイン、スキル、
> MCP ツール、サブエージェント、フックを disclosure として公開。

言語: [English](../README.md) · [한국어](README.ko.md) · **日本語**

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
| Agent-agnostic core | 同じルールが Claude Code、Codex、他のエージェントホストで動作。 |
| ホスト adapter | Claude Code プラグイン同梱; Codex personal plugin package + hook adapter 同梱。 |
| Locale 対応 | 英語デフォルト、韓国語・日本語の footer ラベル/category。 |
| 依存なし | フックは標準ライブラリのみの小さな Python スクリプト。 |

## インストール

### Claude Code

```bash
claude plugin marketplace add akashi-ueda/reply-trace
claude plugin install reply-trace@reply-trace
```

フックが読み込まれるよう Claude Code を再起動します。

### Codex

Codex 対応は 2 つの部分から成ります:

1. `.codex-plugin/plugin.json` と共有 `reply-trace` スキルを含む personal plugin package。
2. 毎ターン reminder を再注入する `UserPromptSubmit` hook adapter。

詳細は [hosts/codex/README.md](../hosts/codex/README.md) を参照。

要約:

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
上書きせず、`reply-trace` entry だけをマージします。その後、
[hosts/codex/hooks.fragment.json](../hosts/codex/hooks.fragment.json) の
`UserPromptSubmit` 設定を `~/.codex/hooks.json` にマージし、Codex を再起動して
personal marketplace から `reply-trace` をインストールし、hook trust の確認が
出たら承認します。

`plugins/reply-trace/hooks/hooks.json` は Claude Code 専用 hook adapter なので、
Codex plugin package にはコピーしません。Codex は代わりに
`hosts/codex/hooks.fragment.json` を使います。

## 設定

すべてのオプションは環境変数で制御します。

| 変数 | デフォルト | 効果 |
|------|-----------|------|
| `REPLY_TRACE_LABEL` | locale デフォルト | footer ラベルを置換。 |
| `REPLY_TRACE_LOCALE` | `en` | category 名を選択。組み込み: `en`, `ko`, `ja`。 |
| `REPLY_TRACE_DISABLE` | unset | `1`, `true`, `on`, `yes` で footer を抑制。 |

レガシーの `AGENT_ATTRIBUTION_*` 変数も fallback として受け付けます。

## Locale

```bash
export REPLY_TRACE_LOCALE=ja
```

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
