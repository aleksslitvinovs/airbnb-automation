from playwright.sync_api import Page, expect

from pages.reserve.reserve_page import ReservePage
from pages.results.listing import Listing
from utils import dates, result_files


class ReservePageOld(ReservePage):
    def __init__(self, page: Page):
        self.page = page
        self.listing_title = page.locator("#LISTING_CARD-title")
        self.price_detail = page.locator("[data-section-id='PRICE_DETAIL'] > div > div > div > div")
        self.county_code_dropdown = page.get_by_test_id("login-signup-countrycode")
        self.phone_input = page.locator("#phoneInputphone-login")

    def enter_phone_number(self, country: str, phone: str):
        self.county_code_dropdown.select_option(country)
        self.phone_input.fill(phone)
        self.phone_input.press("Enter")

    def validate_reservation(
        self,
        number_of_adults: int,
        number_of_children: int,
        checkin: str,
        checkout: str,
        listing: Listing,
    ):
        expect(self.listing_title).to_have_text(listing.full_title)

        expect(
            self.page.get_by_text(f"{number_of_adults+number_of_children} guests")
        ).to_be_visible()

        formated_dates = dates.format_reservation_dates(checkin, checkout)
        expect(self.page.get_by_text(formated_dates)).to_be_visible()

    def log_price_details(self, destination: str) -> None:
        price_details = self.price_detail.all()

        assert len(price_details) != 0, "No price details found"

        costs = {}
        for price_detail in price_details:
            price_text = price_detail.inner_text()

            if "\n" not in price_text:
                continue

            [description, cost_details] = price_text.split("\n", maxsplit=1)

            cost = cost_details
            if "Total\n" in price_text:
                [currency, cost, *_] = cost_details.split("\n")
                description = f"{description} {currency}"

            costs[description] = cost

        result_files.save_json_to_file(f"{destination}_cost_details", costs)
