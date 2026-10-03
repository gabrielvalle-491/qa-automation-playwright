"""CRUD checks for the /posts resource.

JSONPlaceholder is a fake API: writes are accepted and echoed back but not
persisted, so each test asserts on the response it gets, not on later reads.
"""

import pytest
from jsonschema import validate

from tests.api.conftest import ApiClient
from tests.api.schemas import COMMENT_SCHEMA, POST_SCHEMA

NEW_POST = {"title": "QA portfolio", "body": "Automated with pytest + requests", "userId": 1}


@pytest.mark.smoke
def test_list_posts(api: ApiClient) -> None:
    """GET /posts returns 100 posts that all match the schema."""
    response = api.get("/posts")

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
    posts = response.json()
    assert len(posts) == 100
    for post in posts:
        validate(post, POST_SCHEMA)


def test_get_single_post(api: ApiClient) -> None:
    """GET /posts/1 returns exactly that post."""
    response = api.get("/posts/1")

    assert response.status_code == 200
    post = response.json()
    validate(post, POST_SCHEMA)
    assert post["id"] == 1
    assert post["userId"] == 1


def test_get_missing_post_returns_404(api: ApiClient) -> None:
    """Unknown ids return 404 with an empty JSON object."""
    response = api.get("/posts/99999")

    assert response.status_code == 404
    assert response.json() == {}


def test_filter_posts_by_user(api: ApiClient) -> None:
    """The userId query parameter filters the collection."""
    response = api.get("/posts", params={"userId": 3})

    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 10
    assert {post["userId"] for post in posts} == {3}


def test_post_comments(api: ApiClient) -> None:
    """Nested route /posts/1/comments returns that post's comments."""
    response = api.get("/posts/1/comments")

    assert response.status_code == 200
    comments = response.json()
    assert len(comments) == 5
    for comment in comments:
        validate(comment, COMMENT_SCHEMA)
        assert comment["postId"] == 1


def test_create_post(api: ApiClient) -> None:
    """POST /posts returns 201 and echoes the payload with a new id."""
    response = api.post("/posts", json=NEW_POST)

    assert response.status_code == 201
    created = response.json()
    validate(created, POST_SCHEMA)
    assert created == {**NEW_POST, "id": 101}


def test_replace_post(api: ApiClient) -> None:
    """PUT /posts/1 replaces the whole resource."""
    payload = {**NEW_POST, "id": 1, "title": "Updated title"}

    response = api.put("/posts/1", json=payload)

    assert response.status_code == 200
    assert response.json() == payload


def test_patch_post(api: ApiClient) -> None:
    """PATCH /posts/1 updates only the sent fields."""
    response = api.patch("/posts/1", json={"title": "Patched title"})

    assert response.status_code == 200
    post = response.json()
    validate(post, POST_SCHEMA)
    assert post["id"] == 1
    assert post["title"] == "Patched title"


def test_delete_post(api: ApiClient) -> None:
    """DELETE /posts/1 succeeds with an empty body."""
    response = api.delete("/posts/1")

    assert response.status_code == 200
    assert response.json() == {}
