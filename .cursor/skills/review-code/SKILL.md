---
name: review-code
description: Review code for 3-layer framework compliance before commit. Use when reviewing changes, checking violations, or before committing.
disable-model-invocation: true
---

# Review Code

Review changes against the 3-layer framework rules.

## When to Use

- Before committing code
- After making edits
- User asks for code review or compliance check

## Workflow

### 1. Detect Changes

```bash
git status --porcelain
git diff --name-only
git diff --name-only --staged
```

Or run compliance script:

```bash
python .cursor/skills/review-code/scripts/check_compliance.py --git-diff
python .cursor/skills/review-code/scripts/check_compliance.py --path tests/ --path services/ --path pages/
```

### 2. Review by Layer

#### Test Layer (`tests/**/*.py`)

| Check | Violation |
|-------|-----------|
| Uses service fixtures | Direct `Page(...)` or page flows in test |
| `assert` in tests only | N/A (correct here) |
| No raw Playwright | `page.locator(` in test file |

#### Service Layer (`services/**/*.py`)

| Check | Violation |
|-------|-----------|
| Orchestrates pages | `assert`, `raise AssertionError` |
| No direct Playwright | `self.page.click(` bypassing pages |
| No hardcoded waits | `time.sleep(` |

#### Page Layer (`pages/**/*.py`)

| Check | Violation |
|-------|-----------|
| Extends `BasePage` | Plain class without inheritance |
| No assertions | `assert`, `raise AssertionError` |
| Atomic methods | `def .*_and_.*` multi-step methods |
| Boolean naming | `def verify_` instead of `is_`/`has_` |

### 3. Generate Compliance Report

Use this template:

```markdown
## Compliance Report

### Summary
- Files checked: N
- Critical: N | Warnings: N | Info: N

### Critical (Must Fix)
- {file}:{line} — {description}
  Fix: {suggestion}

### Warnings (Should Fix)
- {file}:{line} — {description}

### Passed
- [x] Layer separation
- [x] No assertions in page/service

### Recommendations
1. {priority fix}
```

### 4. Auto-Fixable Issues

| Violation | Fix |
|-----------|-----|
| Assertion in page/service | Move to test or return boolean |
| `time.sleep()` | Use Playwright waits |
| Page flow in test | Move to service method |

### 5. Verify After Fixes

```bash
pytest -m core
python .cursor/skills/review-code/scripts/check_compliance.py --git-diff
```

## Quick Commands

```bash
# Check specific path
python .cursor/skills/review-code/scripts/check_compliance.py --path services/

# Check staged + unstaged
python .cursor/skills/review-code/scripts/check_compliance.py --git-diff
```

## Reference

- `.cursor/rules/framework-core.mdc`
- `.cursor/rules/test-patterns.mdc`
- `.cursor/rules/page-patterns.mdc`
- `.cursor/rules/service-patterns.mdc`
