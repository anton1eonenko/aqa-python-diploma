import re
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class ProductPage(BasePage):

    class _Containers:
        def __init__(self, page: Page) -> None:
            self.MainContainer: Locator = page.locator(".g-page")

    class _Text:
        def __init__(self, container: Locator) -> None:
            self.TITLE: Locator = container.locator("h1.g-page__title")
            self.PRICE: Locator = container.locator("[class*='offers-list__price']")
            self.AVAILABILITY: Locator = container.locator("[class*='offers-list__count']")

    class _Buttons:
        def __init__(self, container: Locator) -> None:
            self.ADD_TO_CART: Locator = container.get_by_role(
                "button", name=re.compile(r"в корзину", re.IGNORECASE)
            )
            self.REVIEWS_TAB: Locator = container.locator("a[href*='#reviews']")
            self.SPECS_TAB: Locator = container.locator("a[href*='#description']")

    class _Sections:
        def __init__(self, container: Locator) -> None:
            self.BREADCRUMBS: Locator = container.locator(".breadcrumbs")
            self.GALLERY: Locator = container.locator("[class*='product-gallery']")
            self.DESCRIPTION: Locator = container.locator("[class*='product-description']")

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.Containers = ProductPage._Containers(page)
        self.Text = ProductPage._Text(self.Containers.MainContainer)
        self.Buttons = ProductPage._Buttons(self.Containers.MainContainer)
        self.Sections = ProductPage._Sections(self.Containers.MainContainer)

    def get_title_element(self) -> Locator:
        return self.Text.TITLE.first

    def get_price_element(self) -> Locator:
        return self.Text.PRICE.first

    def get_add_to_cart_button(self) -> Locator:
        return self.Buttons.ADD_TO_CART.first

    def get_breadcrumbs(self) -> Locator:
        return self.Sections.BREADCRUMBS

    def get_product_title(self) -> str:
        return self.get_title_element().inner_text()

    def get_product_price(self) -> str:
        return self.get_price_element().inner_text()

    def is_add_to_cart_visible(self) -> bool:
        return self.get_add_to_cart_button().is_visible()

    def is_breadcrumbs_visible(self) -> bool:
        return self.get_breadcrumbs().is_visible()

    def add_to_cart(self) -> None:
        self.get_add_to_cart_button().click()
        self.page.wait_for_load_state("networkidle")

    def get_breadcrumb_items(self) -> list[str]:
        items = self.Sections.BREADCRUMBS.locator("a, span")
        return [items.nth(i).inner_text() for i in range(items.count())]

    def open_specifications_tab(self) -> None:
        self.Buttons.SPECS_TAB.first.click()
        self.page.wait_for_load_state("networkidle")

    def open_reviews_tab(self) -> None:
        self.Buttons.REVIEWS_TAB.first.click()
        self.page.wait_for_load_state("networkidle")
