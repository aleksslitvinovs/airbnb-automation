import dataclasses
import json
import os
from datetime import date

from playwright.sync_api import Page, expect

from pages.results.listing import Listing
import utils.dates as utils


class ResultsPage:
    def __init__(self, page: Page):
        self.page = page
        self.search_location = page.get_by_test_id("little-search-location").locator("div")
        self.search_dates = page.get_by_test_id("little-search-anytime").locator("div")
        self.search_button = page.get_by_test_id("little-search-icon")
        self.guest_count = page.get_by_test_id("little-search-guests")
        # TODO: Rewrite as component
        # Filters listings to exclude those in 'Available for similar dates' category
        self.listings = page.get_by_test_id("card-container").filter(has_not_text=" – ")
        self.card_title = page.get_by_test_id("listing-card-title")
        self.price = page.get_by_test_id("price-availability-row").locator(
            "css=button span:first-child"
        )
        # TODO: Handle cases when rating is 'New'
        self.rating = page.get_by_text("average rating")

    def validate_results(
        self,
        destination: str,
        checkin_date: date,
        checkout_date: date,
        guests: int,
    ) -> None:
        expect(self.search_location).to_have_text(destination)

        expected_dates = utils.format_reservation_dates(checkin_date, checkout_date)

        expect(self.search_dates).to_have_text(expected_dates)

        # TODO: Use better guest count selector as the current one returns
        # span+div texts. Then instead of contains, use exact match
        expect(self.guest_count).to_contain_text(f"{guests} guests")

    def get_cheapest_highest_rated(self) -> Listing:
        listings = self.listings.all()

        results: list[Listing] = []

        for index, listing in enumerate(listings):
            try:
                title = listing.locator(self.card_title).text_content()
                price_text = listing.locator(self.price).text_content(timeout=5_000)
                price = int("".join(filter(str.isdigit, price_text)))

                if listing.locator(self.rating).count() == 0:
                    print(f"Listing '{title}' has no rating")
                    continue

                rating_text = listing.locator(self.rating).text_content()
                rating = float(rating_text.split()[0])
                url = listing.locator("a").first.get_attribute("href")

                listing = Listing(title, price, rating, f"https://www.airbnb.com{url}")
                results.append(listing)
            except Exception as e:
                print(f"Failed to parse listing: https://www.airbnb.com{url}")

        assert results, "No listings found"

        max_rating = max(result.rating for result in results)

        top_rated: list[Listing] = []
        for result in results:
            if result.rating == max_rating:
                top_rated.append(result)

        cheapest = min(top_rated, key=lambda r: r.price)

        # Save to JSON file
        os.makedirs("temp", exist_ok=True)
        with open("temp/cheapest_high_rated.json", "w") as f:
            json.dump(dataclasses.asdict(cheapest), f, indent=2)

        return cheapest

    def select_cheapest_highest_rated(self, listing: Listing):
        listings = self.listings.all()

        for l in listings:
            title = l.locator(self.card_title).text_content()

            if title == listing.title:
                l.click()
                break
