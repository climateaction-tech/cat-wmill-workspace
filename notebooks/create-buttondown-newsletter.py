import marimo

__generated_with = "0.9.23"
app = marimo.App(width="medium")


@app.cell
def __(mo):
    mo.md(
        r"""
        # Creating our next Sunday newsletter

        This script creates our next CAT newsletter with Buttondown. It's expected to be run on the Sunday morning we send it out.


        """
    )
    return


@app.cell
def _():
    import marimo as mo
    import os
    return mo, os


@app.cell
def _(os):
    BUTTONDOWN_API_KEY=os.getenv("BUTTONDOWN_API_KEY")
    return (BUTTONDOWN_API_KEY,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### which emails have we sent already?

        We need a list of emails sent from the Buttondown API. The emails are ordered by their creation date in descending order, and the body field is excluded from the response, because it totally bloats the payload size.
        """
    )
    return


@app.cell
def _(BUTTONDOWN_API_KEY):
    import httpx

    url = "https://api.buttondown.com/v1/emails"
    headers = {
      "Authorization": f"Token {BUTTONDOWN_API_KEY}"
    }

    payload = {
        "excluded_fields": ["body"],
        "ordering": "-creation_date"

    }

    response = httpx.get(url, headers=headers, params=payload)
    response
    return headers, httpx, payload, response, url


@app.cell
def _(mo):
    mo.md(
        r"""
        ### What does our response look like?

        Let's have a look. We have our IDs, and the titles. These are what we want to refer to when creating our draft emails later.
        """
    )
    return


@app.cell
def _(response):
    # return as formatted json
    response.json()
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Ok, when is the next newsletter supposed to go out?

        We need this so we can decide to either create a draft newsletter, or if there is already is an existing newsletter, figure out what to do with it.
        """
    )
    return


@app.cell
def _(response):
    newsletters = [result['subject'] for result in response.json()['results']]
    return (newsletters,)


@app.cell
def _(newsletters):
    newsletters
    return


@app.cell
def _(newsletters):
    import datetime
    import calendar
    import re

    def get_next_sunday(newsletters) -> datetime.date:
        _issue_title, _date_string = newsletters[0].split(" - ")
        _extracted_date = datetime.datetime.strptime(_date_string, "%Y-%m-%d")

        # find the week we are in, and add one week to it, and return the sunday
        _new_issue_datetime = _extracted_date + datetime.timedelta(weeks=1)  # next Sunday
        
        return _new_issue_datetime.date()

    get_next_sunday(newsletters)
    return calendar, datetime, get_next_sunday, re


@app.cell
def _(get_next_sunday, newsletters, re):
    def create_new_subject(newsletters):
        sunday_date = get_next_sunday(newsletters)
        last_subject = newsletters[0]
        issue_number = int(re.search(r'\d+', last_subject).group()) + 1
        _new_issue_title = f"🌍 CAT Newsletter {issue_number} - {sunday_date}"
        
        if _new_issue_title in [n for n in newsletters]:
            raise ValueError("A newsletter with this subject already exists.")
        return _new_issue_title
    new_issue_title = create_new_subject(newsletters)
    return create_new_subject, new_issue_title


@app.cell
def __(mo):
    mo.md(
        r"""
        ## OK, now we create our new newsletter, using the API, and `new_issue_title`, and fetching the most recently created newsletter file locally.


        """
    )
    return


@app.cell(disabled=True)
def __(headers, httpx, latest_newsletter_text, new_issue_title, url):
    newsletter_text = ""
    with open(f"./{latest_newsletter_text}") as newsletter_file:
        newsletter_text = newsletter_file.read()

    new_newsletter_payload = {
        "subject": new_issue_title,
        "body": newsletter_text,
        "status": "draft"
    }

    create_response = httpx.post(url, headers=headers, json=new_newsletter_payload)
    create_response
    return (
        create_response,
        new_newsletter_payload,
        newsletter_file,
        newsletter_text,
    )


@app.cell
def __():
    import pathlib

    matching_newsletter_files = [
        entry for entry in 
        pathlib.Path(".").glob("*cat-generated-newsletter*")
    ]
        
    latest_newsletter_text = sorted(matching_newsletter_files)[-1]
    latest_newsletter_text
    return latest_newsletter_text, matching_newsletter_files, pathlib


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
