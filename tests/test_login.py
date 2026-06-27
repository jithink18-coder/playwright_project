import json
import logging

from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.order_confirmation_page import OrderConfirmationPage
from pages.orders_page import OrdersPage
from pages.products_page import ProductsPage

logger = logging.getLogger(__name__)

def test_login_success(setup_page, base_url,credentials):
    logger.info("Starting test_login_success")
    login = LoginPage(setup_page, base_url)
    login.goto()
    login.login_and_wait(credentials["username"], credentials["password"])

    products = ProductsPage(setup_page)
    assert products.is_loaded(), "Products page did not load or expected product not visible"
    logger.info("Test_login_success completed successfully")
    assert False
    
def test_login_api(setup_page, base_url,credentials):
    """Test API-based login and verify products page loads."""
    logger.info("Starting test_login_api")
    # Use the sync request API from the browser context
    request_ctx = setup_page.context.request
    res = request_ctx.post(
        "https://rahulshettyacademy.com/api/ecom/auth/login",
        data={"userEmail": credentials["username"], "userPassword": credentials["password"]},
    )
    assert res.status == 200, f"Login API failed with status {res.status}"
    data = res.json()
    assert "token" in data, "Login API response does not contain token"
    token = data["token"]

    # Set token in localStorage and navigate
    setup_page.goto("about:blank")
    setup_page.add_init_script(f"localStorage.setItem('token', {json.dumps(token)})")
    setup_page.reload()
    setup_page.goto(base_url)
    # sleep(1000)  # wait for page to load and read token
    products = ProductsPage(setup_page)
    assert products.is_loaded(), "Products page did not load after API login"
    logger.info("Test_login_api completed successfully")

def test_place_order_and_verify_order_id(setup_page, base_url, credentials):
    logger.info("Starting test_place_order_and_verify_order_id")
    login = LoginPage(setup_page, base_url)
    login.goto()
    login.login_and_wait(credentials["username"], credentials["password"])

    products = ProductsPage(setup_page)
    assert products.is_loaded(), "Products page did not load"
    first_product_name = products.get_first_product_name()
    assert first_product_name, "Failed to locate the first product name"
    products.add_first_product_to_cart()

    products.go_to_cart()

    cart = CartPage(setup_page)
    assert cart.is_loaded(), "Cart page did not load"
    cart.click_checkout()

    checkout = CheckoutPage(setup_page)
    checkout.fill_country("India")
    checkout.place_order()

    order_confirmation = OrderConfirmationPage(setup_page)
    order_confirmation.wait_for_confirmation()
    order_id = order_confirmation.get_order_id()

    assert order_id, "Order id was not found after placing the order"

    orders = OrdersPage(setup_page)
    orders.go_to_orders()
    assert orders.has_order(order_id), f"Order id {order_id} was not found on the orders page"
    logger.info("Test_place_order_and_verify_order_id completed successfully")
def test_verify_empty_orders_page(setup_page, base_url, credentials):
    logger.info("Starting test_verify_empty_orders_page")
    login = LoginPage(setup_page, base_url)
    login.goto()
    login.login_and_wait(credentials["username"], credentials["password"])

     # intercept the orders API call and return an empty orders payload
    setup_page.route(
        "**/api/ecom/order/get-orders-for-customer/*",
        lambda route, request: route.fulfill(
            json={"data":[],"message":"No Orders"},
        ),
    )

    products = ProductsPage(setup_page)
    assert products.is_loaded(), "Products page did not load"
    orders = OrdersPage(setup_page)
    orders.go_to_orders()
    assert orders.has_no_orders_message(), "Expected 'No Orders' message was not displayed on the orders page"
    logger.info("Test_verify_empty_orders_page completed successfully")
def test_verify_products_are_added_to_cart(setup_page, base_url, credentials):
    logger.info("Starting test_verify_products_are_added_to_cart")
    login = LoginPage(setup_page, base_url)
    login.goto()
    login.login_and_wait(credentials["username"], credentials["password"])

    products=ProductsPage(setup_page)
    products.is_loaded()
    adidas_product_locator_list = setup_page.locator("div.card", has=setup_page.locator("h5", has_text="ADIDAS ORIGINAL"))
    # adidas=adidas_product_locator_list.locator("h5").filter(has_text="ADIDAS ORIGINAL")
    expect(adidas_product_locator_list).to_have_count(1)
    adidas_product_locator_list.first.get_by_role("button", name="Add To Cart").click()

    products.go_to_cart()
    cart=CartPage(setup_page)
    cart.is_loaded()
    expect(cart.get_cart_items()).to_have_count(1)
    cart.click_buy_now()
    logger.info("Test_verify_products_are_added_to_cart completed successfully")