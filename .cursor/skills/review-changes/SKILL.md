---
name: review-changes
description: Perform structured review of git changes with impact analysis and test verification. Use when reviewing diffs before merge or commit.
disable-model-invocation: true
---

# Review Changes

Review git changes with risk awareness and test verification.

## When to Use

- Before merge or commit
- After a feature branch is ready
- User asks to review what changed

## Workflow

### 1. Get Changed Files

```bash
git diff --name-only
git diff --name-only --staged
git diff
```

### 2. Map to Layers

| Path prefix | Layer | Risk if changed |
|-------------|-------|-----------------|
| `tests/` | Test | Assertion or scenario logic |
| `services/` | Service | Workflow breakage |
| `pages/` | Page | Locator/timeout failures |
| `conftest.py` | Fixtures | All tests affected |
| `config/` | Config | Environment-wide impact |

### 3. Find Affected Tests

```bash
# For each changed service/page symbol
rg "<ClassName>" tests/
rg "<method_name>" tests/
```

### 4. Run Targeted Tests

```bash
pytest -m core -v
pytest -k <affected_test_name> -v
```

### 5. Compliance Check

```bash
python .cursor/skills/review-code/scripts/check_compliance.py --git-diff
```

### 6. Output Format

```markdown
## Change Review

### Files Changed
- {file} ({layer})

### Risk Assessment
- **High:** {file} — {reason}
- **Medium:** {file} — {reason}
- **Low:** {file} — {reason}

### Test Coverage
- Tests run: {list}
- Result: pass/fail

### Compliance
- Critical issues: N
- Warnings: N

### Recommendation
- [ ] Ready to merge / needs fixes
```

## Token Budget

Target ≤5 tool calls:
1. `git diff --name-only`
2. `rg` for affected tests
3. `pytest -m core`
4. Compliance script
5. Summarize

## Reference

- `.cursor/skills/review-code/SKILL.md`
- `.cursor/rules/framework-core.mdc`
