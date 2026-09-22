"""Exercise the real client and CLI with simulated HTTP responses."""

from unittest.mock import patch

import requests

import main


def response(status, body):
    result = requests.Response()
    result.status_code = status
    result.encoding = "utf-8"
    result._content = body.encode("utf-8")
    result.url = "https://api.nasa.gov/planetary/apod"
    return result


cases = [
    ("success", response(200, '{"date":"2024-01-01",'
     '"title":"Example nebula","media_type":"image"}'), 0),
    ("timeout", requests.exceptions.Timeout("simulated"), 1),
    ("HTTP error", response(503, "Unavailable"), 1),
    ("invalid JSON", response(200, "not JSON"), 1),
    ("connection error", requests.exceptions.ConnectionError("simulated"), 1),
    ("missing fields", response(200, "{}"), 1),
]

for name, outcome, expected in cases:
    print(f"--- {name} ---")
    with patch("apod_client.requests.get") as fake_get:
        if isinstance(outcome, Exception):
            fake_get.side_effect = outcome
        else:
            fake_get.return_value = outcome
        with patch("sys.argv", ["main.py", "2024-01-01"]):
            code = main.main()
        fake_get.assert_called_once()
        assert code == expected, (name, code)

print("--- invalid date ---")
with patch("apod_client.requests.get") as fake_get:
    with patch("sys.argv", ["main.py", "2024-02-30"]):
        assert main.main() == 1
    fake_get.assert_not_called()

print("All local checks passed.")
