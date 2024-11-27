# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "httpx",
#     "python-dotenv",
#     "rich",
# ]
# ///
import os
import httpx
import rich
import json
import typing
import logging


logger = logging.getLogger(__name__)
logger.addHandler(rich.logging.RichHandler())
logger.setLevel(logging.INFO)


def main(subscribers: typing.List[dict], token: str):
    return subscribe_to_newsletter(subscribers, token)


def subscribe_to_newsletter(subscribers: typing.List[dict], token: str):
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
            logger.info(f"{email_address} has opted-in. Subscribing them")
            payload = {"email_address": email_address, "type": "regular"}
            response = httpx.post(url, json=payload, headers=headers)

            logger.debug(response.text)
        else:
            logger.info(f"{email_address} did not opt-in to the newsletter. Skipping")


if __name__ == "__main__":
    import dotenv

    dotenv.load_dotenv()

    with open("latest_signups.json", "r") as file:
        subscribers = json.load(file)

    token = os.getenv("BUTTONDOWN_API_KEY")
    if token is None:
        raise ValueError("BUTTONDOWN_API_KEY environment variable not set")

    subscribe_to_newsletter(subscribers, token)
