---
name: ollama-performance-tuning
description: Optimize Ollama for CPU-only inference on a 31GB RAM system.
version: 0.1.0
author: Ben Barclay (benbarclay), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ollama, performance, cpu, tuning]
    related_skills: [gateway-optimization-plan]
---

# Ollama Performance Tuning

## When to Use
- Users with CPU-only systems needing to optimize Ollama performance.
- Systems with 31GB RAM or less that need to run large models efficiently.

## Prerequisites
- Ollama installed and running
- 31GB RAM or less available
- CPU-only system (no GPU support)

## How to Run
1. Configure environment variables in `~/.hermes/.env`.
2. Restart Ollama to apply optimizations.
3. Verify performance with model loading.

## Quick Reference
```bash
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_GPU_LAYERS=0
```

## Procedure
1. **Set Environment Variables**: Add the following to `~/.hermes/.env`:
   ```
   OLLAMA_NUM_PARALLEL=1
   OLLAMA_MAX_LOADED_MODELS=1
   OLLAMA_GPU_LAYERS=0
   ```
2. **Apply Settings**: Restart Ollama or reload the service.
3. **Verify**: Check model loading with `ollama ps`.

## Pitfalls
- Ensure `OMP_NUM_THREADS` is set appropriately for your CPU.
- Monitor system resources during model loading.
- Large models may still cause memory issues on 31GB systems.

## Verification
1. Check `~/.hermes/.env` for optimization settings.
2. Verify Ollama is running with `ollama ps`.
3. Load a model and monitor memory usage.
