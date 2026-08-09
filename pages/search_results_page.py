from playwright.sync_api import Page
from pages.base_page import BasePage


class SearchResultsPage(BasePage):
    # Locators
    SEARCH_RESULTS_HEADING = ".search__title, h1.page-title, .results-title"
    PRODUCT_CARDS = ".g-i-tile, .products-list__item, .product-card"
    NO_RESULTS_MESSAGE = ".search-empty, .no-results, :has-text('Ничего не найдено')"
    PRODUCT_TITLE = ".g-i-tile__description a, .product-card__name"
    PRODUCT_PRICE = ".g-i-tile__price, .product-card__price"
    SORT_SELECT = "select[name='sort'], .sort__select"
    FILTER_SECTION = ".filters, .sidebar-filters"
    PAGINATION = ".pagination, .pager"
    RESULTS_COUNT = ".search__count, .results-count"

    def __init__(self, page: Page):
        super().__init__(page)

    def get_results_count(self) -> int:
        return self.page.locator(self.PRODUCT_CARDS).count()

    def is_no_results_shown(self) -> bool:
        return self.page.locator(self.NO_RESULTS_MESSAGE).is_visible()

    def get_first_product_title(self) -> str:
        return self.page.locator(self.PRODUCT_TITLE).first.inner_text()

    def get_first_product_price(self) -> str:
        return self.page.locator(self.PRODUCT_PRICE).first.inner_text()

    def click_first_product(self):
        self.page.locator(self.PRODUCT_TITLE).first.click()
        self.page.wait_for_load_state("networkidle")

    def is_pagination_visible(self) -> bool:
        return self.page.locator(self.PAGINATION).is_visible()

    def is_filter_section_visible(self) -> bool:
        return self.page.locator(self.FILTER_SECTION).is_visible()
