import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='unexpo')
async def unexpo(ctx):
    response = f"Hola {ctx.author.mention}! Tuetudiate en el poli?"
    await ctx.send(response)

@bot.command(name='exercism')
async def exercism(ctx):
    await ctx.send("The exercism command is not implemented yet.")

token = os.getenv('DISCORD_BOT_TOKEN')

if token is None:
    raise ValueError("No token found. Make sure to set the DISCORD_BOT_TOKEN environment variable.")

bot.run(token)
