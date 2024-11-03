# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "outline-python-api",
#     "marimo",
#     "httpx==0.27.2",
#     "rich==13.9.2",
#     "python-dotenv==1.0.1",
# ]
# ///

import marimo

__generated_with = "0.9.1"
app = marimo.App(width="medium")


@app.cell
def __(mo):
    mo.md(r"""## Fetch our dependencies""")
    return


@app.cell
def __():
    import os
    import marimo as mo
    import rich
    from rich.pretty import pprint
    from outline import Outline
    from dotenv import load_dotenv, dotenv_values
    load_dotenv(".env")

    # uncomment to sanity check env vars being loaded in
    # dotenv_values(".env")
    return Outline, dotenv_values, load_dotenv, mo, os, pprint, rich


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
    pprint(auth_info_response.data)
    return auth_info_response, client


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
def __():
    return


if __name__ == "__main__":
    app.run()
