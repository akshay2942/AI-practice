---
name: explore-codebase
description: Navigate and understand the test framework structure using grep, file reads, and pytest collection. Use when exploring the codebase or understanding architecture.
disable-model-invocation: true
---

# Explore Codebase

Understand the 3-layer test framework without external tools.

## When to Use

- User asks how the project is structured
- Need to find pages, services, or tests for a feature
- Tracing imports or dependencies

## Workflow

### 1. Start with Entry Points

Read in order:
1. `README.md` — architecture overview
2. `conftest.py` — fixtures
3. `pytest.ini` — markers and paths
4. `config/settings.py` — URLs and credentials

### 2. Map Layers

```bash
ls pages/ services/ tests/
rg "class \w+Page" pages/
rg "class \w+Service" services/
pytest --collect-only -q
```

### 3. Trace a Feature

Example: authentication flow

```bash
rg "login" tests/ services/ pages/
```

Read chain: `tests/test_auth.py` → `services/auth_service.py` → `pages/login_page.py`

### 4. Find Usages

```bash
rg "AuthService" .
rg "login_as_standard_user" .
```

### 5. Understand Test Coverage

```bash
pytest --collect-only -q
pytest -m core --collect-only -q
```

## Token Budget

Target ≤5 tool calls:
1. Read README or conftest
2. List/grep one layer
3. Read key file for the feature
4. Optional: pytest --collect-only

## Architecture Quick Reference

```
tests/     → assertions, service fixtures
services/  → workflows (AuthService, InventoryService)
pages/     → UI actions (LoginPage, InventoryPage)
config/    → BASE_URL, credentials, timeouts
```

## Reference

- `.cursor/rules/framework-core.mdc`
