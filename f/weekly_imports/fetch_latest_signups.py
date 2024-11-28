# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "gspread",
#     "python-dotenv",
#     "rich",
#     "wmill",
# ]
# ///
import os
import json
import wmill
import gspread
import rich
import logging

from rich.logging import RichHandler

logger = logging.getLogger(__name__)
logger.addHandler(RichHandler())
logger.setLevel(logging.DEBUG)

# You can import any PyPi package.
# See here for more info: https://www.windmill.dev/docs/advanced/dependencies_in_python


def main(gsheet_key: str, worksheet_name: str, override_email: str = None):
    if override_email:
        LAST_EMAIL_ADDRESS = override_email
    else:
        # check for either the last run state or initial variable value
        last_state = wmill.get_state()
        # if we have no last state to refer to, we look for 
        # email stored in the resource in its place
        if not last_state:
            resource_path = "f/weekly_imports/last_email_address_object"
            logger.debug((
                f"No last state found. Fetching email from resource {resource_path} "
                "as a fallback.")
                )
            last_state = wmill.get_resource("f/weekly_imports/last_email_address_object")
            logger.debug(f"Email from resource {resource_path}: {last_state}")

        LAST_EMAIL_ADDRESS = last_state.get("last_email_address")

    logger.info(f"Current Last email address: {LAST_EMAIL_ADDRESS}")

    path_to_resource = "f/weekly_imports/improving_c_gspread_service_account"
    gspread_cred_dict = wmill.get_resource(path_to_resource)

    member_dicts, matching_rows = fetch_latest_signups(
        gspread_cred_dict, gsheet_key, worksheet_name, LAST_EMAIL_ADDRESS
    )

    last_row = member_dicts[-1]

    if not last_row:
        logger.info("No new signups to pass along")
        return []

    if last_row:
        last_email = last_row.get("Email Address")

        if last_email:
            logger.info(f"Setting last email address to: {last_email}")
            new_state = {"last_email_address": last_email}
            wmill.set_state(new_state)

    return member_dicts


def fetch_latest_signups(
    gspread_cred_dict: dict,
    gsheet_key: str,
    worksheet_name: str,
    last_address: str = None,
):
    gc = gspread.service_account_from_dict(gspread_cred_dict)

    gsheet = gc.open_by_key(gsheet_key)
    responses_worksheet = gsheet.worksheet(worksheet_name)
    last_match = responses_worksheet.findall(last_address)[-1]
    # return the rows after the matching email address
    header_rows = responses_worksheet.row_values(1)
    logger.debug(f"Header rows from the worksheet: {header_rows}")
    matching_rows = responses_worksheet.get_values(f"A{last_match.row + 1}:ZZ")

    member_dicts = []

    for row in matching_rows:
        member_dict = {}
        for index, key in enumerate(header_rows):
            member_dict[key] = row[index]
        member_dicts.append(member_dict)

    # return value is converted to JSON
    return member_dicts, matching_rows


if __name__ == "__main__":
    import dotenv

    dotenv.load_dotenv()

    GSHEET_KEY = os.getenv("GSHEET_KEY")
    GSHEET_SHEET = os.getenv("GSHEET_SHEET")
    LAST_EMAIL_ADDRESS = os.getenv("LAST_EMAIL_ADDRESS")

    with open(".env.google.serviceaccount.json") as f:
        GSPREAD_CREDS_DICT = json.loads(f.read(), strict=False)

    gc = gspread.service_account_from_dict(GSPREAD_CREDS_DICT)

    res, _ = fetch_latest_signups(
        gspread_cred_dict=GSPREAD_CREDS_DICT,
        worksheet_name=GSHEET_SHEET,
        gsheet_key=GSHEET_KEY,
        last_address=LAST_EMAIL_ADDRESS,
    )

    with open("latest_signups.json", "w") as f:
        f.write(json.dumps(res, indent=4))
