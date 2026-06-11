---
name: create-test
description: Create new Playwright tests following the 3-layer architecture. Use when the user wants to create a new test, automate a scenario, or add test coverage.
disable-model-invocation: true
---

# Create Test

Create Playwright tests following the 3-layer architecture (tests → services → pages).

## When to Use

- User wants a new test case
- User wants to automate a feature or scenario
- User describes a test scenario to implement

## Workflow

### 1. Understand the Requirement

Clarify:
- **Scenario:** What user action or flow to test?
- **Expected outcome:** What should pass?

### 2. Discover Existing Components

```bash
rg "class \w+Page" pages/
rg "class \w+Service" services/
pytest --collect-only -q
```

Read matching page/service files before adding new ones.

### 3. Create Implementation Plan

Present plan before coding:
- Test file and method name
- Page objects needed (existing or new)
- Service methods needed (existing or new)
- Assertions in test layer only

Wait for approval on large additions.

### 4. Implement (3 Layers)

**Test** (`tests/`):

```python
import pytest

@pytest.mark.smoke
class TestFeature:
    @pytest.mark.core
    def test_scenario(self, auth_service):
        result = auth_service.some_workflow()

        assert result.is_loaded()
```

**Service** (`services/`):

```python
class FeatureService:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.feature_page = FeaturePage(page)

    def some_workflow(self) -> FeaturePage:
        self.feature_page.open()
        self.feature_page.click_action()
        return self.feature_page
```

**Page** (`pages/`):

```python
class FeaturePage(BasePage):
    ACTION_BUTTON = "[data-test='action']"

    def click_action(self) -> None:
        self.page.locator(self.ACTION_BUTTON).click()
```

Add fixture to `conftest.py` if a new service is created.

### 5. Run and Verify

```bash
make test-case NAME=<test_function_name>
make test-case-headed NAME=<test_function_name>
pytest -k <test_function_name> -v
```

### 6. Compliance Check

- [ ] Assertions only in `tests/`
- [ ] Test uses service fixture, not page objects for flows
- [ ] Page methods are atomic
- [ ] Appropriate marker (`smoke`, `core`, `regression`)

## NEVER

- Use raw `page.locator()` in tests
- Import pages in tests for flows (services only)
- Put assertions in page or service layers
- Use `time.sleep()`

## Reference

- `.cursor/rules/framework-core.mdc`
- `.cursor/rules/test-patterns.mdc`
- `.cursor/rules/page-patterns.mdc`
- `.cursor/rules/service-patterns.mdc`
