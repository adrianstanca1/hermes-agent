---
name: gateway-optimization-plan
description: Plan to optimize Hermes gateway using parallel agents, skills, and tools.
version: 1.0.0
author: Administrator, Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [gateway, optimization, swarm, agents]
    related_skills: [hermes-model-config, model-router, self-enhance, hermes-agent]
---

# Gateway Optimization Plan

Multi-agent execution plan to enhance Hermes Agent performance, capabilities, and reliability.

## Prerequisites

- Hermes gateway running (PID 59960)
- Telegram platform connected (verified message_id 1417)
- 3 local Ollama models active
- Agent Swarm skill loaded for parallel execution

## Parallel Agent Workstreams

The plan decomposes into 4 independent workstreams, each assigned to a subagent via `delegate_task`.

### Workstream 1: Computer Use Accessibility Fix (L1 — Hermes L2 gemma2:27b)

**Goal**: Resolve X11/Wayland limitation preventing desktop GUI automation.

**Task**:
```
Research and implement a fix for the "ax_capability: X11 is not reachable" error reported by `hermes computer-use doctor`.
Check if running under Wayland (XDG_SESSION_TYPE=x11 fallback or XWayland bridge).
If Wayland: install and configure XWayland to allow cua-driver AX tree inspection.
Verify: Run `hermes computer-use doctor` and confirm ✅ for ax_capability and screen_capture_capability.
```

**Skills involved**: computer-use, system-audit
**Tools**: terminal (X11 diagnostics, package install), read_file (config inspection)
**Verification**: `hermes computer-use doctor` shows both checks passing.

### Workstream 2: Disabled Toolset Activation (L2 — Hermes L3 Nemotron free)

**Goal**: Activate all disabled toolsets requiring API credentials.

**Task**:
```
Audit all disabled toolsets from `hermes tools list` output:
- x_search (🐦 X/Twitter Search): needs X_SEARCH_API_KEY or X OAuth
- homeassistant (🏠 Home Assistant): needs HOMEASSISTANT_TOKEN or HA URL
- spotify (🎵 Spotify): needs SPOTIFY_CLIENT_ID + SPOTIFY_CLIENT_SECRET
- yuanbao (🤖 Yuanbao): needs YUANBAO_API_KEY

For each, check if credentials exist in ~/.hermes/.env or ~/.hermes/auth.json.
If credentials are present, enable the toolset: hermes tools enable <name>
If credentials are missing, research what credential types are needed and document them as a memory entry.
Report: which toolsets were activated, which need credentials, and where to find them.
```

**Skills involved**: hermes-agent (config tools), model-router (provider setup)
**Tools**: hermes config set, hermes tools enable, read_file (.env inspection)
**Verification**: `hermes tools list` shows all previously disabled toolsets now enabled or documented.

### Workstream 3: Plugin Ecosystem Enhancement (L3 — Hermes L3 Nemotron free)

**Goal**: Enable available browser plugins and image generation plugins that don't require paid API keys.

**Task**:
```
From `hermes plugins list`, identify all bundled plugins currently "not enabled".
Categorize them by requirement:
1. Free tier / no API key needed → enable via `hermes plugins enable <name>`
2. Requires API key (free tier available) → document credential requirement, then enable if key present
3. Requires paid tier → skip, document in memory

Specifically try enabling (check if they work without external keys):
- browser-firecrawl (if FIRECRAWL_API_KEY present or free tier)
- chronos (dashboard analytics)
- disk-cleanup (system maintenance)
- google_meet (Google Meet integration)

After enabling, run `hermes plugins list` and verify status changed to "enabled".
Report: list of newly enabled plugins and any with unsatisfied dependencies.
```

**Skills involved**: hermes-agent, self-enhance (for pattern capture)
**Tools**: hermes plugins enable, hermes plugins list, read_file
**Verification**: `hermes plugins list` shows increased "enabled" count.

### Workstream 4: Skills Authoring & Self-Enhancement (L2 — Hermes L2 gemma2:27b)

**Goal**: Create reusable skills capturing current optimizations and lessons learned, then commit to repo.

**Task**:
```
Create two skills using skill_manage (action='create'):

1. Skill: "gateway-quick-start"
   Category: devops
   Description: "Install and configure Hermes gateway with Telegram in under 5 minutes."
   Content: Steps from today's work — service install, Telegram bot token setup, allowed_users config, restart pattern.

2. Skill: "ollama-performance-tuning"
   Category: devops
   Description: "Optimize Ollama for CPU-only inference on a 31GB RAM system."
   Content: OLLAMA_NUM_PARALLEL=1, OLLAMA_MAX_LOADED_MODELS=1, OLLAMA_GPU_LAYERS=0, compression settings.

After creating, verify both load with `skills_list`.
Then commit changes to git repo with descriptive message.
```

**Skills involved**: self-enhance, hermes-agent-skill-authoring, hermes-model-config
**Tools**: skill_manage, skills_list, terminal (git)
**Verification**: Both skills appear in `skills_list`; git commit created.

## Execution Commands

### Main orchestration (run this first):

```python
from hermes_tools import delegate_task

results = delegate_task(
    tasks=[
        {
            "goal": "Fix X11/Wayland computer-use limitation",
            "context": "Run hermes computer-use doctor. Fix ax_capability and screen_capture_capability errors. Target: both show ✅. Use XWayland if on Wayland."
        },
        {
            "goal": "Activate disabled toolsets (x_search, homeassistant, spotify, yuanbao)",
            "context": "Check ~/.hermes/.env for credentials. Enable toolsets that have keys. Document those needing credentials."
        },
        {
            "goal": "Enable available browser and system plugins",
            "context": "From hermes plugins list, enable free/bundled plugins (firecrawl if free, disk-cleanup, google_meet, chronos). Skip paid-only ones."
        },
        {
            "goal": "Create 2 reusable skills and commit to repo",
            "context": "Create gateway-quick-start and ollama-performance-tuning skills via skill_manage. Verify with skills_list. Commit to git."
        }
    ]
)
```

### Sequencing note:
- Workstream 1 (Computer Use) and Workstream 4 (Skills) are fully independent — can run simultaneously.
- Workstream 2 (Toolsets) and Workstream 3 (Plugins) share .env inspection — run after W1/W4 or in parallel with careful env reading.

## Expected Outcomes

| Workstream | Current | Target |
|-----------|---------|--------|
| Computer Use | X11 degraded | Full AX tree + screen capture functional |
| Disabled Toolsets | 4 disabled | 0-2 disabled (cred-dependent) |
| Plugins | 2 enabled | 5+ enabled |
| Skills | 0 new | 2 new skills created + committed |

## Dependencies & Risks

- **Computer Use fix**: Depends on system packages (xwayland, x11-apps). May require user approval for apt install.
- **Toolset activation**: Blocked if API keys are not available — will document requirements instead.
- **Plugin enablement**: Some may require API keys (FIRECRAWL_API_KEY, etc.) — gracefully skip if absent.
- **Skill creation**: Low risk; uses established authoring format.
- **Rate limits**: OpenRouter free tier (20 RPM, 200 RPD) — L3 agents use this, keep task scope focused.

## Post-Execution Verification

Run after all subagents complete:
1. `hermes computer-use doctor` — confirm no ❌ items
2. `hermes tools list` — confirm disabled count reduced
3. `hermes plugins list` — confirm enabled count increased
4. `skills_list` — confirm 2 new skills present
5. `git log --oneline` — confirm new commits
6. `hermes gateway status` — confirm gateway still running, Telegram still connected
