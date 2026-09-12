---
name: code-cleanup
description: "Improve code hygiene: lint, format, dead code."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [cleanup, lint, hygiene, refactor, formatting]
    related_skills: [codebase-inspection, simplify-code, requesting-code-review]
prerequisites:
  commands: [git, ruff, black, isort]
---

# Code Cleanup: Codebase Hygiene

Improve code hygiene in reversible steps. Always start from a clean git state so every change is reviewable and undoable.

## When to Use
- User asks to 'clean up' a project or directory.
- Before a refactor or review pass.
- As part of the self-enhancement loop when a repeated smell is detected.

## 1. Baseline (git is the safety net)

```bash
git status --short && git stash list
git add -A && git commit -q -m 'wip: pre-cleanup baseline' 2>/dev/null || true
```

## 2. Find Dead Code & Unused Imports

```bash
# Python unused imports / undefined names (no install needed for compile check)
python3 -m pyflakes . 2>/dev/null || python3 -m py_compile $(find . -name '*.py' -not -path '*/node_modules/*' -not -path '*/.git/*')
# List files never imported (manual review)
```

## 3. Auto-Format (safe, deterministic)

```bash
# Prefer ruff (one tool: lint + format + import sort)
pip install --break-system-packages ruff 2>/dev/null || pip install ruff
ruff check --fix . && ruff format .
# Fallbacks if ruff unavailable
black . 2>/dev/null; isort . 2>/dev/null
```

## 4. Trim Dependencies

```bash
# Show what's installed vs declared in requirements
pip list --format=freeze > /tmp/installed.txt
# Diff against requirements.txt / pyproject; flag orphans for manual review (do NOT auto-uninstall in prod)
```

## 5. Review & Commit

```bash
git diff --stat
git add -A && git commit -q -m 'chore: code hygiene pass' 2>/dev/null || true
```

## Safety Rules
- Never auto-delete files or uninstall packages in a production directory — report orphans, let a human pull the trigger.
- Format in a commit separate from logic changes so reviews stay clean.
- Run the project's own test suite after formatting; formatting can expose latent syntax issues.

## Pitfalls
- `black` and `ruff format` disagree on some constructs — pick ONE formatter per repo and stick to it.
- Tree-shaking in dynamic languages (Python/JS) is heuristic; manual confirmation required before deleting 'unused' exports.
