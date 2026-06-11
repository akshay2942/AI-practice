---
name: refactor-safely
description: Plan and execute safe refactoring using grep for usages and pytest for verification. Use when renaming, moving, or restructuring code.
disable-model-invocation: true
---

# Refactor Safely

Refactor with confidence using grep and incremental test runs.

## When to Use

- Renaming methods, classes, or files
- Extracting service or page methods
- Restructuring without breaking tests

## Workflow

### 1. Find All Usages

```bash
rg "<symbol_name>" pages/ services/ tests/ conftest.py
rg "from pages\.<module>" .
rg "from services\.<module>" .
```

### 2. List Impact

| File | Layer | Usage count |
|------|-------|-------------|
| ... | test/service/page | N |

### 3. Plan Incremental Steps

- One symbol or file at a time
- Run tests after each step
- Update imports last if moving files

### 4. Apply Change

Small diffs only. Preserve layer boundaries:
- Page renames → update services that import them
- Service renames → update tests and conftest fixtures

### 5. Verify After Each Step

```bash
pytest -m core -v
pytest -k <affected_test_name> -v
```

### 6. Compliance Check

```bash
python .cursor/skills/review-code/scripts/check_compliance.py --git-diff
```

## Safety Checks

- Preview all `rg` hits before renaming
- Never move assertions into page/service layers during refactor
- Run `pytest -m core` before considering done

## Token Budget

Target ≤5 tool calls:
1. `rg` for symbol
2. Apply small change
3. `pytest -m core`
4. Compliance script if needed

## Reference

- `.cursor/skills/review-code/SKILL.md`
- `.cursor/rules/framework-core.mdc`
