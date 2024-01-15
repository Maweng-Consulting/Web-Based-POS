import base64

import requests

SASA_PAY_URL = ""
SASA_PAY_CLIENT_ID = "Eb62EFOsnLc9ARkrp9cFCj5CQAgXGqY3SSQOTxUC"
SASA_PAY_CLIENT_SECRET = "h5Ef0CsZKWYenftCnY6NZqoKvqPhqtdZ59GDzdZ5tPYmsLy9kquXwqdECdb5CN6aA1HfQRds32al7vq1UjRSiq2dCnltDMw5eVjjgd3fyjTNZRwwuJmYmedup0IboZ5L"


def sasa_pay_auth():
    keys = SASA_PAY_CLIENT_ID + SASA_PAY_CLIENT_SECRET
    sasa_key_str = keys.encode("ascii")
    token = base64.b64encode(sasa_key_str).decode("utf-8")
    headers = {"Authorization": f"Basic {token}"}

    # Make the request to the SasaPay API.
    response = requests.post(
        "https://sandbox.sasapay.app/oauth/v1/generate?grant_type=client_credentials",
        headers=headers,
    )

    # Decode the JSON response.
    # json_response = response.json()

    # Print the JSON response.
    print(response)
