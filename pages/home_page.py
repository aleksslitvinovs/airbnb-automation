from datetime import date

from playwright.sync_api import Page


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.get_by_test_id("structured-search-input-field-query")
        self.search_button = page.get_by_test_id("structured-search-input-search-button")
        self.adults_increase_button = page.get_by_test_id("stepper-adults-increase-button")
        self.child_increase_button = page.get_by_test_id("stepper-children-increase-button")
        self.guests_button = page.get_by_test_id("structured-search-input-field-guests-button")

    def goto(self) -> None:
        self.page.goto("https://www.airbnb.com/")

    def search_destination(self, destination: str) -> None:
        self.search_input.fill(destination)
        self.page.keyboard.press("Enter")

    def select_dates(self, checkin: date, checkout: date) -> None:
        checkin_name = checkin.strftime("%-d, %A, %B %Y.")
        checkout_name = checkout.strftime("%-d, %A, %B %Y.")
        self.page.get_by_role("button", name=checkin_name).click()
        self.page.get_by_role("button", name=checkout_name).click()

    def select_number_of_guests(self, adult_count: int, child_count: int) -> None:
        self.guests_button.click()

        for _ in range(adult_count):
            self.adults_increase_button.click()

        for _ in range(child_count):
            self.child_increase_button.click()

    def submit_search(self) -> None:
        self.search_button.click()

    def search_for_booking(
        self,
        destination: str,
        checkin_date: date,
        checkout_date: date,
        adult_count: int,
        child_count: int,
    ) -> None:
        self.goto()
        self.search_destination(destination)
        self.select_dates(checkin_date, checkout_date)
        self.select_number_of_guests(adult_count, child_count)
        self.submit_search()
