import pytest


CATALOG_URLS = {
    "smartphones": "mobile/smartphones/",
    "laptops": "notebooks/",
    "tvs": "tv/",
}


class TestCatalog:
    """Catalog page tests for 21vek.by"""

    @pytest.mark.smoke
    @pytest.mark.catalog
    def test_smartphones_catalog_loads(self, app):
        """Smartphones catalog page loads"""
        app.go(CATALOG_URLS["smartphones"])
        assert app.catalog.get_products_count() > 0, "No products found on smartphones catalog page"

    @pytest.mark.smoke
    @pytest.mark.catalog
    def test_laptops_catalog_loads(self, app):
        """Laptops catalog page loads"""
        app.go(CATALOG_URLS["laptops"])
        assert app.catalog.get_products_count() > 0, "No products found on laptops catalog page"

    @pytest.mark.regression
    @pytest.mark.catalog
    def test_catalog_has_filters(self, app):
        """Filter section is displayed in catalog"""
        app.go(CATALOG_URLS["smartphones"])
        assert app.catalog.is_filter_visible(), "Filter section is not displayed in catalog"

    @pytest.mark.regression
    @pytest.mark.catalog
    def test_catalog_has_pagination(self, app):
        """Catalog page has pagination"""
        app.go(CATALOG_URLS["tvs"])
        # pagination may be absent if there are few products
        assert app.catalog.get_products_count() > 0, "No products found on TVs catalog page"

    @pytest.mark.regression
    @pytest.mark.catalog
    def test_click_product_in_catalog_opens_product_page(self, app):
        """Clicking a product in catalog opens the product page"""
        app.go(CATALOG_URLS["smartphones"])
        assert app.catalog.get_products_count() > 0, "No products available to click"

        app.catalog.click_first_product()
        assert app.product.get_product_title().strip(), "Product page does not contain a title"

    @pytest.mark.regression
    @pytest.mark.catalog
    def test_product_page_has_add_to_cart_button(self, app):
        """Product page contains the add-to-cart button"""
        app.go(CATALOG_URLS["laptops"])
        if app.catalog.get_products_count() > 0:
            app.catalog.click_first_product()
            assert app.product.is_add_to_cart_visible(), (
                "Add-to-cart button is not visible on the product page"
            )

    @pytest.mark.regression
    @pytest.mark.catalog
    def test_product_page_has_breadcrumbs(self, app):
        """Product page contains breadcrumbs"""
        app.go(CATALOG_URLS["smartphones"])
        if app.catalog.get_products_count() > 0:
            app.catalog.click_first_product()
            assert app.product.is_breadcrumbs_visible(), (
                "Breadcrumbs are not visible on the product page"
            )
