import pytest
import os
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from dotenv import load_dotenv
from pages.page_manager import PageManager

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.21vek.by")
BROWSER_NAME = os.getenv("BROWSER", "chromium")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", "0"))
TIMEOUT = int(os.getenv("TIMEOUT", "30000"))


def pytest_addoption(parser):
    parser.addoption("--browser-name", action="store", default=BROWSER_NAME)
    parser.addoption("--headless", action="store_true", default=HEADLESS)
    parser.addoption("--slow-mo", action="store", type=int, default=SLOW_MO)


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def browser_instance(request):
    browser_name = request.config.getoption("--browser-name", default=BROWSER_NAME)
    headless = request.config.getoption("--headless", default=HEADLESS)
    slow_mo = request.config.getoption("--slow-mo", default=SLOW_MO)

    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=headless, slow_mo=slow_mo)
        yield browser
        browser.close()


_CONTEXT_OPTIONS: dict = {
    "viewport": {"width": 1920, "height": 1080},
    "locale": "ru-RU",
    "user_agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
}


@pytest.fixture(scope="function")
def context(browser_instance: Browser):
    ctx = browser_instance.new_context(**_CONTEXT_OPTIONS)
    ctx.set_default_timeout(TIMEOUT)
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext, base_url: str):
    pg = context.new_page()
    pg.goto(base_url)
    yield pg
    pg.close()


@pytest.fixture(scope="function")
def app(page: Page, base_url: str) -> PageManager:
    """PageManager backed by the default test page."""
    return PageManager(page, base_url)


@pytest.fixture(scope="function")
def make_app(browser_instance: Browser, base_url: str):
    """
    Factory fixture — call it to get a PageManager with a fresh isolated context.
    Mirrors the createAppFixture pattern: each call gets its own browser context
    so tests that need multiple sessions or specific starting URLs can use it.

    Usage:
        def test_something(make_app):
            store = make_app()                   # starts at base URL
            store2 = make_app("order/basket/")   # starts at cart
    """
    _contexts = []

    def _factory(path: str = "", **context_overrides) -> PageManager:
        options = {**_CONTEXT_OPTIONS, **context_overrides}
        ctx = browser_instance.new_context(**options)
        ctx.set_default_timeout(TIMEOUT)
        _contexts.append(ctx)
        pg = ctx.new_page()
        url = f"{base_url.rstrip('/')}/{path.lstrip('/')}" if path else base_url
        pg.goto(url)
        return PageManager(pg, base_url)

    yield _factory

    for ctx in _contexts:
        ctx.close()
