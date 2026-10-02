from urllib.parse import quote

import aiohttp
from discord.ext import commands


class Exercism(commands.Cog):
    def __init__(self, base_url='https://exercism.org', timeout=10):
        self._base_url = base_url
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._session = None

    async def cog_load(self):
        self._session = aiohttp.ClientSession(timeout=self._timeout)

    async def cog_unload(self):
        await self._session.close()

    @commands.command(name='exercism')
    async def exercism(self, ctx, username=None):
        if username is None:
            await ctx.send(f'{ctx.author.mention} you must provide an exercism profile name')
            return

        # Escaped so a name like '../../about' can't point the check at another page
        url = f'{self._base_url}/profiles/{quote(username, safe="")}'
        try:
            async with self._session.get(url) as response:
                status = response.status
        except aiohttp.ClientError, TimeoutError:
            await ctx.send('An error occurred while checking the profile.')
            return

        if status == 404:
            await ctx.send(f'{username} does not appear to be a valid exercism public profile')
        elif status == 200:
            await ctx.send(url)
        else:
            await ctx.send(f'An error occurred while checking the profile. Status code: {status}')
