"""Shared UI fixtures built on top of pytest-playwright's `page` fixture."""

import pytest
from playwright.sync_api import Page, expect

from pages import InventoryPage, LoginPage
from utils.data import PROBLEM_USER, STANDARD_USER, User

# Auto-waiting assertions retry for up to 10 s (Playwright default is 5 s),
# which absorbs slow CI networks without hiding real failures.
expect.set_options(timeout=10_000)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Login page, already opened."""
    login = LoginPage(page)
    login.open()
    return login


def _login(page: Page, user: User) -> InventoryPage:
    login = LoginPage(page)
    login.open()
    login.login_as(user)
    inventory = InventoryPage(page)
    expect(page).to_have_url(f"**{InventoryPage.path}")
    return inventory


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    """Inventory page after logging in as standard_user."""
    return _login(page, STANDARD_USER)


@pytest.fixture
def problem_inventory_page(page: Page) -> InventoryPage:
    """Inventory page after logging in as problem_user (has seeded defects)."""
    return _login(page, PROBLEM_USER)


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Auto-apply `ui` / `api` markers based on the test folder."""
    for item in items:
        path = str(item.path)
        if "/tests/ui/" in path:
            item.add_marker(pytest.mark.ui)
        elif "/tests/api/" in path:
            item.add_marker(pytest.mark.api)
