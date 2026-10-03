"""Shared test data for the Sauce Demo suite.

The credentials below are the public demo accounts printed on the
https://www.saucedemo.com login page; they are not secrets.
"""

from dataclasses import dataclass

PASSWORD = "secret_sauce"


@dataclass(frozen=True)
class User:
    """A Sauce Demo account."""

    username: str
    password: str = PASSWORD


STANDARD_USER = User("standard_user")
LOCKED_OUT_USER = User("locked_out_user")
PROBLEM_USER = User("problem_user")

# Catalogue as published by the demo shop (name -> price in USD).
PRODUCTS: dict[str, float] = {
    "Sauce Labs Backpack": 29.99,
    "Sauce Labs Bike Light": 9.99,
    "Sauce Labs Bolt T-Shirt": 15.99,
    "Sauce Labs Fleece Jacket": 49.99,
    "Sauce Labs Onesie": 7.99,
    "Test.allTheThings() T-Shirt (Red)": 15.99,
}

TAX_RATE = 0.08

CUSTOMER = {"first_name": "Gabriel", "last_name": "Valle", "postal_code": "5730"}
