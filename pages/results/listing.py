from dataclasses import dataclass


@dataclass
class Listing:
    title: str
    price: float
    rating: float
    url: str
    full_title: str = ""
