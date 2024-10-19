import os
import discord
import re
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if re.search(r'\bunexpo\b', message.content, re.IGNORECASE):
        response = f"Hola {message.author.mention}! Tuetudiate en el poli?"
        await message.channel.send(response)

token = os.getenv('DISCORD_BOT_TOKEN')

if token is None:
    raise ValueError("No token found. Make sure to set the DISCORD_BOT_TOKEN environment variable.")

client.run(token)
