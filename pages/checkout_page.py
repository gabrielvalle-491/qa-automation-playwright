"""Checkout flow page objects: information, overview and confirmation."""

from playwright.sync_api import Page

from pages.base_page import BasePage, parse_price


class CheckoutInfoPage(BasePage):
    """Step one: customer information form."""

    path = "/checkout-step-one.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.first_name = page.locator('[data-test="firstName"]')
        self.last_name = page.locator('[data-test="lastName"]')
        self.postal_code = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.cancel_button = page.locator('[data-test="cancel"]')
        self.error = page.locator('[data-test="error"]')

    def fill_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Fill the form (empty strings leave a field blank) and continue."""
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)
        self.continue_button.click()


class CheckoutOverviewPage(BasePage):
    """Step two: order summary with totals."""

    path = "/checkout-step-two.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.item_prices = page.locator('[data-test="inventory-item-price"]')
        self.subtotal_label = page.locator('[data-test="subtotal-label"]')
        self.tax_label = page.locator('[data-test="tax-label"]')
        self.total_label = page.locator('[data-test="total-label"]')
        self.finish_button = page.locator('[data-test="finish"]')

    def item_total(self) -> float:
        """Displayed 'Item total' (subtotal before tax)."""
        return parse_price(self.subtotal_label.inner_text())

    def tax(self) -> float:
        """Displayed tax amount."""
        return parse_price(self.tax_label.inner_text())

    def total(self) -> float:
        """Displayed grand total."""
        return parse_price(self.total_label.inner_text())

    def line_prices(self) -> list[float]:
        """Prices of each line in the summary."""
        return [parse_price(text) for text in self.item_prices.all_inner_texts()]

    def finish(self) -> None:
        """Place the order."""
        self.finish_button.click()


class CheckoutCompletePage(BasePage):
    """Order confirmation page."""

    path = "/checkout-complete.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.header = page.locator('[data-test="complete-header"]')
        self.back_home_button = page.locator('[data-test="back-to-products"]')
