from datetime import date


def format_reservation_dates(
    checkin_date: date, checkout_date: date, include_year: bool = False
) -> str:
    """
    Format the check-in and check-out dates for display.

    Args:
        checkin_date (date): The check-in date.
        checkout_date (date): The check-out date.

    Returns:
        str: Formatted date string.
    """
    expected_dates = ""

    if checkin_date.month == checkout_date.month:
        expected_dates = f"{checkin_date.strftime('%B')} {checkin_date.day} – {checkout_date.day}"
    else:
        expected_dates = f"{checkout_date.strftime('%B')} {checkin_date.day} – {checkout_date.strftime('%B')} {checkout_date.day}"

    if include_year:
        expected_dates = f"{expected_dates}, {checkin_date.year}"
        
    return expected_dates
