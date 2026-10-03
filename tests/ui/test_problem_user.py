"""Known defects seeded into the `problem_user` account.

Each test asserts the *correct* behaviour and is marked xfail (strict), so
the suite stays green while the defect exists and turns red the day it is
fixed — a signal to close the bug report. See docs/bug-reports.md.
"""

import pytest
from playwright.sync_api import Page, expect

from pages import CartPage, CheckoutInfoPage, CheckoutOverviewPage, InventoryPage
from utils.data import CUSTOMER, PRODUCTS

pytestmark = pytest.mark.known_bug


@pytest.mark.xfail(reason="BUG-001: every product shows the same placeholder image")
def test_each_product_has_its_own_image(problem_inventory_page: InventoryPage) -> None:
    """Every product card should display a distinct product photo."""
    images = problem_inventory_page.item_images
    expect(images).to_have_count(len(PRODUCTS))

    sources = [images.nth(i).get_attribute("src") for i in range(images.count())]
    assert len(set(sources)) == len(PRODUCTS), f"image sources: {sources}"


@pytest.mark.xfail(reason="BUG-002: sorting dropdown has no effect for problem_user")
def test_sort_by_price_low_to_high(problem_inventory_page: InventoryPage) -> None:
    """Selecting 'Price (low to high)' should reorder the grid."""
    problem_inventory_page.sort_by("price_asc")

    expected = [f"${price:.2f}" for price in sorted(PRODUCTS.values())]
    expect(problem_inventory_page.item_prices).to_have_text(expected, timeout=5_000)


@pytest.mark.xfail(reason="BUG-003: 'Add to cart' does nothing for some products")
def test_add_every_product_to_cart(problem_inventory_page: InventoryPage) -> None:
    """Clicking 'Add to cart' on all six products should put six items in the cart."""
    problem_inventory_page.add_to_cart(*PRODUCTS)

    expect(problem_inventory_page.cart_badge).to_have_text(str(len(PRODUCTS)), timeout=5_000)


@pytest.mark.xfail(reason="BUG-004: Last Name field cannot be filled, checkout is blocked")
def test_checkout_with_valid_information(problem_inventory_page: InventoryPage, page: Page) -> None:
    """A fully filled information form should lead to the order overview."""
    problem_inventory_page.add_to_cart("Sauce Labs Backpack")
    problem_inventory_page.open_cart()
    CartPage(page).checkout()

    CheckoutInfoPage(page).fill_info(**CUSTOMER)

    expect(page).to_have_url(CheckoutOverviewPage.url_pattern(), timeout=5_000)
