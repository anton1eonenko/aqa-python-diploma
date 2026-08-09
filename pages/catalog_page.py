from playwright.sync_api import Page
from pages.base_page import BasePage


class CatalogPage(BasePage):
    # Locators
    CATEGORY_TITLE = "h1.g-page__title, h1.catalog-title, h1"
    PRODUCT_CARDS = ".g-i-tile, .products-list__item, .product-card"
    PRODUCT_TITLE = ".g-i-tile__description a, .product-card__name"
    PRODUCT_PRICE = ".g-i-tile__price, .product-card__price"
    FILTER_SECTION = ".filters, .sidebar-filters, .filter-block"
    PRICE_FILTER_MIN = "input[name='price_min'], input[placeholder='от']"
    PRICE_FILTER_MAX = "input[name='price_max'], input[placeholder='до']"
    SORT_SELECT = "select[name='sort'], .sort__select"
    PAGINATION = ".pagination, .pager"
    PAGINATION_NEXT = ".pagination__next, a:has-text('Следующая')"
    VIEW_TOGGLE_GRID = "button[data-view='tile'], .view-toggle__grid"
    VIEW_TOGGLE_LIST = "button[data-view='list'], .view-toggle__list"
    SUBCATEGORY_LINKS = ".subcategories a, .catalog-categories a"

    def __init__(self, page: Page):
        super().__init__(page)

    def get_category_title(self) -> str:
        return self.page.locator(self.CATEGORY_TITLE).first.inner_text()

    def get_products_count(self) -> int:
        return self.page.locator(self.PRODUCT_CARDS).count()

    def click_first_product(self):
        self.page.locator(self.PRODUCT_TITLE).first.click()
        self.page.wait_for_load_state("networkidle")

    def get_first_product_title(self) -> str:
        return self.page.locator(self.PRODUCT_TITLE).first.inner_text()

    def is_filter_visible(self) -> bool:
        return self.page.locator(self.FILTER_SECTION).is_visible()

    def is_pagination_visible(self) -> bool:
        return self.page.locator(self.PAGINATION).is_visible()

    def go_to_next_page(self):
        next_btn = self.page.locator(self.PAGINATION_NEXT).first
        if next_btn.is_visible():
            next_btn.click()
            self.page.wait_for_load_state("networkidle")

    def get_subcategory_count(self) -> int:
        return self.page.locator(self.SUBCATEGORY_LINKS).count()
