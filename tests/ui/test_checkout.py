"""Checkout flow: happy path, form validation and price calculation."""

import pytest
from playwright.sync_api import Page, expect

from pages import (
    CartPage,
    CheckoutCompletePage,
    CheckoutInfoPage,
    CheckoutOverviewPage,
    InventoryPage,
)
from utils.data import CUSTOMER, PRODUCTS, TAX_RATE

ITEMS = ["Sauce Labs Backpack", "Sauce Labs Fleece Jacket", "Sauce Labs Onesie"]


@pytest.fixture
def checkout_info(inventory_page: InventoryPage, page: Page) -> CheckoutInfoPage:
    """Checkout step one with ITEMS already in the cart."""
    inventory_page.add_to_cart(*ITEMS)
    inventory_page.open_cart()
    CartPage(page).checkout()
    expect(page).to_have_url(CheckoutInfoPage.url_pattern())
    return CheckoutInfoPage(page)


@pytest.mark.smoke
def test_checkout_happy_path(checkout_info: CheckoutInfoPage, page: Page) -> None:
    """A complete order ends on the confirmation page with an empty cart."""
    checkout_info.fill_info(**CUSTOMER)

    overview = CheckoutOverviewPage(page)
    expect(page).to_have_url(CheckoutOverviewPage.url_pattern())
    overview.finish()

    complete = CheckoutCompletePage(page)
    expect(page).to_have_url(CheckoutCompletePage.url_pattern())
    expect(complete.header).to_have_text("Thank you for your order!")
    expect(complete.cart_badge).to_be_hidden()


@pytest.mark.parametrize(
    ("first_name", "last_name", "postal_code", "message"),
    [
        ("", CUSTOMER["last_name"], CUSTOMER["postal_code"], "Error: First Name is required"),
        (CUSTOMER["first_name"], "", CUSTOMER["postal_code"], "Error: Last Name is required"),
        (CUSTOMER["first_name"], CUSTOMER["last_name"], "", "Error: Postal Code is required"),
    ],
    ids=["missing-first-name", "missing-last-name", "missing-postal-code"],
)
def test_checkout_form_validation(
    checkout_info: CheckoutInfoPage,
    page: Page,
    first_name: str,
    last_name: str,
    postal_code: str,
    message: str,
) -> None:
    """Each required field blocks the checkout with its own error message."""
    checkout_info.fill_info(first_name, last_name, postal_code)

    expect(checkout_info.error).to_have_text(message)
    expect(page).to_have_url(CheckoutInfoPage.url_pattern())


def test_order_totals_are_correct(checkout_info: CheckoutInfoPage, page: Page) -> None:
    """Item total = sum of line prices, tax = 8 %, total = item total + tax."""
    checkout_info.fill_info(**CUSTOMER)
    overview = CheckoutOverviewPage(page)
    expect(overview.item_prices).to_have_count(len(ITEMS))

    expected_subtotal = round(sum(PRODUCTS[name] for name in ITEMS), 2)
    assert overview.line_prices() == [PRODUCTS[name] for name in ITEMS]
    assert overview.item_total() == pytest.approx(expected_subtotal)
    assert overview.tax() == pytest.approx(round(expected_subtotal * TAX_RATE, 2))
    assert overview.total() == pytest.approx(overview.item_total() + overview.tax())


def test_cancel_checkout_returns_to_cart(checkout_info: CheckoutInfoPage, page: Page) -> None:
    """Cancelling step one goes back to the cart without losing items."""
    checkout_info.cancel_button.click()

    cart = CartPage(page)
    expect(page).to_have_url(CartPage.url_pattern())
    expect(cart.item_names).to_have_text(ITEMS)
