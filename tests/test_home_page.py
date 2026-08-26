import re
import allure
import pytest
from playwright.sync_api import expect


@allure.feature("Главная страница")
class TestHomePage:

    @pytest.mark.smoke
    @allure.story("Загрузка страницы")
    def test_page_title_contains_store_name(self, app):
        """Заголовок вкладки содержит название магазина"""
        with allure.step("Проверить заголовок страницы"):
            expect(app.page).to_have_title(re.compile(r"21.*(vek|век)", re.IGNORECASE))

    @pytest.mark.smoke
    @allure.story("Шапка сайта")
    def test_logo_visible_in_header(self, app):
        """Логотип магазина отображается в шапке"""
        with allure.step("Принять куки если есть запрос"):
            app.home.accept_cookies_if_present()
        with allure.step("Логотип виден в шапке"):
            expect(app.home.get_logo()).to_be_visible()

    @pytest.mark.smoke
    @allure.story("Шапка сайта")
    def test_search_input_visible_and_empty_on_load(self, app):
        """Поле поиска отображается и пустое при загрузке страницы"""
        with allure.step("Поле поиска видно"):
            expect(app.home.get_search_input()).to_be_visible()
        with allure.step("Поле поиска пустое"):
            expect(app.home.get_search_input()).to_have_value("")

    @pytest.mark.smoke
    @allure.story("Футер")
    def test_footer_visible_after_scroll(self, app):
        """Футер отображается после прокрутки страницы вниз"""
        with allure.step("Прокрутить страницу вниз"):
            app.home.scroll_to_bottom()
        with allure.step("Футер виден"):
            expect(app.home.get_footer()).to_be_visible()

    @pytest.mark.smoke
    @allure.story("Шапка сайта")
    def test_cart_link_visible_in_header(self, app):
        """Ссылка на корзину видна в шапке"""
        with allure.step("Ссылка на корзину отображается"):
            expect(app.home.get_cart_link()).to_be_visible()

    @pytest.mark.regression
    @allure.story("Поиск")
    def test_search_input_accepts_text(self, app):
        """Поле поиска принимает введённый текст"""
        with allure.step("Ввести текст в поле поиска"):
            app.home.get_search_input().fill("телефон")
        with allure.step("Проверить, что текст появился в поле"):
            expect(app.home.get_search_input()).to_have_value("телефон")

    @pytest.mark.regression
    @allure.story("Поиск")
    def test_search_input_can_be_cleared(self, app):
        """Поле поиска можно очистить"""
        with allure.step("Ввести текст"):
            app.home.get_search_input().fill("laptop")
        with allure.step("Очистить поле"):
            app.home.get_search_input().clear()
        with allure.step("Поле должно быть пустым"):
            expect(app.home.get_search_input()).to_have_value("")

    @pytest.mark.regression
    @allure.story("Поиск")
    def test_search_navigates_to_results_page(self, app):
        """Отправка поискового запроса открывает страницу результатов"""
        with allure.step("Принять куки если есть запрос"):
            app.home.accept_cookies_if_present()
        with allure.step("Ввести запрос и отправить"):
            app.home.search("ноутбук")
        with allure.step("URL содержит параметр поиска"):
            expect(app.page).to_have_url(re.compile(r"search|query|q="))
        with allure.step("На странице есть карточки товаров"):
            expect(app.search_results.get_product_cards().first).to_be_visible()

    @pytest.mark.regression
    @allure.story("Загрузка страницы")
    def test_page_url_matches_base_url(self, app, base_url):
        """URL главной страницы совпадает с базовым URL"""
        with allure.step("Проверить URL"):
            expect(app.page).to_have_url(re.compile(re.escape(base_url.rstrip("/"))))

    @pytest.mark.regression
    @allure.story("Навигация")
    def test_user_navigates_to_category_and_sees_products(self, app):
        """Пользователь переходит по ссылке категории с главной страницы и попадает в каталог"""
        with allure.step("Принять куки"):
            app.home.accept_cookies_if_present()
        with allure.step("Убедиться, что блок категорий присутствует"):
            category_links = app.home.get_category_links()
            assert category_links.count() > 0, "На главной нет ссылок на категории"
        with allure.step("Кликнуть по первой ссылке категории"):
            category_links.first.click()
            app.page.wait_for_load_state("networkidle")
        with allure.step("URL изменился — перешли в категорию"):
            expect(app.page).not_to_have_url(re.compile(r"^https://www\.21vek\.by/$"))
        with allure.step("На странице есть заголовок категории"):
            expect(app.page.locator("h1").first).to_be_visible()
        with allure.step("Страница содержит карточки товаров"):
            expect(app.catalog.get_product_cards().first).to_be_visible()

    @pytest.mark.regression
    @allure.story("Поиск")
    def test_two_different_searches_return_different_results(self, app):
        """Два разных поисковых запроса возвращают разные наборы результатов"""
        with allure.step("Принять куки"):
            app.home.accept_cookies_if_present()

        with allure.step("Первый поиск — телевизоры"):
            app.home.search("телевизор")
            expect(app.search_results.get_product_cards().first).to_be_visible()
            first_title = app.search_results.get_first_product_title()

        with allure.step("Вернуться на главную и выполнить второй поиск — холодильники"):
            app.go("")
            app.home.search("холодильник")
            expect(app.search_results.get_product_cards().first).to_be_visible()
            second_title = app.search_results.get_first_product_title()

        with allure.step("Результаты двух поисков отличаются"):
            assert first_title != second_title, (
                "Первые результаты по запросам «телевизор» и «холодильник» одинаковы"
            )

    @pytest.mark.regression
    @allure.story("Шапка сайта")
    def test_header_stays_visible_after_scroll_down_and_back(self, app):
        """Шапка сайта остаётся видимой при прокрутке страницы"""
        with allure.step("Принять куки"):
            app.home.accept_cookies_if_present()
        with allure.step("Шапка видна до прокрутки"):
            expect(app.home.get_logo()).to_be_visible()
            expect(app.home.get_search_input()).to_be_visible()
        with allure.step("Прокрутить страницу вниз"):
            app.home.scroll_to_bottom()
        with allure.step("Прокрутить страницу вверх"):
            app.page.evaluate("window.scrollTo(0, 0)")
        with allure.step("Шапка снова полностью видна"):
            expect(app.home.get_logo()).to_be_visible()
            expect(app.home.get_search_input()).to_be_visible()
            expect(app.home.get_cart_link()).to_be_visible()

    @pytest.mark.smoke
    @allure.story("Шапка сайта")
    def test_logo_visible_in_header(self, app):
        """Логотип магазина отображается в шапке"""
        with allure.step("Принять куки если есть запрос"):
            app.home.accept_cookies_if_present()
        with allure.step("Логотип виден в шапке"):
            expect(app.home.get_logo()).to_be_visible()

    @pytest.mark.smoke
    @allure.story("Шапка сайта")
    def test_search_input_visible_and_empty_on_load(self, app):
        """Поле поиска отображается и пустое при загрузке страницы"""
        with allure.step("Поле поиска видно"):
            expect(app.home.get_search_input()).to_be_visible()
        with allure.step("Поле поиска пустое"):
            expect(app.home.get_search_input()).to_have_value("")

    @pytest.mark.smoke
    @allure.story("Футер")
    def test_footer_visible_after_scroll(self, app):
        """Футер отображается после прокрутки страницы вниз"""
        with allure.step("Прокрутить страницу вниз"):
            app.home.scroll_to_bottom()
        with allure.step("Футер виден"):
            expect(app.home.get_footer()).to_be_visible()

    @pytest.mark.smoke
    @allure.story("Шапка сайта")
    def test_cart_link_visible_in_header(self, app):
        """Ссылка на корзину видна в шапке"""
        with allure.step("Ссылка на корзину отображается"):
            expect(app.home.get_cart_link()).to_be_visible()

    @pytest.mark.regression
    @allure.story("Поиск")
    def test_search_input_accepts_text(self, app):
        """Поле поиска принимает введённый текст"""
        with allure.step("Ввести текст в поле поиска"):
            app.home.get_search_input().fill("телефон")
        with allure.step("Проверить, что текст появился в поле"):
            expect(app.home.get_search_input()).to_have_value("телефон")

    @pytest.mark.regression
    @allure.story("Поиск")
    def test_search_input_can_be_cleared(self, app):
        """Поле поиска можно очистить"""
        with allure.step("Ввести текст"):
            app.home.get_search_input().fill("laptop")
        with allure.step("Очистить поле"):
            app.home.get_search_input().clear()
        with allure.step("Поле должно быть пустым"):
            expect(app.home.get_search_input()).to_have_value("")

    @pytest.mark.regression
    @allure.story("Поиск")
    def test_search_navigates_to_results_page(self, app):
        """Отправка поискового запроса открывает страницу результатов"""
        with allure.step("Принять куки если есть запрос"):
            app.home.accept_cookies_if_present()
        with allure.step("Ввести запрос и отправить"):
            app.home.search("ноутбук")
        with allure.step("URL содержит параметр поиска"):
            expect(app.page).to_have_url(re.compile(r"search|query|q="))
        with allure.step("На странице есть карточки товаров"):
            expect(app.search_results.get_product_cards().first).to_be_visible()

    @pytest.mark.regression
    @allure.story("Загрузка страницы")
    def test_page_url_matches_base_url(self, app, base_url):
        """URL главной страницы совпадает с базовым URL"""
        with allure.step("Проверить URL"):
            expect(app.page).to_have_url(re.compile(re.escape(base_url.rstrip("/"))))
