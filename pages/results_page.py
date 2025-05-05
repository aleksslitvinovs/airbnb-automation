from datetime import date

from playwright.sync_api import Page, expect


class ResultsPage:
    def __init__(self, page: Page):
        self.page = page
        self.search_location = page.get_by_test_id("little-search-location").locator("div")
        self.search_dates = page.get_by_test_id("little-search-anytime").locator("div")
        self.search_button = page.get_by_test_id("little-search-icon")
        self.guest_count = page.get_by_test_id("little-search-guests")

    def validate_results(
        self,
        destination: str,
        checkin_date: date,
        checkout_date: date,
        guests: int,
    ) -> None:
        expect(self.search_location).to_have_text(destination)

        expected_dates = ""
        if checkin_date.month == checkout_date.month:
            expected_dates = (
                f"{checkin_date.strftime('%B')} {checkin_date.day} – {checkout_date.day}"
            )
        else:
            expected_dates = f"{checkout_date.strftime('%B')} {checkin_date.day} – {checkout_date.strftime('%B')} {checkout_date.day}"

        expect(self.search_dates).to_have_text(expected_dates)

        # TODO: Use better guest count selector as the current one returns
        # span+div texts. Then instead of contains, use exact match
        expect(self.guest_count).to_contain_text(f"{guests} guests")
