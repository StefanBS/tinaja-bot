import aiohttp
from discord.ext import commands


class Exercism(commands.Cog):
    @commands.command(name='exercism')
    async def exercism(self, ctx, username=None):
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
