from playwright.sync_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):
    # Locators
    CART_TITLE = "h1:has-text('Корзина'), h1.cart-title"
    CART_ITEMS = ".cart-item, .basket-item, .order-item"
    EMPTY_CART_MSG = "[class*='emptyText']"
    ITEM_TITLE = "[class*='BasketItem_title_']"
    ITEM_PRICE = ".cart-item__price, .basket-item__price"
    ITEM_QUANTITY = ".cart-item__quantity input, .basket-item__quantity input"
    REMOVE_ITEM_BTN = "button.cart-item__remove, .remove-item"
    TOTAL_PRICE = ".cart-total__price, .order-total, .total-price"
    CHECKOUT_BUTTON = "a:has-text('Оформить заказ'), button:has-text('Оформить заказ'), .checkout-btn"

    def __init__(self, page: Page):
        super().__init__(page)

    def get_items_count(self) -> int:
        return self.page.locator(self.CART_ITEMS).count()

    def is_cart_empty(self) -> bool:
        return self.page.locator(self.EMPTY_CART_MSG).is_visible()

    def get_total_price(self) -> str:
        return self.page.locator(self.TOTAL_PRICE).first.inner_text()

    def is_checkout_button_visible(self) -> bool:
        return self.page.locator(self.CHECKOUT_BUTTON).is_visible()

    def get_first_item_title(self) -> str:
        return self.page.locator(self.ITEM_TITLE).first.inner_text()

    def remove_first_item(self):
        self.page.locator(self.REMOVE_ITEM_BTN).first.click()
        self.page.wait_for_load_state("networkidle")
