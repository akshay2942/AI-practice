"""Authentication workflows — orchestrates login/logout across pages."""

from playwright.sync_api import Page

from config.settings import VALID_PASSWORD, VALID_USER, LOCKED_OUT_USER
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class AuthService:
    """High-level auth operations for tests to consume."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.login_page = LoginPage(page)
        self.inventory_page = InventoryPage(page)

    def open_login_page(self) -> LoginPage:
        return self.login_page.open()

    def login(self, username: str, password: str) -> InventoryPage:
        self.login_page.open()
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_login()
        return self.inventory_page

    def login_as_standard_user(self) -> InventoryPage:
        return self.login(VALID_USER, VALID_PASSWORD)

    def attempt_login_locked_user(self) -> LoginPage:
        self.login_page.open()
        self.login_page.enter_username(LOCKED_OUT_USER)
        self.login_page.enter_password(VALID_PASSWORD)
        self.login_page.click_login()
        return self.login_page

    def logout(self) -> LoginPage:
        self.inventory_page.open_menu()
        self.inventory_page.click_logout()
        return self.login_page
