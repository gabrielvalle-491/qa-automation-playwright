"""Fixtures for the JSONPlaceholder REST API tests."""

from collections.abc import Iterator
from typing import Any

import pytest
import requests

API_BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT_SECONDS = 15


class ApiClient:
    """Thin wrapper over requests.Session that prefixes the base URL and sets a timeout."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(
            {"Accept": "application/json", "User-Agent": "qa-automation-playwright/1.0"}
        )

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        """Send a request to `base_url + path`."""
        kwargs.setdefault("timeout", TIMEOUT_SECONDS)
        return self.session.request(method, f"{self.base_url}{path}", **kwargs)

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", path, **kwargs)


@pytest.fixture(scope="session")
def api() -> Iterator[ApiClient]:
    """One HTTP session shared by all API tests."""
    client = ApiClient(API_BASE_URL)
    yield client
    client.session.close()
