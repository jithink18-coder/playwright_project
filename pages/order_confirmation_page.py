import re
from playwright.sync_api import Page, expect

class OrderConfirmationPage:
    def __init__(self, page: Page):
        self.page = page
        self.order_id_locator = page.locator("label.ng-star-inserted")
        # self.confirmation_heading = page.locator("text=Order Confirmation, text= Thankyou for the order. , text=Your order has been placed")
        self.confirmation_heading = page.get_by_role("heading", name="Thankyou for the order.")

    def wait_for_confirmation(self, timeout: int = 15000) -> None:
        expect(self.confirmation_heading).to_be_visible(timeout=timeout)

    def get_order_id(self) -> str:
        expect(self.order_id_locator.first).to_be_visible(timeout=15000)
        text = (self.order_id_locator.first.text_content() or "").strip()
        if not text:
            fallback_locators = [
                self.page.locator("span.order-id"),
                self.page.locator(".order-id"),
                self.page.locator("[data-test='order-id']"),
            ]
            for locator in fallback_locators:
                if locator.first.count() > 0 and locator.first.is_visible():
                    text = (locator.first.text_content() or "").strip()
                    if text:
                        break
        match = re.search(r"[A-Za-z0-9\-]+", text)
        return match.group(0) if match else text
