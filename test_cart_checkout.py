import json
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

with open("utils/test_data.json") as f:
    TEST_DATA = json.load(f)


@pytest.fixture
def logged_in_page(page):
    """Fixture: Returns a page already logged in as standard_user."""
    login = LoginPage(page)
    login.navigate()
    login.login(
        TEST_DATA["valid_user"]["username"],
        TEST_DATA["valid_user"]["password"]
    )
    return page


class TestCart:
    """Test suite for Cart functionality."""

    def test_add_single_item_to_cart(self, logged_in_page):
        """TC007: Adding one product should update cart badge to 1."""
        inventory = InventoryPage(logged_in_page)
        inventory.add_product_to_cart(TEST_DATA["products"]["sauce_labs_backpack"])
        assert inventory.get_cart_count() == 1

    def test_add_multiple_items_to_cart(self, logged_in_page):
        """TC008: Adding multiple products should reflect correct count."""
        inventory = InventoryPage(logged_in_page)
        inventory.add_product_to_cart(TEST_DATA["products"]["sauce_labs_backpack"])
        inventory.add_product_to_cart(TEST_DATA["products"]["sauce_labs_bike_light"])
        assert inventory.get_cart_count() == 2

    def test_remove_item_from_cart(self, logged_in_page):
        """TC009: Removing an item from cart should decrease cart count."""
        inventory = InventoryPage(logged_in_page)
        inventory.add_product_to_cart(TEST_DATA["products"]["sauce_labs_backpack"])
        inventory.add_product_to_cart(TEST_DATA["products"]["sauce_labs_bike_light"])
        inventory.go_to_cart()

        cart = CartPage(logged_in_page)
        cart.remove_item(TEST_DATA["products"]["sauce_labs_backpack"])
        assert cart.get_cart_item_count() == 1

    def test_cart_persists_after_navigation(self, logged_in_page):
        """TC010: Cart items should persist when navigating back from cart."""
        inventory = InventoryPage(logged_in_page)
        inventory.add_product_to_cart(TEST_DATA["products"]["sauce_labs_backpack"])
        inventory.go_to_cart()

        cart = CartPage(logged_in_page)
        cart.continue_shopping()

        # Cart count should still be 1
        assert inventory.get_cart_count() == 1

    def test_product_visible_in_cart(self, logged_in_page):
        """TC011: Added product name should appear in cart."""
        product_name = TEST_DATA["products"]["sauce_labs_backpack"]
        inventory = InventoryPage(logged_in_page)
        inventory.add_product_to_cart(product_name)
        inventory.go_to_cart()

        cart = CartPage(logged_in_page)
        assert product_name in cart.get_item_names()


class TestCheckout:
    """Test suite for Checkout flow."""

    def test_successful_checkout(self, logged_in_page):
        """TC012: Full checkout flow should show order confirmation."""
        inventory = InventoryPage(logged_in_page)
        inventory.add_product_to_cart(TEST_DATA["products"]["sauce_labs_backpack"])
        inventory.go_to_cart()

        cart = CartPage(logged_in_page)
        cart.proceed_to_checkout()

        checkout = CheckoutPage(logged_in_page)
        checkout.fill_details(
            TEST_DATA["checkout_details"]["first_name"],
            TEST_DATA["checkout_details"]["last_name"],
            TEST_DATA["checkout_details"]["postal_code"]
        )
        checkout.continue_to_overview()
        checkout.finish_order()

        assert "Thank you" in checkout.get_confirmation_text()

    def test_checkout_missing_first_name(self, logged_in_page):
        """TC013: Checkout without first name should show error."""
        inventory = InventoryPage(logged_in_page)
        inventory.add_product_to_cart(TEST_DATA["products"]["sauce_labs_backpack"])
        inventory.go_to_cart()

        cart = CartPage(logged_in_page)
        cart.proceed_to_checkout()

        checkout = CheckoutPage(logged_in_page)
        checkout.fill_details("", "Jain", "400001")
        checkout.continue_to_overview()

        assert checkout.is_error_visible()
        assert "First Name is required" in checkout.get_error_message()

    def test_checkout_missing_postal_code(self, logged_in_page):
        """TC014: Checkout without postal code should show error."""
        inventory = InventoryPage(logged_in_page)
        inventory.add_product_to_cart(TEST_DATA["products"]["sauce_labs_backpack"])
        inventory.go_to_cart()

        cart = CartPage(logged_in_page)
        cart.proceed_to_checkout()

        checkout = CheckoutPage(logged_in_page)
        checkout.fill_details("Pruthvi", "Jain", "")
        checkout.continue_to_overview()

        assert checkout.is_error_visible()
        assert "Postal Code is required" in checkout.get_error_message()


class TestSorting:
    """Test suite for product sorting on inventory page."""

    def test_sort_products_a_to_z(self, logged_in_page):
        """TC015: Products sorted A-Z should be in ascending alphabetical order."""
        inventory = InventoryPage(logged_in_page)
        inventory.sort_products("az")
        names = inventory.get_all_product_names()
        assert names == sorted(names), "Products should be in A-Z order"

    def test_sort_products_z_to_a(self, logged_in_page):
        """TC016: Products sorted Z-A should be in descending alphabetical order."""
        inventory = InventoryPage(logged_in_page)
        inventory.sort_products("za")
        names = inventory.get_all_product_names()
        assert names == sorted(names, reverse=True), "Products should be in Z-A order"

    def test_sort_price_low_to_high(self, logged_in_page):
        """TC017: Products sorted low-high should be in ascending price order."""
        inventory = InventoryPage(logged_in_page)
        inventory.sort_products("lohi")
        prices = inventory.get_all_product_prices()
        assert prices == sorted(prices), "Prices should be in ascending order"

    def test_sort_price_high_to_low(self, logged_in_page):
        """TC018: Products sorted high-low should be in descending price order."""
        inventory = InventoryPage(logged_in_page)
        inventory.sort_products("hilo")
        prices = inventory.get_all_product_prices()
        assert prices == sorted(prices, reverse=True), "Prices should be in descending order"
