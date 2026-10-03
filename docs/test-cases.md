# Test Cases

Priority: **P1** = critical path / release blocker · **P2** = important · **P3** = nice to have.
Automated tests live in `tests/`; the last column gives the test function.

Common precondition for UI cases (unless stated): browser on https://www.saucedemo.com, fresh session.
`standard_user` / `secret_sauce` are the public demo credentials.

## Authentication

| ID | Title | Preconditions | Steps | Expected result | Priority | Automated |
|----|-------|---------------|-------|-----------------|----------|-----------|
| TC-LOGIN-01 | Valid login | — | 1. Enter `standard_user` / `secret_sauce` 2. Click Login | Inventory page opens, title "Products" | P1 | Yes — `test_valid_login_opens_inventory` |
| TC-LOGIN-02 | Locked-out user | — | 1. Enter `locked_out_user` / `secret_sauce` 2. Click Login | Error "Sorry, this user has been locked out."; stays on login | P1 | Yes — `test_locked_out_user_is_rejected` |
| TC-LOGIN-03 | Wrong password | — | 1. Enter `standard_user` / `wrong_password` 2. Click Login | Error "Username and password do not match any user in this service" | P1 | Yes — `test_wrong_password_shows_error` |
| TC-LOGIN-04 | Both fields empty | — | 1. Leave fields empty 2. Click Login | Error "Username is required" | P2 | Yes — `test_empty_fields_show_required_error[both-empty]` |
| TC-LOGIN-05 | Empty username | — | 1. Enter only password 2. Click Login | Error "Username is required" | P2 | Yes — `test_empty_fields_show_required_error[empty-username]` |
| TC-LOGIN-06 | Empty password | — | 1. Enter only username 2. Click Login | Error "Password is required" | P2 | Yes — `test_empty_fields_show_required_error[empty-password]` |
| TC-LOGIN-07 | Dismiss error banner | An error is displayed | 1. Click the X on the error | Error banner disappears | P3 | Yes — `test_error_message_can_be_dismissed` |
| TC-LOGIN-08 | Logout | Logged in | 1. Open menu 2. Click Logout | Login form shown with empty username | P1 | Yes — `test_logout_returns_to_login` |
| TC-LOGIN-09 | Protected page after logout | Logged in, then logged out | 1. Navigate to `/inventory.html` | Error "You can only access '/inventory.html' when you are logged in." | P1 | Yes — `test_inventory_requires_session_after_logout` |
| TC-LOGIN-10 | Password field is masked | — | 1. Type in Password | Characters are hidden (type=password) | P3 | No (manual) |

## Inventory

| ID | Title | Preconditions | Steps | Expected result | Priority | Automated |
|----|-------|---------------|-------|-----------------|----------|-----------|
| TC-INV-01 | Catalogue content | Logged in as `standard_user` | 1. View inventory | 6 products with the published names and prices | P1 | Yes — `test_all_products_are_listed` |
| TC-INV-02 | Default order | Logged in | 1. View inventory without sorting | Products ordered by name A→Z | P2 | Yes — `test_default_sort_is_name_ascending` |
| TC-INV-03 | Sort name A→Z | Logged in | 1. Select "Name (A to Z)" | Names ascending | P2 | Yes — `test_sort_by_name[a-to-z]` |
| TC-INV-04 | Sort name Z→A | Logged in | 1. Select "Name (Z to A)" | Names descending | P2 | Yes — `test_sort_by_name[z-to-a]` |
| TC-INV-05 | Sort price low→high | Logged in | 1. Select "Price (low to high)" | Prices ascending | P2 | Yes — `test_sort_by_price[low-to-high]` |
| TC-INV-06 | Sort price high→low | Logged in | 1. Select "Price (high to low)" | Prices descending | P2 | Yes — `test_sort_by_price[high-to-low]` |
| TC-INV-07 | Product detail page | Logged in | 1. Click a product name | Detail page of that product with same price | P2 | No (manual) |

## Cart

| ID | Title | Preconditions | Steps | Expected result | Priority | Automated |
|----|-------|---------------|-------|-----------------|----------|-----------|
| TC-CART-01 | Add one item | Logged in, empty cart | 1. Click "Add to cart" on Backpack | Badge shows 1, button changes to "Remove" | P1 | Yes — `test_add_single_item_updates_badge` |
| TC-CART-02 | Badge counts several items | Logged in, empty cart | 1. Add Backpack, Bike Light, Onesie | Badge shows 3 | P1 | Yes — `test_badge_counts_multiple_items` |
| TC-CART-03 | Remove from inventory | 2 items in cart | 1. Click Remove on each | Badge 2 → 1 → hidden; buttons back to "Add to cart" | P2 | Yes — `test_remove_from_inventory_updates_badge` |
| TC-CART-04 | Cart page lists items | Logged in | 1. Add Backpack + Onesie 2. Open cart | Both items listed | P1 | Yes — `test_cart_page_lists_added_items` |
| TC-CART-05 | Remove on cart page | 2 items in cart | 1. Open cart 2. Remove Backpack | Only Bike Light remains, badge 1 | P2 | Yes — `test_remove_item_on_cart_page` |
| TC-CART-06 | Cart persists while shopping | 1 item in cart | 1. Open cart 2. Continue Shopping | Back on inventory, badge still 1 | P2 | Yes — `test_cart_persists_after_continue_shopping` |
| TC-CART-07 | Cart persists after logout/login | 1 item in cart | 1. Logout 2. Login again | Item still in cart (current product behaviour) | P3 | No (manual) |

## Checkout

| ID | Title | Preconditions | Steps | Expected result | Priority | Automated |
|----|-------|---------------|-------|-----------------|----------|-----------|
| TC-CHK-01 | Complete order | 3 items in cart | 1. Checkout 2. Fill first/last name and ZIP 3. Continue 4. Finish | "Thank you for your order!", cart badge cleared | P1 | Yes — `test_checkout_happy_path` |
| TC-CHK-02 | First name required | At checkout step one | 1. Leave First Name empty 2. Continue | "Error: First Name is required" | P1 | Yes — `test_checkout_form_validation[missing-first-name]` |
| TC-CHK-03 | Last name required | At checkout step one | 1. Leave Last Name empty 2. Continue | "Error: Last Name is required" | P1 | Yes — `test_checkout_form_validation[missing-last-name]` |
| TC-CHK-04 | Postal code required | At checkout step one | 1. Leave Postal Code empty 2. Continue | "Error: Postal Code is required" | P1 | Yes — `test_checkout_form_validation[missing-postal-code]` |
| TC-CHK-05 | Totals calculation | Backpack, Fleece Jacket, Onesie in cart | 1. Reach overview | Item total = sum of prices; tax = 8 % of item total; total = item total + tax | P1 | Yes — `test_order_totals_are_correct` |
| TC-CHK-06 | Cancel checkout | At checkout step one | 1. Click Cancel | Back to cart with all items | P2 | Yes — `test_cancel_checkout_returns_to_cart` |
| TC-CHK-07 | Checkout with empty cart | Empty cart | 1. Open cart 2. Click Checkout | Checkout should be blocked (currently allowed — candidate defect) | P3 | No (manual) |

## Known defects (`problem_user`)

| ID | Title | Preconditions | Steps | Expected result | Priority | Automated |
|----|-------|---------------|-------|-----------------|----------|-----------|
| TC-PU-01 | Distinct product images | Logged in as `problem_user` | 1. View inventory | Each product shows its own photo | P2 | Yes (xfail BUG-001) — `test_each_product_has_its_own_image` |
| TC-PU-02 | Sorting works | Logged in as `problem_user` | 1. Select "Price (low to high)" | Prices ascending | P2 | Yes (xfail BUG-002) — `test_sort_by_price_low_to_high` |
| TC-PU-03 | Add every product | Logged in as `problem_user` | 1. Click "Add to cart" on all 6 products | Badge shows 6 | P1 | Yes (xfail BUG-003) — `test_add_every_product_to_cart` |
| TC-PU-04 | Checkout information form | `problem_user`, 1 item in cart | 1. Checkout 2. Fill all fields 3. Continue | Overview page opens | P1 | Yes (xfail BUG-004) — `test_checkout_with_valid_information` |

## API — JSONPlaceholder

| ID | Title | Preconditions | Steps | Expected result | Priority | Automated |
|----|-------|---------------|-------|-----------------|----------|-----------|
| TC-API-01 | List posts | — | GET `/posts` | 200, JSON, 100 items matching post schema | P1 | Yes — `test_list_posts` |
| TC-API-02 | Get one post | — | GET `/posts/1` | 200, id = 1, schema valid | P1 | Yes — `test_get_single_post` |
| TC-API-03 | Missing post | — | GET `/posts/99999` | 404, body `{}` | P2 | Yes — `test_get_missing_post_returns_404` |
| TC-API-04 | Filter by user | — | GET `/posts?userId=3` | 200, 10 posts, all userId 3 | P2 | Yes — `test_filter_posts_by_user` |
| TC-API-05 | Post comments | — | GET `/posts/1/comments` | 200, 5 comments with valid email | P2 | Yes — `test_post_comments` |
| TC-API-06 | Create post | — | POST `/posts` with title/body/userId | 201, payload echoed with id 101 | P1 | Yes — `test_create_post` |
| TC-API-07 | Replace post | — | PUT `/posts/1` | 200, payload echoed | P2 | Yes — `test_replace_post` |
| TC-API-08 | Patch post | — | PATCH `/posts/1` with new title | 200, title updated, other fields kept | P2 | Yes — `test_patch_post` |
| TC-API-09 | Delete post | — | DELETE `/posts/1` | 200, body `{}` | P2 | Yes — `test_delete_post` |
| TC-API-10 | Users schema | — | GET `/users` | 200, 10 users, unique ids, nested address/geo/company | P2 | Yes — `test_list_users_schema` |
| TC-API-11 | User's posts | — | GET `/users/2/posts` | 200, all posts have userId 2 | P3 | Yes — `test_user_posts_belong_to_user` |
| TC-API-12 | Response time | — | GET `/users/1` | Response in < 3 s | P3 | Yes — `test_response_time_is_acceptable` |
