
# list all the available commands
default:
    just --list

# generate the newsletter locally fetching from outline
make_newletter:
    uv run python ./notebooks/fetch-outline-newsletter.py