from playwright.sync_api import Page
from pages.base_page import BasePage


class ProductPage(BasePage):
    # Locators
    PRODUCT_TITLE = "h1.g-page__title, h1.product-title, h1"
    PRODUCT_PRICE = ".offers-list__price, .product-price, .price"
    ADD_TO_CART_BUTTON = "button:has-text('В корзину'), .add-to-cart, button.cart-btn"
    PRODUCT_DESCRIPTION = ".product-description, .description-tab, .tab-description"
    PRODUCT_IMAGES = ".product-gallery img, .product-images img"
    BREADCRUMBS = ".breadcrumbs, nav[aria-label='breadcrumb']"
    RATING = ".product-rating, .stars-rating"
    REVIEWS_TAB = "a:has-text('Отзывы'), button:has-text('Отзывы')"
    SPECIFICATIONS_TAB = "a:has-text('Характеристики'), button:has-text('Характеристики')"
    AVAILABILITY = ".offers-list__count, .availability-status"

    def __init__(self, page: Page):
        super().__init__(page)

    def get_product_title(self) -> str:
        return self.page.locator(self.PRODUCT_TITLE).first.inner_text()

    def get_product_price(self) -> str:
        return self.page.locator(self.PRODUCT_PRICE).first.inner_text()

    def is_add_to_cart_visible(self) -> bool:
        return self.page.locator(self.ADD_TO_CART_BUTTON).first.is_visible()

    def add_to_cart(self):
        self.page.locator(self.ADD_TO_CART_BUTTON).first.click()
        self.page.wait_for_load_state("networkidle")

    def get_breadcrumbs(self) -> list[str]:
        crumbs = self.page.locator(self.BREADCRUMBS + " a, " + self.BREADCRUMBS + " span")
        return [crumbs.nth(i).inner_text() for i in range(crumbs.count())]

    def open_specifications_tab(self):
        tab = self.page.locator(self.SPECIFICATIONS_TAB).first
        if tab.is_visible():
            tab.click()
            self.page.wait_for_load_state("networkidle")

    def open_reviews_tab(self):
        tab = self.page.locator(self.REVIEWS_TAB).first
        if tab.is_visible():
            tab.click()
            self.page.wait_for_load_state("networkidle")

    def is_breadcrumbs_visible(self) -> bool:
        return self.page.locator(self.BREADCRUMBS).is_visible()
