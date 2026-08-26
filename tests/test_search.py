import re
import allure
import pytest
from playwright.sync_api import expect


@allure.feature("Поиск товаров")
class TestSearch:

    @pytest.mark.smoke
    @pytest.mark.search
    @allure.story("Результаты поиска")
    def test_search_returns_relevant_results(self, app):
        """Поиск по запросу «телевизор» возвращает карточки товаров"""
        with allure.step("Принять куки"):
            app.home.accept_cookies_if_present()
        with allure.step("Ввести запрос и отправить"):
            app.home.search("телевизор")
        with allure.step("Первая карточка товара видна"):
            expect(app.search_results.get_product_cards().first).to_be_visible()
        with allure.step("Количество результатов больше 0"):
            assert app.search_results.get_results_count() > 0

    @pytest.mark.smoke
    @pytest.mark.search
    @allure.story("URL страницы поиска")
    def test_search_url_contains_query_parameter(self, app):
        """URL после поиска содержит поисковый параметр"""
        with allure.step("Выполнить поиск"):
            app.home.search("ноутбук")
        with allure.step("URL содержит параметр поиска"):
            expect(app.page).to_have_url(re.compile(r"search|query|q="))

    @pytest.mark.regression
    @pytest.mark.search
    @allure.story("Карточка товара")
    def test_search_result_shows_title_and_price(self, app):
        """Карточка товара в результатах поиска содержит название и цену"""
        with allure.step("Поиск смартфона"):
            app.home.search("смартфон")
        with allure.step("Результаты поиска загружены"):
            expect(app.search_results.get_product_cards().first).to_be_visible()
        with allure.step("Первый товар имеет непустое название"):
            first_title = app.search_results.get_first_product_title()
            assert first_title.strip(), "Название первого товара пустое"
        with allure.step("Цена первого товара видна и содержит число"):
            expect(app.search_results.get_first_product_price()).to_be_visible()
            expect(app.search_results.get_first_product_price()).to_have_text(
                re.compile(r"\d")
            )

    @pytest.mark.regression
    @pytest.mark.search
    @allure.story("Переход к товару")
    def test_click_search_result_opens_product_page(self, app):
        """Клик по товару в результатах поиска открывает страницу товара"""
        with allure.step("Поиск холодильника"):
            app.home.search("холодильник")
        with allure.step("Результаты поиска загружены"):
            expect(app.search_results.get_product_cards().first).to_be_visible()
        with allure.step("Запомнить название первого товара"):
            title_before = app.search_results.get_first_product_title()
        with allure.step("Кликнуть по первому товару"):
            app.search_results.click_first_product()
        with allure.step("Открылась страница товара, а не страница поиска"):
            expect(app.page).not_to_have_url(re.compile(r"search"))
        with allure.step("Заголовок товара виден"):
            expect(app.product.get_title_element()).to_be_visible()
        with allure.step("Заголовок товара не пустой"):
            expect(app.product.get_title_element()).to_have_text(re.compile(r"\S"))

    @pytest.mark.regression
    @pytest.mark.search
    @allure.story("Пустой поиск")
    def test_empty_search_does_not_crash(self, app):
        """Отправка пустого поиска не вызывает критическую ошибку"""
        with allure.step("Принять куки"):
            app.home.accept_cookies_if_present()
        with allure.step("Отправить пустой запрос"):
            app.home.get_search_input().press("Enter")
            app.home.wait_for_page_load()
        with allure.step("Страница доступна — заголовок не пустой"):
            expect(app.page).to_have_title(re.compile(r"\S"))

    @pytest.mark.regression
    @pytest.mark.search
    @allure.story("Несуществующий товар")
    def test_search_nonexistent_item_shows_no_results(self, app):
        """Поиск несуществующего товара показывает 0 результатов или сообщение «ничего не найдено»"""
        with allure.step("Поиск заведомо несуществующего товара"):
            app.home.search("xzxzxzxzxzxz_nonexistent_item_12345")
            app.home.wait_for_page_load()
        with allure.step("Нет результатов или видно сообщение об отсутствии"):
            count = app.search_results.get_results_count()
            no_results = app.search_results.is_no_results_shown()
            assert count == 0 or no_results, (
                "Поиск несуществующего товара вернул результаты без сообщения"
            )

    @pytest.mark.regression
    @pytest.mark.search
    @allure.story("Переход к товару")
    def test_user_opens_product_from_search_then_navigates_back(self, app):
        """Пользователь открывает товар из результатов поиска и возвращается назад"""
        with allure.step("Принять куки и найти товар"):
            app.home.accept_cookies_if_present()
            app.home.search("телевизор")
            expect(app.search_results.get_product_cards().first).to_be_visible()

        with allure.step("Запомнить URL страницы результатов"):
            search_url = app.page.url

        with allure.step("Запомнить название первого товара и открыть его"):
            first_title = app.search_results.get_first_product_title()
            app.search_results.click_first_product()
            expect(app.product.get_title_element()).to_be_visible()

        with allure.step("Нажать «Назад» в браузере"):
            app.page.go_back()
            app.page.wait_for_load_state("networkidle")

        with allure.step("Вернулись на страницу результатов поиска"):
            expect(app.page).to_have_url(re.compile(r"search|query|q="))
            expect(app.search_results.get_product_cards().first).to_be_visible()

        with allure.step("Первый товар в результатах тот же"):
            title_after_back = app.search_results.get_first_product_title()
            assert title_after_back == first_title, (
                "После возврата первый результат поиска изменился"
            )

    @pytest.mark.regression
    @pytest.mark.search
    @allure.story("Результаты поиска")
    def test_two_different_searches_return_different_results(self, app):
        """Два разных поисковых запроса возвращают разные наборы результатов"""
        with allure.step("Принять куки"):
            app.home.accept_cookies_if_present()

        with allure.step("Первый поиск — телевизоры"):
            app.home.search("телевизор")
            expect(app.search_results.get_product_cards().first).to_be_visible()
            first_search_title = app.search_results.get_first_product_title()
            first_search_count = app.search_results.get_results_count()

        with allure.step("Второй поиск — холодильники (со страницы результатов)"):
            app.go("")
            app.home.search("холодильник")
            expect(app.search_results.get_product_cards().first).to_be_visible()
            second_search_title = app.search_results.get_first_product_title()

        with allure.step("Первые результаты двух поисков различаются"):
            assert first_search_title != second_search_title, (
                "Первые результаты по запросам «телевизор» и «холодильник» одинаковы"
            )
