"""Service layer: business workflows composed from page objects."""

from services.auth_service import AuthService
from services.inventory_service import InventoryService

__all__ = ["AuthService", "InventoryService"]
