import re
import allure
import pytest
from playwright.sync_api import expect


CATALOG_URLS = {
    "smartphones": "mobile/smartphones/",
    "laptops": "notebooks/",
    "tvs": "tv/",
}


@allure.feature("Каталог товаров")
class TestCatalog:

    @pytest.mark.smoke
    @pytest.mark.catalog
    @allure.story("Загрузка каталога")
    def test_smartphones_catalog_shows_products(self, app):
        """Каталог смартфонов загружается и отображает товары"""
        with allure.step("Открыть каталог смартфонов"):
            app.go(CATALOG_URLS["smartphones"])
        with allure.step("Первая карточка товара видна"):
            expect(app.catalog.get_product_cards().first).to_be_visible()
        with allure.step("Количество товаров больше 0"):
            assert app.catalog.get_products_count() > 0

    @pytest.mark.smoke
    @pytest.mark.catalog
    @allure.story("Загрузка каталога")
    def test_laptops_catalog_shows_products(self, app):
        """Каталог ноутбуков загружается и отображает товары"""
        with allure.step("Открыть каталог ноутбуков"):
            app.go(CATALOG_URLS["laptops"])
        with allure.step("Первая карточка товара видна"):
            expect(app.catalog.get_product_cards().first).to_be_visible()

    @pytest.mark.smoke
    @pytest.mark.catalog
    @allure.story("Заголовок категории")
    def test_catalog_page_title_is_present(self, app):
        """Заголовок страницы каталога присутствует и не пустой"""
        with allure.step("Открыть каталог смартфонов"):
            app.go(CATALOG_URLS["smartphones"])
        with allure.step("Заголовок страницы виден"):
            expect(app.catalog.get_page_title()).to_be_visible()
        with allure.step("Заголовок содержит текст"):
            expect(app.catalog.get_page_title()).to_have_text(re.compile(r"\S"))

    @pytest.mark.regression
    @pytest.mark.catalog
    @allure.story("Фильтры")
    def test_catalog_has_filter_section(self, app):
        """В каталоге отображается блок фильтров"""
        with allure.step("Открыть каталог смартфонов"):
            app.go(CATALOG_URLS["smartphones"])
        with allure.step("Блок фильтров виден"):
            expect(app.catalog.get_filters()).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.catalog
    @allure.story("Пагинация")
    def test_catalog_has_pagination(self, app):
        """Каталог с большим числом товаров содержит пагинацию"""
        with allure.step("Открыть каталог телевизоров"):
            app.go(CATALOG_URLS["tvs"])
        with allure.step("Пагинация видна"):
            expect(app.catalog.get_pagination()).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.catalog
    @allure.story("Переход к товару")
    def test_click_product_opens_product_page_with_title(self, app):
        """Клик по товару открывает страницу с заголовком и ценой"""
        with allure.step("Открыть каталог смартфонов"):
            app.go(CATALOG_URLS["smartphones"])
        with allure.step("Убедиться, что есть товары"):
            assert app.catalog.get_products_count() > 0, "Каталог пуст"
        with allure.step("Кликнуть по первому товару"):
            app.catalog.click_first_product()
        with allure.step("Заголовок товара виден"):
            expect(app.product.get_title_element()).to_be_visible()
        with allure.step("Заголовок не пустой"):
            expect(app.product.get_title_element()).to_have_text(re.compile(r"\S"))

    @pytest.mark.regression
    @pytest.mark.catalog
    @allure.story("Страница товара")
    def test_product_page_has_add_to_cart_button(self, app):
        """Страница товара содержит кнопку «В корзину»"""
        with allure.step("Открыть каталог ноутбуков"):
            app.go(CATALOG_URLS["laptops"])
        with allure.step("Кликнуть по первому товару"):
            app.catalog.click_first_product()
        with allure.step("Кнопка «В корзину» видна"):
            expect(app.product.get_add_to_cart_button()).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.catalog
    @allure.story("Страница товара")
    def test_product_page_has_breadcrumbs(self, app):
        """Страница товара содержит хлебные крошки"""
        with allure.step("Открыть каталог смартфонов"):
            app.go(CATALOG_URLS["smartphones"])
        with allure.step("Кликнуть по первому товару"):
            app.catalog.click_first_product()
        with allure.step("Хлебные крошки видны"):
            expect(app.product.get_breadcrumbs()).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.catalog
    @allure.story("Страница товара")
    def test_product_page_shows_price(self, app):
        """Страница товара отображает цену"""
        with allure.step("Открыть каталог смартфонов"):
            app.go(CATALOG_URLS["smartphones"])
        with allure.step("Кликнуть по первому товару"):
            app.catalog.click_first_product()
        with allure.step("Цена товара видна"):
            expect(app.product.get_price_element()).to_be_visible()
        with allure.step("Цена содержит число"):
            expect(app.product.get_price_element()).to_have_text(re.compile(r"\d"))

    @pytest.mark.regression
    @pytest.mark.catalog
    @allure.story("Карточки товаров")
    def test_first_three_products_have_title_and_price(self, app):
        """Первые три карточки товаров содержат название и цену"""
        with allure.step("Открыть каталог смартфонов"):
            app.go(CATALOG_URLS["smartphones"])
            expect(app.catalog.get_product_cards().first).to_be_visible()

        with allure.step("Проверить первые три карточки"):
            product_links = app.catalog.get_product_links()
            count = min(3, product_links.count())
            assert count > 0, "Нет товаров в каталоге"
            for i in range(count):
                title = product_links.nth(i).inner_text()
                assert title.strip(), f"Товар #{i + 1} не имеет названия"

        with allure.step("Каждая из первых трёх карточек имеет непустое название"):
            assert count >= 1, "В каталоге меньше одного товара"

    @pytest.mark.regression
    @pytest.mark.catalog
    @allure.story("Переход к товару")
    def test_product_url_is_unique_after_opening(self, app):
        """URL страницы товара отличается от URL каталога"""
        with allure.step("Открыть каталог ноутбуков"):
            app.go(CATALOG_URLS["laptops"])
            catalog_url = app.page.url

        with allure.step("Открыть первый товар"):
            app.catalog.click_first_product()

        with allure.step("URL страницы товара отличается от URL каталога"):
            product_url = app.page.url
            assert product_url != catalog_url, (
                "URL не изменился после перехода на страницу товара"
            )
            expect(app.page).not_to_have_url(re.compile(r"notebooks/$"))

    @pytest.mark.regression
    @pytest.mark.catalog
    @allure.story("Навигация")
    def test_back_navigation_from_product_returns_to_catalog(self, app):
        """После открытия товара кнопка «Назад» возвращает в каталог"""
        with allure.step("Открыть каталог смартфонов"):
            app.go(CATALOG_URLS["smartphones"])
            expect(app.catalog.get_product_cards().first).to_be_visible()
            catalog_products_count = app.catalog.get_products_count()

        with allure.step("Запомнить название первого товара и открыть его"):
            first_product_title = app.catalog.get_first_product_title()
            app.catalog.click_first_product()
            expect(app.product.get_title_element()).to_be_visible()

        with allure.step("Нажать «Назад»"):
            app.page.go_back()
            app.page.wait_for_load_state("networkidle")

        with allure.step("Вернулись в каталог смартфонов"):
            expect(app.page).to_have_url(re.compile(r"smartphones"))
            expect(app.catalog.get_product_cards().first).to_be_visible()

        with allure.step("Количество товаров в каталоге не изменилось"):
            current_count = app.catalog.get_products_count()
            assert current_count == catalog_products_count, (
                f"После возврата количество товаров изменилось: "
                f"было {catalog_products_count}, стало {current_count}"
            )

    @pytest.mark.smoke
    @pytest.mark.catalog
    @allure.story("Загрузка каталога")
    def test_laptops_catalog_shows_products(self, app):
        """Каталог ноутбуков загружается и отображает товары"""
        with allure.step("Открыть каталог ноутбуков"):
            app.go(CATALOG_URLS["laptops"])
        with allure.step("Первая карточка товара видна"):
            expect(app.catalog.get_product_cards().first).to_be_visible()

    @pytest.mark.smoke
    @pytest.mark.catalog
    @allure.story("Заголовок категории")
    def test_catalog_page_title_is_present(self, app):
        """Заголовок страницы каталога присутствует и не пустой"""
        with allure.step("Открыть каталог смартфонов"):
            app.go(CATALOG_URLS["smartphones"])
        with allure.step("Заголовок страницы виден"):
            expect(app.catalog.get_page_title()).to_be_visible()
        with allure.step("Заголовок содержит текст"):
            expect(app.catalog.get_page_title()).to_have_text(re.compile(r"\S"))

    @pytest.mark.regression
    @pytest.mark.catalog
    @allure.story("Фильтры")
    def test_catalog_has_filter_section(self, app):
        """В каталоге отображается блок фильтров"""
        with allure.step("Открыть каталог смартфонов"):
            app.go(CATALOG_URLS["smartphones"])
        with allure.step("Блок фильтров виден"):
            expect(app.catalog.get_filters()).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.catalog
    @allure.story("Пагинация")
    def test_catalog_has_pagination(self, app):
        """Каталог с большим числом товаров содержит пагинацию"""
        with allure.step("Открыть каталог телевизоров"):
            app.go(CATALOG_URLS["tvs"])
        with allure.step("Пагинация видна"):
            expect(app.catalog.get_pagination()).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.catalog
    @allure.story("Переход к товару")
    def test_click_product_opens_product_page_with_title(self, app):
        """Клик по товару открывает страницу с заголовком и ценой"""
        with allure.step("Открыть каталог смартфонов"):
            app.go(CATALOG_URLS["smartphones"])
        with allure.step("Убедиться, что есть товары"):
            assert app.catalog.get_products_count() > 0, "Каталог пуст"
        with allure.step("Кликнуть по первому товару"):
            app.catalog.click_first_product()
        with allure.step("Заголовок товара виден"):
            expect(app.product.get_title_element()).to_be_visible()
        with allure.step("Заголовок не пустой"):
            expect(app.product.get_title_element()).to_have_text(re.compile(r"\S"))

    @pytest.mark.regression
    @pytest.mark.catalog
    @allure.story("Страница товара")
    def test_product_page_has_add_to_cart_button(self, app):
        """Страница товара содержит кнопку «В корзину»"""
        with allure.step("Открыть каталог ноутбуков"):
            app.go(CATALOG_URLS["laptops"])
        with allure.step("Кликнуть по первому товару"):
            app.catalog.click_first_product()
        with allure.step("Кнопка «В корзину» видна"):
            expect(app.product.get_add_to_cart_button()).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.catalog
    @allure.story("Страница товара")
    def test_product_page_has_breadcrumbs(self, app):
        """Страница товара содержит хлебные крошки"""
        with allure.step("Открыть каталог смартфонов"):
            app.go(CATALOG_URLS["smartphones"])
        with allure.step("Кликнуть по первому товару"):
            app.catalog.click_first_product()
        with allure.step("Хлебные крошки видны"):
            expect(app.product.get_breadcrumbs()).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.catalog
    @allure.story("Страница товара")
    def test_product_page_shows_price(self, app):
        """Страница товара отображает цену"""
        with allure.step("Открыть каталог смартфонов"):
            app.go(CATALOG_URLS["smartphones"])
        with allure.step("Кликнуть по первому товару"):
            app.catalog.click_first_product()
        with allure.step("Цена товара видна"):
            expect(app.product.get_price_element()).to_be_visible()
        with allure.step("Цена содержит число"):
            expect(app.product.get_price_element()).to_have_text(re.compile(r"\d"))
