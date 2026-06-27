from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.checkout_button = page.locator("button:has-text('Checkout'), button:has-text('CHECKOUT')")
        # self.cart_heading = page.locator("text=Cart")
        self.cart_heading = page.locator("xpath=//h1[contains(text(),'My Cart')]")


    def is_loaded(self, timeout: int = 10000) -> bool:
        try:
            expect(self.cart_heading).to_be_visible(timeout=timeout)
            return True
        except Exception:
            return False

    def click_checkout(self):
        expect(self.checkout_button).to_be_visible()
        self.click(self.checkout_button)

    def get_cart_items(self):
        return self.page.locator("li.items.even.ng-star-inserted")

    def click_buy_now(self):
        buy_now_button = self.get_cart_items().get_by_role("button", name="Buy Now")
        expect(buy_now_button).to_be_visible()
        self.click(buy_now_button)
