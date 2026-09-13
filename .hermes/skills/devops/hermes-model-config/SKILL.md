---
name: hermes-model-config
description: Configure Hermes Agent model router with free aliases.
version: 1.0.0
author: administrator
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, model, router, ollama, openrouter, free]
    related_skills: [model-router, self-enhance, hermes-agent]
prerequisites:
  commands: [hermes, ollama]
---

# Hermes Model Router Configuration

Configure Hermes Agent model router to use free cloud and local models at $0 cost.

## When to Use This Skill
- Initial setup with zero-cost model routing
- Switching between local Ollama and cloud OpenRouter free tiers
- Configuring model aliases for rapid session switching
- Optimizing for $0 per-token cost while maintaining capability

## Configuration Steps

### 1. Set OpenRouter as provider
```bash
hermes config set model.provider openrouter
hermes config set model.default openrouter/free
```

### 2. Configure model aliases
```bash
hermes config set model.aliases '{"l1": "llama3.1:8b", "l2": "gemma2:27b", "l3": "hermes3:latest", "l4": "openrouter/free", "code-free": "openrouter/cohere/north-mini-code:free", "reasoning-free": "openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free", "gemma-free": "openrouter/google/gemma-4-26b-a4b-it:free", "auto-free": "openrouter/free"}'
```

### 3. Verify
```bash
hermes chat -q "Confirmation"
```

**Pitfall**: Local Ollama model IDs need Hermes formatting (`llama3.1:8b` not `ollama/llama3.1:8b`). Verify with `hermes chat -q`.

## Model Alias Map

| Alias | Type | Model | Cost |
|-------|------|-------|------|
| `l1` | Local | `llama3.1:8b` (Ollama) | $0 |
| `l2` | Local | `gemma2:27b` (Ollama) | $0 |
| `l3` | Local | `hermes3:latest` (Ollama) | $0 |
| `l4` | Cloud | `openrouter/free` (router) | $0 |
| `code-free` | Cloud | `openrouter/cohere/north-mini-code:free` | $0 |
| `reasoning-free` | Cloud | `openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | $0 |
| `gemma-free` | Cloud | `openrouter/google/gemma-4-26b-a4b-it:free` | $0 |
| `auto-free` | Cloud | `openrouter/free` (router) | $0 |

## Decision Heuristic

1. Mechanical → `l1` local Llama 3.1 8B
2. Planning → `l2` local Gemma 2 27B
3. Ambiguous judgment → `l4` OpenRouter free router
4. Code → `code-free` Cohere North Mini Code
5. Complex reasoning → `reasoning-free` Nemotron 3 Nano Omni
6. General purpose → `gemma-free` Gemma 4 26B
7. Auto-select → `auto-free` OpenRouter router

## Pitfalls
- Local model ID format: Hermes transforms raw Ollama IDs; CLI format fails HTTP 400
- Cloud rate limits: 20 RPM / 200 RPD on OpenRouter free tier
- Non-deterministic router: `openrouter/free` selects any available free model
- Fallback chain: primary → fallback_providers → free router
- Never hand-edit `config.yaml`; use `hermes config set`
- Secrets in `.env`, settings in `config.yaml` only

## Verified Commands
```bash
hermes config set model.provider openrouter
hermes config set model.default openrouter/free
hermes config set model.aliases '{"l1": "llama3.1:8b", "l2": "gemma2:27b", "l3": "hermes3:latest", "l4": "openrouter/free", "code-free": "openrouter/cohere/north-mini-code:free", "reasoning-free": "openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free", "gemma-free": "openrouter/google/gemma-4-26b-a4b-it:free", "auto-free": "openrouter/free"}'
hermes chat -q "Router configured and working"
```

## Session Results
- OpenRouter free tier confirmed working via `hermes chat -q`
- Local Ollama models installed: llama3.1:8b, gemma2:27b, hermes3:latest
- All configurations saved to `~/.hermes/config.yaml`