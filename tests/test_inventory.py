"""Inventory test scenarios (test layer)."""

import pytest


@pytest.mark.smoke
class TestInventory:
    """Catalog visibility via InventoryService."""

    @pytest.mark.core
    def test_catalog_lists_products(self, inventory_service):
        inventory = inventory_service.view_catalog_as_standard_user()

        assert inventory.is_loaded()
        assert inventory.get_product_count() > 0

    def test_catalog_has_six_items(self, inventory_service):
        count = inventory_service.get_product_count_for_standard_user()

        assert count == 6

    @pytest.mark.core
    def test_add_item_to_cart(self, inventory_service):
        cart_count = inventory_service.add_backpack_to_cart_as_standard_user()

        assert cart_count == 1
