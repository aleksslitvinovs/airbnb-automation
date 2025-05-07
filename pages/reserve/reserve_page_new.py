from datetime import date

from playwright.sync_api import Page, expect

from utils import dates, result_files
from pages.reserve.reserve_page import ReservePage
from pages.results.listing import Listing


class ReservePageNew(ReservePage):
    def __init__(self, page: Page):
        self.page = page
        self.county_code_dropdown = page.get_by_test_id("login-signup-countrycode")
        self.phone_input = page.locator("#phoneInputphone-login")
        self.listing_title = page.locator("#LISTING_CARD-title")
        self.price_breakdown = page.get_by_text("Price breakdown")
        self.price_details = page.get_by_test_id("modal-container").locator(
            "[role='dialog'] > div:nth-of-type(2) > div.dir-ltr"
        )

    def enter_phone_number(self, country: str, phone: str):
        self.county_code_dropdown.select_option(country)
        self.phone_input.fill(phone)
        self.phone_input.press("Enter")

    def validate_reservation(
        self, guest_count: int, checkin: date, checkout: date, listing: Listing
    ):
        expect(self.page.get_by_text(listing.full_title)).to_be_visible()

        expect(self.page.get_by_text(f"{guest_count} adults")).to_be_visible()

        formated_dates = dates.format_reservation_dates(checkin, checkout, include_year=True)
        expect(self.page.get_by_text(formated_dates)).to_be_visible()

    def log_price_details(self, destination: str) -> None:
        self.price_breakdown.click()

        price_details = self.price_details.all()

        assert len(price_details) != 0, "No price details found"

        costs = {}
        for price_detail in price_details:
            price_text = price_detail.inner_text()

            if "\n" not in price_text:
                continue

            [description, cost_details] = price_text.split("\n", maxsplit=1)

            cost = cost_details
            if "\n" in cost_details:
                if "Total\n" in price_text:
                    [currency, cost, *_] = cost_details.split("\n")
                    description = f"{description} ({currency})"
                else:
                    [cost, *_] = cost_details.split("\n")

            costs[description] = cost

        result_files.save_json_to_file(f"{destination}_cost_details", costs)
