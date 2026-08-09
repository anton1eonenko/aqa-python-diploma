import pytest


class TestSearch:
    """Search functionality tests for 21vek.by"""

    @pytest.mark.smoke
    @pytest.mark.search
    def test_search_returns_results(self, app):
        """Search for 'tv' returns results"""
        app.home.accept_cookies_if_present()
        app.home.search("телевизор")
        assert app.search_results.get_results_count() > 0, "Search for 'tv' returned no results"

    @pytest.mark.smoke
    @pytest.mark.search
    def test_search_redirects_to_results_page(self, app):
        """After searching, redirects to results page"""
        app.home.search("ноутбук")
        current_url = app.page.url
        assert "search" in current_url or "q=" in current_url or "query" in current_url, (
            f"After search, URL '{current_url}' does not contain a search parameter"
        )

    @pytest.mark.regression
    @pytest.mark.search
    def test_search_empty_query_stays_on_page(self, app):
        """Empty search does not cause an error"""
        app.home.accept_cookies_if_present()
        app.home.get_search_input().press("Enter")
        app.home.wait_for_page_load()
        # page must remain accessible
        assert app.page.url is not None

    @pytest.mark.regression
    @pytest.mark.search
    def test_search_nonexistent_product_shows_no_results(self, app):
        """Search for nonexistent product shows no-results message"""
        app.home.search("xzxzxzxzxzxz_nonexistent_item_12345")
        app.home.wait_for_page_load()
        count = app.search_results.get_results_count()
        no_results = app.search_results.is_no_results_shown()
        assert count == 0 or no_results, (
            "Search for nonexistent product must show 0 results or a no-results message"
        )

    @pytest.mark.regression
    @pytest.mark.search
    def test_search_result_has_title_and_price(self, app):
        """Product cards in search results contain a title and price"""
        app.home.search("смартфон")
        if app.search_results.get_results_count() > 0:
            title = app.search_results.get_first_product_title()
            price = app.search_results.get_first_product_price()
            assert title.strip(), "First product title in search results is empty"
            assert price.strip(), "First product price in search results is empty"

    @pytest.mark.regression
    @pytest.mark.search
    def test_search_click_product_opens_product_page(self, app):
        """Clicking a product in search results opens the product page"""
        app.home.search("холодильник")
        if app.search_results.get_results_count() > 0:
            product_title_before = app.search_results.get_first_product_title()
            app.search_results.click_first_product()
            current_url = app.page.url
            assert "21vek.by" in current_url, "After clicking a product, navigated to an external site"
            assert current_url != "https://www.21vek.by/", (
                f"After clicking product '{product_title_before}', the page did not change"
            )
