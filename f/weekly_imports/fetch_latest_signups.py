import wmill
import gspread
import rich

# You can import any PyPi package.
# See here for more info: https://www.windmill.dev/docs/advanced/dependencies_in_python

# 1. figure out how to fetch resources to auth
# 2. figure out how to auth with gspread
# 3. fetch data with gspread
# 4. manipulate and store state each time
# 5. set up cronjob


def main(gsheet_key: str, worksheet_name: str, override_email: str = None):
    if override_email:
        LAST_EMAIL_ADDRESS = override_email
    else:
        last_state = wmill.get_state()
        LAST_EMAIL_ADDRESS = last_state.get("last_email_address")

    rich.print(f"Current Last email address: {LAST_EMAIL_ADDRESS}")

    path_to_resource = "f/weekly_imports/improving_c_gspread_service_account"
    gspread_cred_dict = wmill.get_resource(path_to_resource)

    gc = gspread.service_account_from_dict(gspread_cred_dict)

    gsheet = gc.open_by_key(gsheet_key)
    responses_worksheet = gsheet.worksheet(worksheet_name)
    last_match = responses_worksheet.findall(LAST_EMAIL_ADDRESS)[-1]
    # return the rows after the matching email address
    header_rows = responses_worksheet.row_values(1)
    rich.print(f"Header rows from the worksheet: {header_rows}")
    matching_rows = responses_worksheet.get_values(f"A{last_match.row + 1}:ZZ")
    last_row = matching_rows[-1]

    if not last_row:
        rich.print("No new signups to pass along")
        return []

    if last_row:
        last_email = last_row[1]

        if last_email:
            rich.print(f"Setting last email address to: {last_email}")
            new_state = {"last_email_address": last_email}
            wmill.set_state(new_state)

    member_dicts = []

    for row in matching_rows:
        member_dict = {}
        for index, key in enumerate(header_rows):
            member_dict[key] = row[index]
        member_dicts.append(member_dict)

    # return value is converted to JSON
    return member_dicts
