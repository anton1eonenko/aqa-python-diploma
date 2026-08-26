import re
import allure
import pytest
from playwright.sync_api import expect


@allure.feature("Корзина")
class TestCart:

    @pytest.mark.smoke
    @pytest.mark.cart
    @allure.story("Пустая корзина")
    def test_empty_cart_page_loads_with_empty_message(self, app):
        """Страница корзины открывается и показывает сообщение о пустой корзине"""
        with allure.step("Открыть страницу корзины напрямую по URL"):
            app.go("order/basket/")
        with allure.step("URL содержит 'basket'"):
            expect(app.page).to_have_url(re.compile(r"basket"))
        with allure.step("Сообщение о пустой корзине видно"):
            expect(app.cart.get_empty_message()).to_be_visible()
        with allure.step("Количество товаров в корзине равно 0"):
            assert app.cart.get_items_count() == 0, "В корзине есть товары при первом открытии"

    @pytest.mark.regression
    @pytest.mark.cart
    @allure.story("Добавление товара")
    def test_add_product_to_cart_full_flow(self, app):
        """Пользователь ищет наушники, открывает карточку и добавляет товар в корзину"""
        with allure.step("Принять куки"):
            app.home.accept_cookies_if_present()

        with allure.step("Поиск товара «наушники»"):
            app.home.search("наушники")

        with allure.step("Результаты поиска появились"):
            expect(app.search_results.get_product_cards().first).to_be_visible()
            assert app.search_results.get_results_count() > 0, "Нет результатов поиска"

        with allure.step("Запомнить название первого товара"):
            product_title = app.search_results.get_first_product_title()
            assert product_title.strip(), "Название первого товара пустое"

        with allure.step("Открыть страницу первого товара"):
            app.search_results.click_first_product()
            expect(app.page).not_to_have_url(re.compile(r"search"))

        with allure.step("Страница товара содержит заголовок, цену и кнопку корзины"):
            expect(app.product.get_title_element()).to_be_visible()
            expect(app.product.get_price_element()).to_be_visible()
            expect(app.product.get_add_to_cart_button()).to_be_visible()

        with allure.step("Добавить товар в корзину"):
            app.product.add_to_cart()

        with allure.step("Перейти в корзину"):
            app.go("order/basket/")

        with allure.step("Корзина не пустая — товар добавлен"):
            assert not app.cart.is_cart_empty(), (
                f"Корзина пуста после добавления «{product_title}»"
            )
            assert app.cart.get_items_count() > 0

        with allure.step("Название товара в корзине видно и не пустое"):
            expect(app.cart.get_first_item_title()).to_be_visible()
            expect(app.cart.get_first_item_title()).to_have_text(re.compile(r"\S"))

        with allure.step("Кнопка оформления заказа доступна"):
            expect(app.cart.get_checkout_button()).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.cart
    @allure.story("Добавление товара")
    def test_cart_shows_total_price_after_adding_item(self, app):
        """После добавления товара в корзине отображается итоговая стоимость"""
        with allure.step("Принять куки"):
            app.home.accept_cookies_if_present()

        with allure.step("Поиск и открытие первого товара"):
            app.home.search("смартфон")
            expect(app.search_results.get_product_cards().first).to_be_visible()
            app.search_results.click_first_product()

        with allure.step("Добавить товар"):
            expect(app.product.get_add_to_cart_button()).to_be_visible()
            app.product.add_to_cart()

        with allure.step("Открыть корзину"):
            app.go("order/basket/")
            assert app.cart.get_items_count() > 0, "Корзина пуста после добавления товара"

        with allure.step("Название товара видно и не пустое"):
            expect(app.cart.get_first_item_title()).to_be_visible()
            expect(app.cart.get_first_item_title()).to_have_text(re.compile(r"\S"))

        with allure.step("Итоговая стоимость отображается и содержит число"):
            expect(app.cart.get_total_price_element()).to_be_visible()
            expect(app.cart.get_total_price_element()).to_have_text(re.compile(r"\d"))

    @pytest.mark.regression
    @pytest.mark.cart
    @allure.story("Оформление заказа")
    def test_checkout_button_present_when_cart_has_items(self, app):
        """Кнопка «Оформить заказ» видна, когда в корзине есть товары"""
        with allure.step("Принять куки"):
            app.home.accept_cookies_if_present()

        with allure.step("Добавить товар через поиск"):
            app.home.search("телефон")
            expect(app.search_results.get_product_cards().first).to_be_visible()
            app.search_results.click_first_product()
            expect(app.product.get_add_to_cart_button()).to_be_visible()
            app.product.add_to_cart()

        with allure.step("Перейти в корзину"):
            app.go("order/basket/")

        with allure.step("Кнопка «Оформить заказ» видна"):
            assert app.cart.get_items_count() > 0, "Товар не добавился в корзину"
            expect(app.cart.get_checkout_button()).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.cart
    @allure.story("Сохранение корзины")
    def test_cart_persists_after_navigating_away_and_back(self, app):
        """Товар в корзине сохраняется при уходе на другую страницу и возврате"""
        with allure.step("Принять куки"):
            app.home.accept_cookies_if_present()

        with allure.step("Найти и добавить товар в корзину"):
            app.home.search("холодильник")
            expect(app.search_results.get_product_cards().first).to_be_visible()
            app.search_results.click_first_product()
            expect(app.product.get_add_to_cart_button()).to_be_visible()
            app.product.add_to_cart()

        with allure.step("Убедиться, что товар в корзине"):
            app.go("order/basket/")
            items_before = app.cart.get_items_count()
            assert items_before > 0, "Корзина пуста после добавления"

        with allure.step("Уйти в каталог ноутбуков"):
            app.go("notebooks/")
            expect(app.catalog.get_product_cards().first).to_be_visible()

        with allure.step("Вернуться в корзину"):
            app.go("order/basket/")

        with allure.step("Товар всё ещё в корзине — корзина не очистилась"):
            items_after = app.cart.get_items_count()
            assert items_after == items_before, (
                f"Количество товаров изменилось: было {items_before}, стало {items_after}"
            )
            expect(app.cart.get_first_item_title()).to_be_visible()
            expect(app.cart.get_checkout_button()).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.cart
    @allure.story("Добавление товара")
    def test_add_product_to_cart_full_flow(self, app):
        """Сценарий: поиск → карточка товара → добавление в корзину → проверка"""
        with allure.step("Принять куки"):
            app.home.accept_cookies_if_present()

        with allure.step("Поиск товара «наушники»"):
            app.home.search("наушники")

        with allure.step("Результаты поиска появились"):
            expect(app.search_results.get_product_cards().first).to_be_visible()

        with allure.step("Запомнить название первого товара"):
            product_title = app.search_results.get_first_product_title()

        with allure.step("Открыть страницу первого товара"):
            app.search_results.click_first_product()

        with allure.step("Кнопка «В корзину» доступна"):
            expect(app.product.get_add_to_cart_button()).to_be_visible()

        with allure.step("Добавить товар в корзину"):
            app.product.add_to_cart()

        with allure.step("Перейти в корзину"):
            app.go("order/basket/")

        with allure.step("Корзина не пустая"):
            assert not app.cart.is_cart_empty(), (
                f"Корзина пуста после добавления «{product_title}»"
            )
            assert app.cart.get_items_count() > 0

        with allure.step("Кнопка оформления заказа доступна"):
            expect(app.cart.get_checkout_button()).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.cart
    @allure.story("Добавление товара")
    def test_cart_item_title_visible_after_adding(self, app):
        """После добавления товара в корзине отображается название товара"""
        with allure.step("Принять куки"):
            app.home.accept_cookies_if_present()

        with allure.step("Поиск и открытие первого товара"):
            app.home.search("смартфон")
            expect(app.search_results.get_product_cards().first).to_be_visible()
            app.search_results.click_first_product()

        with allure.step("Добавить товар"):
            expect(app.product.get_add_to_cart_button()).to_be_visible()
            app.product.add_to_cart()

        with allure.step("Открыть корзину"):
            app.go("order/basket/")
            assert app.cart.get_items_count() > 0, "Корзина пуста после добавления товара"

        with allure.step("Название товара в корзине видно и не пустое"):
            expect(app.cart.get_first_item_title()).to_be_visible()
            expect(app.cart.get_first_item_title()).to_have_text(re.compile(r"\S"))

    @pytest.mark.regression
    @pytest.mark.cart
    @allure.story("Оформление заказа")
    def test_checkout_button_present_when_cart_has_items(self, app):
        """Кнопка оформления заказа видна, когда в корзине есть товары"""
        with allure.step("Принять куки"):
            app.home.accept_cookies_if_present()

        with allure.step("Добавить товар через поиск"):
            app.home.search("телефон")
            expect(app.search_results.get_product_cards().first).to_be_visible()
            app.search_results.click_first_product()
            expect(app.product.get_add_to_cart_button()).to_be_visible()
            app.product.add_to_cart()

        with allure.step("Перейти в корзину"):
            app.go("order/basket/")

        with allure.step("Кнопка «Оформить заказ» видна"):
            assert app.cart.get_items_count() > 0, "Товар не добавился в корзину"
            expect(app.cart.get_checkout_button()).to_be_visible()
