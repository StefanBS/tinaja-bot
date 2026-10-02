import discord
from discord.ext import commands
from prometheus_client import Gauge


class Census(commands.Cog):
    """Publishes the Server Census: Members and Online members per Server"""

    def __init__(self, bot):
        self.bot = bot
        self.total_users = Gauge('discord_total_users', 'Total number of users registered in the Discord server', registry=bot.registry)
        self.online_users = Gauge('discord_online_users', 'Total number of online users in the Discord server', registry=bot.registry)

    async def update_metrics(self):
        """Update Prometheus metrics with current Discord stats"""
        for guild in self.bot.guilds:
            # Update total users metric
            self.total_users.set(len(guild.members))
            # Update online users metric (includes online, idle, and dnd statuses)
            online_count = len([m for m in guild.members if m.status != discord.Status.offline])
            self.online_users.set(online_count)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.update_metrics()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.update_metrics()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.update_metrics()

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        await self.update_metrics()
