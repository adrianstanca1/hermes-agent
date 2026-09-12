# Hermes Agent — Verified State & Known Limitations

## Environment
- **Host**: AMD EPYC Rome, 16 CPUs, 31 GB RAM, no GPU
- **OS**: Ubuntu 26.04.1 LTS (x86_64)
- **User**: `administrator` (UID 1000)
- **Hermes**: v0.21.2 (code_sha `d595e636c83aa0b9606d4e914e1140ae9c796897`)
- **Model router**: OpenRouter free + local Ollama (l1–l4, code-free, reasoning-free, gemma-free, auto-free)
- **Gateway**: `hermes-gateway.service` (PID 76175, running since 2026-09-12 22:50:25 UTC)
- **Telegram**: bot token `8692191625:***`, allowed user `5900448653`, message 1500 delivered
- **Ollama**: CPU-only (`OLLAMA_NUM_PARALLEL=1`, `OLLAMA_MAX_LOADED_MODELS=1`, `OLLAMA_GPU_LAYERS=0`)

## Verified Working ✅
- **Gateway + Telegram**: polling mode, `telegram.state=connected`, `getUpdates ok: True`
- **Model router**: 8 aliases, OpenRouter free tier + local Ollama (hermes3:8B, llama3.1:8b, gemma2:27b)
- **Toolsets enabled**: web, browser, terminal, file, code_execution, vision, stt, tts, computer_use, skills, todo, kanban, memory, context_engine, session_search, connections, clarify, delegation, cronjob, image_gen, video_gen
- **Plugins enabled**: browser-browser-use, browser-browserbase, chronos, google_meet, disk-cleanup
- **Skills**: gateway-optimization-plan, gateway-quick-start, ollama-performance-tuning, self-enhance, hermes-agent-skill-authoring, github, computer-use, hermes-model-config, model-router
- **Git**: remote `https://github.com/adrianstanca1/hermes-agent.git`, commits `d8ce299`, `31a900f`, `af62c4c`

## Computer Use — Headless Xvfb Workaround ✅
- **Xvfb service**: `xvfb.service` (systemd user unit, PID 73743, `:99`, 1920×1080, auto-restart on failure)
- **Gateway env override**: `hermes-gateway.service.d/override.conf` injects `DISPLAY=:99`, `XDG_SESSION_TYPE=x11`, `XWAYLAND_DISPLAY=`
- **Doctor**: `ax_capability` ✅, `screen_capture_capability` ✅
- **Capture verified**: `computer_use_29908d3b416f4de28ba49fa46147ede0.png` (484×316, XTerm on `:99`)
- **Limitation**: headless Xvfb is for CI/automation only (per Cua docs). Full desktop requires SSH X11 forwarding or a graphical session.

## Remaining Blockers ⚠️
- **Disabled toolsets**: `x_search` (needs `X_SEARCH_API_KEY`), `homeassistant` (needs `HOMEASSISTANT_TOKEN`), `spotify` (needs `SPOTIFY_CLIENT_ID` + `SPOTIFY_CLIENT_SECRET`), `yuanbao` (needs `YUANBAO_API_KEY`)
- **Firecrawl**: enabled but needs `FIRECRAWL_API_KEY` (paid feature)
- **Computer Use**: headless Xvfb only — no real desktop UI; `startx`/SSH X11 forwarding needed for real desktop apps
- **Model routing**: `meta-llama/llama3.1:8b` returns HTTP 400 from OpenRouter; `l1` alias fails. Use `l2` (gemma2:27b) or `l4` (openrouter/free) instead.
- **Git**: remote `https://github.com/adrianstanca1/hermes-agent.git` confirmed working (pushed `af62c4c`)

## Key Decisions
- **Remote URL**: changed from `Administrator/hermes-agent-config.git` (404) to `adrianstanca1/hermes-agent.git` (verified accessible via `gh repo list`)
- **Ollama CPU-only tuning**: `PARALLEL=1`, `MAX_LOADED_MODELS=1` since no GPU available
- **Computer Use workaround**: persistent `xvfb.service` + gateway env override (systemd drop-in) — not SSH X11 forwarding (not applicable to headless VPS)
- **Telegram access**: allowlisted user `5900448653` only (not public open-all)

## Commands to Re-verify
```bash
systemctl --user status xvfb.service
systemctl --user status hermes-gateway.service
DISPLAY=:99 hermes computer-use doctor
hermes tools list
hermes plugins list
git log --oneline -3
```