"""Login and logout scenarios."""

import pytest
from playwright.sync_api import Page, expect

from pages import InventoryPage, LoginPage
from utils.data import LOCKED_OUT_USER, PASSWORD, STANDARD_USER


@pytest.mark.smoke
def test_valid_login_opens_inventory(login_page: LoginPage, page: Page) -> None:
    """standard_user lands on the product list."""
    login_page.login_as(STANDARD_USER)

    expect(page).to_have_url(InventoryPage.url_pattern())
    expect(InventoryPage(page).title).to_have_text("Products")


def test_locked_out_user_is_rejected(login_page: LoginPage, page: Page) -> None:
    """locked_out_user gets a clear error and stays on the login page."""
    login_page.login_as(LOCKED_OUT_USER)

    expect(login_page.error).to_have_text("Epic sadface: Sorry, this user has been locked out.")
    expect(page).not_to_have_url(InventoryPage.url_pattern())


def test_wrong_password_shows_error(login_page: LoginPage) -> None:
    """A valid username with a wrong password is rejected."""
    login_page.login(STANDARD_USER.username, "wrong_password")

    expect(login_page.error).to_have_text(
        "Epic sadface: Username and password do not match any user in this service"
    )


@pytest.mark.parametrize(
    ("username", "password", "message"),
    [
        ("", "", "Epic sadface: Username is required"),
        ("", PASSWORD, "Epic sadface: Username is required"),
        (STANDARD_USER.username, "", "Epic sadface: Password is required"),
    ],
    ids=["both-empty", "empty-username", "empty-password"],
)
def test_empty_fields_show_required_error(
    login_page: LoginPage, username: str, password: str, message: str
) -> None:
    """Required-field validation fires before any credential check."""
    login_page.login(username, password)

    expect(login_page.error).to_have_text(message)


def test_error_message_can_be_dismissed(login_page: LoginPage) -> None:
    """The X button on the error banner hides it."""
    login_page.login("", "")
    expect(login_page.error).to_be_visible()

    login_page.error_close.click()

    expect(login_page.error).to_be_hidden()


@pytest.mark.smoke
def test_logout_returns_to_login(inventory_page: InventoryPage, page: Page) -> None:
    """Logging out from the menu goes back to the login form."""
    inventory_page.logout()

    login = LoginPage(page)
    expect(login.login_button).to_be_visible()
    expect(login.username).to_have_value("")


def test_inventory_requires_session_after_logout(inventory_page: InventoryPage, page: Page) -> None:
    """After logout, deep-linking to the inventory is blocked."""
    inventory_page.logout()
    login = LoginPage(page)
    expect(login.login_button).to_be_visible()

    inventory_page.open()

    expect(login.error).to_have_text(
        "Epic sadface: You can only access '/inventory.html' when you are logged in."
    )
