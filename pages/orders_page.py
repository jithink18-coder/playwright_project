from pydoc import html

from playwright.sync_api import Page, expect


class OrdersPage:
    def __init__(self, page: Page):
        self.page = page
        self.orders_button = page.locator("button:has-text('ORDERS'), button:has-text('Orders')")
        self.orders_heading = page.locator("h1:has-text('Your Orders'), h2:has-text('Your Orders'), h3:has-text('Your Orders')")
        self.go_back_to_shop_button = page.locator("button:has-text('Go Back to Shop')")
        self.no_orders_message = page.locator("text= You have No Orders to show at this time.")

    def go_to_orders(self):
        expect(self.orders_button.first).to_be_visible()
        self.orders_button.first.click()
        expect(self.go_back_to_shop_button).to_be_visible(timeout=15000)
        

    def has_order(self, order_id: str) -> bool:
        order_locator = self.page.locator(f"text={order_id}")
        expect(order_locator).to_be_visible(timeout=15000)
        return order_locator.first.count() > 0 and order_locator.first.is_visible()

    def has_no_orders_message(self) -> bool:
        expect(self.no_orders_message).to_be_visible(timeout=15000)
        return self.no_orders_message.is_visible()