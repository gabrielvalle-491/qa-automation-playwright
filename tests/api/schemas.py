"""JSON Schemas for the JSONPlaceholder resources under test."""

from typing import Any

POST_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["userId", "id", "title", "body"],
    "properties": {
        "userId": {"type": "integer", "minimum": 1},
        "id": {"type": "integer", "minimum": 1},
        "title": {"type": "string", "minLength": 1},
        "body": {"type": "string", "minLength": 1},
    },
    "additionalProperties": False,
}

COMMENT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["postId", "id", "name", "email", "body"],
    "properties": {
        "postId": {"type": "integer"},
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string", "pattern": r"^[^@\s]+@[^@\s]+\.[^@\s]+$"},
        "body": {"type": "string"},
    },
}

USER_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["id", "name", "username", "email", "address", "phone", "website", "company"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string", "pattern": r"^[^@\s]+@[^@\s]+\.[^@\s]+$"},
        "address": {
            "type": "object",
            "required": ["street", "city", "zipcode", "geo"],
            "properties": {
                "geo": {
                    "type": "object",
                    "required": ["lat", "lng"],
                    "properties": {"lat": {"type": "string"}, "lng": {"type": "string"}},
                }
            },
        },
        "company": {"type": "object", "required": ["name"]},
    },
}
