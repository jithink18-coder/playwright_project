from playwright.sync_api import Page, expect


class ProductsPage:
    def __init__(self, page: Page):
        self.page = page
        self.product_cards = page.locator("div.card, div.product, div[class*='product'], div[class*='card']")
        self.product_titles = page.locator("div.card h5, div.product h5, div.card h4, div.product h4")
        self.add_to_cart_buttons = page.locator("button:has-text('Add To Cart'), button:has-text('Add to cart')")
        self.cart_button = page.locator("button:has-text('Cart'), button:has-text('CART')")
        self.orders_button = page.locator("button:has-text('ORDERS'), button:has-text('Orders')")
        self.cart_button1=page.get_by_text("Cart")
    def is_loaded(self, timeout: int = 10000) -> bool:
        try:
            expect(self.page.locator("h5", has_text="ADIDAS ORIGINAL")).to_be_visible(timeout=timeout)
            return True
        except Exception:
            return False

    def add_first_product_to_cart(self):
        expect(self.add_to_cart_buttons.first).to_be_visible()
        self.add_to_cart_buttons.first.click()

    def get_first_product_name(self) -> str:
        return (self.product_titles.first.text_content() or "").strip()

    def go_to_cart(self):
        expect(self.cart_button1.first).to_be_visible()
        self.cart_button1.first.click()

    def go_to_orders(self):
        expect(self.orders_button.first).to_be_visible()
        self.orders_button.first.click()
