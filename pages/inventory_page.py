"""Inventory (products) page object — post-login catalog screen."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Sauce Demo inventory / products listing."""

    PAGE_TITLE = ".title"
    INVENTORY_LIST = ".inventory_list"
    SHOPPING_CART_BADGE = ".shopping_cart_badge"
    ADD_BACKPACK_BUTTON = "[data-test='add-to-cart-sauce-labs-backpack']"
    MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def is_loaded(self) -> bool:
        return (
            self.page.locator(self.PAGE_TITLE).is_visible()
            and self.page.locator(self.INVENTORY_LIST).is_visible()
        )

    def get_page_heading(self) -> str:
        return self.page.locator(self.PAGE_TITLE).inner_text()

    def get_product_count(self) -> int:
        return self.page.locator(".inventory_item").count()

    def click_add_backpack_to_cart(self) -> None:
        self.page.locator(self.ADD_BACKPACK_BUTTON).click()

    def get_cart_badge_count(self) -> int:
        badge = self.page.locator(self.SHOPPING_CART_BADGE)
        if not badge.is_visible():
            return 0
        return int(badge.inner_text())

    def open_menu(self) -> "InventoryPage":
        self.page.locator(self.MENU_BUTTON).click()
        return self

    def click_logout(self) -> None:
        self.page.locator(self.LOGOUT_LINK).click()
