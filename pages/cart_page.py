from playwright.sync_api import Page, expect

class CartPage:
    def __init__(self, page: Page):
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
        self.checkout_button.click()
