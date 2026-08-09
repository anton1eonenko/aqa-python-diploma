from playwright.sync_api import Page
from pages.base_page import BasePage


class HomePage(BasePage):
    # Locators
    LOGO = "[itemprop='logo']"
    SEARCH_INPUT = "input[name='query']"
    SEARCH_BUTTON = "button[type='submit'].search__submit"
    CATALOG_BUTTON = "button.header__catalog-btn, [data-testid='catalog-button'], .header__catalog"
    CART_ICON = "a.header__cart, .cart-icon"
    HEADER = "header, .header"
    MAIN_BANNER = ".main-slider, .banner-slider, .main-banner"
    CATEGORY_LINKS = ".main-categories a, .categories-grid a"
    FOOTER = "footer, .footer"
    COOKIE_ACCEPT_BUTTON = "button:has-text('Принять'), button:has-text('OK'), .cookie-accept"

    def __init__(self, page: Page):
        super().__init__(page)

    def accept_cookies_if_present(self):
        try:
            btn = self.page.locator(self.COOKIE_ACCEPT_BUTTON).first
            if btn.is_visible(timeout=3000):
                btn.click()
        except Exception:
            pass

    def is_logo_visible(self) -> bool:
        return self.page.locator(self.LOGO).is_visible()

    def is_header_visible(self) -> bool:
        return self.page.locator(self.HEADER).is_visible()

    def is_footer_visible(self) -> bool:
        return self.page.locator(self.FOOTER).is_visible()

    def search(self, query: str):
        self.page.locator(self.SEARCH_INPUT).fill(query)
        self.page.locator(self.SEARCH_INPUT).press("Enter")
        self.page.wait_for_load_state("networkidle")

    def get_search_input(self):
        return self.page.locator(self.SEARCH_INPUT)

    def click_cart(self):
        self.page.locator(self.CART_ICON).first.click()
        self.page.wait_for_load_state("networkidle")

    def get_category_links_count(self) -> int:
        return self.page.locator(self.CATEGORY_LINKS).count()
