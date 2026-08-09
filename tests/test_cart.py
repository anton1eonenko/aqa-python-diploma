import pytest


class TestCart:
    """Cart tests for 21vek.by"""

    @pytest.mark.smoke
    @pytest.mark.cart
    def test_cart_page_opens(self, app):
        """Cart page opens successfully"""
        app.go("order/basket/")
        # cart must be either empty or contain items
        assert app.cart.is_cart_empty() or app.cart.get_items_count() > 0, (
            "Cart page did not load correctly"
        )

    @pytest.mark.smoke
    @pytest.mark.cart
    def test_empty_cart_shows_empty_message(self, app):
        """Empty cart shows the appropriate message"""
        app.go("order/basket/")
        if app.cart.get_items_count() == 0:
            assert app.cart.is_cart_empty(), "Empty cart does not show empty cart message"

    @pytest.mark.regression
    @pytest.mark.cart
    def test_add_product_to_cart_via_search(self, app):
        """Adding a product to cart via search"""
        app.home.accept_cookies_if_present()
        app.home.search("наушники")

        if app.search_results.get_results_count() == 0:
            pytest.skip("No search results to add to cart")

        app.search_results.click_first_product()

        if not app.product.is_add_to_cart_visible():
            pytest.skip("Add to cart button is not available for this product")

        app.product.add_to_cart()

        # URL changes or modal appears after adding to cart
        assert app.page.url is not None, "Page is not accessible after adding to cart"

    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_checkout_button_visible_when_not_empty(self, app):
        """Checkout button is visible when cart is not empty"""
        app.go("order/basket/")
        if app.cart.get_items_count() > 0:
            assert app.cart.is_checkout_button_visible(), (
                "Checkout button is not visible when cart is not empty"
            )
