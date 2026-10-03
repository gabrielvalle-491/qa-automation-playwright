# Test Plan — Sauce Demo & JSONPlaceholder

| Item | Detail |
|------|--------|
| Project | QA automation portfolio (personal project, not client work) |
| Author | Gabriel Valle |
| Version | 1.0 — October 2026 |
| Systems under test | [Sauce Demo](https://www.saucedemo.com) web shop (UI) · [JSONPlaceholder](https://jsonplaceholder.typicode.com) REST API |

## 1. Objective

Verify that the core purchase journey of the Sauce Demo shop works for a regular customer,
that input validation protects the flow, and that the seeded defects of the `problem_user`
account are detected and documented. Separately, verify the contract (status codes, payload
shape) of a public REST API.

## 2. Scope

### In scope

| Area | What is covered |
|------|-----------------|
| Authentication | Valid login, locked-out account, wrong password, required fields, error dismissal, logout, session protection of deep links |
| Inventory | Product list content and prices, default order, sorting by name and price (both directions) |
| Cart | Add/remove from grid and from cart page, badge count, persistence while navigating |
| Checkout | Happy path to confirmation, required-field validation, item total / tax / total calculation, cancel |
| Known defects | `problem_user` images, sorting, add-to-cart and checkout form (tracked as `xfail`) |
| API | `/posts` CRUD (GET/POST/PUT/PATCH/DELETE), filtering, nested routes, 404, JSON Schema of posts/comments/users, basic response time |

### Out of scope

- Performance/load testing, security testing, accessibility audit.
- Visual regression (pixel comparison).
- `performance_glitch_user`, `error_user` and `visual_user` accounts.
- Browsers other than Chromium (the framework supports Firefox/WebKit via `--browser`, but CI runs Chromium only).
- Persistence of API writes — JSONPlaceholder does not store them by design.

## 3. Approach

- **UI:** Python + pytest + Playwright (sync API) with the **Page Object Model** (`pages/`).
  Locators use the site's `data-test` attributes, which are stable and independent of styling.
- **Waiting strategy:** only Playwright auto-waiting (`expect(...)` web-first assertions and
  actionability checks). No `sleep()` calls.
- **Test independence:** every test gets a fresh browser context (pytest-playwright default),
  logs in through a fixture and does not depend on other tests.
- **Data-driven:** validation and sorting cases use `pytest.mark.parametrize`.
- **Known bugs:** written as tests of the *expected* behaviour and marked
  `xfail(strict=True)` with the bug id, so the suite is green while the bug exists and fails
  as soon as the bug is fixed (reminder to close the report).
- **API:** pytest + requests, response bodies validated with `jsonschema`.
- **Techniques:** equivalence partitioning (valid / invalid / empty credentials),
  boundary-style checks on totals, negative testing, state-transition checks on the cart.

## 4. Environments

| Item | Value |
|------|-------|
| UI base URL | https://www.saucedemo.com (public demo, production-like) |
| API base URL | https://jsonplaceholder.typicode.com |
| Browser | Chromium (headless in CI, headed optional locally) |
| Runtime | Python 3.11, versions pinned in `requirements.txt` |
| CI | GitHub Actions, `ubuntu-latest`, on every push / pull request |
| Test accounts | Public demo accounts shown on the login page (`standard_user`, `locked_out_user`, `problem_user`, password `secret_sauce`) |

## 5. Entry criteria

- Both target sites are reachable (HTTP 200 on the home page / `/posts/1`).
- Dependencies install cleanly and `playwright install chromium` succeeds.
- Lint (`ruff`) passes.

## 6. Exit criteria

- 100 % of non-`known_bug` tests pass on CI.
- Every `known_bug` test is reported as `xfailed` (no unexpected `xpass`).
- Every failing behaviour has a bug report in [`bug-reports.md`](bug-reports.md).
- HTML report is published as a CI artifact.

## 7. Risks and mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Public demo sites change markup or content without notice | Tests break for non-product reasons | `data-test` locators, Page Objects isolate changes to one file |
| Network latency / slow CI runners | Flaky timeouts | Auto-waiting assertions with a 10 s budget, no fixed sleeps |
| Third-party outage or rate limiting | Whole suite red | Re-run job once to confirm; entry criteria check reachability |
| Seeded `problem_user` defects get fixed upstream | `xfail` turns into `XPASS` → failure | Strict xfail makes this visible; update bug report and test |
| JSONPlaceholder does not persist writes | False expectations in CRUD tests | Tests assert only on the immediate response |

## 8. Deliverables

- Automated suite (`tests/ui`, `tests/api`) and Page Objects (`pages/`).
- [Test cases](test-cases.md) and [bug reports](bug-reports.md).
- CI workflow with downloadable HTML report.
