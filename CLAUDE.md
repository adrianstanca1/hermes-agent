# Hermes Agent — AI Routing Gateway

## Overview

Global AI routing gateway that routes requests to the best available AI provider with automatic fallback.

## Stack

**Stack**: Python + FastAPI

## Config

Config location: `~/.hermes/config.yaml`

```yaml
model:
  default: anthropic/claude-sonnet-4
  provider: openrouter
fallback_providers: [ollama]
fallback_model:
  provider: ollama
  model: qwen2.5:7b
  base_url: http://localhost:11434
```

## Development

```bash
cd ~/.hermes/hermes-agent
venv/bin/python cli.py --gateway
```

Health check (when running):
```bash
curl http://localhost:8644/health
```

Note: Hermes is a messaging gateway — health endpoint availability depends on how it's started.

## Key Directories

| Directory | Purpose |
|-----------|---------|
| `agent/` | Core agent logic |
| `gateway/` | Gateway/routing layer |
| `tools/` | Tool implementations (browser, web, voice, etc.) |
| `hermes_cli/` | CLI commands and configuration |

## Key Files

- `cli.py` — Main CLI entry point
- `gateway/run.py` — Gateway server
- `agent/` — Agent implementation
- `tools/` — Tool implementations
