---
name: hybrid-orchestrator
description: "Route local/cloud. Batch 5-parallel delegation."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [orchestration, delegation, routing, hybrid, performance]
    related_skills: [context-switch, model-router, agent-swarm, self-enhance]
prerequisites:
  commands: [hermes, ollama, tmux]
---

# Hybrid Orchestrator: Local + Cloud Routing + True 5-Parallel Delegation

## Architecture

```
User Request → Orchestrator (this agent)
    │
    ├─► L1 Fast (local llama3.1:8b)  → formatting, extraction, classification
    ├─► L2 Strategic (local gemma2:27b) → planning, architecture, multi-step reasoning
    ├─► L3 Expert (cloud Nemotron free) → ambiguous, external API, nuanced judgment
    ├─► L4 Omniscient (cloud router/free) → deep analysis, last-resort hard reasoning
    └─► Delegate Pool (openrouter/free) → parallel subagents for batch work
```

## Routing Decision Logic

```python
# Pseudo-code for the orchestrator
def route_task(task: str, complexity: str, requires_external: bool) -> dict:
    if complexity == "mechanical" and not requires_external:
        return {"tier": "L1", "model": "l1", "provider": "ollama", "local": True}
    elif complexity in ["planning", "architecture", "reasoning"] and not requires_external:
        return {"tier": "L2", "model": "l2", "provider": "ollama", "local": True}
    elif requires_external or complexity == "ambiguous":
        return {"tier": "L3", "model": "l3", "provider": "openrouter", "local": False}
    else:
        return {"tier": "L4", "model": "l4", "provider": "openrouter", "local": False}
```

## True 5+ Parallel Delegation

**Hermes has no hard 4-child ceiling.** The effective cap is `delegation.max_concurrent_children`. Multiple `delegate_task` calls in one assistant turn can be truncated, and reasoning models may self-limit batches even when the configured cap is higher.

**Solution**: Put all independent tasks in one `delegate_task(tasks=[...])` call. Use `execute_code` only to construct the task list deterministically; it is not bypassing a runtime cap. For workloads above the configured cap, use independent tmux sessions.

```python
from hermes_tools import delegate_task

tasks = [
    {"goal": "Task 1", "context": "..."},
    {"goal": "Task 2", "context": "..."},
    {"goal": "Task 3", "context": "..."},
    {"goal": "Task 4", "context": "..."},
    {"goal": "Task 5", "context": "..."},
]

# One call with the full array; Hermes enforces the configured cap. The model may still self-limit.
results = delegate_task(tasks=tasks)
```

**For >5 parallel**: Use tmux spawning (each gets full tool access, independent process).

```bash
# Spawn 8 parallel Hermes agents via tmux
tmux new-session -d -s agent1 'hermes chat -q "Task 1"'
tmux new-session -d -s agent2 'hermes chat -q "Task 2"'
# ... up to agent8
```

## Performance Tuning (Verified Config)

```yaml
# ~/.hermes/config.yaml (already set)
model:
  default: openrouter/free
  provider: openrouter
  aliases:
    l1: llama3.1:8b          # local, fast
    l2: gemma2:27b           # local, strategic
    l3: openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free
    l4: openrouter/free      # cloud router
    code-free: openrouter/cohere/north-mini-code:free
    reasoning-free: openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free
    gemma-free: openrouter/google/gemma-4-26b-a4b-it:free
    auto-free: openrouter/free

fallback_providers:
  provider: openrouter
  model: nvidia/nemotron-3-ultra-550b-a55b:free

fallback_model:
  provider: openrouter
  model: anthropic/claude-sonnet-4

delegation:
  model: openrouter/free
  provider: openrouter
  max_concurrent_children: 5
  max_spawn_depth: 1
  orchestrator_enabled: true

# CPU-only Ollama
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_GPU_LAYERS=0
```

## Orchestrator Prompt Template

```markdown
# ORCHESTRATOR: You are the hybrid task router.
# Analyze the user request for:
# 1. COMPLEXITY: mechanical | planning | reasoning | deep-analysis
# 2. EXTERNAL_DEPS: true/false (needs web search, API calls, file I/O beyond local)
# 3. PARALLELIZABLE: true/false (can be split into independent subtasks)
# 4. BATCH_SIZE: if parallelizable, how many subtasks (1-10)

# ROUTE:
# - mechanical + !external → L1 local (l1)
# - planning/reasoning + !external → L2 local (l2)
# - external OR ambiguous → L3 cloud (l3)
# - deep-analysis → L4 cloud (l4)
# - batch > 1 → delegate_task with batch_size tasks (use execute_code for >4)

# OUTPUT FORMAT:
# ```json
# {
#   "route": "L1|L2|L3|L4|BATCH",
#   "model": "alias",
#   "tasks": [{"goal": "...", "context": "..."}, ...]  # if BATCH
# }
# ```
```

## Usage

```bash
# Quick route check
hermes chat -q "Classify: 'summarize this file' → mechanical, local"

# Batch delegation (5 parallel)
python -c "
from hermes_tools import delegate_task
tasks = [{'goal': f'Analyze log {i}', 'context': '...'} for i in range(5)]
delegate_task(tasks=tasks)
"
```

## Verification Checklist

- [ ] `hermes config get delegation.max_concurrent_children` → 5
- [ ] `hermes config get model.aliases.l1` → llama3.1:8b
- [ ] `hermes config get model.aliases.l2` → gemma2:27b
- [ ] `OLLAMA_NUM_PARALLEL=1` and `OLLAMA_MAX_LOADED_MODELS=1` in env
- [ ] `delegate_task` batch of 5 executes without truncation (check logs)
- [ ] Local models respond via `ollama run <model> 'test'`
- [ ] Cloud models respond via `hermes chat -m l3 -q 'test'`

## Memory Note

This skill captures the routing logic and batching pattern. Apply with:
- `skill_view(hybrid-orchestrator)` in future sessions
- Memory entry: "Hybrid-Elite routing: L1/L2 local (Ollama), L3/L4 cloud (OpenRouter free). Delegate batching via execute_code for true 5+ parallel."
