import discord
from discord.ext import commands
import time
import sys
import os
from classes.helping import Helping


class OwnerOnly(commands.Cog):
    """
These commands has been reserved for the ownership team to streamline development.
    """
    def __init__(self, bot):
        self.bot = bot
        self.icon = '<:meds:715935011160719360>'
        self.thumbnail = 'https://cdn.discordapp.com/attachments/693832161660370945/716316377778094090/pill.png'

    @commands.command(description="Owner only.")
    @commands.is_owner()
    async def load(self, ctx, extension):
        """
        Loads specified cog.
        """
        try:
            self.bot.load_extension(f"cogs.{extension}")
        except commands.errors.ExtensionAlreadyLoaded:
            await ctx.send(f"<:rcross:711530086251364373> | **Cog already loaded: `{extension}`**")
        else:
            await ctx.send(f"<:check:711530148196909126> | **Loaded Cog: `{extension}`**")

    @commands.command(description="Owner only.")
    @commands.is_owner()
    async def reload(self, ctx, extension):
        """
        Reloads specified cog.
        """
        try:
            self.bot.unload_extension(f"cogs.{filename[:-3]}")
        except commands.errors.ExtensionNotLoaded:
            await ctx.send(f"<:rcross:711530086251364373> | **Cog not loaded: `{extension}`**")
        else:
            self.bot.load_extension(f"cogs.{filename[:-3]}")
            await ctx.send(f"<:check:711530148196909126> | **Realoded Cog: `{extension}`**")

    @commands.command(description="Owner only.")
    @commands.is_owner()
    async def unload(self, ctx, extension):
        """
        Unloads specified cog.
        """
        try:
            self.bot.unload_extension(f"cogs.{extension}")
        except commands.errors.ExtensionNotLoaded:
            await ctx.send(f"<:rcross:711530086251364373> | **Cog not loaded: `{extension}`**")
        else:
            await ctx.send(f"<:check:711530148196909126> | **Unloaded Cog: `{extension}`**")

    @commands.command(description="Owner only.")
    @commands.is_owner()
    async def r(self, ctx):
        """
        Reloads all cogs.
        """

        embed=discord.Embed(title="a", color=0x36393E)
        # embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
        # await ctx.send(embed=embed)
        # return
        description=""
        loaded=0
        not_loaded=0
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    self.bot.unload_extension(f"cogs.{filename[:-3]}")
                except commands.errors.ExtensionNotLoaded:
                    description += f"<:warningerrors:713782413381075536> | **Cog not loaded: `{filename[:-3]}`**\n"
                    not_loaded+=1
                else:
                    self.bot.load_extension(f"cogs.{filename[:-3]}")
                    description += f"<:check:711530148196909126> | **Realoded Cog: `{filename[:-3]}`**\n"
                    loaded+=1

                    # await ctx.send(f"<:check:711530148196909126> | **Realoded Cog: `{filename[:-3]}`**")
        #await ctx.send(f"<:check:711530148196909126> | `Reloaded the cogs`")
        embed.title=f'{loaded} modules where loaded & {not_loaded} modules where not loaded.'
        embed.description=description
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
        await ctx.send(embed=embed)

    @commands.command(description="Owner only.")
    @commands.is_owner()
    async def cogs(self, ctx):
        """
        Shows all cogs.
        """
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await ctx.send(f"`{filename[:-3]}`")


    @commands.group()
    @commands.is_owner()
    async def debugmode(self, ctx):
        """
        Bots mode respective to the subcommand.
        """
        pass
        # self.bot.unload_extension(f"events.errors")
        #
        # await ctx.send(f"<:check:711530148196909126> | **Bot has been changed to debuging mode.**")

    @debugmode.command(name='-on')
    async def _on(self, ctx):
        """
        Changes bot to debug mode.
        """
        try:
            self.bot.unload_extension(f"events.errors")
            await ctx.send(f"<:check:711530148196909126> | **Bot has been changed to debuging mode.**")
        except:
            await ctx.send(f"<:rcross:711530086251364373> | **The bot is already in debug mode.**")

    @debugmode.command(name='-off')
    async def _off(self, ctx):
        """
        Turns debug mode off.
        """
        try:
            self.bot.load_extension(f"events.errors")
            await ctx.send(f"<:check:711530148196909126> | **Debuging mode has been turned off.**")
        except:
            await ctx.send(f"<:rcross:711530086251364373> | **Debug mode is already off.**")

def setup(bot):
    bot.add_cog(OwnerOnly(bot))
