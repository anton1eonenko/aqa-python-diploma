from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class HomePage(BasePage):

    class _Containers:
        def __init__(self, page: Page) -> None:
            self.MainContainer: Locator = page.locator(".header")

    class _Buttons:
        def __init__(self, container: Locator, page: Page) -> None:
            self.SEARCH_SUBMIT: Locator = container.locator("button.search__submit")
            self.CATALOG_MENU: Locator = container.locator("button.header__catalog-btn")
            self.COOKIE_ACCEPT: Locator = page.locator("button[class*='cookieAccept']")

    class _InputFields:
        def __init__(self, container: Locator) -> None:
            self.SEARCH: Locator = container.locator("input[name='query']")

    class _Links:
        def __init__(self, container: Locator) -> None:
            self.LOGO: Locator = container.locator("[itemprop='logo']")
            self.CART: Locator = container.locator("a.header__cart")

    class _Sections:
        def __init__(self, page: Page) -> None:
            self.FOOTER: Locator = page.locator("footer.footer")
            self.CATEGORIES: Locator = page.locator(".main-categories")

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.Containers = HomePage._Containers(page)
        self.Buttons = HomePage._Buttons(self.Containers.MainContainer, page)
        self.InputFields = HomePage._InputFields(self.Containers.MainContainer)
        self.Links = HomePage._Links(self.Containers.MainContainer)
        self.Sections = HomePage._Sections(page)

    def accept_cookies_if_present(self) -> None:
        try:
            btn = self.Buttons.COOKIE_ACCEPT.first
            if btn.is_visible(timeout=3000):
                btn.click()
        except Exception:
            pass

    def search(self, query: str) -> None:
        self.InputFields.SEARCH.fill(query)
        self.InputFields.SEARCH.press("Enter")
        self.page.wait_for_load_state("networkidle")

    def get_search_input(self) -> Locator:
        return self.InputFields.SEARCH

    def get_logo(self) -> Locator:
        return self.Links.LOGO

    def get_cart_link(self) -> Locator:
        return self.Links.CART

    def get_footer(self) -> Locator:
        return self.Sections.FOOTER

    def click_cart(self) -> None:
        self.Links.CART.click()
        self.page.wait_for_load_state("networkidle")

    def get_category_links(self) -> Locator:
        return self.Sections.CATEGORIES.locator("a")
