# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "rich",
#     "slackclient",
#     "python-dotenv"
# ]
# ///
import os
import json
import typing
import logging
import slack

from rich.logging import RichHandler

logger = logging.getLogger(__name__)
logger.addHandler(RichHandler())
logger.setLevel(logging.INFO)


def invite_users_chat_template(emails: str):
    return f"""
    
The following new users have signed up for CAT, and want to join the Slack workspace:

{emails}

1. Click the workspace icon
2. Select "Invite People to ClimateAction.tech"
3. Paste the list of names for the invite
4. Click "Send Invites"
5. Delete this message
6. Share a message acknowledging the import for anyone else in the channel.
"""


def send_slack_message(slack_message: str, channel: str, slack_token: str):
    
    if not slack_token:
        logger.error("SLACK_API_TOKEN environment variable not set.")
        return

    client = slack.WebClient(token=slack_token)
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=slack_message
        )
        if response["ok"]:
            logger.info(f"Message sent to {channel} successfully.")
        else:
            logger.error(f"Failed to send message: {response['error']}")
    except Exception as e:
        logger.error(f"Error sending message to Slack: {e}")

def list_slack_joiners(subscribers: typing.List[dict]):
    
    slack_invite_emails = [subscriber.get("Email Address") for subscriber in subscribers]

    return {
        "slack_invite_emails": slack_invite_emails
    }

def main(subscribers: typing.List[dict], channel: str, token: str):
    
    new_emails = list_slack_joiners(subscribers)["slack_invite_emails"]
    formatted_email_list = "\n".join(new_emails)
    invite_to_slack_mgs = invite_users_chat_template(formatted_email_list)

    send_slack_message(invite_to_slack_mgs, channel=channel, slack_token=token)
    return subscribers


if __name__ == "__main__":
    """This is run for local testing."""
    import dotenv
    

    dotenv.load_dotenv()
    slack_token = os.getenv("SLACK_API_TOKEN")

    with open("latest_signups.json", "r") as file:
        subscribers = json.load(file)

    new_emails = list_slack_joiners(subscribers)["slack_invite_emails"]

    emails = "\n".join(new_emails)

    invite_to_slack_mgs = invite_users_chat_template(emails)
    logger.info(invite_to_slack_mgs)


