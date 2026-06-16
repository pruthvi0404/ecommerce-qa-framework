class InventoryPage:
    """Page Object for the Inventory/Products page of SauceDemo."""

    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page):
        self.page = page
        self.product_items = page.locator(".inventory_item")
        self.cart_icon = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.sort_dropdown = page.locator("[data-test='product_sort_container']")
        self.burger_menu = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")

    def get_product_count(self) -> int:
        return self.product_items.count()

    def add_product_to_cart(self, product_name: str):
        """Add a specific product to the cart by its name."""
        product = self.page.locator(f".inventory_item:has-text('{product_name}')")
        product.locator("button").click()

    def get_cart_count(self) -> int:
        if self.cart_badge.is_visible():
            return int(self.cart_badge.inner_text())
        return 0

    def go_to_cart(self):
        self.cart_icon.click()

    def sort_products(self, option: str):
        """Sort products. Options: 'az', 'za', 'lohi', 'hilo'"""
        self.sort_dropdown.select_option(option)

    def get_all_product_names(self) -> list:
        return self.page.locator(".inventory_item_name").all_inner_texts()

    def get_all_product_prices(self) -> list:
        prices = self.page.locator(".inventory_item_price").all_inner_texts()
        return [float(p.replace("$", "")) for p in prices]

    def logout(self):
        self.burger_menu.click()
        self.page.wait_for_selector("#logout_sidebar_link", state="visible")
        self.logout_link.click()
