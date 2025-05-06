from playwright.sync_api import Page

from pages.results.listing import Listing


class RoomPage:
    def __init__(self, page: Page):
        self.page = page
        self.close_translation_dialog_button = page.get_by_role("button", name="Close")
        self.reserve_button = page.get_by_role("button", name="Reserve")
        self.listing_title = page.locator("[data-section-id='TITLE_DEFAULT'] h1")
        self.county_code_dropdown = page.get_by_test_id("login-signup-countrycode")
        self.phone_input = page.locator("#phoneInputphone-login")

    def reserve_room(self, cheapest_listing: Listing) -> None:
        self.close_translation_dialog_button.click()

        cheapest_listing.full_title = self.listing_title.text_content()
        
        self.reserve_button.click()
