import pytest
import allure


@allure.feature("UI Elements")
class TestUI:
    """UI element tests for 21vek.by"""

    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.story("Page Title")
    def test_page_title_not_empty(self, app):
        """Browser tab title is not empty"""
        assert app.page.title() != ""

    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.story("Search Input")
    def test_search_input_empty_on_load(self, app):
        """Search input is empty on home page load"""
        assert app.home.get_search_input().input_value() == ""

    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.story("Page Language")
    def test_page_has_lang_attribute(self, app):
        """HTML element has a lang attribute"""
        lang = app.page.locator("html").get_attribute("lang")
        assert lang is not None

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.story("Search Input")
    def test_search_input_accepts_text(self, app):
        """Search input accepts text input"""
        app.home.get_search_input().fill("test")
        assert app.home.get_search_input().input_value() == "test"

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.story("Site Header")
    def test_header_has_logo_and_search(self, app):
        """Header contains logo and search input simultaneously"""
        assert app.home.is_logo_visible()
        assert app.home.get_search_input().is_visible()

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.story("Search Input")
    def test_search_input_cleared_after_fill_and_clear(self, app):
        """Search input can be cleared"""
        app.home.get_search_input().fill("something")
        app.home.get_search_input().clear()
        assert app.home.get_search_input().input_value() == ""
