import time
from datetime import date, timedelta

import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.reserve.reserve_page_base import ReservePage
from pages.reserve.reserve_page_new import ReservePageNew
from pages.reserve.reserve_page_old import ReservePageOld
from pages.results.results_page import ResultsPage
from pages.room_page import RoomPage


# TODO: Handle Tel Aviv. In Search URL Tel Aviv is changed to Tel-Aviv
@pytest.mark.parametrize("destination", ["Berlin"])
def test_search_destination(page, destination):
    page.set_default_timeout(10_000)

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

    cheapest_listing = results_page.get_cheapest_highest_rated()
    with page.context.expect_page() as room_window:
        results_page.select_cheapest_highest_rated(cheapest_listing)

    room_page = RoomPage(room_window.value)
    room_page.reserve_room(cheapest_listing)

    reserve_page = get_page_model(room_window.value)
    # reserve_page.enter_phone_number(country="Israel (+972)", phone="123456789")
    reserve_page.validate_reservation(
        guest_count,
        checkin,
        checkout,
        cheapest_listing,
    )

    details = reserve_page.log_price_details()
    print(details)


def get_dates() -> tuple[date, date]:
    checkin = date.today() + timedelta(days=7)
    checkout = checkin + timedelta(days=7)

    return [checkin, checkout]


def get_page_model(page: Page) -> ReservePage:
    time.sleep(3)

    if page.get_by_test_id("step-0").is_visible():
        return ReservePageNew(page)
    else:
        return ReservePageOld(page)
