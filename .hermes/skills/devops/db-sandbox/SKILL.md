---
name: db-sandbox
description: "Run isolated DB experiments without touching real data."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [database, sandbox, postgres, sqlite, docker, isolation]
    related_skills: [fast-prototype, system-audit]
prerequisites:
  commands: [docker, sqlite3]
---

# DB Sandbox: Isolated Database Containers

Run database experiments in disposable, isolated environments so nothing touches real data. Tear down after.

## When to Use
- Testing schema migrations, queries, or ORM behavior.
- Any 'try this against a DB' task where the data must not be production.
- Reproducing a bug that needs a clean DB state.

## 1. SQLite (zero-dependency, fastest)

For most experiments, a temp SQLite file is enough and needs no container:

```bash
DB=$(mktemp -d)/sandbox.db
sqlite3 "$DB" 'CREATE TABLE t(id INTEGER PRIMARY KEY, v TEXT); INSERT INTO t(v) VALUES ("hello");'
sqlite3 "$DB" 'SELECT * FROM t;'
# cleanup
rm -f "$DB"
```

## 2. Postgres (Docker, isolated, ephemeral)

```bash
# Start a disposable instance on a random port, no volume (data dies with container)
CID=$(docker run -d --rm -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=sandbox -P postgres:16-alpine)
PORT=$(docker port "$CID" 5432/tcp | cut -d: -f2)
# Wait for readiness
docker exec "$CID" pg_isready -U postgres >/dev/null 2>&1 && echo 'postgres ready on port '$PORT
# Connect
PGPASSWORD=secret psql -h 127.0.0.1 -p "$PORT" -U postgres -d sandbox -c 'SELECT version();'
# TEARDOWN
docker stop "$CID" >/dev/null
```

## 3. Redis (Docker, ephemeral)

```bash
CID=$(docker run -d --rm -P redis:7-alpine)
PORT=$(docker port "$CID" 6379/tcp | cut -d: -f2)
docker exec "$CID" redis-cli -p 6379 ping
docker stop "$CID" >/dev/null
```

## 4. Safety Rules
- Always use `--rm` so containers self-delete on stop.
- Never mount a host data directory into a sandbox DB.
- Use a non-default DB name (`sandbox`, not `production`/`app`).
- Capture the container ID to a variable; never assume a fixed name for teardown.

## Pitfalls
- `docker run -P` picks an ephemeral host port — always resolve it with `docker port`, never hardcode 5432.
- Postgres needs a moment to accept connections; check `pg_isready` before connecting.
- On CPU-only hosts, prefer `-alpine` images to cut memory/startup cost.
