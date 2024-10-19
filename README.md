# Tinaja-bot
A bot for TINAJA Ingenieria Discord server, written in Python.

## Manual installation
- Install dependencies
`pip install --user -r requirements.txt`
- Create a new `.env` file using `env.sample` as a template to set the required credentials.
- Run the bot
`python main.py`

## Docker installation
- Build docker container
`docker build -t tinaja-bot .`
- Create a new `.env` file using `env.sample` as a template to set the required credentials.
- Run docker container passing your env file:
`docker run -it --env-file .env tinaja-bot`
