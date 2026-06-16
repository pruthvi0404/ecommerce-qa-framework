import json
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

# Load test data
with open("utils/test_data.json") as f:
    TEST_DATA = json.load(f)


class TestLogin:
    """Test suite for Login functionality."""

    def test_valid_login(self, page):
        """TC001: Valid credentials should redirect to inventory page."""
        login = LoginPage(page)
        login.navigate()
        login.login(
            TEST_DATA["valid_user"]["username"],
            TEST_DATA["valid_user"]["password"]
        )
        assert "inventory" in page.url, "User should be redirected to inventory page"

    def test_invalid_credentials(self, page):
        """TC002: Invalid credentials should show error message."""
        login = LoginPage(page)
        login.navigate()
        login.login(
            TEST_DATA["invalid_user"]["username"],
            TEST_DATA["invalid_user"]["password"]
        )
        assert login.is_error_visible(), "Error message should be visible"
        assert "Username and password do not match" in login.get_error_message()

    def test_locked_out_user(self, page):
        """TC003: Locked user should see locked out error."""
        login = LoginPage(page)
        login.navigate()
        login.login(
            TEST_DATA["locked_user"]["username"],
            TEST_DATA["locked_user"]["password"]
        )
        assert login.is_error_visible(), "Error should be visible for locked user"
        assert "locked out" in login.get_error_message().lower()

    def test_empty_username(self, page):
        """TC004: Empty username should show validation error."""
        login = LoginPage(page)
        login.navigate()
        login.login("", TEST_DATA["valid_user"]["password"])
        assert login.is_error_visible()
        assert "Username is required" in login.get_error_message()

    def test_empty_password(self, page):
        """TC005: Empty password should show validation error."""
        login = LoginPage(page)
        login.navigate()
        login.login(TEST_DATA["valid_user"]["username"], "")
        assert login.is_error_visible()
        assert "Password is required" in login.get_error_message()

    def test_logout(self, page):
        """TC006: User should be able to logout successfully."""
        login = LoginPage(page)
        login.navigate()
        login.login(
            TEST_DATA["valid_user"]["username"],
            TEST_DATA["valid_user"]["password"]
        )
        inventory = InventoryPage(page)
        inventory.logout()
        assert page.url == LoginPage.URL, "User should be redirected to login page"
