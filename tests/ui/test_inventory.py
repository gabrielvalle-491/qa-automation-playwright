"""Product list content and sorting."""

import pytest
from playwright.sync_api import expect

from pages import InventoryPage
from utils.data import PRODUCTS


def test_all_products_are_listed(inventory_page: InventoryPage) -> None:
    """The six catalogue products are shown with their published prices."""
    expect(inventory_page.items).to_have_count(len(PRODUCTS))

    displayed = dict(zip(inventory_page.names(), inventory_page.prices(), strict=True))
    assert displayed == PRODUCTS


def test_default_sort_is_name_ascending(inventory_page: InventoryPage) -> None:
    """Without any interaction products are ordered A to Z."""
    expect(inventory_page.item_names).to_have_text(sorted(PRODUCTS))


@pytest.mark.parametrize(
    ("option", "reverse"),
    [("name_asc", False), ("name_desc", True)],
    ids=["a-to-z", "z-to-a"],
)
def test_sort_by_name(inventory_page: InventoryPage, option: str, reverse: bool) -> None:
    """Name sorting orders the grid alphabetically."""
    inventory_page.sort_by(option)

    expect(inventory_page.item_names).to_have_text(sorted(PRODUCTS, reverse=reverse))


@pytest.mark.parametrize(
    ("option", "reverse"),
    [("price_asc", False), ("price_desc", True)],
    ids=["low-to-high", "high-to-low"],
)
def test_sort_by_price(inventory_page: InventoryPage, option: str, reverse: bool) -> None:
    """Price sorting orders the grid numerically."""
    inventory_page.sort_by(option)

    expected = [f"${price:.2f}" for price in sorted(PRODUCTS.values(), reverse=reverse)]
    expect(inventory_page.item_prices).to_have_text(expected)
