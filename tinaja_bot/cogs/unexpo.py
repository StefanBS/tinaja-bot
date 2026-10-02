from discord.ext import commands


class Unexpo(commands.Cog):
    @commands.command(name='unexpo')
    async def unexpo(self, ctx):
        response = f"Hola {ctx.author.mention}! Tuetudiate en el poli?"
        await ctx.send(response)
