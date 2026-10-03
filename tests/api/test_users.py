"""Read-only checks for the /users resource."""

from jsonschema import validate

from tests.api.conftest import ApiClient
from tests.api.schemas import USER_SCHEMA


def test_list_users_schema(api: ApiClient) -> None:
    """GET /users returns 10 users with unique ids and valid nested objects."""
    response = api.get("/users")

    assert response.status_code == 200
    users = response.json()
    assert len(users) == 10
    for user in users:
        validate(user, USER_SCHEMA)
    assert len({user["id"] for user in users}) == len(users)


def test_user_posts_belong_to_user(api: ApiClient) -> None:
    """Nested route /users/2/posts only returns posts written by user 2."""
    response = api.get("/users/2/posts")

    assert response.status_code == 200
    posts = response.json()
    assert posts, "expected at least one post"
    assert all(post["userId"] == 2 for post in posts)


def test_response_time_is_acceptable(api: ApiClient) -> None:
    """A simple read answers in under 3 seconds (generous budget for CI networks)."""
    response = api.get("/users/1")

    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 3
