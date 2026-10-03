"""Shopping cart page object."""

from playwright.sync_api import Page

from pages.base_page import BasePage, parse_price
from pages.inventory_page import slug


class CartPage(BasePage):
    """Cart contents with the checkout entry point."""

    path = "/cart.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.items = page.locator('[data-test="inventory-item"]')
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.item_prices = page.locator('[data-test="inventory-item-price"]')
        self.checkout_button = page.locator('[data-test="checkout"]')
        self.continue_shopping_button = page.locator('[data-test="continue-shopping"]')

    def names(self) -> list[str]:
        """Names of the products currently in the cart."""
        return self.item_names.all_inner_texts()

    def prices(self) -> list[float]:
        """Prices of the products currently in the cart."""
        return [parse_price(text) for text in self.item_prices.all_inner_texts()]

    def remove(self, product_name: str) -> None:
        """Remove a product from the cart page."""
        self.page.locator(f'[data-test="remove-{slug(product_name)}"]').click()

    def checkout(self) -> None:
        """Start the checkout flow."""
        self.checkout_button.click()
