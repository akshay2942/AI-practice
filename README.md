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

## Run tests

```bash
# All tests (headless)
pytest

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

**Available test names:** `test_standard_user_can_login`, `test_locked_out_user_sees_error`, `test_user_can_logout`, `test_catalog_lists_products`, `test_catalog_has_six_items`

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

## Project layout

```
.
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
