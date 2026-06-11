---
name: fix-test
description: Fix failing Playwright tests by identifying locator, flow, or layer violations. Use when a test fails or the user asks to fix a test.
disable-model-invocation: true
---

# Fix Test

Run failing tests, identify root cause, fix in the correct layer.

## When to Use

- User reports a failing test
- User asks to fix a test
- Locator, flow, or timeout failures

## Workflow

### 1. Parse Test Target

Accept formats:
- Function name: `test_standard_user_can_login`
- File path: `tests/test_auth.py`
- Full node: `tests/test_auth.py::TestLogin::test_standard_user_can_login`

Find test:

```bash
python .cursor/skills/fix-test/scripts/find_test.py --test "test_name"
# or
pytest --collect-only -q -k test_name
```

### 2. Run the Test

```bash
pytest -k <test_name> -v --tb=long
make test-case-headed NAME=<test_name>
```

### 3. Classify Failure

| Error | Layer | Typical Fix |
|-------|-------|-------------|
| `TimeoutError` on locator | Page | Update selector, add wait |
| Wrong page/state | Service | Fix flow order, missing step |
| Assertion failed | Test | Fix expected value or service return |
| Import/fixture error | conftest | Wire new service fixture |

### 4. Trace Call Chain

```bash
rg "<failing_method>" tests/ services/ pages/
```

Follow: test → service → page → locator.

### 5. Apply Fix

**Locator (page layer):**

```python
# Prefer stable data-test selectors
BUTTON = "[data-test='login-button']"
```

**Flow (service layer):**

```python
def login(self, username: str, password: str) -> InventoryPage:
    self.login_page.open()
    self.login_page.enter_username(username)
    self.login_page.enter_password(password)
    self.login_page.click_login()
    return self.inventory_page
```

**Assertion (test layer only):**

```python
assert inventory.is_loaded()
assert "locked out" in login_page.get_error_text().lower()
```

### 6. Verify Fix

```bash
pytest -k <test_name> -v
pytest -m core
```

### 7. Compliance

- [ ] No assertions added to page/service
- [ ] No `time.sleep()`
- [ ] Fix in correct layer

## Common Issues

| Symptom | Fix |
|---------|-----|
| Timeout on click | Element not ready; check selector |
| Stale element | Re-query after navigation |
| Wrong assertion | Update test expected value |
| Missing fixture | Add to `conftest.py` |

## Reference

- `.cursor/skills/review-code/SKILL.md` for compliance checks
