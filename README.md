# Tinaja-bot
A bot for TINAJA Ingenieria Discord server, written in Python.

## Run using published container image
- Create a new `.env` file using `env.sample` as a template to set the required credentials.
- Pull latest image
```bash
docker pull ghcr.io/stefanbs/tinaja-bot/tinaja-bot:latest
```
- Run docker container passing your env file:
```bash
docker run -it --env-file .env ghcr.io/stefanbs/tinaja-bot/tinaja-bot
```

## Run manually
- Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then install the dependencies (uv fetches Python 3.14 if you don't have it)
```bash
uv sync
```
- Create a new `.env` file using `env.sample` as a template to set the required credentials.
- Run the bot
```bash
uv run python -m tinaja_bot
```

## Local Docker build and run
- Build docker container
```bash
docker build -t tinaja-bot .
```
- Create a new `.env` file using `env.sample` as a template to set the required credentials.
- Run docker container passing your env file:
```bash
docker run -it --env-file .env tinaja-bot
```

## Run tests
```bash
uv run pytest
```

## Lint and format
```bash
uv run ruff check .       # lint (add --fix to apply safe fixes)
uv run ruff format .      # format
```
CI fails if either reports a problem.

## Manage dependencies
Dependencies are declared in `pyproject.toml` and pinned in `uv.lock`.
```bash
uv add <package>          # add a runtime dependency
uv add --dev <package>    # add a development dependency
uv lock --upgrade         # upgrade everything to the latest versions
```
