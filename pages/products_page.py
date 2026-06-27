import logging

from playwright.sync_api import Page, expect

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class ProductsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.product_cards = page.locator("div.card")
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
        self.click(self.cart_button1.first)

    def go_to_orders(self):
        expect(self.orders_button.first).to_be_visible()
        self.orders_button.first.click()

    def add_product_to_cart_by_name(self, product_name: str):
        response_message = '{"message":"Product Added To Cart"}'
        product_card = self.product_cards.filter(has_text=product_name)
        expect(product_card).to_have_count(1)
        add_to_cart_button = product_card.locator("button:has-text('Add To Cart'), button:has-text('Add to cart')")
        with self.page.expect_response(
            lambda response: response.request.method == "POST"
            and "/api/ecom/user/add-to-cart" in response.url,
            timeout=10000,
        ) as response_info:
            self.click(add_to_cart_button)
        assert response_info.value.ok, f"Add to cart request failed with status {response_info.value.status}"
        logger.info(f"Add to cart request succeeded with status {response_info.value.text()}")
        
        assert response_info.value.text() == response_message, f"Unexpected response message: {response_info.value.text()}"
        logger.info("Product added to cart successfully.")        
        