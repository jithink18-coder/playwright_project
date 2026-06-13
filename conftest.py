import datetime
import logging
import os

import pytest
import pytest_html.extras as extras
from dotenv import load_dotenv
from playwright.sync_api import Browser, Playwright

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@pytest.fixture(scope="session")
def credentials():
    load_dotenv()  # Load environment variables from .env file
    return {
        "username": os.getenv("USERID"),
        "password": os.getenv("PASSWORD")
    }

@pytest.fixture(scope="session")
def base_url():
    return "https://rahulshettyacademy.com/client/#/auth/login"

def pytest_addoption(parser):
    """Register custom pytest command-line options."""
    # parser.addoption("--headed", action="store_true", default=False, help="Run browser in headed mode")
    parser.addoption("--browsername", action="store", default="chromium", help="Browser type")

@pytest.fixture(scope="session")
def browser_type_launch_options(request: pytest.FixtureRequest):
    """Return browser launch options based on pytest CLI arguments."""
    headed = request.config.getoption("headed", False)
    browser = request.config.getoption("browsername", "chromium")
    logger.info(f"Launching browser: {browser}")
    logger.info(f"Headed mode: {headed}")
    opts = {"headless": not headed}
    if browser:
        opts["browser"] = browser
    return opts

@pytest.fixture(scope="session")
def browser_instance(playwright: Playwright, browser_type_launch_options: dict[str, bool]):
    """Launch and yield a Playwright browser instance for the session.

    The browser type is selected based on the provided command-line option.
    The browser is closed after the session ends.
    """
    browser_name = browser_type_launch_options.get("browser", "chromium")
    launch_opts = {k: v for k, v in browser_type_launch_options.items() if k != "browser"}

    if browser_name == "firefox":
        browser = playwright.firefox.launch(**launch_opts)
    elif browser_name == "webkit":
        browser = playwright.webkit.launch(**launch_opts)
    else:
        browser = playwright.chromium.launch(**launch_opts)

    yield browser
    browser.close()

@pytest.fixture
def browser_context(browser_instance: Browser):
    """Create a fresh browser context for each test and close it after use."""
    context = browser_instance.new_context()
    yield context
    context.close()

@pytest.fixture
def setup_page(browser_context, request: pytest.FixtureRequest):
    browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = browser_context.new_page()
    yield page

    datetime_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    test_name = request.node.nodeid.replace("::", "_").replace("/", "_")
    # trace only on failure
    if request.node.rep_call.failed:
        tracefilename = f"{datetime_str}_{test_name}_trace.zip"
        browser_context.tracing.stop(path=f"./traces/{tracefilename}")
    page.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    rep.extras = getattr(rep, "extra", [])

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("setup_page")

        if page:
            try:
                os.makedirs("screenshots", exist_ok=True)
                screenshot_filename = f"{item.name}.png"
                screenshot_path = os.path.join("screenshots", screenshot_filename)
                page.screenshot(path=screenshot_path)
                rep.extras.append(extras.image(os.path.relpath(screenshot_path)))
            except Exception as e:
                logger.warning(f"Screenshot failed: {e}")