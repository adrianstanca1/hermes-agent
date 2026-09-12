---
name: self-enhance
description: "Capture a workflow or failure as a skill or memory."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [self-improvement, recursive, meta, skill-authoring, persistence]
    related_skills: [hermes-agent-skill-authoring, context-switch, knowledge-map]
prerequisites:
  commands: [skill_manage]
---

# Self-Enhance: The Recursive Optimization Loop

Per the autonomous core's Prime Directive, every interaction should grow the system. This skill operationalizes that: detect a pattern, capture it as a skill or memory, persist it.

## When to Trigger
- A tool call failed and you found a non-obvious fix (capture the pitfall).
- You repeated the same 3+ command sequence this session (extract a skill).
- A task type recurs across sessions (author a reusable skill).
- You discovered an environment fact every session needs (write a memory).

## 1. Analyze (what did we learn?)

Before enhancing, name the lesson as an imperative rule + why:
- GOOD: 'Prefer ruff over black+isort — one tool, no formatter conflict.'
- BAD: 'Fixed the lint issue on Sept 12.' (that's a log, not a lesson)

## 2. Decide the Target

| Lesson type | Target |
|-------------|--------|
| Reusable workflow for a task class | New skill via `skill_manage` create |
| Fix/pitfall for an existing skill | `skill_manage` patch on that skill |
| Fact true in EVERY session (env, user, convention) | `memory` tool, target `memory` or `user` |
| Project-specific state | Project file (CLAUDE.md) — but prefer skills/memory |

## 3. Author the Skill (if new)

Use the established SKILL.md format (see `hermes-agent-skill-authoring`):
- YAML frontmatter: `name`, `description` (first 57 chars a self-contained trigger), `version`, `platforms`, `metadata.hermes.tags`, `prerequisites.commands`.
- Body: When to Use, numbered steps with real commands, Pitfalls, Safety Rules.
- Create under `~/.hermes/skills/<category>/<name>/SKILL.md`.

## 4. Persist & Verify

```bash
# After skill_manage create/patch, confirm it loads
skills_list 2>/dev/null | grep -i '<name>'
```

## 5. Loop Closure

Report what changed: which skill/memory was added or patched, and the one rule it now encodes. Keep it to a few lines — the point is the persistent artifact, not the narration.

## Pitfalls
- Don't over-skill: if a workflow is a one-off, a memory note beats a whole skill.
- Memory is injected into EVERY turn and has a hard char budget — keep entries compact and high-signal; put procedures in skills, not memory.
- Skills must be self-contained: a future session loads only the SKILL.md, so include real commands and pitfalls, not 'see chat history'.
