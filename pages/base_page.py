from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def get_title(self) -> str:
        return self.page.title()

    def get_url(self) -> str:
        return self.page.url

    def wait_for_page_load(self):
        self.page.wait_for_load_state("networkidle")

    def scroll_to_bottom(self):
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_element(self, locator):
        locator.scroll_into_view_if_needed()
