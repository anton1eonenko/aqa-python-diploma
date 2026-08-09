import pytest


class TestHomePage:
    """Home page tests for 21vek.by"""

    @pytest.mark.smoke
    def test_page_title_contains_21vek(self, app):
        """Page title contains the store name"""
        title = app.home.get_title()
        assert "21vek" in title.lower() or "21век" in title.lower(), (
            f"Page title does not contain '21vek': '{title}'"
        )

    @pytest.mark.smoke
    def test_logo_is_visible(self, app):
        """Logo is visible on the home page"""
        app.home.accept_cookies_if_present()
        assert app.home.is_logo_visible(), "Logo is not visible on the home page"

    @pytest.mark.smoke
    def test_header_is_visible(self, app):
        """Site header is visible"""
        assert app.home.is_header_visible(), "Site header is not visible"

    @pytest.mark.smoke
    def test_footer_is_visible(self, app):
        """Site footer is visible"""
        app.home.scroll_to_bottom()
        assert app.home.is_footer_visible(), "Site footer is not visible"

    @pytest.mark.smoke
    def test_search_input_is_present(self, app):
        """Search input is present on the home page"""
        assert app.home.get_search_input().is_visible(), "Search input is not visible"

    @pytest.mark.regression
    def test_page_url_is_correct(self, app, base_url):
        """Home page URL is correct"""
        current_url = app.home.get_url()
        assert base_url in current_url, (
            f"Page URL '{current_url}' does not match expected '{base_url}'"
        )

    @pytest.mark.regression
    def test_page_loads_successfully(self, app):
        """Page loads without errors"""
        app.home.wait_for_page_load()
        title = app.home.get_title()
        assert title, "Page title is empty — page did not load"
