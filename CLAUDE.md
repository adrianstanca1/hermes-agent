# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hermes Agent is a self-improving AI agent built by Nous Research. It routes AI requests across multiple providers (OpenRouter, Ollama, OpenAI, etc.) and supports messaging platforms (Telegram, Discord, Slack, WhatsApp). Key features include skills system, memory/recall, cron scheduling, and subagent delegation.

## Commands

```bash
# Development setup
source venv/bin/activate                    # Activate venv (REQUIRED before any Python)
uv pip install -e ".[all,dev]"              # Install with dev dependencies
./scripts/run_tests.sh                      # Run full test suite (CI-parity)
./scripts/run_tests.sh tests/path/to/test   # Run specific test file/directory

# Development
python -m pytest tests/ -q -n 4            # Direct pytest (only if wrapper unavailable)
```

### TUI Development (ui-tui/)
```bash
cd ui-tui && npm run dev                   # Watch mode for TUI changes
npm run build                               # Production build
npm run type-check                          # TypeScript check only
```

## Architecture

```
hermes-agent/
├── run_agent.py          # AIAgent class — core conversation loop
├── model_tools.py        # Tool orchestration (discovers + dispatches tools)
├── toolsets.py           # Toolset definitions (_HERMES_CORE_TOOLS list)
├── cli.py               # HermesCLI — interactive CLI orchestrator (485KB)
├── hermes_state.py     # SessionDB — SQLite FTS5 session storage
├── tools/               # Tool implementations (one file per tool)
│   ├── registry.py      # Central registry (no deps — imported by all tools)
│   └── *.py            # Each calls registry.register() at import time
├── agent/              # Agent internals
│   ├── prompt_builder.py
│   ├── context_compressor.py
│   └── display.py     # KawaiiSpinner, tool preview formatting
├── hermes_cli/         # CLI subcommands, config, setup wizard
│   ├── main.py         # Entry point for all `hermes` subcommands
│   ├── config.py       # DEFAULT_CONFIG, OPTIONAL_ENV_VARS
│   └── commands.py    # COMMAND_REGISTRY — all slash commands
├── gateway/            # Messaging platform gateway
│   └── platforms/      # Adapters: telegram, discord, slack, whatsapp, signal
├── ui-tui/            # Ink (React) terminal UI
└── tui_gateway/       # Python JSON-RPC backend for TUI
```

### Agent Loop (run_agent.py)

```python
while api_call_count < self.max_iterations:
    response = client.chat.completions.create(model=model, messages=messages, tools=tool_schemas)
    if response.tool_calls:
        for tool_call in response.tool_calls:
            result = handle_function_call(tool_call.name, tool_call.args, task_id)
            messages.append(tool_result_message(result))
    else:
        return response.content
```

### Tool Registration Pattern

Tools auto-discover via `registry.register()` at import time. Two files to modify:

**1. `tools/your_tool.py`:**
```python
from tools.registry import registry

def your_tool(param: str, task_id: str = None) -> str:
    return json.dumps({"success": True, "data": "..."})

registry.register(
    name="your_tool",
    toolset="your_toolset",
    schema={"name": "your_tool", "description": "...", "parameters": {...}},
    handler=lambda args, **kw: your_tool(param=args.get("param"), task_id=kw.get("task_id")),
)
```

**2. `toolsets.py`** — add to `_HERMES_CORE_TOOLS` or a new toolset.

### Profiles (Multi-Instance)

Hermes supports multiple isolated profiles via `HERMES_HOME`. **All paths must use `get_hermes_home()`** — never hardcode `~/.hermes`.

```python
from hermes_constants import get_hermes_home, display_hermes_home

config_path = get_hermes_home() / "config.yaml"     # For code
print(f"Config at {display_hermes_home()}")           # For user-facing messages
```

## Key Conventions

### Path Constants (hermes_constants.py)
- `get_hermes_home()` — active profile's Hermes directory (code paths)
- `display_hermes_home()` — for user-facing messages
- `HERMES_HOME` env var — profile isolation mechanism

### Slash Commands (hermes_cli/commands.py)
Add to `COMMAND_REGISTRY` in `commands.py`:
```python
CommandDef("mycommand", "Description", "Category", aliases=("mc",), args_hint="<arg>")
```
Then add handler in `cli.py` (`process_command()`) and `gateway/run.py`.

### Config System (hermes_cli/config.py)
Two loaders: `load_cli_config()` for CLI, `load_config()` for gateway. Add new config keys to `DEFAULT_CONFIG`, bump `_config_version` to trigger migration.

### Skin/Theme Engine (hermes_cli/skin_engine.py)
Data-driven CLI theming — skins are YAML configs, no code changes needed. Built-in skins: `default`, `ares`, `mono`, `slate`.

## Important Policies

### Prompt Caching Integrity
Never change toolsets, reload memories, or rebuild system prompts mid-conversation. Cache-breaking forces dramatically higher costs. The ONLY permitted mid-conversation change is context compression.

### Profile-Safe Code Rules
1. Use `get_hermes_home()` for all paths — never `~/.hermes` or `Path.home() / ".hermes"`
2. Use `display_hermes_home()` for user-facing print/log messages
3. Tests must use `_isolate_hermes_home` fixture (tests/conftest.py)

## Known Pitfalls

| Pitfall | Solution |
|---------|----------|
| Hardcoding `~/.hermes` | Use `get_hermes_home()` from `hermes_constants` |
| Using `simple_term_menu` | Use `curses` (stdlib) — tmux/iTerm2 rendering bugs |
| Using `\033[K` ANSI escape | Use space-padding instead — leaks in prompt_toolkit |
| Cross-tool schema references | Add dynamically in `get_tool_definitions()` in model_tools.py |

## Full Developer Guide

The `AGENTS.md` file contains comprehensive documentation covering:
- TUI architecture (ui-tui + tui_gateway)
- Adding new tools and slash commands
- Config system internals
- Skin/theme system
- Profile system details
- Testing philosophy and wrapper rationale

For deep work on CLI, gateway, tools, or agent internals, read `AGENTS.md` first.
