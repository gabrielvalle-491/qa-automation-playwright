# QA Automation with Playwright + pytest

[![CI](https://github.com/gabrielvalle-491/qa-automation-playwright/actions/workflows/ci.yml/badge.svg)](https://github.com/gabrielvalle-491/qa-automation-playwright/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Playwright](https://img.shields.io/badge/playwright-1.63-2EAD33)
![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey)

*Leer en [español](README.es.md).*

A portfolio project showing how I test a web application end to end: a **UI test suite**
for the [Sauce Demo](https://www.saucedemo.com) shop written with **Playwright + pytest**
and the **Page Object Model**, a small **REST API suite** for
[JSONPlaceholder](https://jsonplaceholder.typicode.com), **QA documentation**
(test plan, test cases, bug reports) and **CI on GitHub Actions** that runs everything on
every push and publishes an HTML report.

> This is a personal portfolio project against public demo sites — not client work.

## What is tested

| Area | Tests | Highlights |
|------|------:|-----------|
| Login / logout | 9 | valid login, locked-out user, wrong password, empty fields (parametrized), dismiss error, logout, deep link blocked after logout |
| Inventory | 6 | catalogue names and prices, default order, sort by name and price in both directions |
| Cart | 6 | add/remove from grid and cart page, badge count, cart kept while navigating |
| Checkout | 6 | full order to confirmation, required-field validation (×3), **item total + 8 % tax = total**, cancel |
| Known bugs (`problem_user`) | 4 | wrong images, broken sorting, add-to-cart failing, broken Last Name field — `xfail(strict=True)` |
| REST API | 12 | GET/POST/PUT/PATCH/DELETE, filters, nested routes, 404, JSON Schema validation, response time |
| **Total** | **43** | |

Every automated test is mapped to a test case ID in [`docs/test-cases.md`](docs/test-cases.md).

## Results

Output copied from a real CI run
([run #2](https://github.com/gabrielvalle-491/qa-automation-playwright/actions/runs/37161068047),
Chromium headless on `ubuntu-latest`, 2026-10-03):

```
collected 43 items

tests/api/test_posts.py .........                                        [ 20%]
tests/api/test_users.py ...                                              [ 27%]
tests/ui/test_cart.py ......                                             [ 41%]
tests/ui/test_checkout.py ....                                           [ 51%]
tests/ui/test_inventory.py ....                                          [ 60%]
tests/ui/test_login.py .......                                           [ 76%]
tests/ui/test_problem_user.py xxxx                                       [ 86%]
tests/ui/test_checkout.py .                                              [ 88%]
tests/ui/test_inventory.py ..                                            [ 93%]
tests/ui/test_login.py .                                                 [ 95%]
tests/ui/test_checkout.py .                                              [ 97%]
tests/ui/test_login.py .                                                 [100%]

=========================== short test summary info ============================
XFAIL tests/ui/test_problem_user.py::test_each_product_has_its_own_image[chromium] - BUG-001: every product shows the same placeholder image
XFAIL tests/ui/test_problem_user.py::test_sort_by_price_low_to_high[chromium] - BUG-002: sorting dropdown has no effect for problem_user
XFAIL tests/ui/test_problem_user.py::test_add_every_product_to_cart[chromium] - BUG-003: 'Add to cart' does nothing for some products
XFAIL tests/ui/test_problem_user.py::test_checkout_with_valid_information[chromium] - BUG-004: Last Name field cannot be filled, checkout is blocked
======================== 39 passed, 4 xfailed in 32.96s ========================
```

- **39 passed** — every functional check for `standard_user` and the API.
- **4 xfailed** — real defects of `problem_user`, written up in [`docs/bug-reports.md`](docs/bug-reports.md).
  They are *strict* xfails: if one of them is ever fixed the suite turns red, so the bug report can be closed.

The HTML report (and screenshots of any failure) is attached to each run as the
`test-report` artifact: open the run in the **Actions** tab → *Artifacts*.

## Project structure

```
qa-automation-playwright/
├── pages/                    # Page Object Model
│   ├── base_page.py          #   header, menu, logout, URL helpers
│   ├── login_page.py
│   ├── inventory_page.py     #   sorting, add/remove buttons
│   ├── cart_page.py
│   └── checkout_page.py      #   info form, overview totals, confirmation
├── tests/
│   ├── ui/                   # Playwright tests (saucedemo.com)
│   │   ├── test_login.py
│   │   ├── test_inventory.py
│   │   ├── test_cart.py
│   │   ├── test_checkout.py
│   │   └── test_problem_user.py   # known bugs (xfail)
│   └── api/                  # requests tests (jsonplaceholder)
│       ├── conftest.py       #   ApiClient fixture
│       ├── schemas.py        #   JSON Schemas
│       ├── test_posts.py
│       └── test_users.py
├── utils/data.py             # demo users, product catalogue, tax rate
├── conftest.py               # login fixtures, auto ui/api markers
├── docs/
│   ├── test-plan.md
│   ├── test-cases.md
│   └── bug-reports.md
├── .github/workflows/ci.yml  # lint + tests + HTML report artifact
├── pytest.ini
└── requirements.txt
```

## How to run

Requirements: Python 3.11+.

```bash
git clone https://github.com/gabrielvalle-491/qa-automation-playwright.git
cd qa-automation-playwright
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

pytest                                   # everything (headless)
pytest -m api                            # API tests only
pytest -m ui --headed --slowmo 300       # watch the browser
pytest -m smoke                          # critical path only
pytest --html=reports/report.html --self-contained-html   # HTML report
```

Useful markers: `ui`, `api`, `smoke`, `known_bug`.

## Design decisions

- **Page Object Model** — locators live in one place; tests read like the test cases.
- **`data-test` locators** — stable against CSS/layout changes.
- **No `sleep()`** — only Playwright auto-waiting (`expect(...)` web-first assertions),
  which retries until the condition is true or the 10 s timeout expires.
- **Isolated tests** — fresh browser context per test, login via fixtures, any order works.
- **Parametrized data** — validation and sorting cases share one test body.
- **Strict xfail for known bugs** — the suite stays green, the bugs stay visible.
- **Schema validation** for API responses with `jsonschema`, not just status codes.

## Tools

Python 3.11 · pytest · Playwright (sync API) · pytest-playwright · pytest-html · requests ·
jsonschema · ruff · GitHub Actions

## Documentation

- [Test plan](docs/test-plan.md) — scope, approach, environments, entry/exit criteria, risks
- [Test cases](docs/test-cases.md) — 47 cases with priority and automation status
- [Bug reports](docs/bug-reports.md) — 4 defects with steps, expected vs actual, severity and evidence

## Other projects

[pdf-invoice-to-excel](https://github.com/gabrielvalle-491/pdf-invoice-to-excel) ·
[excel-data-cleaner](https://github.com/gabrielvalle-491/excel-data-cleaner) ·
[lead-management-automation](https://github.com/gabrielvalle-491/lead-management-automation) ·
[business-kpi-dashboard](https://github.com/gabrielvalle-491/business-kpi-dashboard) ·
[ai-document-assistant](https://github.com/gabrielvalle-491/ai-document-assistant)

## License

[MIT](LICENSE) © 2026 Gabriel Valle

---

**Gabriel Valle — QA & Automation · Villa Mercedes, Argentina · Remote**
