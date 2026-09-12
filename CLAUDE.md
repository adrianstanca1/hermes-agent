# Project Environment: Ultra-Local Autonomous VPS

## Architecture
- **Host**: AMD EPYC Rome (16 CPUs, 31GB RAM)
- **LLM Backend**: Ollama (Local)
- **Primary Model**: `gemma2:27b` (Reasoning/Architecture)
- **Fast Model**: `llama3.1:8b` (Utility/Formatting)
- **Memory**: ZRAM enabled for stability.

## Optimizations
- **Inference**: `OLLAMA_NUM_PARALLEL=1`, `OLLAMA_MAX_LOADED_MODELS=1` (CPU-only tuning).
- **Harness**: `.claude/settings.json` tuned for medium effort and 128k window.
- **Structured Memory**: SQLite MCP (`mcp-knowledge.db`) for persistent project state.
- **Web Access**: Fetch MCP for documentation ingestion.

## Custom Skills
- `/skill db-sandbox`: Isolated DB containers.
- `/skill system-audit`: Hardware/Resource health check.
- `/skill code-cleanup`: Codebase hygiene.
- `/skill context-switch`: Model routing.
- `/skill knowledge-map`: Dependency graphing.
- `/skill fast-prototype`: Isolated runtime testing.

## Autonomous Engine
The agent operates in **Full Autonomous Mode**. It independently expands prompts into technical plans, selects resources, and executes workflows without per-step approval.

## 🚀 Autonomous Core (The Prime Directive)
All operations are governed by `/home/administrator/.claude/autonomous_core.md`. 
- **Strict Evidence**: No simulation. No assumptions.
- **Hybrid-Elite Routing**: L1 (Local Fast) $\rightarrow$ L2 (Local Strategic) $\rightarrow$ L3 (Cloud Expert) $\rightarrow$ L4 (Cloud Omniscient).
- **Recursive Growth**: The system is designed to self-enhance via the `/skill self-enhance` loop.

## 🛠️ Additional Advanced Skills
- `/skill self-enhance`: Triggers the recursive optimization loop to improve system efficiency based on interaction history.
