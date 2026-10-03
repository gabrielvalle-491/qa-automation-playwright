"""Base class shared by every page object."""

from playwright.sync_api import Locator, Page


def parse_price(text: str) -> float:
    """Extract the numeric amount from labels like '$29.99' or 'Tax: $2.40'."""
    return float(text.rsplit("$", 1)[1])


class BasePage:
    """Holds the Playwright page and the header widgets present on most pages."""

    path: str = "/"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.title: Locator = page.locator('[data-test="title"]')
        self.cart_link: Locator = page.locator('[data-test="shopping-cart-link"]')
        self.cart_badge: Locator = page.locator('[data-test="shopping-cart-badge"]')
        self.menu_button: Locator = page.locator("#react-burger-menu-btn")
        self.logout_link: Locator = page.locator('[data-test="logout-sidebar-link"]')

    def open(self) -> None:
        """Navigate directly to this page (relative to the configured base URL)."""
        self.page.goto(self.path)

    def open_cart(self) -> None:
        """Click the cart icon in the header."""
        self.cart_link.click()

    def logout(self) -> None:
        """Log out through the burger menu."""
        self.menu_button.click()
        self.logout_link.click()
