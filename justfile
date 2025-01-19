
# list all the available commands
default:
    just --list

# run an arbitrary command with the .env vars set
run *options:
    {{ options }}

# run uv with environment variables set
uv *options:
    uv {{ options }}

# generate the newsletter locally fetching from outline
make_newsletter:
    uv run python ./notebooks/fetch-outline-newsletter.py

# edit the newsletter locally fetching from outline
edit_newsletter:
    uv run marimo edit ./notebooks/fetch-outline-newsletter.py