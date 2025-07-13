# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "outline-python-api",
#     "marimo",
#     "httpx==0.27.2",
#     "rich==13.9.2",
#     "python-dotenv==1.0.1",
#     "gspread==6.2.0",
# ]
# ///

import marimo

__generated_with = "0.9.23"
app = marimo.App(width="medium")


@app.cell
def __(mo):
    mo.md(
        """
        # Build our latest CAT newsletter

        This marimo script / notebook does the following

        1. Fetch the latest newsletter from the CAT wiki, Outline.
        2. Clean up some text artefacts we don't want in the newsletter
        3. Add the latest events
        4. Add the latest jobs
        5. Write it to a local file for inspection and further processing

        It's intended to be run on a Sunday as part of the process for getting the CAT newsletter ready, while still providing some editorial control.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"""## Fetch our dependencies""")
    return


@app.cell
def __():
    import os
    import marimo as mo
    import rich
    import datetime
    from rich.pretty import pprint
    from outline import Outline
    from dotenv import load_dotenv, dotenv_values
    load_dotenv(".env")

    # uncomment to sanity check env vars being loaded in
    # dotenv_values(".env")
    return (
        Outline,
        datetime,
        dotenv_values,
        load_dotenv,
        mo,
        os,
        pprint,
        rich,
    )


@app.cell
def __(mo):
    mo.md(r"""First of all, do we have access to the necessary API key?""")
    return


@app.cell
def __(os):
    API_KEY = os.environ.get("CAT_OUTLINE_API_KEY")

    if not API_KEY:
        raise Exception("""
        This notebook needs an API key to continue.
        You can get one from: https://climate-tech.getoutline.com/settings/tokens
        """)
    return (API_KEY,)


@app.cell
def __(mo):
    mo.md("""## Now authenticate to the Outline API""")
    return


@app.cell
def __(API_KEY, Outline, pprint):
    client = Outline(
        # This is the default and can be omitted
        bearer_token=API_KEY
    )

    auth_info_response = client.auth.info()
    outline_team = auth_info_response.data.team.name 
    user_name = auth_info_response.data.user.name
    if auth_info_response.data:
        pprint(f"Logged successfully in as user: {user_name}, in outline team: {outline_team}")


    return auth_info_response, client, outline_team, user_name


@app.cell
def __(mo):
    mo.md(r"""## Can we fetch a single document as markdown to work with?""")
    return


@app.cell
def __(client):
    res = client.documents.export(id="latest-newsletter-8EiA2tLfkZ")
    return (res,)


@app.cell
def __(res):
    res.data[:400]
    return


@app.cell
def __(mo):
    mo.md("""## Can we filter out the bits we manually change each time?""")
    return


@app.cell
def __():
    import re
    return (re,)


@app.cell
def __(mo):
    mo.md(r"""First of all, let's get rid of the weird backslashes followed by the new lines.""")
    return


@app.cell
def __(re):
    pattern = re.compile(r"\\\n")
    return (pattern,)


@app.cell
def __(pattern, res):
    pattern.findall(res.data)
    return


@app.cell
def __(mo):
    mo.md(r"""We also want to clear out the admonishments that are wrapped in `:::info` and so on,""")
    return


@app.cell
def __(re, res):
    multi_line_pattern = re.compile(r'(?m)(^:::info$\n.*?\n^:::$)', re.DOTALL)


    multi_line_pattern.findall(res.data)
    return (multi_line_pattern,)


@app.cell
def __(multi_line_pattern, pattern, res):
    data_copy = res.data

    for match_pattern in multi_line_pattern.findall(res.data):
        data_copy = data_copy.replace(match_pattern, "")

    for new_line_match in pattern.findall(res.data):
        data_copy = data_copy.replace(new_line_match, "")


    data_copy
    return data_copy, match_pattern, new_line_match


@app.cell
def __(mo):
    mo.md(
        """
        ### We have submitted events to import

        We want all events submitted after the cut off window, in ascending order of the event date - not the submission date.
        """
    )
    return


@app.cell
def __(gc, os):
    EVENTS_SHEET_KEY = os.environ.get("CAT_EVENTS_SHEET_KEY")
    events_sheet = gc.open_by_key(EVENTS_SHEET_KEY)
    events_worksheet = events_sheet.worksheet("Form Responses 1")
    event_header_row = events_worksheet.row_values(1)
    events_list = events_worksheet.get_all_records(expected_headers=event_header_row)
    return (
        EVENTS_SHEET_KEY,
        event_header_row,
        events_list,
        events_sheet,
        events_worksheet,
    )


@app.cell
def __(datetime, events_list):
    def within_event_horizon(event):
        """return true if the event is taking place in the future still"""
        today = datetime.datetime.now().date()
        event_date = datetime.datetime.strptime(
            event.get("Event date"), 
            "%m/%d/%Y"
        ).date()

        return event_date > today


    future_events = [event for event in events_list if within_event_horizon(event)]
    f"There are {len(future_events)} events to list"

    future_events = sorted(future_events, key=lambda x: datetime.datetime.strptime(x["Event date"], "%m/%d/%Y"))
    return future_events, within_event_horizon


@app.cell
def __(datetime, future_events):
    def event_template(event: dict) -> str:
        """Return a rendered template of an event, for inclusion in the newsletter"""
        parsed_date = datetime.datetime.strptime(event.get('Event date'), "%m/%d/%Y")


        # add day of the week to this snippet
        rendered_date = parsed_date.strftime("%A %b %d, %Y")
        return f"""

    ### [{rendered_date} - {event.get('What is this event called?')}]({ event.get('Registration link ')})


    {event.get('Event Description')}

    """

    event_template(future_events[0])
    return (event_template,)


@app.cell
def __(event_template, future_events):
    rendered_events = "\n".join([event_template(event) for event in future_events])

    events_section = f"""

    ---

    {rendered_events}


    ---
    """

    # data_copy.replace("INSERT_SUBMITTED_EVENTS_HERE", events_section)
    return events_section, rendered_events


@app.cell
def __(mo):
    mo.md(
        r"""
        ### We also have jobs to import

        To do this, we need to fetch the most recent files from the jobs file, and filter out any jobs outside the date range.
        """
    )
    return


@app.cell
def __():
    # data_copy.replace("INSERT_EVENTS_HERE", "## Upcoming Events\n\n")
    return


@app.cell
def __():
    import json
    import gspread

    with open(".env.google.serviceaccount.json") as f:
        GSPREAD_CREDS_DICT = json.loads(f.read(), strict=False)

        gc = gspread.service_account_from_dict(GSPREAD_CREDS_DICT)


    gc
    return GSPREAD_CREDS_DICT, f, gc, gspread, json


@app.cell
def __(gc, os):
    JOBS_SHEET_KEY = os.environ.get("CAT_JOBS_SHEET_KEY")
    jobs_sheet = gsheet = gc.open_by_key(JOBS_SHEET_KEY)
    jobs_worksheet = jobs_sheet.worksheet("Form Responses 1")
    header_row = jobs_worksheet.row_values(1)
    jobs_list = jobs_worksheet.get_all_records(expected_headers=header_row)
    return (
        JOBS_SHEET_KEY,
        gsheet,
        header_row,
        jobs_list,
        jobs_sheet,
        jobs_worksheet,
    )


@app.cell
def __(datetime, jobs_list):
    jobs_list[0]

    datetime.datetime.strptime(jobs_list[0]["Timestamp"], "%m/%d/%Y %H:%M:%S").date()
    return


@app.cell
def __(datetime):
    from datetime import timedelta

    today = datetime.datetime.now().date()
    job_cutoff_window = today - timedelta(weeks=4)
    job_cutoff_window
    return job_cutoff_window, timedelta, today


@app.cell
def __(datetime, job_cutoff_window, jobs_list):
    def within_cutoff_period(job):
        job_submission_date = datetime.datetime.strptime(
            job.get("Timestamp"), 
            "%m/%d/%Y %H:%M:%S"
        ).date()

        return job_submission_date > job_cutoff_window



    recent_jobs = [job for job in jobs_list if within_cutoff_period(job)]
    len(recent_jobs)
    return recent_jobs, within_cutoff_period


@app.cell
def __():
    def job_template(job):
        return f"""

    ### [{job.get('Company')} - {job.get('Role')} - {job.get('Salary Range')} - {job.get('Contract Type')} - { job.get('In-office expectations')}]({job.get('Link to Job Description')})

    {job.get('Short description')}
    """
    return (job_template,)


@app.cell
def __(job_template, recent_jobs):
    job_listings = []
    for job in recent_jobs:
        job_listings.append(job_template(job))

    rendered_jobs = "\n".join(job_listings)

    job_section = f"""

    ---

    {rendered_jobs}

    ---


    """
    return job, job_listings, job_section, rendered_jobs


@app.cell
def __(data_copy, events_section, job_section):
    _content_copy = data_copy

    _content_copy = _content_copy.replace("INSERT_SUBMITTED_EVENTS_HERE", events_section)

    _content_copy = _content_copy.replace("INSERT_JOBS_HERE", job_section)

    newsletter_content_with_jobs_and_events = _content_copy

    newsletter_content_with_jobs_and_events
    return (newsletter_content_with_jobs_and_events,)


@app.cell
def __(datetime, newsletter_content_with_jobs_and_events):
    timestamp: str = str(datetime.datetime.now().strftime("%Y-%m-%d--%H-%M"))
    new_newsletter_filename = f"cat-generated-newsletter-{timestamp}.md"
    with open(new_newsletter_filename, "w") as cat_file:
        cat_file.write(newsletter_content_with_jobs_and_events)

        print(f"Saved newsletter to {new_newsletter_filename}")
    return cat_file, new_newsletter_filename, timestamp


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
