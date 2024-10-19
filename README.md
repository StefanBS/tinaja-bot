# Tinaja-bot
A bot for TINAJA Ingenieria Discord server, written in Python.

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

## Docker build and run
- Build docker container
```bash
docker build -t tinaja-bot .
```
- Create a new `.env` file using `env.sample` as a template to set the required credentials.
- Run docker container passing your env file:
```bash
docker run -it --env-file .env tinaja-bot
```
