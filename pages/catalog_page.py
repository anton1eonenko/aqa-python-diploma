from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class CatalogPage(BasePage):

    class _Containers:
        def __init__(self, page: Page) -> None:
            self.MainContainer: Locator = page.locator(".g-page")

    class _Text:
        def __init__(self, container: Locator) -> None:
            self.PAGE_TITLE: Locator = container.locator("h1.g-page__title")

    class _Items:
        def __init__(self, container: Locator) -> None:
            self.PRODUCT_CARD: Locator = container.locator(".g-i-tile")
            self.PRODUCT_LINK: Locator = container.locator(".g-i-tile__description > a")
            self.PRODUCT_PRICE: Locator = container.locator("[class*='g-i-tile__price']")

    class _Sections:
        def __init__(self, container: Locator) -> None:
            self.FILTERS: Locator = container.locator("[class*='sidebar']")
            self.PAGINATION: Locator = container.locator(".pagination")
            self.SUBCATEGORIES: Locator = container.locator(".subcategories")

    class _Buttons:
        def __init__(self, container: Locator) -> None:
            self.PAGINATION_NEXT: Locator = container.locator("a.pagination__next")
            self.VIEW_GRID: Locator = container.locator("button[data-view='tile']")
            self.VIEW_LIST: Locator = container.locator("button[data-view='list']")

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.Containers = CatalogPage._Containers(page)
        self.Text = CatalogPage._Text(self.Containers.MainContainer)
        self.Items = CatalogPage._Items(self.Containers.MainContainer)
        self.Sections = CatalogPage._Sections(self.Containers.MainContainer)
        self.Buttons = CatalogPage._Buttons(self.Containers.MainContainer)

    def get_page_title(self) -> Locator:
        return self.Text.PAGE_TITLE.first

    def get_product_cards(self) -> Locator:
        return self.Items.PRODUCT_CARD

    def get_product_links(self) -> Locator:
        return self.Items.PRODUCT_LINK

    def get_filters(self) -> Locator:
        return self.Sections.FILTERS

    def get_pagination(self) -> Locator:
        return self.Sections.PAGINATION

    def get_pagination_next(self) -> Locator:
        return self.Buttons.PAGINATION_NEXT

    def get_subcategory_links(self) -> Locator:
        return self.Sections.SUBCATEGORIES.locator("a")

    def get_products_count(self) -> int:
        return self.get_product_cards().count()

    def get_first_product_title(self) -> str:
        return self.get_product_links().first.inner_text()

    def click_first_product(self) -> None:
        self.get_product_links().first.click()
        self.page.wait_for_load_state("networkidle")

    def go_to_next_page(self) -> None:
        self.Buttons.PAGINATION_NEXT.click()
        self.page.wait_for_load_state("networkidle")
