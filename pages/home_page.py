import re
from datetime import date
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.get_by_test_id("structured-search-input-field-query")
        self.search_button = page.get_by_test_id("structured-search-input-search-button")
        self.adults_increase_button = page.get_by_test_id("stepper-adults-increase-button")
        self.guests_button = page.get_by_test_id("structured-search-input-field-guests-button")

    def goto(self):
        self.page.goto("https://www.airbnb.com/")

    def search_destination(self, destination: str):
        self.search_input.fill(destination)
        self.page.keyboard.press("Enter")

    def select_dates(self, checkin: date, checkout: date):
        checkin_name = checkin.strftime("%-d, %A, %B %Y.")
        checkout_name = checkout.strftime("%-d, %A, %B %Y.")
        self.page.get_by_role("button", name=checkin_name).click()
        self.page.get_by_role("button", name=checkout_name).click()

    def set_guests(self, guest_count: int):
        self.guests_button.click()

        for _ in range(guest_count):
            self.adults_increase_button.click()

    def submit_search(self):
        self.search_button.click()

    def validate_airbnb_url(
        self, destination: str, checkin_date: date, checkout_date: date
    ) -> None:
        # Validate city in path
        expect(self.page).to_have_url(re.compile(f".*/s/{destination}/homes"))

        url = self.page.url
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)

        # Get and check check-in and check-out dates
        checkin_actual = params.get("checkin", [None])[0]
        checkout_actual = params.get("checkout", [None])[0]

        assert checkin_actual, "Checkin date is missing in URL"
        assert checkout_actual, "Checkout date is missing in URL"

        checkin_expected_formatted = checkin_date.strftime("%Y-%m-%d")
        checkout_expected_formatted = checkout_date.strftime("%Y-%m-%d")

        # Validate dates
        assert (
            checkin_actual == checkin_expected_formatted
        ), f"Expected checkin date {checkin_expected_formatted}, but got {checkin_actual}"

        assert (
            checkout_actual == checkout_expected_formatted
        ), f"Expected checkout date {checkout_expected_formatted}, but got {checkout_actual}"
