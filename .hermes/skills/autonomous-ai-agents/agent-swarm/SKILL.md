---
name: agent-swarm
description: Orchestrate multi-agent swarms with Hermes and coding agents
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [swarm, multi-agent, delegation, claude-code, codex, opencode]
    related_skills: [hermes-agent, claude-code, codex, opencode, context-switch, self-enhance]
prerequisites:
  commands: [tmux, claude, codex, opencode]
---

# Agent Swarm: Multi-Agent Orchestration

Run parallel autonomous coding agents (Claude Code, Codex, OpenCode) alongside Hermes delegation for complex multi-faceted tasks.

## When to Use
- Large features requiring backend + frontend + tests + docs
- Batch issue fixing across multiple files
- Parallel PR reviews
- Any task that decomposes into independent workstreams

## Architecture

```
Hermes (orchestrator)
├── delegate_task → Subagents (Hermes-native, free tier)
├── tmux + claude -p  → Claude Code (print mode, one-shot)
├── tmux + codex exec → Codex (one-shot, requires auth)
└── tmux + opencode run → OpenCode (one-shot, requires auth)
```

## Prerequisites

```bash
# Install external agents
npm install -g @anthropic-ai/claude-code @openai/codex opencode-ai

# Authenticate each
claude auth login          # or set ANTHROPIC_API_KEY
codex login --device-auth  # or set OPENAI_API_KEY
opencode auth login        # or set OPENROUTER_API_KEY
```

## Hermes Delegation (Native Subagents)

Uses free OpenRouter model (`delegation.model: openrouter/free`):

```python
from hermes_tools import delegate_task

delegate_task(
    tasks=[
        {"goal": "Fix auth bug in src/auth.py", "context": "..."},
        {"goal": "Write tests for API endpoints", "context": "..."},
        {"goal": "Update README with new endpoints", "context": "..."}
    ]
)
```

## External Agent One-Shots (Print Mode)

### Claude Code
```bash
# One-shot, no PTY needed
claude -p 'Add retry logic to API calls' --allowedTools 'Read,Edit' --max-turns 10

# With JSON output
claude -p 'Analyze security issues' --output-format json --max-turns 5
```

### Codex
```bash
# One-shot (needs git repo)
cd /tmp && git init && codex exec 'Build a snake game in Python' --sandbox workspace-write
```

### OpenCode
```bash
# One-shot (needs git repo)
cd /tmp && git init && opencode run 'Create REST API with auth' --sandbox workspace-write
```

## Parallel Interactive Sessions (Tmux)

```bash
# Start 3 agents in parallel
tmux new-session -d -s agent-backend -x 140 -y 40
tmux send-keys -t agent-backend 'cd ~/project && claude -p "Build auth API" --allowedTools "Read,Write,Bash" --max-turns 15' Enter

tmux new-session -d -s agent-frontend -x 140 -y 40
tmux send-keys -t agent-frontend 'cd ~/project && opencode run "Build React dashboard"' Enter

tmux new-session -d -s agent-tests -x 140 -y 40
tmux send-keys -t agent-tests 'cd ~/project && codex exec "Write integration tests" --sandbox workspace-write' Enter

# Monitor progress
for s in agent-backend agent-frontend agent-tests; do
  echo "=== $s ==="
  tmux capture-pane -t $s -p -S -30
  echo
done
```

## Worktree Isolation Pattern

```bash
# Create isolated worktrees
git worktree add -b feat/auth /tmp/feat-auth main
git worktree add -b feat/ui /tmp/feat-ui main
git worktree add -b feat/tests /tmp/feat-tests main

# Launch agents in each
tmux new-session -d -s auth -x 140 -y 40 && tmux send-keys -t auth 'cd /tmp/feat-auth && claude -p "Implement JWT auth"' Enter
tmux new-session -d -s ui -x 140 -y 40 && tmux send-keys -t ui 'cd /tmp/feat-ui && opencode run "Build login page"' Enter
tmux new-session -d -s tests -x 140 -y 40 && tmux send-keys -t tests 'cd /tmp/feat-tests && codex exec "Write auth tests"' Enter
```

## Routing by Task Type

| Task Type | Best Agent |
|-----------|------------|
| Complex reasoning, architecture | Hermes L2 (gemma2:27b) or L3 (Nemotron) |
| Code implementation, refactoring | Claude Code (best reasoning) |
| Fast coding, batch tasks | Codex (fast, OpenAI) |
| PR review, code review | OpenCode (built-in PR command) |
| Simple utility, formatting | Hermes L1 (llama3.1:8b) |
| Parallel sub-tasks | Hermes delegation (free tier) |

## Verification

```bash
# Check all agents installed
which claude codex opencode

# Check auth
claude auth status
codex auth list
opencode auth list

# Test each
claude -p 'echo OK' --max-turns 1
cd /tmp && git init && codex exec 'echo OK' --sandbox workspace-write
cd /tmp && git init && opencode run 'echo OK'
```

## Pitfalls
- Codex/OpenCode require git repo (use `mktemp -d && git init` for scratch)
- Codex needs OAuth or OPENAI_API_KEY; OpenCode needs OPENROUTER_API_KEY
- Tmux sessions persist — always `tmux kill-session -t <name>` when done
- `--dangerously-skip-permissions` in Claude Code: dialog defaults to NO, must send Down+Enter
- Delegation subagents share context window — keep tasks focused
- Free tier models have rate limits (20 RPM, 200 RPD on OpenRouter)
