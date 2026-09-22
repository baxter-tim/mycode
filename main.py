"""Command-line interface for the APOD client."""

import argparse
import os

import requests

from apod_client import fetch_apod, format_apod


def main():
    parser = argparse.ArgumentParser(description="Read NASA APOD metadata")
    parser.add_argument("day", help="APOD date in YYYY-MM-DD format")
    args = parser.parse_args()
    api_key = os.environ.get("NASA_API_KEY", "DEMO_KEY")

    try:
        apod = fetch_apod(args.day, api_key=api_key)
        label = format_apod(apod)
    except requests.exceptions.Timeout:
        print("Request timed out.")
        return 1
    except requests.exceptions.HTTPError as exc:
        print(f"NASA returned HTTP {exc.response.status_code}.")
        return 1
    except requests.exceptions.JSONDecodeError:
        print("NASA returned invalid JSON.")
        return 1
    except requests.exceptions.RequestException:
        print("The HTTP request failed.")
        return 1
    except ValueError:
        print("Invalid date. Use a real calendar date in YYYY-MM-DD format.")
        return 1
    except (KeyError, TypeError):
        print("The response did not have the expected APOD fields.")
        return 1
    else:
        print(label)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
