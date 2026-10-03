"""Adding and removing products, cart badge and cart page."""

import pytest
from playwright.sync_api import Page, expect

from pages import CartPage, InventoryPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"
ONESIE = "Sauce Labs Onesie"


@pytest.mark.smoke
def test_add_single_item_updates_badge(inventory_page: InventoryPage) -> None:
    """Adding one product shows badge '1' and flips the button to Remove."""
    expect(inventory_page.cart_badge).to_be_hidden()

    inventory_page.add_to_cart(BACKPACK)

    expect(inventory_page.cart_badge).to_have_text("1")
    expect(inventory_page.remove_button(BACKPACK)).to_be_visible()


def test_badge_counts_multiple_items(inventory_page: InventoryPage) -> None:
    """The badge reflects the number of distinct products added."""
    inventory_page.add_to_cart(BACKPACK, BIKE_LIGHT, ONESIE)

    expect(inventory_page.cart_badge).to_have_text("3")


def test_remove_from_inventory_updates_badge(inventory_page: InventoryPage) -> None:
    """Removing products from the grid decrements and finally hides the badge."""
    inventory_page.add_to_cart(BACKPACK, BIKE_LIGHT)
    expect(inventory_page.cart_badge).to_have_text("2")

    inventory_page.remove_from_cart(BACKPACK)
    expect(inventory_page.cart_badge).to_have_text("1")

    inventory_page.remove_from_cart(BIKE_LIGHT)
    expect(inventory_page.cart_badge).to_be_hidden()
    expect(inventory_page.add_button(BIKE_LIGHT)).to_be_visible()


def test_cart_page_lists_added_items(inventory_page: InventoryPage, page: Page) -> None:
    """Products added from the grid appear on the cart page."""
    inventory_page.add_to_cart(BACKPACK, ONESIE)

    inventory_page.open_cart()

    cart = CartPage(page)
    expect(cart.item_names).to_have_text([BACKPACK, ONESIE])


def test_remove_item_on_cart_page(inventory_page: InventoryPage, page: Page) -> None:
    """Removing a product on the cart page removes its row and updates the badge."""
    inventory_page.add_to_cart(BACKPACK, BIKE_LIGHT)
    inventory_page.open_cart()
    cart = CartPage(page)

    cart.remove(BACKPACK)

    expect(cart.item_names).to_have_text([BIKE_LIGHT])
    expect(cart.cart_badge).to_have_text("1")


def test_cart_persists_after_continue_shopping(inventory_page: InventoryPage, page: Page) -> None:
    """Going back to the shop keeps the cart contents and button states."""
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.open_cart()

    CartPage(page).continue_shopping_button.click()

    expect(page).to_have_url(InventoryPage.url_pattern())
    expect(inventory_page.cart_badge).to_have_text("1")
    expect(inventory_page.remove_button(BACKPACK)).to_be_visible()
