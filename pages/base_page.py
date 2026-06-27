from playwright.sync_api import expect


class BasePage:
    def __init__(self, page):
        self.page = page

    def click(self, locator):
        # locator.wait_for(state="visible")
        expect(locator).to_be_visible()
        locator.click()

    def fill(self, locator, value):
        # locator.wait_for(state="visible")
        expect(locator).to_be_visible()
        locator.fill(value)