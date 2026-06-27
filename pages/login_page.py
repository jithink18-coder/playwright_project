import logging

from playwright.sync_api import Page

from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.page = page
        self.url = base_url
        self.email = page.locator("input#userEmail, input[placeholder='email@example.com'], input[name='userEmail']")
        self.password = page.locator("input#userPassword, input[placeholder='enter your passsword'], input[name='userPassword']")
        self.login_button = page.locator("input#login, input[type='submit'][value='Login']")

    def goto(self):
        self.page.goto(self.url)

    def login(self, email: str, password: str):
        logger.info(f"Attempting to login with email: {email}")
        self.fill(self.email, email)
        self.fill(self.password, password)
        self.click(self.login_button)
        logger.info("Login button clicked")

    def login_and_wait(self, email: str, password: str, timeout: int = 15000):
        self.login(email, password)
        self.page.wait_for_url("**/dashboard/**", timeout=timeout)
        logger.info("Login successful, navigated to dashboard")
