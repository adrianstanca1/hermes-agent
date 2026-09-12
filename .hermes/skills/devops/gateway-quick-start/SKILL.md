---
name: gateway-quick-start
description: Install and verify the Hermes gateway in 5 minutes.
version: 1.0.0
author: Administrator, Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [gateway, setup, telegram, install]
    related_skills: [hermes-agent]
---

# Gateway Quick Start

Use this when you need to bring a new Hermes gateway online fast.

## Prerequisites
- Linux host with systemd (or run `hermes gateway run` in a session)
- Telegram bot token (from @BotFather) and allowed user ID
- Network egress to https://api.telegram.org and OpenRouter/Ollama endpoints

## 1. Install & enroll the gateway

```bash
hermes gateway install      # creates hermes-gateway.service
hermes gateway setup        # enroll Telegram bot token interactively
```

## 2. Configure the model router

```bash
hermes config set model.default openrouter/free
hermes config set model.provider openrouter
hermes config set model.aliases.l1 llama3.1:8b
hermes config set model.aliases.l2 gemma2:27b
```

Local Ollama fallback:
```bash
hermes config set model.aliases.l1 ollama/llama3.1:8b
hermes config set model.provider ollama
```

## 3. Enable toolsets & plugins

```bash
hermes tools enable web browser terminal file code_execution vision stt tts
hermes plugins enable browser-browser-use disk-cleanup chronos google_meet
```

## 4. Restart the gateway

```bash
hermes gateway restart
```

## 5. Verify

```bash
hermes gateway status        # systemd unit active
hermes telegram verify        # Telegram API reachable; bot responds
hermes chat -q               # one-shot query through the gateway
hermes ollama list           # local models loaded
```

If `hermes gateway status` shows `mixed sys.modules`, always restart after any `hermes update` so the daemon picks up the latest code:

```bash
hermes gateway restart
```

## Common fixes

| Symptom | Fix |
|---|---|
| "X11 is not reachable" in `hermes computer-use doctor` | Pure TTY session — no display server. Use SSH X11 forwarding or run under a graphical session. |
| Telegram bot not delivering | Confirm token in `~/.hermes/.env`, allowed user ID matches your chat, and bot was added to a group/channel with posting rights. |
| OpenRouter free-tier errors | Verify `OPENROUTER_API_KEY` in `.env`; some free endpoints rate-limit. |
