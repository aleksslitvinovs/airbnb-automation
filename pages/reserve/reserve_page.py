from abc import abstractmethod

from pages.results.listing import Listing


class ReservePage:
    @abstractmethod
    def validate_reservation(self, guest_count: int, checkin: str, checkout: str, listing: Listing):
        pass

    @abstractmethod
    def log_price_details(self, destination: str) -> None:
        pass