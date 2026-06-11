"""Authentication test scenarios (test layer)."""

import pytest

from config.test_data import SAUS01_ACCOUNTS
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

    @pytest.mark.core
    @pytest.mark.parametrize("account", SAUS01_ACCOUNTS, ids=lambda a: a["username"])
    def test_saus01_login_with_multiple_accounts(self, auth_service, account):
        """Saus01: login to Sauce Demo with each account from data/saus01_accounts.json.

        Steps:
        1. Open saucedemo.com
        2. Enter username
        3. Enter password
        4. Click Login
        """
        inventory = auth_service.login(account["username"], account["password"])

        if account["expected_success"]:
            assert inventory.is_loaded()
            assert inventory.get_page_heading() == "Products"
        else:
            assert auth_service.login_page.is_error_displayed()
            assert "locked out" in auth_service.login_page.get_error_text().lower()


@pytest.mark.regression
class TestLogout:
    """Session teardown via service layer."""

    def test_user_can_logout(self, auth_service):
        auth_service.login_as_standard_user()
        login_page = auth_service.logout()

        assert isinstance(login_page, LoginPage)
        assert auth_service.login_page.is_visible(LoginPage.LOGIN_BUTTON)
