from abc import abstractmethod

from pages.results.listing import Listing


class ReservePage:
    @abstractmethod
    def enter_phone_number(self, country: str, phone: str):
        pass

    @abstractmethod
    def validate_reservation(
        self,
        number_of_adults: int,
        number_of_children: int,
        checkin: str,
        checkout: str,
        listing: Listing,
    ):
        pass

    @abstractmethod
    def log_price_details(self, destination: str) -> None:
        pass
