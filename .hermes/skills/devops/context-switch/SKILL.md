---
name: context-switch
description: "Route tasks to the right LLM tier or profile."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [routing, model-selection, context, hybrid-llm]
    related_skills: [self-enhance, system-audit]
prerequisites:
  commands: [ollama]
---

# Context Switch: Hybrid-Elite Model Routing

Route each task to the cheapest model that can do it well, per the autonomous core's Hybrid Intelligence tiers. Spend tokens where they pay off; stay local where they don't.

## Routing Table (from autonomous_core.md)

| Tier | Model | Role | Use for |
|------|-------|------|----------|
| L1 Fast | `llama3.1:8b` (local) | Utility/formatting | Summaries, extraction, formatting, classification, short rewrites |
| L2 Strategic | `gemma2:27b` (local) | Reasoning/architecture | Planning, design decisions, multi-step reasoning, code architecture |
| L3 Expert | Claude 3.5 Sonnet (OpenRouter) | Cloud expert | Nuanced judgment, ambiguous requirements, external API design |
| L4 Omniscient | Llama 3.1 405B / GPT-4o (OpenRouter) | Cloud heavy | Last-resort hard reasoning, deep analysis |

## Decision Heuristic

1. Is it mechanical (format, extract, classify, short)? -> L1 local.
2. Does it need reasoning/planning but stays on known ground? -> L2 local.
3. Is it ambiguous, requires external-tool judgment, or risks being wrong locally? -> L3 cloud.
4. Only escalate to L4 for genuinely hard reasoning the local 27B can't crack.

## Calling a Local Model (Ollama)

```bash
# L1 fast
ollama run llama3.1:8b "Summarize in one line: $TEXT"
# L2 strategic
ollama run gemma2:27b 'Design a module layout for a FastAPI app with auth and jobs.'
```

## Switching the Active Hermes Profile

Profiles live under `~/.hermes/profiles/<name>/` with their own skills/plugins/cron/memories. To switch:
- Identify the profile name from `ls ~/.hermes/profiles/`.
- Set `HERMES_PROFILE=<name>` before launching Hermes. This session's profile is `default`.

## Pitfalls
- Local is CPU-only: keep parallelism at 1 (`OLLAMA_NUM_PARALLEL=1`, `OLLAMA_MAX_LOADED_MODELS=1`). Don't route two big models concurrently.
- Cloud tiers need OpenRouter credentials — if absent, degrade gracefully to L2 local and say so.
- Don't burn L4 on tasks L1/L2 handle; the point of the table is cost discipline.
