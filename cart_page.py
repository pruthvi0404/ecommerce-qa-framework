class CartPage:
    """Page Object for the Cart page of SauceDemo."""

    URL = "https://www.saucedemo.com/cart.html"

    def __init__(self, page):
        self.page = page
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.locator("[data-test='checkout']")
        self.continue_shopping_button = page.locator("[data-test='continue-shopping']")
        self.remove_buttons = page.locator(".cart_item button")

    def get_cart_item_count(self) -> int:
        return self.cart_items.count()

    def get_item_names(self) -> list:
        return self.page.locator(".inventory_item_name").all_inner_texts()

    def remove_item(self, product_name: str):
        item = self.page.locator(f".cart_item:has-text('{product_name}')")
        item.locator("button").click()

    def proceed_to_checkout(self):
        self.checkout_button.click()

    def continue_shopping(self):
        self.continue_shopping_button.click()
