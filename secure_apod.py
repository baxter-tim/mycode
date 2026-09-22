"""Retrieve APOD metadata with explicit transport and error policies."""

import os

import requests

APOD_URL = "https://api.nasa.gov/planetary/apod"


def fetch_apod(api_key):
    if not api_key or not api_key.strip():
        raise ValueError("NASA_API_KEY is required")

    with requests.get(
        APOD_URL,
        params={"api_key": api_key, "date": "2024-01-01"},
        timeout=(3.05, 10),
        allow_redirects=False,
        verify=True,
    ) as response:
        if 300 <= response.status_code < 400:
            raise RuntimeError("Unexpected redirect refused")
        response.raise_for_status()
        return response.json()


def main():
    try:
        apod = fetch_apod(os.environ.get("NASA_API_KEY"))
        title = apod["title"]
    except requests.exceptions.SSLError:
        print("TLS verification or negotiation failed.")
        return 1
    except requests.exceptions.Timeout:
        print("The request timed out.")
        return 1
    except requests.exceptions.HTTPError as exc:
        print(f"NASA returned HTTP {exc.response.status_code}.")
        return 1
    except requests.exceptions.JSONDecodeError:
        print("NASA returned invalid JSON.")
        return 1
    except requests.exceptions.RequestException:
        print("The request failed.")
        return 1
    except ValueError:
        print("Set NASA_API_KEY before running this program.")
        return 1
    except RuntimeError:
        print("Unexpected redirect refused.")
        return 1
    except (KeyError, TypeError):
        print("The response did not contain the expected APOD title.")
        return 1
    else:
        print(title)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
