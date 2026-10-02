import discord
from discord.ext import commands
from prometheus_client import CollectorRegistry

from tinaja_bot.cogs.census import Census
from tinaja_bot.cogs.exercism import Exercism
from tinaja_bot.cogs.unexpo import Unexpo
from tinaja_bot.metrics import MetricsEndpoint


class TinajaBot(commands.Bot):
    def __init__(self, config):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True  # Required for online status tracking
        super().__init__(command_prefix='!', intents=intents)

        self.config = config
        self.registry = CollectorRegistry()
        self.metrics_endpoint = MetricsEndpoint(self.registry, config.metrics_host, config.metrics_port)

    async def setup_hook(self):
        # Runs once before connecting, unlike on_ready which fires on every reconnect
        await self.add_cog(Census(self))
        await self.add_cog(Unexpo())
        await self.add_cog(Exercism())
        await self.metrics_endpoint.start()

    async def close(self):
        await self.metrics_endpoint.stop()
        await super().close()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
