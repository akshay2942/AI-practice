"""Pytest fixtures wiring Playwright to the three-layer architecture."""

import pytest
from playwright.sync_api import Page

from services.auth_service import AuthService
from services.inventory_service import InventoryService


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Apply defaults to every browser context."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }


@pytest.fixture
def auth_service(page: Page) -> AuthService:
    """Service layer fixture for authentication workflows."""
    return AuthService(page)


@pytest.fixture
def inventory_service(page: Page) -> InventoryService:
    """Service layer fixture for inventory workflows."""
    return InventoryService(page)


@pytest.fixture
def logged_in_page(auth_service: AuthService) -> Page:
    """Page already authenticated as the standard demo user."""
    auth_service.login_as_standard_user()
    return auth_service.page
