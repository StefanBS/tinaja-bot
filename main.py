import os
import discord
import aiohttp
from discord.ext import commands
from prometheus_client import Gauge, generate_latest
from dotenv import load_dotenv
from aiohttp import web

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True  # Required for online status tracking

bot = commands.Bot(command_prefix='!', intents=intents)

# Define Prometheus metrics
total_users = Gauge('discord_total_users', 'Total number of users registered in the Discord server')
online_users = Gauge('discord_online_users', 'Total number of online users in the Discord server')

async def metrics_handler(request):
    """Handler for /metrics endpoint"""
    return web.Response(body=generate_latest(), content_type='text/plain')

async def start_metrics_server():
    """Start the metrics HTTP server"""
    app = web.Application()
    app.router.add_get('/metrics', metrics_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    await site.start()
    print(f"Metrics server started at http://localhost:8000/metrics")

async def update_metrics():
    """Update Prometheus metrics with current Discord stats"""
    for guild in bot.guilds:
        # Update total users metric
        total_users.set(len(guild.members))
        # Update online users metric (includes online, idle, and dnd statuses)
        online_count = len([m for m in guild.members if m.status != discord.Status.offline])
        online_users.set(online_count)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await start_metrics_server()
    await update_metrics()

@bot.event
async def on_member_join(member):
    await update_metrics()

@bot.event
async def on_member_remove(member):
    await update_metrics()

@bot.event
async def on_presence_update(before, after):
    await update_metrics()

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
