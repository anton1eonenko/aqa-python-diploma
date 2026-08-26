import re
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class CartPage(BasePage):

    class _Containers:
        def __init__(self, page: Page) -> None:
            self.MainContainer: Locator = page.locator("main")

    class _Text:
        def __init__(self, container: Locator) -> None:
            self.TITLE: Locator = container.locator("h1")
            self.TOTAL_PRICE: Locator = container.locator(
                "[class*='totalPrice'], [class*='basketTotal'], [class*='total-price']"
            )

    class _Items:
        def __init__(self, container: Locator) -> None:
            self.CART_ITEM: Locator = container.locator("[class*='BasketItem']")
            self.ITEM_TITLE: Locator = container.locator("[class*='BasketItem_title']")
            self.ITEM_PRICE: Locator = container.locator("[class*='BasketItem_price']")
            self.ITEM_QUANTITY: Locator = container.locator(
                "[class*='BasketItem'] input[type='number']"
            )

    class _Buttons:
        def __init__(self, container: Locator) -> None:
            self.REMOVE_ITEM: Locator = container.locator(
                "button[class*='BasketItem_remove'], button[class*='removeItem']"
            )

    class _Links:
        def __init__(self, container: Locator) -> None:
            self.CHECKOUT: Locator = container.get_by_role(
                "link", name=re.compile(r"оформить", re.IGNORECASE)
            )

    class _Sections:
        def __init__(self, page: Page) -> None:
            self.EMPTY_MESSAGE: Locator = page.locator("[class*='emptyText']")

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.Containers = CartPage._Containers(page)
        self.Text = CartPage._Text(self.Containers.MainContainer)
        self.Items = CartPage._Items(self.Containers.MainContainer)
        self.Buttons = CartPage._Buttons(self.Containers.MainContainer)
        self.Links = CartPage._Links(self.Containers.MainContainer)
        self.Sections = CartPage._Sections(page)

    def get_cart_items(self) -> Locator:
        return self.Items.CART_ITEM

    def get_empty_message(self) -> Locator:
        return self.Sections.EMPTY_MESSAGE

    def get_total_price_element(self) -> Locator:
        return self.Text.TOTAL_PRICE.first

    def get_checkout_button(self) -> Locator:
        return self.Links.CHECKOUT.first

    def get_first_item_title(self) -> Locator:
        return self.Items.ITEM_TITLE.first

    def get_items_count(self) -> int:
        return self.get_cart_items().count()

    def is_cart_empty(self) -> bool:
        return self.get_empty_message().is_visible()

    def get_total_price(self) -> str:
        return self.get_total_price_element().inner_text()

    def is_checkout_button_visible(self) -> bool:
        return self.get_checkout_button().is_visible()

    def remove_first_item(self) -> None:
        self.Buttons.REMOVE_ITEM.first.click()
        self.page.wait_for_load_state("networkidle")
