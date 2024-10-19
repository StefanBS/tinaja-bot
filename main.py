import os
import discord
import aiohttp
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
async def exercism(ctx, username=None):
    if username is None:
        await ctx.send(f"{ctx.author.mention} you must provide an exercism profile name")
        return

    url = f"https://exercism.org/profiles/{username}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 404:
                await ctx.send(f"{username} does not appear to be a valid exercism public profile")
            elif response.status == 200:
                await ctx.send(url)
            else:
                await ctx.send(f"An error occurred while checking the profile. Status code: {response.status}")

token = os.getenv('DISCORD_BOT_TOKEN')

if token is None:
    raise ValueError("No token found. Make sure to set the DISCORD_BOT_TOKEN environment variable.")

bot.run(token)
