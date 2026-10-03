# Bug Reports — Sauce Demo (`problem_user`)

These defects are seeded on purpose by the Sauce Demo team for the `problem_user` account.
They are written up here as they would be in a real tracker, using what the automated
suite actually observed in CI.

**Environment for all reports**

| Item | Value |
|------|-------|
| URL | https://www.saucedemo.com |
| Account | `problem_user` / `secret_sauce` (public demo account) |
| Browser | Chromium (Chrome for Testing 153.0.8010.12), headless, Playwright 1.63.0 |
| OS | Ubuntu 24.04 (GitHub Actions `ubuntu-latest`) |
| Date observed | 2026-10-03 |
| Evidence | [CI run #2](https://github.com/gabrielvalle-491/qa-automation-playwright/actions/runs/37161068047) — step *"Show known-bug evidence"* re-runs the `known_bug` tests with `--runxfail` and prints the real assertion output |
| Control | The same steps with `standard_user` pass (see `tests/ui/test_inventory.py`, `test_cart.py`, `test_checkout.py`) |

---

## BUG-001 — All products on the inventory page show the same image

| Field | Value |
|-------|-------|
| Severity | Minor (cosmetic, but misleads the buyer) |
| Priority | P2 |
| Component | Inventory page |
| Automated test | `tests/ui/test_problem_user.py::test_each_product_has_its_own_image` (xfail) |

**Steps to reproduce**
1. Open https://www.saucedemo.com.
2. Log in as `problem_user` / `secret_sauce`.
3. Look at the product images on the inventory page.

**Expected result:** each of the 6 products shows its own photo (backpack, bike light, t-shirts, jacket, onesie).

**Actual result:** all 6 product cards display the same picture (a dog). The `src` of every image is identical:

```
['/assets/sl-404-Cq1a9k9X.jpg', '/assets/sl-404-Cq1a9k9X.jpg', '/assets/sl-404-Cq1a9k9X.jpg',
 '/assets/sl-404-Cq1a9k9X.jpg', '/assets/sl-404-Cq1a9k9X.jpg', '/assets/sl-404-Cq1a9k9X.jpg']
assert 1 == 6   # distinct image sources vs. products
```

The file name `sl-404` suggests the app falls back to a "not found" placeholder for every product.

---

## BUG-002 — Sorting dropdown does not reorder products

| Field | Value |
|-------|-------|
| Severity | Major (core browsing feature does not work) |
| Priority | P2 |
| Component | Inventory page — sort control |
| Automated test | `tests/ui/test_problem_user.py::test_sort_by_price_low_to_high` (xfail) |

**Steps to reproduce**
1. Log in as `problem_user` / `secret_sauce`.
2. Open the sort dropdown (top right) and select **Price (low to high)**.

**Expected result:** products are listed by ascending price:
`$7.99, $9.99, $15.99, $15.99, $29.99, $49.99`.

**Actual result:** the order does not change (it stays in the default A→Z order) even after waiting 5 seconds:

```
Locator expected to have text ['$7.99', '$9.99', '$15.99', '$15.99', '$29.99', '$49.99']
Actual value:                 ['$29.99', '$9.99', '$15.99', '$49.99', '$7.99', '$15.99']
```

No error message is shown to the user, so they cannot tell the sort failed.

---

## BUG-003 — "Add to cart" does nothing for half of the products

| Field | Value |
|-------|-------|
| Severity | Critical (customer cannot buy some products → lost revenue) |
| Priority | P1 |
| Component | Inventory page — cart buttons |
| Automated test | `tests/ui/test_problem_user.py::test_add_every_product_to_cart` (xfail) |

**Steps to reproduce**
1. Log in as `problem_user` / `secret_sauce`.
2. Click **Add to cart** on each of the 6 products, top to bottom.
3. Check the cart badge in the header.

**Expected result:** cart badge shows **6**.

**Actual result:** cart badge shows **3**. For three of the products the click has no effect — no item is added and no error is shown:

```
Locator expected to have text '6'
Actual value: 3
  locator resolved to <span class="shopping_cart_badge" data-test="shopping-cart-badge">3</span>
```

**Notes:** the test clicks each button once and Playwright confirms every click was delivered
(actionability checks passed), so this is not a timing issue in the test.

---

## BUG-004 — Typing in "Last Name" writes into "First Name"; checkout is blocked

| Field | Value |
|-------|-------|
| Severity | Critical (no order can be completed) |
| Priority | P1 |
| Component | Checkout — Your Information form |
| Automated test | `tests/ui/test_problem_user.py::test_checkout_with_valid_information` (xfail) |

**Steps to reproduce**
1. Log in as `problem_user` / `secret_sauce`.
2. Add **Sauce Labs Backpack** to the cart and open the cart.
3. Click **Checkout**.
4. Type `Gabriel` in First Name, `Valle` in Last Name, `5730` in Zip/Postal Code.
5. Click **Continue**.

**Expected result:** the Checkout: Overview page (`/checkout-step-two.html`) opens.

**Actual result:** the user stays on `/checkout-step-one.html`. The text typed into Last Name
ends up in the First Name field, Last Name stays empty, and the form shows
*"Error: Last Name is required"*. Page state captured by Playwright:

```
- form "Checkout information":
    - textbox "First Name": Valle
    - textbox "Last Name"
    - textbox "Zip/Postal Code": "5730"
    - alert: "Error: Last Name is required"
```

**Impact:** the checkout cannot be completed by any means for this user, so it blocks all purchases.
