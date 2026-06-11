# Playwright Python + Pytest (3-Layer POM)

End-to-end test framework using **Playwright**, **pytest**, and **Page Object Model** with a strict three-layer architecture.

## Architecture

```
tests/          → Test layer: assertions & scenarios only
services/       → Service layer: business workflows (compose pages)
pages/          → Page layer: locators & atomic UI interactions
config/         → URLs, credentials, timeouts
```

| Layer | Responsibility | Example |
|-------|----------------|---------|
| **Page** | Locators, clicks, fills, reads | `LoginPage.enter_username()` |
| **Service** | User journeys across pages | `AuthService.login_as_standard_user()` |
| **Test** | Arrange/act/assert via services | `test_standard_user_can_login` |

Tests must **not** call page objects directly for flows — use services. Page objects stay free of assertions.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

**Important:** Run tests from the virtualenv so the Playwright `page` fixture is available:

```bash
source .venv/bin/activate
# or prefix commands: .venv/bin/pytest ...
```

If you see `fixture 'page' not found`, you are using system Python instead of `.venv`.

## Run tests

```bash
# All tests (headless) — use venv pytest
.venv/bin/pytest

# Headed browser
pytest --headed

# Smoke only
pytest -m smoke

# Core test cases only (@pytest.mark.core)
make test-core
# equivalent:
pytest -m core

# List core tests without running
make list-core
# equivalent:
pytest -m core --collect-only -q

# Core tests in headed Chrome
make test-core-headed

# Run by test case name (function name)
make test-case NAME=test_catalog_lists_products
make test-case NAME=test_standard_user_can_login

# List matching tests by name (no run)
make list-test-case NAME=test_catalog_lists_products

# Run by name in headed Chrome
make test-case-headed NAME=test_catalog_lists_products

# Shell script (from project root)
chmod +x scripts/run_test_by_name.sh
./scripts/run_test_by_name.sh test_catalog_lists_products
./scripts/run_test_by_name.sh test_catalog_lists_products --headed --browser-channel=chrome

# pytest equivalent (full node path — exact match)
pytest tests/test_inventory.py::TestInventory::test_catalog_lists_products

# pytest equivalent (by name substring)
pytest -k test_catalog_lists_products

# Single file
pytest tests/test_auth.py
```

**Available test names:** `test_standard_user_can_login`, `test_locked_out_user_sees_error`, `test_user_can_logout`, `test_catalog_lists_products`, `test_catalog_has_six_items`, `test_add_item_to_cart`

### Markers

| Marker | Purpose |
|--------|---------|
| `core` | Essential tests for targeted runs (`make test-core`) |
| `smoke` | Quick smoke suite |
| `regression` | Full regression suite |

Apply `core` on any test you want in the core suite:

```python
@pytest.mark.core
def test_my_flow(self, auth_service):
    ...
```

## Configuration

Environment variables (optional):

| Variable | Default |
|----------|---------|
| `BASE_URL` | `https://www.saucedemo.com` |
| `TEST_USER` | `standard_user` |
| `TEST_PASSWORD` | `secret_sauce` |
| `DEFAULT_TIMEOUT_MS` | `10000` |

## AI-assisted development

Cursor rules and skills in `.cursor/` guide the AI agent when working on this framework.

### Rules (`.cursor/rules/`)

| Rule | Applies when |
|------|----------------|
| `framework-core.mdc` | Always — 3-layer architecture and critical rules |
| `workflow.mdc` | Always — plan before large changes, summarize after |
| `test-patterns.mdc` | Editing `tests/**/*.py` |
| `page-patterns.mdc` | Editing `pages/**/*.py` |
| `service-patterns.mdc` | Editing `services/**/*.py` |

### Skills (`.cursor/skills/`)

| Skill | Use for |
|-------|---------|
| `create-test` | Adding new test scenarios |
| `fix-test` | Debugging failing tests |
| `review-code` | Framework compliance before commit |
| `fix-lints` | Optional ruff formatting/linting |
| `explore-codebase` | Understanding project structure |
| `refactor-safely` | Renames and safe refactors |
| `debug-issue` | Tracing failures test → service → page |
| `review-changes` | Git diff review with test verification |

### Example prompts

- "Create a test for adding an item to the cart"
- "Fix `test_standard_user_can_login` — it's timing out"
- "Review my changes for framework compliance"
- "How does the login flow work in this project?"

### Helper scripts

```bash
# Find a test by name
python .cursor/skills/fix-test/scripts/find_test.py --test test_standard_user_can_login

# Check framework compliance
python .cursor/skills/review-code/scripts/check_compliance.py --git-diff
python .cursor/skills/review-code/scripts/check_compliance.py --path tests/ --path services/ --path pages/
```

> **Note:** `.claude/` is legacy and gitignored. Use `.cursor/` for AI configuration in this project.

## Project layout

```
.
├── .cursor/
│   ├── rules/          # Cursor AI rules
│   └── skills/         # Cursor AI skills + helper scripts
├── config/
│   └── settings.py
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   └── inventory_page.py
├── services/
│   ├── auth_service.py
│   └── inventory_service.py
├── tests/
│   ├── test_auth.py
│   └── test_inventory.py
├── conftest.py
├── pytest.ini
└── requirements.txt
```
