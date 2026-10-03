"""Inventory (product list) page object."""

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage, parse_price


def slug(product_name: str) -> str:
    """Convert a product name to the slug used in its data-test ids."""
    return product_name.lower().replace(" ", "-")


class InventoryPage(BasePage):
    """Product grid shown after a successful login."""

    path = "/inventory.html"

    SORT_OPTIONS = {
        "name_asc": "az",
        "name_desc": "za",
        "price_asc": "lohi",
        "price_desc": "hilo",
    }

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.items = page.locator('[data-test="inventory-item"]')
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.item_prices = page.locator('[data-test="inventory-item-price"]')
        self.item_images = page.locator(".inventory_item_img img")
        self.sort_select = page.locator('[data-test="product-sort-container"]')

    def sort_by(self, option: str) -> None:
        """Sort the grid; option is a key of SORT_OPTIONS (e.g. 'price_asc')."""
        self.sort_select.select_option(self.SORT_OPTIONS[option])

    def names(self) -> list[str]:
        """Product names in the order they are displayed."""
        return self.item_names.all_inner_texts()

    def prices(self) -> list[float]:
        """Product prices in the order they are displayed."""
        return [parse_price(text) for text in self.item_prices.all_inner_texts()]

    def add_button(self, product_name: str) -> Locator:
        """'Add to cart' button of a given product."""
        return self.page.locator(f'[data-test="add-to-cart-{slug(product_name)}"]')

    def remove_button(self, product_name: str) -> Locator:
        """'Remove' button of a given product (visible once it is in the cart)."""
        return self.page.locator(f'[data-test="remove-{slug(product_name)}"]')

    def add_to_cart(self, *product_names: str) -> None:
        """Add one or more products to the cart from the grid."""
        for name in product_names:
            self.add_button(name).click()

    def remove_from_cart(self, *product_names: str) -> None:
        """Remove one or more products from the cart using the grid buttons."""
        for name in product_names:
            self.remove_button(name).click()
