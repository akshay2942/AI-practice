"""Authentication test scenarios (test layer)."""

import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.mark.smoke
class TestLogin:
    """Valid and invalid login flows via AuthService."""

    @pytest.mark.core
    def test_standard_user_can_login(self, auth_service):
        inventory = auth_service.login_as_standard_user()

        assert inventory.is_loaded()
        assert inventory.get_page_heading() == "Products"

    def test_locked_out_user_sees_error(self, auth_service):
        login_page = auth_service.attempt_login_locked_user()

        assert login_page.is_error_displayed()
        assert "locked out" in login_page.get_error_text().lower()


@pytest.mark.regression
class TestLogout:
    """Session teardown via service layer."""

    def test_user_can_logout(self, auth_service):
        auth_service.login_as_standard_user()
        login_page = auth_service.logout()

        assert isinstance(login_page, LoginPage)
        assert auth_service.login_page.is_visible(LoginPage.LOGIN_BUTTON)
