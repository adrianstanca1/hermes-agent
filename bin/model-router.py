#!/usr/bin/env python3
"""
model-router.py - Unified local + cloud LLM access for the autonomous VPS.

Backends (Hybrid-Elite tiers from autonomous_core.md):
  L1 fast      -> Ollama llama3.1:8b        (local, default for utility)
  L2 strategic -> Ollama gemma2:27b         (local, default for reasoning)
  L3 expert    -> OpenRouter / Anthropic    (cloud)
  L4 omniscient-> OpenRouter big models     (cloud)

Reads API keys from ~/.env (OPENROUTER_API_KEY, ANTHROPIC_API_KEY).
Stdlib only - no pip dependencies.

Usage:
  model-router.py --tier L1 --prompt "hello"
  model-router.py --model openrouter:anthropic/claude-3.5-sonnet --prompt "..."
  model-router.py --backend ollama --model gemma2:27b --prompt "..."
  echo "text" | model-router.py --tier L2
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error

ENV_PATH = os.path.expanduser("~/.env")
OLLAMA_URL = "http://localhost:11434/api/generate"

# Default model per local tier
TIER_LOCAL = {
    "L1": "llama3.1:8b",
    "L2": "gemma2:27b",
}
# Default cloud model per tier (OpenRouter slugs - keep current; retired models
# like claude-3.5-sonnet / llama-3.1-405b no longer have endpoints).
TIER_CLOUD = {
    "L3": "openrouter:anthropic/claude-opus-4.7",
    "L4": "openrouter:anthropic/claude-opus-5",
}
# Cheap/free fallback if the default cloud model is unavailable
TIER_CLOUD_FALLBACK = {
    "L3": "openrouter:google/gemini-3.5-flash",
    "L4": "openrouter:deepseek/deepseek-v4-pro",
}


def load_env():
    """Load KEY=VALUE pairs from ~/.env without leaking into process env unnecessarily."""
    env = {}
    try:
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return env


def call_ollama(model, prompt, temperature=0.7):
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature},
    }).encode()
    req = urllib.request.Request(OLLAMA_URL, data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.loads(r.read().decode())
    return data.get("response", "").strip()


def call_openrouter(model_slug, prompt, api_key, temperature=0.7):
    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = json.dumps({
        "model": model_slug,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
    }).encode()
    req = urllib.request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://localhost/agentos",
        "X-Title": "agentos",
    })
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read().decode())
    return data["choices"][0]["message"]["content"].strip()


def call_anthropic(model, prompt, api_key, temperature=0.7):
    url = "https://api.anthropic.com/v1/messages"
    payload = json.dumps({
        "model": model,
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
    }).encode()
    req = urllib.request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    })
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read().decode())
    return "".join(b.get("text", "") for b in data.get("content", [])).strip()


def resolve(backend_model):
    """Map a --model value like 'openrouter:slug' or 'anthropic:claude-...' to (backend, model)."""
    if ":" in backend_model:
        backend, model = backend_model.split(":", 1)
        return backend.lower(), model
    return "ollama", backend_model


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", default=None)
    ap.add_argument("--tier", default=None, choices=["L1", "L2", "L3", "L4"])
    ap.add_argument("--model", default=None, help="e.g. gemma2:27b, openrouter:slug, anthropic:model")
    ap.add_argument("--backend", default=None)
    ap.add_argument("--temperature", type=float, default=0.7)
    args = ap.parse_args()

    prompt = args.prompt or sys.stdin.read().strip()
    if not prompt:
        print("error: no prompt provided (--prompt or stdin)", file=sys.stderr)
        sys.exit(2)

    env = load_env()

    # Determine target
    if args.tier:
        if args.tier in TIER_LOCAL:
            backend, model = "ollama", TIER_LOCAL[args.tier]
        else:
            backend, model = resolve(TIER_CLOUD[args.tier])
    elif args.model:
        backend, model = resolve(args.model)
        # --backend overrides the backend half of a bare --model (e.g. "claude-...")
        if args.backend and backend == "ollama":
            backend = args.backend.lower()
    elif args.backend:
        backend = args.backend.lower()
        model = {"ollama": "llama3.1:8b", "openrouter": "anthropic/claude-opus-4.7",
                 "anthropic": "claude-3-5-sonnet-latest"}.get(backend, args.model or "llama3.1:8b")
    else:
        backend, model = "ollama", TIER_LOCAL["L1"]

    try:
        if backend == "ollama":
            out = call_ollama(model, prompt, args.temperature)
        elif backend == "openrouter":
            key = env.get("OPENROUTER_API_KEY")
            if not key:
                print("error: OPENROUTER_API_KEY not set in ~/.env", file=sys.stderr); sys.exit(3)
            try:
                out = call_openrouter(model, prompt, key, args.temperature)
            except urllib.error.HTTPError as e:
                # Retired/unavailable default -> try the tier fallback once
                fb = TIER_CLOUD_FALLBACK.get(args.tier)
                if fb and resolve(fb)[1] != model:
                    print(f"warn: default cloud model unavailable ({e.code}); trying fallback {fb}",
                          file=sys.stderr)
                    out = call_openrouter(resolve(fb)[1], prompt, key, args.temperature)
                else:
                    raise
        elif backend == "anthropic":
            key = env.get("ANTHROPIC_API_KEY")
            if not key:
                print("error: ANTHROPIC_API_KEY not set in ~/.env", file=sys.stderr); sys.exit(3)
            out = call_anthropic(model, prompt, key, args.temperature)
        else:
            print(f"error: unknown backend {backend}", file=sys.stderr); sys.exit(2)
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:500]
        print(f"error: HTTP {e.code} from {backend}: {body}", file=sys.stderr); sys.exit(4)
    except urllib.error.URLError as e:
        print(f"error: cannot reach {backend}: {e.reason}", file=sys.stderr); sys.exit(5)

    print(out)


if __name__ == "__main__":
    main()
