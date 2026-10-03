"""Page Object Model for https://www.saucedemo.com."""

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutCompletePage, CheckoutInfoPage, CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

__all__ = [
    "CartPage",
    "CheckoutCompletePage",
    "CheckoutInfoPage",
    "CheckoutOverviewPage",
    "InventoryPage",
    "LoginPage",
]
