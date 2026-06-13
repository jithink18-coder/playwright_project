import re
from time import sleep
from playwright.sync_api import Page, expect

class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.country_input = page.locator("input[placeholder*='Country'], input[name='country'], input[id*='country']")
        self.place_order_button = page.locator("a:has-text('Place Order'), button:has-text('PLACE ORDER')")
        self.order_id_label = page.locator("text=Order ID")
        self.country_suggestions = page.get_by_role("textbox", name="Select Country")

    def fill_country(self, country: str):
        expect(self.country_input).to_be_visible()
        self.country_suggestions.click()
        self.country_suggestions.type(country)
        # sleep(1)  # Wait for suggestions to load
        # self.country_input.press("Tab")
        # sleep(1)  # Wait for the dropdown to process the input
        # self.country_input.press("Tab")
        # sleep(1)  # Ensure the focus is on the correct element before pressing Enter
        # self.country_input.press("Enter")
        self.page.get_by_role("button", name=" India").click()
        

    def place_order(self):
        expect(self.place_order_button).to_be_visible()
        self.place_order_button.click()

    def get_order_id(self) -> str:
        expect(self.order_id_label.first).to_be_visible(timeout=15000)
        text = (self.order_id_label.first.text_content() or "").strip()
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
