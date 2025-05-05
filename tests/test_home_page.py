from datetime import date, timedelta

import pytest

from pages.home_page import HomePage
from pages.results_page import ResultsPage


# TODO: Handle Tel Aviv. In Search URL Tel Aviv is changed to Tel-Aviv
@pytest.mark.parametrize("destination", ["Riga"])
def test_search_destination(page, destination):
    home_page = HomePage(page)
    home_page.goto()
    home_page.search_destination(destination)

    [checkin, checkout] = get_dates()
    home_page.select_dates(checkin, checkout)

    guest_count = 2
    home_page.set_guests(guest_count)

    home_page.submit_search()
    home_page.validate_airbnb_url(destination, checkin, checkout)

    results_page = ResultsPage(page)
    results_page.validate_results(
        destination=destination,
        checkin_date=checkin,
        checkout_date=checkout,
        guests=2,
    )


def get_dates() -> tuple[date, date]:
    checkin = date.today() + timedelta(days=7)
    checkout = checkin + timedelta(days=7)

    return [checkin, checkout]
