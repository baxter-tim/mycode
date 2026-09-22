"""Reusable functions for retrieving NASA APOD metadata."""

from datetime import date

import requests

APOD_URL = "https://api.nasa.gov/planetary/apod"


def fetch_apod(day, *, api_key="AlrvsUE4WaIg3Q9I2MQAAKzXerLoAkdc7qbW2o7C", timeout=5.0):
    """Return metadata for one date; raise on invalid input or response."""
    parsed = date.fromisoformat(day)
    if parsed.isoformat() != day:
        raise ValueError("date must use YYYY-MM-DD")

    response = requests.get(
        APOD_URL,
        params={"date": day, "api_key": api_key},
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


def format_apod(apod):
    """Format required fields from a single-date APOD response."""
    return f"{apod['date']} | {apod['title']} | {apod['media_type']}"

def attribution(apod):
    return apod.get("copyright", "Not supplied")


assert attribution({"copyright": "Example photographer"}) == "Example photographer"
assert attribution({}) == "Not supplied"
