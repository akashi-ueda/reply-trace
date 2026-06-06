# reply-trace (Español)

> Haz visible el comportamiento del agente de IA: revela los plugins,
> habilidades, herramientas MCP, subagentes y hooks usados en cada respuesta.

Idiomas: [English](../README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · **Español** · [中文](README.zh.md)

`reply-trace` añade una línea final de transparencia cuando un agente usa
automatización entre bastidores:

```text
Usado automáticamente — plugins: Browser; habilidades: browser:control-in-app-browser; MCP: anthropicDocs/search_docs; subagentes: reviewer (revisa el diff); hooks: pre_tool_use (revisa la política de comandos)
```

- Si no se usó nada, no se imprime ninguna línea.
- Las categorías vacías se omiten.

## Por qué

Los agentes de programación modernos pueden incorporar plugins, habilidades,
servidores MCP, subagentes y hooks en silencio. Es potente, pero dificulta
auditar una respuesta. Este plugin mantiene la divulgación pequeña, consistente
y siempre al final de la respuesta.

## Características

| Función | Qué hace |
|---------|----------|
| Footer de una línea | Añade una línea de atribución compacta solo cuando hace falta. |
| Núcleo agnóstico de agente | La misma regla funciona en Claude Code, Codex, Cursor, Antigravity y más. |
| Plugin o regla | Paquete de plugin en Claude Code/Codex; regla siempre activa en Cursor/Antigravity. |
| Idioma automático | El footer se escribe en el mismo idioma de cada respuesta — sin ajuste de locale. |
| Sin dependencias | El hook es un pequeño script de Python que usa solo la librería estándar. |

## Instalación

### Claude Code

```bash
claude plugin marketplace add akashi-ueda/reply-trace
claude plugin install reply-trace@reply-trace
```

Reinicia Claude Code para que cargue el hook.

### Codex

El mismo flujo de dos comandos que en Claude Code:

```bash
codex plugin marketplace add akashi-ueda/reply-trace
codex plugin install reply-trace@reply-trace
```

Reinicia Codex, ejecuta `/hooks` y confía una vez en el hook `reply-trace` (los
hooks de plugin son non-managed, así que Codex pide aprobación antes de
ejecutarlos).

El mismo paquete sirve para ambos hosts: Codex lee el `.claude-plugin/marketplace.json`
compatible, instala desde `.codex-plugin/plugin.json` y autodescubre el
`hooks/hooks.json` incluido. El comando del hook usa `${CLAUDE_PLUGIN_ROOT}`, que
Codex define por compatibilidad — sin cableado manual. Instalación local de
desarrollo: [hosts/codex/README.md](../hosts/codex/README.md).

### Cursor

Cursor no tiene paquete de plugin, pero sus **Rules** son instrucciones siempre
activas que se reinyectan cada turno — equivalente a la mitad de instrucción
duradera del plugin. Instala como regla always-apply:

```bash
mkdir -p .cursor/rules
cp rules/reply-trace.mdc .cursor/rules/reply-trace.mdc
```

La regla usa `alwaysApply: true`, así que Cursor la incluye cada turno. El hook
`beforeSubmitPrompt` de Cursor no puede inyectar contexto (solo bloquear), por lo
que la regla siempre activa (no un hook) lleva el recordatorio. Opciones
global/user-rule y detalles: [hosts/cursor/README.md](../hosts/cursor/README.md).

### Google Antigravity

Antigravity también usa **Rules** siempre activas y no tiene hook en tiempo de
prompt, así que la regla es todo el adaptador:

```bash
mkdir -p .agents/rules
cp hosts/antigravity/rules/reply-trace.md .agents/rules/reply-trace.md
```

Luego abre **Customizations → Rules** y pon la activación de la regla
`reply-trace` en **Always On**. Para una regla global, añádela a
`~/.gemini/GEMINI.md`. Detalles: [hosts/antigravity/README.md](../hosts/antigravity/README.md).

## Configuración

Todas las opciones usan variables de entorno.

| Variable | Por defecto | Efecto |
|----------|-------------|--------|
| `REPLY_TRACE_LABEL` | `Auto-used` | Reemplaza la etiqueta del footer. |
| `REPLY_TRACE_DISABLE` | sin definir | Pon `1`, `true`, `on` o `yes` para suprimir el footer. |

Las variables heredadas `AGENT_ATTRIBUTION_*` se aceptan como respaldo.

## Idioma

El idioma del footer siempre sigue al de tu respuesta — una respuesta en español
obtiene un footer en español, sin configuración. No hay ajuste de locale; el
idioma sigue la conversación. Por ejemplo, una respuesta en español termina con:

```text
Usado automáticamente — plugins: Browser; habilidades: browser:control-in-app-browser; MCP: anthropicDocs/search_docs; subagentes: reviewer (revisa el diff); hooks: pre_tool_use (revisa la política de comandos)
```

## Núcleo agnóstico de agente

El plugin tiene dos piezas:

| Pieza | Rol |
|-------|-----|
| `skills/reply-trace/SKILL.md` | Define cuándo emitir el footer y cómo formatearlo. |
| `hooks/reminder.py` | Reinyecta un breve recordatorio cada prompt para que la regla no se diluya. |

El hook no escribe el footer. Lo escribe el agente, porque solo el agente sabe
exactamente qué plugins, herramientas, subagentes y hooks se usaron ese turno.

Esto es una convención de transparencia, no un registro de auditoría a prueba de
manipulaciones. Depende de que el agente anfitrión siga la instrucción cargada y
el recordatorio en tiempo de prompt.

Portar a otro host de agente:

1. Carga `SKILL.md` (o una regla equivalente) mediante el mecanismo de
   instrucción duradera, skill, regla o extensión de ese host.
2. Si el host admite hooks en tiempo de prompt, ejecuta `reminder.py` o
   middleware equivalente antes de cada prompt. Si no (p. ej. Cursor,
   Antigravity), una regla siempre activa ya se reaplica cada turno.
3. Mapea los conceptos del host a estas categorías:
   `plugins`, `skills`, `MCP`, `subagents`, `hooks`.
4. Mantén la divulgación final como una sola línea al final de la respuesta.

## Licencia

MIT — ver [LICENSE](../LICENSE).
