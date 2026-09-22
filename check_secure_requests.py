"""Verify client policy without connecting to NASA."""

from unittest.mock import Mock, patch

import requests

import secure_apod

with patch("secure_apod.requests.get") as get:
    try:
        secure_apod.fetch_apod("")
    except ValueError:
        pass
    else:
        raise AssertionError("Missing key was accepted")
    get.assert_not_called()
print("Missing key: no request")

response = Mock()
response.__enter__ = Mock(return_value=response)
response.__exit__ = Mock(return_value=False)
response.status_code = 302

with patch("secure_apod.requests.get", return_value=response) as get:
    try:
        secure_apod.fetch_apod("fake-test-key")
    except RuntimeError:
        pass
    else:
        raise AssertionError("Redirect was accepted")
    get.assert_called_once_with(
        secure_apod.APOD_URL,
        params={"api_key": "fake-test-key", "date": "2024-01-01"},
        timeout=(3.05, 10),
        allow_redirects=False,
        verify=True,
    )
    response.json.assert_not_called()
print("Redirect: refused; TLS verification and timeouts enabled")

with patch.dict("os.environ", {"NASA_API_KEY": "fake-test-key"}):
    with patch(
        "secure_apod.requests.get",
        side_effect=requests.exceptions.SSLError("simulated failure"),
    ) as get:
        assert secure_apod.main() == 1
        get.assert_called_once()
print("TLS failure: stopped without an insecure retry")
