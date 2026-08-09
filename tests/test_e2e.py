import pytest
import allure


@allure.feature("E2E")
class TestE2E:

    @pytest.mark.regression
    @pytest.mark.e2e
    @allure.story("Add to Cart")
    def test_search_product_and_add_to_cart(self, app):
        """Full flow: search → open product → add to cart → verify cart contains the item"""
        with allure.step("Accept cookies and search for a product"):
            app.home.accept_cookies_if_present()
            app.home.search("смартфон")

        with allure.step("Verify search returned results"):
            results_count = app.search_results.get_results_count()
            assert results_count > 0, "Search returned no results — cannot proceed with the flow"

        with allure.step("Remember product title and open product page"):
            expected_title = app.search_results.get_first_product_title()
            assert expected_title.strip(), "First search result has an empty title"
            app.search_results.click_first_product()

        with allure.step("Verify product page loaded correctly"):
            product_title = app.product.get_product_title()
            assert product_title.strip(), "Product page does not have a title"
            assert app.product.is_add_to_cart_visible(), (
                "Add-to-cart button is not visible — cannot add product to cart"
            )

        with allure.step("Add product to cart"):
            app.product.add_to_cart()

        with allure.step("Open cart and verify product is present"):
            app.go("order/basket/")
            assert not app.cart.is_cart_empty(), (
                f"Cart is empty after adding '{product_title}' — product was not added"
            )
            assert app.cart.get_items_count() > 0, "Cart shows 0 items after adding a product"

        with allure.step("Verify checkout button is available"):
            assert app.cart.is_checkout_button_visible(), (
                "Checkout button is not visible in non-empty cart"
            )

    @pytest.mark.regression
    @pytest.mark.e2e
    @allure.story("Catalog to Product Details")
    def test_catalog_browse_to_product_details(self, app):
        """Full flow: open catalog → go to next page → click product → check title,
        price, breadcrumbs and specifications tab"""
        with allure.step("Open laptops catalog"):
            app.go("notebooks/")
            products_count = app.catalog.get_products_count()
            assert products_count > 0, "Laptops catalog is empty — cannot proceed"

        with allure.step("Navigate to page 2 of the catalog"):
            first_page_title = app.catalog.get_first_product_title()
            app.catalog.go_to_next_page()
            second_page_count = app.catalog.get_products_count()
            assert second_page_count > 0, "Page 2 of catalog has no products"

        with allure.step("Verify page 2 contains different products"):
            second_page_title = app.catalog.get_first_product_title()
            assert first_page_title != second_page_title, (
                "First product on page 2 is the same as on page 1 — pagination may not work"
            )

        with allure.step("Click first product on page 2"):
            app.catalog.click_first_product()

        with allure.step("Verify product page title and price are present"):
            product_title = app.product.get_product_title()
            product_price = app.product.get_product_price()
            assert product_title.strip(), "Product page does not have a title"
            assert product_price.strip(), "Product page does not show a price"

        with allure.step("Verify breadcrumbs are displayed"):
            assert app.product.is_breadcrumbs_visible(), (
                "Breadcrumbs are not displayed on the product page"
            )
            crumbs = app.product.get_breadcrumbs()
            assert len(crumbs) >= 2, (
                f"Expected at least 2 breadcrumb levels, got {len(crumbs)}: {crumbs}"
            )

        with allure.step("Open specifications tab and verify page remains accessible"):
            app.product.open_specifications_tab()
            assert app.product.get_product_title().strip(), (
                "Product title disappeared after opening specifications tab"
            )
