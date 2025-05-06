from abc import abstractmethod
import json
import os

from pages.results.listing import Listing


class ReservePage:
    @abstractmethod
    def validate_reservation(self, guest_count: int, checkin: str, checkout: str, listing: Listing):
        pass

    @abstractmethod
    def log_price_details(self) -> dict[str, str]:
        pass

    def dump_cost_details(self, data: dict[str, str]):
        os.makedirs("temp", exist_ok=True)
        
        with open("temp/cost_details.json", "w") as f:
            json.dump(data, f, indent=2)
