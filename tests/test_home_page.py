import random
import time
from datetime import date, timedelta

import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.reserve.reserve_page import ReservePage
from pages.reserve.reserve_page_new import ReservePageNew
from pages.reserve.reserve_page_old import ReservePageOld
from pages.results.results_page import ResultsPage
from pages.room_page import RoomPage


@pytest.mark.parametrize("destination", ["Tel Aviv"])
def test_search_destination(page, destination: str) -> None:
    checkin, checkout = __get_dates()
    number_of_adults = 2
    number_of_children = 1

    home_page = HomePage(page)
    home_page.search_for_booking(
        destination, checkin, checkout, number_of_adults, number_of_children
    )

    results_page = ResultsPage(page)
    results_page.validate_airbnb_url(
        destination, checkin, checkout, number_of_adults, number_of_children
    )
    results_page.validate_results(
        destination,
        checkin,
        checkout,
        number_of_adults,
        number_of_children,
    )

    cheapest_highest_rated = results_page.get_cheapest_highest_rated(destination)
    with page.context.expect_page() as room_window:
        results_page.select_cheapest_highest_rated(cheapest_highest_rated)

    room_page = RoomPage(room_window.value)
    room_page.reserve_room(cheapest_highest_rated)

    reserve_page = __get_page_model(room_window.value)
    reserve_page.enter_phone_number("Israel (+972)", "123456789")
    reserve_page.validate_reservation(
        number_of_adults,
        number_of_children,
        checkin,
        checkout,
        cheapest_highest_rated,
    )

    reserve_page.log_price_details(destination)


def __get_dates() -> tuple[date, date]:
    random_delta = random.randint(1, 7)
    checkin = date.today() + timedelta(days=random_delta)

    random_delta = random.randint(1, 7)
    checkout = checkin + timedelta(days=random_delta)

    return checkin, checkout


# Retrieves page model based whether new or old page is displayed as it seems
# that Airbnb is currently doing A/B testing
def __get_page_model(page: Page) -> ReservePage:
    time.sleep(3)

    if page.get_by_test_id("step-0").is_visible():
        return ReservePageNew(page)

    return ReservePageOld(page)
