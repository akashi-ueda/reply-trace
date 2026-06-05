# reply-trace (한국어)

> AI 에이전트 동작을 보이게: 매 응답에 사용한 플러그인, 스킬, MCP 도구,
> 서브에이전트, 훅을 disclosure로 공개.

언어: [English](../README.md) · **한국어** · [日本語](README.ja.md)

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
| Agent-agnostic core | 같은 규칙이 Claude Code, Codex, 기타 에이전트 호스트에서 동작. |
| 호스트 adapter | Claude Code 플러그인 포함; Codex personal plugin package + hook adapter 포함. |
| Locale 지원 | 영어 기본, 한국어·일본어 footer 라벨/category 제공. |
| 무의존성 | 훅은 표준 라이브러리만 쓰는 작은 Python 스크립트. |

## 설치

### Claude Code

```bash
claude plugin marketplace add akashi-ueda/reply-trace
claude plugin install reply-trace@reply-trace
```

훅이 로드되도록 Claude Code를 재시작합니다.

### Codex

Codex 지원은 두 부분으로 구성됩니다:

1. `.codex-plugin/plugin.json`과 공유 `reply-trace` 스킬을 담은 personal plugin package.
2. 매 턴 reminder를 다시 주입하는 `UserPromptSubmit` hook adapter.

자세히는 [hosts/codex/README.md](../hosts/codex/README.md) 참고.

요약:

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
말고 `reply-trace` entry만 병합합니다. 그 다음
[hosts/codex/hooks.fragment.json](../hosts/codex/hooks.fragment.json)의
`UserPromptSubmit` 항목을 `~/.codex/hooks.json`에 병합하고, Codex를 재시작한 뒤
personal marketplace에서 `reply-trace`를 설치하고, hook trust 확인이 나오면
승인합니다.

`plugins/reply-trace/hooks/hooks.json`은 Claude Code 전용 hook adapter이므로
Codex plugin package에는 복사하지 않습니다. Codex는 대신
`hosts/codex/hooks.fragment.json`을 씁니다.

## 설정

모든 옵션은 환경 변수로 제어합니다.

| 변수 | 기본값 | 효과 |
|------|--------|------|
| `REPLY_TRACE_LABEL` | locale 기본값 | footer 라벨 교체. |
| `REPLY_TRACE_LOCALE` | `en` | category 이름 선택. 내장: `en`, `ko`, `ja`. |
| `REPLY_TRACE_DISABLE` | unset | `1`, `true`, `on`, `yes` 설정 시 footer 억제. |

레거시 `AGENT_ATTRIBUTION_*` 변수도 fallback으로 허용됩니다.

## Locale

```bash
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
