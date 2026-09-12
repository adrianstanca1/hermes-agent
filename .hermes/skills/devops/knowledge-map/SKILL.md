---
name: knowledge-map
description: "Map dependencies between files, skills, services."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [dependency-graph, map, architecture, impact-analysis]
    related_skills: [codebase-inspection, knowledge-map]
prerequisites:
  commands: [grep, python3]
---

# Knowledge Map: Dependency Graphing

Build a map of how things depend on each other — imports between modules, skill cross-references, or service call edges — to answer 'what breaks if I change X'.

## When to Use
- Before a refactor: know upstream/downstream impact.
- Mapping the skill ecosystem or service topology.
- The self-enhancement loop: detect orphaned or duplicated capabilities.

## 1. Module Dependency Map (Python)

```bash
# List internal imports per file (exclude stdlib/third-party by package root)
PKG=myapp  # set to the project's top-level package
for f in $(find . -name '*.py' -not -path '*/node_modules/*' -not -path '*/.git/*'); do
  deps=$(grep -oE "^from $PKG[^ ]*|^import $PKG" "$f" | sort -u | tr '\n' ' ')
  [ -n "$deps" ] && echo "$f -> $deps"
done
```

## 2. Skill Cross-Reference Map

```bash
# Which skills reference which others (related_skills frontmatter)
for s in ~/.hermes/skills/*/*/SKILL.md; do
  name=$(grep -m1 '^name:' "$s" | sed 's/name: //')
  rel=$(grep -m1 'related_skills' "$s" | sed 's/.*\[\(.*\)\]/\1/')
  echo "$name -> $rel"
done
```

## 3. Service Topology (this host)

```bash
# Listening ports -> what's advertising them
ss -ltnp 2>/dev/null | grep LISTEN | awk '{print $4, $6}'
# Cross-reference with the agentos / ollama / docker apps
```

## 4. Render as a Graph (optional)

If `graphviz` is installed, emit DOT and render to PNG:
```bash
pip install --break-system-packages graphviz 2>/dev/null || pip install graphviz
echo 'digraph G { "a" -> "b"; }' | dot -Tpng -o map.png
```

## Pitfalls
- Regex import detection misses dynamic imports (`__import__`, `importlib`) — flag those for manual review.
- Map is a snapshot; re-run after structural changes. Don't cache it across sessions without noting the date.
