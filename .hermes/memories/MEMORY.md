Hermes Agent: 8 aliases (OpenRouter free + local Ollama). Config at ~/.hermes/config.yaml. Verified via hermes chat -q.
§
VPS: AMD EPYC 16-core, 31GB RAM, no GPU, Ubuntu 26.04.1. Ollama CPU-only: PARALLEL=1, MAX_LOADED_MODELS=1. Rules: verify live; no simulated results; no PR/issue IDs; no date stamps.
§
Gateway active (DISPLAY=:99, Telegram 5900448653), computer_use OK (Xvfb :99). 63 skills, CLAUDE.md, remote adrianstanca1/hermes-agent.git. Blockers: 4 toolsets need API keys, firecrawl needs FIRECRAWL_API_KEY, l1 alias fails (use l2/l4).
§
Hybrid orchestrator skill created (2026-09-13): Local L1/L2 (llama3.1:8b, gemma2:27b) for mechanical/planning; Cloud L3/L4 (Nemotron free, router/free) for ambiguous/deep. True 5-parallel delegation via execute_code batching (native delegate_task caps at 4). Config: max_concurrent_children=5, orchestrator_enabled=true, OLLAMA_NUM_PARALLEL=1, MAX_LOADED_MODELS=1.
§
Final state 2026-09-13: All swarm artifacts created (5/5), hybrid-orchestrator skill saved, 3 plugins enabled (disk-cleanup, basic, web-brave-free), tmux 5-parallel verified, memory consolidated to 63%. Gateway PID 87316 active. Config: 8 model aliases, delegation.max_concurrent_children=5, orchestrator_enabled=true. Disabled: x_search, homeassistant, spotify, yuanbao (need API keys). Credentials: OPENROUTER_API_KEY, HF_TOKEN, BRAVE_SEARCH_API_KEY present. Ready for session close.
§
Resources: 31GB RAM (28GB avail), 16 cores, load 0.54-0.65, disk 7%, 775G. Ollama: 3 models loaded (llama3.1:8b, gemma2:27b, hermes3). OpenRouter free tier (20 RPM/200 RPD). Plugins: disk-cleanup, basic, web-brave-free enabled; 10+ disabled (no keys). Skills: 68 active, hybrid-orchestrator added. Memory: 63% (1399/2200 chars) — consolidated.
§
User asked for Google Docs MCP connection (2026-09-13 session). None exists in environment (no plugin, no MCP server, no G_DOCS_TOKEN). Clarified: not a missing capability but an undefined endpoint. User tends to give 1-word/fragment directives; when ambiguous, ask immediately before inventing connections.