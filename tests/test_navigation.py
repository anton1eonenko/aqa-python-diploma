import pytest
import allure


@allure.feature("Navigation")
class TestNavigation:
    """Navigation tests for 21vek.by"""

    @pytest.mark.smoke
    @pytest.mark.navigation
    @allure.story("Page Accessibility")
    def test_basket_page_accessible(self, app):
        """Cart page opens successfully"""
        app.go("order/basket/")
        assert "basket" in app.page.url

    @pytest.mark.smoke
    @pytest.mark.navigation
    @allure.story("Page Accessibility")
    def test_contacts_page_accessible(self, app, base_url):
        """Contacts page opens successfully"""
        app.page.goto(f"{base_url}/contacts/")
        app.page.wait_for_load_state("domcontentloaded")
        assert app.page.title()

    @pytest.mark.smoke
    @pytest.mark.navigation
    @allure.story("Page Accessibility")
    def test_about_page_accessible(self, app, base_url):
        """About page opens successfully"""
        app.page.goto(f"{base_url}/about/")
        app.page.wait_for_load_state("domcontentloaded")
        assert app.page.title()

    @pytest.mark.regression
    @pytest.mark.navigation
    @allure.story("Back Navigation")
    def test_browser_back_returns_to_home(self, app, base_url):
        """Browser back button returns to home page"""
        app.home.search("телефон")
        app.page.go_back()
        app.page.wait_for_load_state("domcontentloaded")
        assert base_url in app.page.url

    @pytest.mark.regression
    @pytest.mark.navigation
    @allure.story("Unknown Page")
    def test_unknown_url_does_not_crash(self, app, base_url):
        """Unknown URL does not cause an unhandled error"""
        app.page.goto(f"{base_url}/this-page-xyz-does-not-exist-789/")
        app.page.wait_for_load_state("domcontentloaded")
        assert app.page.title()
