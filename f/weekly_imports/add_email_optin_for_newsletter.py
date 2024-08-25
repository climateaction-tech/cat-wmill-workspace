import requests
import rich


def main(subscribers: [dict], token: str):
    url = "https://api.buttondown.com/v1/subscribers"
    headers = {
        "accept": "application/json",
        "authorization": f"Token {token}",
        "content-type": "application/json",
    }

    for subscriber in subscribers:
        email_address = subscriber["Email Address"]
        opt_in = subscriber["Our weekly CAT newsletter"]
        if opt_in:
            rich.print(f"{email_address} has opted-in. Subscribing them")
            payload = {"email_address": email_address, "type": "regular"}
            response = requests.post(url, json=payload, headers=headers)
            rich.print(response.text)
        else:
            rich.print(f"{email_address} did not opt-in to the newsletter. Skipping")
