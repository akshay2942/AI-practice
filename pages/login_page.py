"""Login page object — locators and atomic UI actions."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Sauce Demo login screen."""

    # Locators
    USERNAME_INPUT = "[data-test='username']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    ERROR_MESSAGE = "[data-test='error']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "LoginPage":
        self.navigate()
        return self

    def enter_username(self, username: str) -> "LoginPage":
        self.page.locator(self.USERNAME_INPUT).fill(username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        self.page.locator(self.PASSWORD_INPUT).fill(password)
        return self

    def click_login(self) -> None:
        self.page.locator(self.LOGIN_BUTTON).click()

    def get_error_text(self) -> str:
        return self.page.locator(self.ERROR_MESSAGE).inner_text()

    def is_error_displayed(self) -> bool:
        return self.page.locator(self.ERROR_MESSAGE).is_visible()
