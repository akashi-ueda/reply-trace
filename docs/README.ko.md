# reply-trace (한국어)

> AI 에이전트 동작을 보이게: 매 응답에 사용한 플러그인, 스킬, MCP 도구,
> 서브에이전트, 훅을 disclosure로 공개.

언어: [English](../README.md) · **한국어** · [日本語](README.ja.md) · [Español](README.es.md) · [中文](README.zh.md)

`reply-trace`는 에이전트가 뒤에서 자동화를 사용했을 때 응답 마지막에
한 줄 transparency footer를 추가합니다:

```text
사용한 자동 트리거 — 플러그인: Browser; 스킬: browser:control-in-app-browser; MCP: anthropicDocs/search_docs; 서브에이전트: reviewer (diff 검토); 훅: pre_tool_use (명령 정책 확인)
```

- 아무것도 사용하지 않으면 줄을 출력하지 않습니다.
- 빈 category는 생략합니다.

## 왜

요즘 코딩 에이전트는 플러그인, 스킬, MCP 서버, 서브에이전트, 훅을 조용히
끌어옵니다. 강력하지만 응답을 감사하기 어렵게 만듭니다. 이 플러그인은
disclosure를 작고 일관되게, 항상 응답 끝에 둡니다.

## 특징

| 기능 | 설명 |
|------|------|
| 한 줄 footer | 필요할 때만 간결한 attribution 줄 추가. |
| Agent-agnostic core | 같은 규칙이 Claude Code, Codex, Cursor, Antigravity 등에서 동작. |
| 플러그인 또는 rule | Claude Code/Codex는 플러그인 패키지, Cursor/Antigravity는 always-on rule. |
| Locale 지원 | 영어 기본, 한국어·일본어·스페인어·중국어 footer 라벨/category 제공. |
| 무의존성 | 훅은 표준 라이브러리만 쓰는 작은 Python 스크립트. |

## 설치

### Claude Code

```bash
claude plugin marketplace add akashi-ueda/reply-trace
claude plugin install reply-trace@reply-trace
```

훅이 로드되도록 Claude Code를 재시작합니다.

### Codex

Claude Code와 동일한 두 명령:

```bash
codex plugin marketplace add akashi-ueda/reply-trace
codex plugin install reply-trace@reply-trace
```

Codex를 재시작하고 `/hooks`에서 `reply-trace` 훅을 한 번 trust 합니다(플러그인
훅은 non-managed라 실행 전 승인 필요).

같은 플러그인 패키지가 두 호스트를 다 지원합니다: Codex는 legacy 호환
`.claude-plugin/marketplace.json`을 읽고 `.codex-plugin/plugin.json`으로 설치한
뒤 번들된 `hooks/hooks.json`을 자동 인식합니다. 훅 명령은
`${CLAUDE_PLUGIN_ROOT}`를 쓰는데 Codex가 플러그인 훅 호환용으로 이 변수를
설정하므로 수동 훅 와이어링이 필요 없습니다. 로컬 개발 설치는
[hosts/codex/README.md](../hosts/codex/README.md) 참고.

### Cursor

Cursor엔 플러그인 패키지가 없지만 **Rules**가 매 턴 다시 주입되는 always-on
지침이라 플러그인의 durable-instruction 역할과 동등합니다. always-apply rule로
설치:

```bash
mkdir -p .cursor/rules
cp hosts/cursor/rules/reply-trace.mdc .cursor/rules/reply-trace.mdc
```

rule이 `alwaysApply: true`라 Cursor가 매 턴 포함합니다. Cursor의 per-turn
`beforeSubmitPrompt` 훅은 context 주입이 안 되므로(차단만 가능) 훅 대신 always-on
rule이 reminder를 담당합니다. global/user-rule 옵션·상세:
[hosts/cursor/README.md](../hosts/cursor/README.md).

### Google Antigravity

Antigravity도 always-on **Rules**를 쓰고 prompt-time 훅이 없어 rule이 어댑터
전부입니다:

```bash
mkdir -p .agents/rules
cp hosts/antigravity/rules/reply-trace.md .agents/rules/reply-trace.md
```

그 다음 **Customizations → Rules**에서 `reply-trace` rule 활성화를 **Always On**
으로 설정합니다. 전역 rule은 `~/.gemini/GEMINI.md`에 덧붙입니다. 상세:
[hosts/antigravity/README.md](../hosts/antigravity/README.md).

## 설정

모든 옵션은 환경 변수로 제어합니다.

| 변수 | 기본값 | 효과 |
|------|--------|------|
| `REPLY_TRACE_LABEL` | locale 기본값 | footer 라벨 교체. |
| `REPLY_TRACE_LOCALE` | `auto` | `auto`는 footer를 응답 언어에 맞춤; `en`/`ko`/`ja`/기타 설정 시 그 언어로 고정. |
| `REPLY_TRACE_DISABLE` | unset | `1`, `true`, `on`, `yes` 설정 시 footer 억제. |

레거시 `AGENT_ATTRIBUTION_*` 변수도 fallback으로 허용됩니다.

## Locale

기본값(`REPLY_TRACE_LOCALE=auto`)에서는 footer 언어가 응답 언어를 따라갑니다 —
한국어로 답하면 한국어 footer, 일본어로 답하면 일본어 footer, 설정 불필요.
한 언어로 고정하고 canonical category 단어를 쓰려면 명시적 locale을 설정합니다.

```bash
# 한국어로 고정 (auto면 응답이 한국어일 때 자동)
export REPLY_TRACE_LOCALE=ko
```

```text
사용한 자동 트리거 — 플러그인: Browser; 스킬: browser:control-in-app-browser; MCP: anthropicDocs/search_docs; 서브에이전트: reviewer (diff 검토); 훅: pre_tool_use (명령 정책 확인)
```

## Agent-Agnostic Core

플러그인은 두 조각으로 구성됩니다:

| 조각 | 역할 |
|------|------|
| `skills/reply-trace/SKILL.md` | footer를 언제 어떻게 출력할지 정의. |
| `hooks/reminder.py` | 규칙이 흐려지지 않도록 prompt-time reminder 재주입. |

훅은 footer를 쓰지 않습니다. 그 턴에 어떤 플러그인·도구·서브에이전트·훅이
쓰였는지는 에이전트만 알기 때문에 footer는 에이전트가 씁니다.

이것은 transparency convention이지 변조 불가능한 감사 로그가 아닙니다.
호스트 에이전트가 로드된 지침과 prompt-time reminder를 따른다는 전제에
의존합니다.

다른 에이전트 호스트로 이식:

1. 그 호스트의 durable instruction·skill·extension 메커니즘으로 `SKILL.md` 로드.
2. 매 user prompt 전에 `reminder.py` 또는 동등한 미들웨어 실행.
3. 호스트 개념을 `plugins`, `skills`, `MCP`, `subagents`, `hooks` category에 매핑.
4. 최종 disclosure를 응답 끝 한 줄로 유지.

## 라이선스

MIT — [LICENSE](../LICENSE) 참고.
