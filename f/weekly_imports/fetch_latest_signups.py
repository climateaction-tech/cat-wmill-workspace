import os
import wmill
import rich

import gspread

# You can import any PyPi package.
# See here for more info: https://www.windmill.dev/docs/advanced/dependencies_in_python

# 1. figure out how to fetch resources to auth
# 2. figure out how to auth with gspread
# 3. fetch data with gspread
# 4. manipulate and store state each time
# 5. set up cronjob




def main():
    print("Running a check")

    # a resource

    



    # gc = gspread.service_account(filename=settings.GSPREAD_SERVICE_ACCOUNT)
    # gsheet = gc.open_by_key(settings.GSPREAD_KEY)
    # responses_worksheet = gsheet.worksheet(CAT_RESPONSES_WORKSHEET)

    # res = wmill.get_resource("u/mrchrisadams/improving_c_gspread_service_account")
    res = wmill.get_resource("f/weekly_imports/improving_c_gspread_service_account")





    rich.print(res)

    # Get last state of this script execution by the same trigger/user
    last_state = wmill.get_state()
    new_state = {"last_email_address": 42} if last_state is None else last_state
    new_state["last_email_address"] += 1
    wmill.set_state(new_state)

    # fetch context variables
    signups = []

    # return value is converted to JSON
    return {"signups": signups, "state": []}
