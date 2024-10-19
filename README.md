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
- Install dependencies
```bash
pip install --user -r requirements.txt
```
- Create a new `.env` file using `env.sample` as a template to set the required credentials.
- Run the bot
```bash
python main.py
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
