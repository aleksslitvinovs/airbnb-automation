import dataclasses
import re
from datetime import date
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import Page, expect

from pages.results.listing import Listing
from utils import dates, result_files


class ResultsPage:
    def __init__(self, page: Page):
        self.page = page
        self.search_location = page.get_by_test_id("little-search-location").locator("div")
        self.search_dates = page.get_by_test_id("little-search-anytime").locator("div")
        self.search_button = page.get_by_test_id("little-search-icon")
        self.guest_count = page.get_by_test_id("little-search-guests")
        # Filters listings to exclude those in 'Available for similar dates' category
        self.listings = page.get_by_test_id("card-container").filter(has_not_text=" – ")
        self.card_title = page.get_by_test_id("listing-card-title")
        self.price = page.get_by_test_id("price-availability-row").locator(
            "css=button span:first-child"
        )
        self.rating = page.get_by_text("average rating")

    def validate_url(
        self,
        destination: str,
        checkin_date: date,
        checkout_date: date,
        number_of_adults: int,
        number_of_children: int,
    ) -> None:
        self.__validate_destination(destination)
        self.__validate_booking_dates(checkin_date, checkout_date)
        self.__validate_number_of_adults(number_of_adults)
        self.__validate_number_of_children(number_of_children)

    def validate_results(
        self,
        destination: str,
        checkin_date: date,
        checkout_date: date,
        number_of_adults: int,
        number_of_children: int,
    ) -> None:
        expect(self.search_location).to_have_text(destination)

        expected_dates = dates.format_reservation_dates(checkin_date, checkout_date)
        expect(self.search_dates).to_have_text(expected_dates)

        expect(self.guest_count).to_contain_text(f"{number_of_adults+number_of_children} guests")

    def get_cheapest_highest_rated(self, destination) -> Listing:
        listings = self.listings.all()

        results: list[Listing] = []

        for listing in listings:
            try:
                title = listing.locator(self.card_title).text_content()
                price_text = listing.locator(self.price).text_content(timeout=5_000)
                price = int("".join(filter(str.isdigit, price_text)))

                # Handle cases when rating is 'New' or not available
                if listing.locator(self.rating).count() == 0:
                    print(f"Listing '{title}' has no rating")
                    continue

                rating_text = listing.locator(self.rating).text_content()
                rating = float(rating_text.split()[0])
                url = listing.locator("a").first.get_attribute("href")

                listing = Listing(title, price, rating, f"https://www.airbnb.com{url}")
                results.append(listing)
            except Exception as _:
                print(f"Failed to parse listing: https://www.airbnb.com{url}")

        assert results, "No listings found"

        max_rating = max(result.rating for result in results)

        top_rated: list[Listing] = []
        for result in results:
            if result.rating == max_rating:
                top_rated.append(result)

        cheapest = min(top_rated, key=lambda r: r.price)

        # Save to JSON file
        result_files.save_json_to_file(
            f"{destination}_cheapest_high_rated", dataclasses.asdict(cheapest)
        )

        return cheapest

    def select_cheapest_highest_rated(self, listing: Listing) -> None:
        listings = self.listings.all()

        for l in listings:
            title = l.locator(self.card_title).text_content()

            if title == listing.title:
                l.click()
                break

    def __validate_destination(self, expected_destination: str) -> None:
        match = re.search(r"/s/([^/]+)/homes", self.page.url)

        actual_destination = ""
        if match:
            actual_destination = match.group(1)

        assert (
            expected_destination.lower().replace(" ", "-") == actual_destination.lower()
        ), f"Expected location {expected_destination} in URL does not match actual location {actual_destination}"

    def __validate_booking_dates(self, checkin: date, checkout: date) -> None:
        parsed_url = urlparse(self.page.url)
        params = parse_qs(parsed_url.query)

        checkin_actual = params.get("checkin", [None])[0]
        checkout_actual = params.get("checkout", [None])[0]

        assert checkin_actual, "Checkin date is missing in URL"
        assert checkout_actual, "Checkout date is missing in URL"

        checkin_expected_formatted = checkin.strftime("%Y-%m-%d")
        checkout_expected_formatted = checkout.strftime("%Y-%m-%d")

        # Validate dates
        assert (
            checkin_actual == checkin_expected_formatted
        ), f"Expected checkin date {checkin_expected_formatted}, but got {checkin_actual}"

        assert (
            checkout_actual == checkout_expected_formatted
        ), f"Expected checkout date {checkout_expected_formatted}, but got {checkout_actual}"

    def __validate_number_of_adults(self, expected_adult_count: int) -> None:
        parsed_url = urlparse(self.page.url)
        params = parse_qs(parsed_url.query)

        adult_count_actual = params.get("adults", [None])[0]

        assert adult_count_actual, "Adult count is missing in URL"

        assert (
            str(expected_adult_count) == adult_count_actual
        ), f"Expected {expected_adult_count} adults, but got {adult_count_actual}"

    def __validate_number_of_children(self, expected_child_count: int) -> None:
        parsed_url = urlparse(self.page.url)
        params = parse_qs(parsed_url.query)

        child_count_actual = params.get("children", [None])[0]

        assert child_count_actual, "Children count is missing in URL"

        assert (
            str(expected_child_count) == child_count_actual
        ), f"Expected {expected_child_count} children, but got {child_count_actual}"
