import re
import allure
import pytest
from playwright.sync_api import expect


@allure.feature("Навигация")
class TestNavigation:

    @pytest.mark.smoke
    @pytest.mark.navigation
    @allure.story("Страница корзины")
    def test_basket_page_accessible_with_content(self, app):
        """Страница корзины открывается и отображает ожидаемое содержимое"""
        with allure.step("Перейти на страницу корзины"):
            app.go("order/basket/")
        with allure.step("URL содержит 'basket'"):
            expect(app.page).to_have_url(re.compile(r"basket"))
        with allure.step("Страница показывает пустую корзину или список товаров"):
            empty = app.cart.is_cart_empty()
            has_items = app.cart.get_items_count() > 0
            assert empty or has_items, "Страница корзины не отобразила ожидаемый контент"

    @pytest.mark.smoke
    @pytest.mark.navigation
    @allure.story("Страница контактов")
    def test_contacts_page_shows_heading(self, app, base_url):
        """Страница контактов открывается и содержит заголовок h1"""
        with allure.step("Перейти на страницу контактов"):
            app.page.goto(f"{base_url}/contacts/")
            app.page.wait_for_load_state("domcontentloaded")
        with allure.step("Страница имеет непустой заголовок вкладки"):
            expect(app.page).to_have_title(re.compile(r"\S"))
        with allure.step("Заголовок h1 виден на странице"):
            expect(app.page.locator("h1").first).to_be_visible()

    @pytest.mark.smoke
    @pytest.mark.navigation
    @allure.story("Страница о компании")
    def test_about_page_shows_heading(self, app, base_url):
        """Страница «О компании» открывается и содержит заголовок h1"""
        with allure.step("Перейти на страницу «О компании»"):
            app.page.goto(f"{base_url}/about/")
            app.page.wait_for_load_state("domcontentloaded")
        with allure.step("Страница имеет непустой заголовок вкладки"):
            expect(app.page).to_have_title(re.compile(r"\S"))
        with allure.step("Заголовок h1 виден на странице"):
            expect(app.page.locator("h1").first).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.navigation
    @allure.story("Навигация назад")
    def test_browser_back_returns_to_home_with_search_field(self, app, base_url):
        """Кнопка «Назад» возвращает на главную страницу с полем поиска"""
        with allure.step("Выполнить поиск (уходим с главной)"):
            app.home.search("телефон")
        with allure.step("Нажать «Назад»"):
            app.page.go_back()
            app.page.wait_for_load_state("domcontentloaded")
        with allure.step("URL совпадает с главной страницей"):
            expect(app.page).to_have_url(re.compile(re.escape(base_url.rstrip("/"))))
        with allure.step("Поле поиска снова видно — мы на главной"):
            expect(app.home.get_search_input()).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.navigation
    @allure.story("404 страница")
    def test_unknown_url_shows_page_with_heading(self, app, base_url):
        """Несуществующий URL возвращает страницу с заголовком (404 или редирект)"""
        with allure.step("Перейти на несуществующий URL"):
            app.page.goto(f"{base_url}/this-page-xyz-does-not-exist-789/")
            app.page.wait_for_load_state("domcontentloaded")
        with allure.step("Страница имеет непустой заголовок вкладки"):
            expect(app.page).to_have_title(re.compile(r"\S"))
        with allure.step("Заголовок h1 виден — страница не сломана"):
            expect(app.page.locator("h1").first).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.navigation
    @allure.story("Логотип")
    def test_logo_click_navigates_to_homepage_from_catalog(self, app, base_url):
        """Клик по логотипу из каталога возвращает пользователя на главную страницу"""
        with allure.step("Перейти в каталог смартфонов"):
            app.go("mobile/smartphones/")
            expect(app.catalog.get_product_cards().first).to_be_visible()

        with allure.step("Кликнуть по логотипу в шапке"):
            app.home.get_logo().click()
            app.page.wait_for_load_state("networkidle")

        with allure.step("Перешли на главную страницу"):
            expect(app.page).to_have_url(re.compile(re.escape(base_url.rstrip("/"))))

        with allure.step("Поле поиска видно — это главная страница"):
            expect(app.home.get_search_input()).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.navigation
    @allure.story("Хлебные крошки")
    def test_breadcrumb_link_navigates_to_parent_category(self, app):
        """Клик по предпоследнему элементу хлебных крошек открывает родительскую категорию"""
        with allure.step("Открыть каталог ноутбуков и перейти к первому товару"):
            app.go("notebooks/")
            expect(app.catalog.get_product_cards().first).to_be_visible()
            app.catalog.click_first_product()

        with allure.step("Страница товара загружена с хлебными крошками"):
            expect(app.product.get_title_element()).to_be_visible()
            expect(app.product.get_breadcrumbs()).to_be_visible()
            crumbs = app.product.get_breadcrumb_items()
            assert len(crumbs) >= 2, f"Ожидалось ≥ 2 хлебных крошек, получено: {crumbs}"

        with allure.step("Запомнить URL страницы товара"):
            product_url = app.page.url

        with allure.step("Кликнуть по предпоследней хлебной крошке (родительская категория)"):
            breadcrumb_links = app.product.get_breadcrumbs().locator("a")
            link_count = breadcrumb_links.count()
            assert link_count >= 1, "В хлебных крошках нет ссылок"
            breadcrumb_links.nth(link_count - 1).click()
            app.page.wait_for_load_state("networkidle")

        with allure.step("Перешли на страницу категории, а не на страницу товара"):
            assert app.page.url != product_url, (
                "URL не изменился после клика по хлебной крошке"
            )
            expect(app.page.locator("h1").first).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.navigation
    @allure.story("Пагинация каталога")
    def test_catalog_pagination_pages_differ_in_content(self, app):
        """Страницы каталога при навигации показывают разный набор товаров"""
        with allure.step("Открыть каталог телевизоров"):
            app.go("tv/")
            expect(app.catalog.get_product_cards().first).to_be_visible()

        with allure.step("Запомнить товары первой страницы"):
            page1_title = app.catalog.get_first_product_title()
            expect(app.catalog.get_pagination()).to_be_visible()
            expect(app.catalog.get_pagination_next()).to_be_visible()

        with allure.step("Перейти на страницу 2"):
            app.catalog.go_to_next_page()
            expect(app.catalog.get_product_cards().first).to_be_visible()

        with allure.step("Товары на странице 2 отличаются от страницы 1"):
            page2_title = app.catalog.get_first_product_title()
            assert page1_title != page2_title, (
                "Первый товар на стр. 2 совпадает с первым товаром на стр. 1"
            )

        with allure.step("URL содержит номер страницы или параметр пагинации"):
            expect(app.page).to_have_url(re.compile(r"page|p=|offset|\?[^/]"))

    @pytest.mark.smoke
    @pytest.mark.navigation
    @allure.story("Страница контактов")
    def test_contacts_page_shows_heading(self, app, base_url):
        """Страница контактов открывается и содержит заголовок h1"""
        with allure.step("Перейти на страницу контактов"):
            app.page.goto(f"{base_url}/contacts/")
            app.page.wait_for_load_state("domcontentloaded")
        with allure.step("Страница имеет непустой заголовок вкладки"):
            expect(app.page).to_have_title(re.compile(r"\S"))
        with allure.step("Заголовок h1 виден на странице"):
            expect(app.page.locator("h1").first).to_be_visible()

    @pytest.mark.smoke
    @pytest.mark.navigation
    @allure.story("Страница о компании")
    def test_about_page_shows_heading(self, app, base_url):
        """Страница «О компании» открывается и содержит заголовок h1"""
        with allure.step("Перейти на страницу «О компании»"):
            app.page.goto(f"{base_url}/about/")
            app.page.wait_for_load_state("domcontentloaded")
        with allure.step("Страница имеет непустой заголовок вкладки"):
            expect(app.page).to_have_title(re.compile(r"\S"))
        with allure.step("Заголовок h1 виден на странице"):
            expect(app.page.locator("h1").first).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.navigation
    @allure.story("Навигация назад")
    def test_browser_back_returns_to_home_with_search_field(self, app, base_url):
        """Кнопка «Назад» возвращает на главную страницу с полем поиска"""
        with allure.step("Выполнить поиск (уходим с главной)"):
            app.home.search("телефон")
        with allure.step("Нажать «Назад»"):
            app.page.go_back()
            app.page.wait_for_load_state("domcontentloaded")
        with allure.step("URL совпадает с главной страницей"):
            expect(app.page).to_have_url(re.compile(re.escape(base_url.rstrip("/"))))
        with allure.step("Поле поиска снова видно — мы на главной"):
            expect(app.home.get_search_input()).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.navigation
    @allure.story("404 страница")
    def test_unknown_url_shows_page_with_heading(self, app, base_url):
        """Несуществующий URL возвращает страницу с заголовком (404 или редирект)"""
        with allure.step("Перейти на несуществующий URL"):
            app.page.goto(f"{base_url}/this-page-xyz-does-not-exist-789/")
            app.page.wait_for_load_state("domcontentloaded")
        with allure.step("Страница имеет непустой заголовок вкладки"):
            expect(app.page).to_have_title(re.compile(r"\S"))
        with allure.step("Заголовок h1 виден — страница не сломана"):
            expect(app.page.locator("h1").first).to_be_visible()
