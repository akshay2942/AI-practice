"""Base page object with shared Playwright interactions."""

from playwright.sync_api import Page, Locator

from config.settings import BASE_URL, DEFAULT_TIMEOUT_MS


class BasePage:
    """Parent for all page objects. Holds page reference and common helpers."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.base_url = BASE_URL
        self.page.set_default_timeout(DEFAULT_TIMEOUT_MS)

    def navigate(self, path: str = "") -> None:
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}" if path else self.base_url
        self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()

    def wait_for_url(self, pattern: str) -> None:
        self.page.wait_for_url(pattern)

    def locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()
