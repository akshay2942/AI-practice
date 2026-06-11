---
name: debug-issue
description: Systematically debug test failures or code issues using pytest output, grep, and git history. Use when investigating bugs or unexpected behavior.
disable-model-invocation: true
---

# Debug Issue

Trace and debug issues through the test → service → page chain.

## When to Use

- Test fails unexpectedly
- Regression after a change
- User reports broken behavior

## Workflow

### 1. Reproduce

```bash
pytest -k <test_name> -v --tb=long
make test-case-headed NAME=<test_name>
```

Capture full traceback and failing line.

### 2. Identify Failing Layer

| Failure location | Layer to fix |
|------------------|--------------|
| `tests/` assert line | Test expectation or service return value |
| `services/` | Flow orchestration |
| `pages/` | Locator or UI action |
| Timeout | Usually page layer selector/wait |

### 3. Trace Call Chain

```bash
rg "<failing_function>" tests/ services/ pages/
```

Follow imports from test method → service → page.

### 4. Check Recent Changes

```bash
git log -5 --oneline -- <file_path>
git diff HEAD~1 -- <file_path>
```

### 5. Inspect Related Tests

```bash
rg "<service_or_page_class>" tests/
pytest -k <related_test> -v
```

### 6. Fix and Verify

Apply fix in correct layer, then:

```bash
pytest -k <test_name> -v
pytest -m core
```

## Tips

- Timeouts → check locator and `DEFAULT_TIMEOUT_MS` in config
- Assertion failures → verify service returns expected type/value
- Import errors → check `conftest.py` fixtures

## Token Budget

Target ≤5 tool calls:
1. Run pytest with verbose traceback
2. `rg` failing symbol
3. Read 1–2 files in chain
4. Apply fix
5. Re-run test

## Reference

- `.cursor/skills/fix-test/SKILL.md`
- `.cursor/skills/explore-codebase/SKILL.md`
