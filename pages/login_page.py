"""Login page object."""

from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.data import User


class LoginPage(BasePage):
    """The landing page with the username/password form."""

    path = "/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username = page.locator('[data-test="username"]')
        self.password = page.locator('[data-test="password"]')
        self.login_button = page.locator('[data-test="login-button"]')
        self.error = page.locator('[data-test="error"]')
        self.error_close = page.locator('[data-test="error-button"]')

    def login(self, username: str, password: str) -> None:
        """Fill the form with raw values and submit it."""
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()

    def login_as(self, user: User) -> None:
        """Log in with one of the predefined demo accounts."""
        self.login(user.username, user.password)
