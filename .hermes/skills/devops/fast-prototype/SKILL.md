---
name: fast-prototype
description: "Validate an idea in an isolated throwaway runtime."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [prototype, spike, throwaway, validate, isolated]
    related_skills: [spike, db-sandbox, system-audit]
prerequisites:
  commands: [python3, docker, node]
---

# Fast Prototype: Isolated Runtime Testing

Validate an idea in a throwaway, isolated runtime before writing production code. Goal: answer 'does this approach work?' fast, with zero blast radius.

## When to Use
- 'Can we do X with library Y?' before architecting it.
- Smoke-testing an API contract or a third-party SDK.
- The self-enhancement loop: test a new skill's workflow in isolation first.

## 1. Python One-File Spike

```bash
# Use the project venv; keep it to one file in /tmp
cat > /tmp/spike.py <<'PY'
# minimal repro of the idea
def main():
    print('works')
if __name__ == '__main__':
    main()
PY
python3 /tmp/spike.py && rm -f /tmp/spike.py
```

## 2. Isolated API Prototype (FastAPI in venv)

```bash
~/venv/bin/pip install fastapi uvicorn 2>/dev/null
cat > /tmp/app.py <<'PY'
from fastapi import FastAPI
app = FastAPI()
@app.get('/health')
def h(): return {'ok': True}
PY
~/venv/bin/uvicorn /tmp/app:app --port 9011 &
sleep 2; curl -s http://localhost:9011/health; kill %1; rm -f /tmp/app.py
```

## 3. Container Prototype (Docker)

```bash
CID=$(docker run -d --rm -P node:20-alpine sh -c 'node -e "console.log(1+1)"')  # or your test cmd
docker logs "$CID"; docker stop "$CID" >/dev/null
```

## 4. Validation Checklist
- [ ] Ran end-to-end at least once (no 'should work' claims).
- [ ] Isolated: no writes to project dirs, no real credentials, `--rm` containers.
- [ ] Teardown confirmed (process killed, temp file removed).

## Pitfalls
- Prototypes are throwaway — never let a spike file migrate into `~/dev` or a repo unmodified.
- Don't install prototype deps into the system Python; use the venv or a temp venv.
- Confirm the process is actually killed; a stray background uvicorn will hold the port.
