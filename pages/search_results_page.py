from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class SearchResultsPage(BasePage):

    class _Containers:
        def __init__(self, page: Page) -> None:
            self.MainContainer: Locator = page.locator(".search")

    class _Text:
        def __init__(self, container: Locator) -> None:
            self.HEADING: Locator = container.locator(
                "h1[class*='search__title'], h1.page-title"
            )
            self.NO_RESULTS: Locator = container.locator(
                "[class*='search-empty'], [class*='noResults']"
            )
            self.RESULTS_COUNT: Locator = container.locator(
                "[class*='search__count'], [class*='resultsCount']"
            )

    class _Items:
        def __init__(self, container: Locator) -> None:
            self.PRODUCT_CARD: Locator = container.locator(".g-i-tile")
            self.PRODUCT_LINK: Locator = container.locator(".g-i-tile__description > a")
            self.PRODUCT_PRICE: Locator = container.locator("[class*='g-i-tile__price']")

    class _Sections:
        def __init__(self, container: Locator) -> None:
            self.FILTERS: Locator = container.locator("[class*='sidebar']")
            self.PAGINATION: Locator = container.locator(".pagination")

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.Containers = SearchResultsPage._Containers(page)
        self.Text = SearchResultsPage._Text(self.Containers.MainContainer)
        self.Items = SearchResultsPage._Items(self.Containers.MainContainer)
        self.Sections = SearchResultsPage._Sections(self.Containers.MainContainer)

    def get_heading(self) -> Locator:
        return self.Text.HEADING.first

    def get_product_cards(self) -> Locator:
        return self.Items.PRODUCT_CARD

    def get_product_links(self) -> Locator:
        return self.Items.PRODUCT_LINK

    def get_no_results_message(self) -> Locator:
        return self.Text.NO_RESULTS

    def get_first_product_price(self) -> Locator:
        return self.Items.PRODUCT_PRICE.first

    def get_filters(self) -> Locator:
        return self.Sections.FILTERS

    def get_pagination(self) -> Locator:
        return self.Sections.PAGINATION

    def get_results_count(self) -> int:
        return self.get_product_cards().count()

    def is_no_results_shown(self) -> bool:
        return self.get_no_results_message().is_visible()

    def get_first_product_title(self) -> str:
        return self.get_product_links().first.inner_text()

    def click_first_product(self) -> None:
        self.get_product_links().first.click()
        self.page.wait_for_load_state("networkidle")
