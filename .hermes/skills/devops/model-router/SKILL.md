---
name: model-router
description: Unified LLM routing across local and cloud backends.
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [routing, model, ollama, openrouter, anthropic]
    related_skills: [context-switch, self-enhance, hermes-agent]
prerequisites:
  commands: [python3, curl]
---

# Model Router: Unified LLM Routing

Provides a complete routing configuration for Hermes Agent using the Hybrid-Elite L1–L4 tier model from the autonomous core, with free OpenRouter models as cloud tiers and local Ollama models as local tiers.

## Routing Table (Hybrid-Elite Tiers)

| Tier | Alias | Model | Provider | Use For |
|------|-------|-------|----------|----------|
| L1 Fast | `l1` | `llama3.1:8b` | ollama | Summaries, extraction, formatting, classification, short rewrites |
| L2 Strategic | `l2` | `gemma2:27b` | ollama | Planning, design decisions, multi-step reasoning, code architecture |
| L3 Expert | `l3` | `nvidia/nemotron-3-ultra-550b-a55b:free` | openrouter | Nuanced judgment, ambiguous requirements, external API design |
| L4 Omniscient | `l4` | `openrouter/free` (router) | openrouter | Last-resort hard reasoning, deep analysis |

## Specialized Free Model Aliases

| Alias | Model | Provider | Best For |
|-------|-------|----------|----------|
| `code-free` | `cohere/north-mini-code:free` | openrouter | Code generation, refactoring |
| `reasoning-free` | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | openrouter | Complex reasoning, math, logic |
| `gemma-free` | `google/gemma-4-26b-a4b-it:free` | openrouter | General purpose, instruction following |
| `auto-free` | `openrouter/free` | openrouter | Auto-select best free model |

## Configuration (Applied via `hermes config`)

```yaml
model:
  default: anthropic/claude-sonnet-4
  provider: openrouter
  base_url: https://openrouter.ai/api/v1
  aliases:
    l1: ollama/llama3.1:8b
    l2: ollama/gemma2:27b
    l3: openrouter/nvidia/nemotron-3-ultra-550b-a55b:free
    l4: openrouter/free
    code-free: openrouter/cohere/north-mini-code:free
    reasoning-free: openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free
    gemma-free: openrouter/google/gemma-4-26b-a4b-it:free
    auto-free: openrouter/free

fallback_providers:
  provider: openrouter
  model: nvidia/nemotron-3-ultra-550b-a55b:free

# Delegation (subagents) uses free tier
# delegation:
#   model: openrouter/free
#   provider: openrouter
#   base_url: https://openrouter.ai/api/v1
#   max_concurrent_children: 4
```

## Usage

```bash
# Switch model for this session
/model l1          # Local fast (llama3.1:8b)
/model l2          # Local strategic (gemma2:27b)
/model l3          # Free cloud expert (Nemotron 3 Ultra)
/model l4          # Free cloud omniscient (router)
/model code-free   # Free coding model
/model reasoning-free # Free reasoning model

# Use in delegation (subagents)
/delegate "task"   # Uses delegation.model (openrouter/free)
```

## Decision Heuristic (from context-switch)

1. Mechanical (format, extract, classify, short) → L1 local
2. Reasoning/planning on known ground → L2 local
3. Ambiguous, external-tool judgment, risk of local error → L3 cloud (free)
4. Genuinely hard reasoning L2 can't crack → L4 cloud (free router)

## Pitfalls
- Local is CPU-only: `OLLAMA_NUM_PARALLEL=1`, `OLLAMA_MAX_LOADED_MODELS=1`
- Cloud free models have rate limits (20 RPM, 200 RPD on OpenRouter)
- `openrouter/free` router may select any available free model — not deterministic
- Fallback chain: primary → fallback_providers → free router
- Delegation model MUST be free tier to avoid burning credits

