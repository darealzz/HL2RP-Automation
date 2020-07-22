import discord
from discord.ext import commands
import time
import sys
import os
from cogs.info import EmbedHelpCommand
from classes.helping import Helping


class Errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.BadArgument):
            embed=discord.Embed(title="You did not give valid permiters for that command.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}help {ctx.command}` for help.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.NotOwner):
            embed=discord.Embed(title="You don't have permissions to run this command.", description=f'<:warningerrors:713782413381075536> `{ctx.prefix}{ctx.command}` has been restricted to owner usage only.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="You are missing required arguments for that command.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}help {ctx.command}` for help.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.CommandOnCooldown):
            embed=discord.Embed(title=f"Cooldown is active.", description=f'<:warningerrors:713782413381075536> The command `{ctx.prefix}{ctx.command}` can only be called once every 4 hours.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.CheckFailure):
            embed=discord.Embed(title="You don't have permissions to run this command.", description=f'<:warningerrors:713782413381075536> `{ctx.prefix}{ctx.command}` has been restricted for specific members & roles.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return



def setup(bot):
    bot.add_cog(Errors(bot))
