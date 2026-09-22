"""Prepare authentication examples locally; send no HTTP requests."""

import requests

EXAMPLE_URL = "https://api.example.com/private"

bearer = requests.Request(
    "GET",
    EXAMPLE_URL,
    headers={"Authorization": "Bearer classroom-token-not-a-secret"},
).prepare()

basic = requests.Request(
    "GET",
    EXAMPLE_URL,
    auth=("classroom-user", "classroom-password-not-a-secret"),
).prepare()

for name, prepared in [("Bearer", bearer), ("Basic", basic)]:
    scheme = prepared.headers["Authorization"].split(" ", 1)[0]
    print(f"{name}: {scheme} [REDACTED]")
    print(f"Credential in URL: {'?' in prepared.url}")
