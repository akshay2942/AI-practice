---
name: fix-lints
description: Fix linting issues with ruff when available. Use when the user asks to fix lints, format code, or clean up imports.
disable-model-invocation: true
---

# Fix Lints

Fix linting issues using ruff (optional — skip if not installed).

## When to Use

- User asks to fix lints or format code
- After code changes before commit
- Import ordering or style cleanup

## Workflow

### 1. Check if ruff is available

```bash
ruff --version 2>/dev/null || echo "ruff not installed"
```

If not installed, report that linting is optional and suggest:

```bash
pip install ruff
```

### 2. Check Issues

```bash
ruff check pages/ services/ tests/ config/
```

### 3. Auto-Fix

```bash
ruff check --fix pages/ services/ tests/ config/
ruff format pages/ services/ tests/ config/
```

### 4. Import Ordering Only

```bash
ruff check --select I --fix .
```

### 5. Report Results

List remaining issues that need manual fixes.

## Scope

Lint these directories only:
- `pages/`
- `services/`
- `tests/`
- `config/`
- `conftest.py`

## Common Fixes

| Issue | Fix |
|-------|-----|
| Unused import (F401) | Remove import |
| Import not sorted (I001) | `ruff check --select I --fix` |
| Undefined name (F821) | Add import |

## After Linting

Run compliance and tests:

```bash
python .cursor/skills/review-code/scripts/check_compliance.py --git-diff
pytest -m core
```

## Reference

- `.cursor/skills/review-code/SKILL.md`
