import re
import allure
import pytest
from playwright.sync_api import expect


@allure.feature("End-to-End сценарии")
class TestE2E:

    @pytest.mark.regression
    @pytest.mark.e2e
    @allure.story("Добавление товара в корзину через поиск")
    def test_search_product_and_add_to_cart(self, app):
        """Пользователь ищет смартфон, открывает карточку товара, изучает её и добавляет в корзину"""
        with allure.step("Принять куки и перейти к поиску"):
            app.home.accept_cookies_if_present()
            expect(app.home.get_search_input()).to_be_visible()
            expect(app.home.get_search_input()).to_have_value("")

        with allure.step("Ввести запрос «смартфон» и отправить"):
            app.home.search("смартфон")
            expect(app.page).to_have_url(re.compile(r"search|query|q="))

        with allure.step("Страница результатов показывает карточки товаров"):
            expect(app.search_results.get_product_cards().first).to_be_visible()
            results_count = app.search_results.get_results_count()
            assert results_count > 0, "Поиск не вернул ни одного результата"

        with allure.step("Карточка первого товара содержит название и цену"):
            first_title = app.search_results.get_first_product_title()
            assert first_title.strip(), "Название первого товара в результатах пустое"
            expect(app.search_results.get_first_product_price()).to_be_visible()
            expect(app.search_results.get_first_product_price()).to_have_text(re.compile(r"\d"))

        with allure.step("Открыть страницу первого товара"):
            app.search_results.click_first_product()
            expect(app.page).not_to_have_url(re.compile(r"search"))

        with allure.step("Страница товара содержит заголовок, цену и хлебные крошки"):
            expect(app.product.get_title_element()).to_be_visible()
            expect(app.product.get_title_element()).to_have_text(re.compile(r"\S"))
            expect(app.product.get_price_element()).to_be_visible()
            expect(app.product.get_price_element()).to_have_text(re.compile(r"\d"))
            expect(app.product.get_breadcrumbs()).to_be_visible()

        with allure.step("Кнопка «В корзину» доступна"):
            expect(app.product.get_add_to_cart_button()).to_be_visible()

        with allure.step("Добавить товар в корзину"):
            product_title = app.product.get_product_title()
            product_price = app.product.get_product_price()
            app.product.add_to_cart()

        with allure.step("Перейти в корзину и убедиться, что товар добавлен"):
            app.go("order/basket/")
            expect(app.page).to_have_url(re.compile(r"basket"))
            assert not app.cart.is_cart_empty(), (
                f"Корзина пуста после добавления «{product_title}»"
            )
            assert app.cart.get_items_count() > 0

        with allure.step("Название товара в корзине видно и не пустое"):
            expect(app.cart.get_first_item_title()).to_be_visible()
            expect(app.cart.get_first_item_title()).to_have_text(re.compile(r"\S"))

        with allure.step("Общая стоимость отображается в корзине"):
            expect(app.cart.get_total_price_element()).to_be_visible()
            expect(app.cart.get_total_price_element()).to_have_text(re.compile(r"\d"))

        with allure.step("Кнопка «Оформить заказ» доступна"):
            expect(app.cart.get_checkout_button()).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.e2e
    @allure.story("Просмотр каталога и детали товара")
    def test_catalog_browse_to_product_details(self, app):
        """Пользователь открывает каталог ноутбуков, пролистывает страницы, изучает товар"""
        with allure.step("Открыть каталог ноутбуков"):
            app.go("notebooks/")
            expect(app.catalog.get_page_title()).to_be_visible()
            expect(app.catalog.get_page_title()).to_have_text(re.compile(r"\S"))

        with allure.step("Каталог содержит несколько товаров"):
            expect(app.catalog.get_product_cards().first).to_be_visible()
            count = app.catalog.get_products_count()
            assert count > 0, "Каталог ноутбуков пуст"

        with allure.step("Блок фильтров отображается рядом с каталогом"):
            expect(app.catalog.get_filters()).to_be_visible()

        with allure.step("Запомнить первый товар страницы 1 и перейти на страницу 2"):
            first_page_title = app.catalog.get_first_product_title()
            expect(app.catalog.get_pagination_next()).to_be_visible()
            app.catalog.go_to_next_page()

        with allure.step("Страница 2 содержит товары, отличные от страницы 1"):
            expect(app.catalog.get_product_cards().first).to_be_visible()
            second_page_title = app.catalog.get_first_product_title()
            assert first_page_title != second_page_title, (
                "Пагинация не сменила набор товаров"
            )

        with allure.step("Открыть первый товар на странице 2"):
            app.catalog.click_first_product()
            expect(app.page).not_to_have_url(re.compile(r"notebooks/$"))

        with allure.step("Страница товара содержит заголовок и цену"):
            expect(app.product.get_title_element()).to_be_visible()
            expect(app.product.get_title_element()).to_have_text(re.compile(r"\S"))
            expect(app.product.get_price_element()).to_be_visible()
            expect(app.product.get_price_element()).to_have_text(re.compile(r"\d"))

        with allure.step("Хлебные крошки видны и содержат минимум 2 уровня навигации"):
            expect(app.product.get_breadcrumbs()).to_be_visible()
            crumbs = app.product.get_breadcrumb_items()
            assert len(crumbs) >= 2, (
                f"Ожидалось ≥ 2 уровней хлебных крошек, получено {len(crumbs)}: {crumbs}"
            )

        with allure.step("Вкладка характеристик открывается, заголовок товара сохраняется"):
            app.product.open_specifications_tab()
            expect(app.product.get_title_element()).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.e2e
    @allure.story("Полный путь от главной страницы до корзины")
    def test_full_journey_homepage_category_product_cart(self, app):
        """Пользователь заходит на главную, переходит по категории, выбирает товар и добавляет в корзину"""
        with allure.step("Пользователь открывает главную страницу"):
            app.home.accept_cookies_if_present()
            expect(app.home.get_logo()).to_be_visible()
            expect(app.home.get_search_input()).to_be_visible()
            expect(app.home.get_cart_link()).to_be_visible()

        with allure.step("Вместо поиска пользователь переходит в каталог смартфонов напрямую"):
            app.go("mobile/smartphones/")
            expect(app.catalog.get_page_title()).to_be_visible()

        with allure.step("В каталоге есть товары с ценами"):
            expect(app.catalog.get_product_cards().first).to_be_visible()
            assert app.catalog.get_products_count() > 0

        with allure.step("Пользователь открывает первый товар в каталоге"):
            product_name_in_catalog = app.catalog.get_first_product_title()
            app.catalog.click_first_product()

        with allure.step("Страница товара содержит полную информацию"):
            expect(app.product.get_title_element()).to_be_visible()
            expect(app.product.get_price_element()).to_be_visible()
            expect(app.product.get_breadcrumbs()).to_be_visible()
            expect(app.product.get_add_to_cart_button()).to_be_visible()

        with allure.step("Пользователь добавляет товар в корзину"):
            product_page_title = app.product.get_product_title()
            app.product.add_to_cart()

        with allure.step("Пользователь нажимает «Корзина» в шапке"):
            app.home.click_cart()
            expect(app.page).to_have_url(re.compile(r"basket"))

        with allure.step("В корзине есть добавленный товар"):
            assert not app.cart.is_cart_empty(), (
                f"Корзина пуста — товар «{product_page_title}» не был добавлен"
            )
            expect(app.cart.get_first_item_title()).to_be_visible()

        with allure.step("Отображается цена и кнопка оформления заказа"):
            expect(app.cart.get_total_price_element()).to_be_visible()
            expect(app.cart.get_checkout_button()).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.e2e
    @allure.story("Сравнение результатов поиска и выбор товара")
    def test_user_searches_and_selects_specific_product(self, app):
        """Пользователь ищет наушники, просматривает несколько карточек и выбирает подходящий товар"""
        with allure.step("Поиск наушников"):
            app.home.accept_cookies_if_present()
            app.home.search("наушники")
            expect(app.search_results.get_product_cards().first).to_be_visible()

        with allure.step("В результатах более одного товара"):
            count = app.search_results.get_results_count()
            assert count >= 2, f"Найдено слишком мало товаров: {count}"

        with allure.step("Первые два товара имеют разные названия"):
            title_first = app.search_results.get_product_links().nth(0).inner_text()
            title_second = app.search_results.get_product_links().nth(1).inner_text()
            assert title_first.strip(), "Название первого товара пустое"
            assert title_second.strip(), "Название второго товара пустое"
            assert title_first != title_second, "Первые два товара имеют одинаковое название"

        with allure.step("Открыть первый товар и проверить его детальную страницу"):
            app.search_results.click_first_product()
            expect(app.product.get_title_element()).to_be_visible()
            expect(app.product.get_price_element()).to_be_visible()
            expect(app.product.get_add_to_cart_button()).to_be_visible()

        with allure.step("Добавить товар в корзину и перейти в неё"):
            chosen_title = app.product.get_product_title()
            app.product.add_to_cart()
            app.go("order/basket/")

        with allure.step("Корзина содержит выбранный товар"):
            assert app.cart.get_items_count() > 0, "Корзина пуста после добавления"
            expect(app.cart.get_first_item_title()).to_be_visible()
            expect(app.cart.get_checkout_button()).to_be_visible()
