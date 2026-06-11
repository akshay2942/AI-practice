"""Inventory workflows — catalog browsing after authentication."""

from playwright.sync_api import Page

from pages.inventory_page import InventoryPage
from services.auth_service import AuthService


class InventoryService:
    """Business operations on the product inventory."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.auth_service = AuthService(page)
        self.inventory_page = InventoryPage(page)

    def view_catalog_as_standard_user(self) -> InventoryPage:
        self.auth_service.login_as_standard_user()
        return self.inventory_page

    def get_product_count_for_standard_user(self) -> int:
        self.view_catalog_as_standard_user()
        return self.inventory_page.get_product_count()

    def add_backpack_to_cart_as_standard_user(self) -> int:
        self.auth_service.login_as_standard_user()
        self.inventory_page.click_add_backpack_to_cart()
        return self.inventory_page.get_cart_badge_count()
