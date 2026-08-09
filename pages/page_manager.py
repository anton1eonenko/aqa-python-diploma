from __future__ import annotations

from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.search_results_page import SearchResultsPage


class PageManager:
    """Provides lazy access to every page object for a single Playwright page instance."""

    def __init__(self, page: Page, base_url: str) -> None:
        self._page = page
        self._base_url = base_url.rstrip("/")

    @property
    def page(self) -> Page:
        """Raw Playwright page for operations not covered by page objects."""
        return self._page

    # --- page object properties (created on first access) ---

    @property
    def home(self) -> HomePage:
        return HomePage(self._page)

    @property
    def catalog(self) -> CatalogPage:
        return CatalogPage(self._page)

    @property
    def cart(self) -> CartPage:
        return CartPage(self._page)

    @property
    def product(self) -> ProductPage:
        return ProductPage(self._page)

    @property
    def search_results(self) -> SearchResultsPage:
        return SearchResultsPage(self._page)

    # --- navigation helper ---

    def go(self, path_or_url: str = "") -> None:
        """Navigate to a relative path or full URL and wait for network idle."""
        url = (
            path_or_url
            if path_or_url.startswith("http")
            else f"{self._base_url}/{path_or_url.lstrip('/')}"
        )
        self._page.goto(url)
        self._page.wait_for_load_state("networkidle")
