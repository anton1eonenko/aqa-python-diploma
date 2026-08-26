import re
import allure
import pytest
from playwright.sync_api import expect


@allure.feature("UI элементы")
class TestUI:

    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.story("Заголовок страницы")
    def test_page_title_not_empty(self, app):
        """Заголовок вкладки браузера не пустой"""
        with allure.step("Заголовок содержит непустую строку"):
            expect(app.page).to_have_title(re.compile(r"\S"))

    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.story("Поле поиска")
    def test_search_input_empty_on_load(self, app):
        """Поле поиска пустое при загрузке главной страницы"""
        with allure.step("Значение поля поиска — пустая строка"):
            expect(app.home.get_search_input()).to_have_value("")

    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.story("Атрибуты HTML")
    def test_page_has_lang_attribute(self, app):
        """Тег HTML имеет непустой атрибут lang"""
        with allure.step("Получить атрибут lang тега html"):
            lang = app.page.locator("html").get_attribute("lang")
        with allure.step("Атрибут lang присутствует и не пустой"):
            assert lang is not None and lang.strip() != "", (
                "Атрибут lang пустой или отсутствует"
            )

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.story("Поле поиска")
    def test_search_input_accepts_text(self, app):
        """Поле поиска принимает ввод пользователя"""
        with allure.step("Ввести текст в поле поиска"):
            app.home.get_search_input().fill("test")
        with allure.step("Текст отображается в поле"):
            expect(app.home.get_search_input()).to_have_value("test")

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.story("Шапка сайта")
    def test_header_contains_logo_and_search(self, app):
        """Шапка одновременно содержит логотип и поле поиска"""
        with allure.step("Логотип виден"):
            expect(app.home.get_logo()).to_be_visible()
        with allure.step("Поле поиска видно"):
            expect(app.home.get_search_input()).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.story("Поле поиска")
    def test_search_input_cleared_after_fill_and_clear(self, app):
        """Поле поиска очищается методом clear()"""
        with allure.step("Ввести значение"):
            app.home.get_search_input().fill("something")
        with allure.step("Очистить поле"):
            app.home.get_search_input().clear()
        with allure.step("Поле пустое"):
            expect(app.home.get_search_input()).to_have_value("")

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.story("Кнопка корзины")
    def test_cart_link_navigates_to_cart_page(self, app):
        """Клик по иконке корзины открывает страницу корзины"""
        with allure.step("Кликнуть по иконке корзины"):
            app.home.click_cart()
        with allure.step("URL содержит 'basket'"):
            expect(app.page).to_have_url(re.compile(r"basket"))
        with allure.step("Страница корзины показывает пустую корзину или товары"):
            loaded = app.cart.is_cart_empty() or app.cart.get_items_count() > 0
            assert loaded, "Страница корзины не загрузила ожидаемый контент"
