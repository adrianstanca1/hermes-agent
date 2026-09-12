---
name: system-audit
description: "Check VPS health: CPU, RAM, disk, services, models."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [audit, health, resources, monitoring, system]
    related_skills: [fast-prototype, self-enhance]
prerequisites:
  commands: [free, df, top, systemctl, ollama]
---

# System Audit: Hardware & Resource Health

Produce a verified health snapshot of the VPS before claiming anything about system state. Never report intent or assumption — only tool-backed fact.

## When to Use
- A task touches performance, stability, or capacity (RAM, disk, CPU).
- Before starting long-running jobs, builds, or model loads.
- Proactively at session start on the autonomous core (no-assumption policy).

## 1. Resource Snapshot (run together, independent)

```bash
# Memory
echo '== MEM =='; free -h; echo '== SWAP/ZRAM =='; swapon --show 2>/dev/null || cat /proc/swaps
# Disk
echo '== DISK =='; df -h / /home 2>/dev/null
# Load / CPUs
echo '== LOAD =='; uptime; nproc
# Top processes by RAM
echo '== TOP MEM =='; ps -eo pid,ppid,comm,%mem,%cpu --sort=-%mem | head -8
```

## 2. Service & Daemon Health

```bash
# Ollama (LLM backend)
echo '== OLLAMA =='; curl -s http://localhost:11434/api/tags || echo 'ollama not responding'
# Docker (if used)
echo '== DOCKER =='; docker info --format '{{.ServerVersion}}' 2>/dev/null || echo 'docker not ready'
# agentos local API (this host)
echo '== AGENTOS =='; curl -s http://localhost:9000/health 2>/dev/null || echo 'agentos not running'
```

## 3. Model Availability (Hybrid-Elite routing table)

Verify the local models the autonomous core expects actually load:

```bash
ollama list
# Smoke-test a quick inference to confirm the backend is live
ollama run llama3.1:8b 'reply with the single word: ok' 2>/dev/null | tail -1
```

Expected local models: `gemma2:27b` (L2 strategic), `llama3.1:8b` (L1 fast), `hermes3:latest`.

## 4. Report Format

Always return a structured report:
```
<check>
  MEM:   used/total (avail)
  DISK:  used/total (pct)
  LOAD:  uptime load avg
  OLLAMA: models present + smoke test result
  DOCKER: version or 'not ready'
</check>
```

## Pitfalls
- ZRAM shows under `swapon --show` not as a disk device — don't report 'no swap'.
- `curl` to localhost services returns empty if the service is down; treat empty as 'not running', never as success.
- The VPS is CPU-only (no GPU). Ollama runs with `OLLAMA_NUM_PARALLEL=1`, `OLLAMA_MAX_LOADED_MODELS=1` — loading two big models at once will OOM. Audit before loading.
