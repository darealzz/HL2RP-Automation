from __future__ import annotations
import discord
from discord.ext import commands
import time
import sys
import os
import datetime
from classes.helping import Helping

class EmbedHelpCommand(commands.HelpCommand):

    COLOUR = 0x36393E
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.verify_checks = False
        # self.command_attrs = {"checks": [is_owner]}

    def get_ending_note(self):
        now = datetime.datetime.now()
        if len(str(now.minute)  ) == 1:
            x = f"0{now.minute}"
        else:
            x = now.minute
        return f'[-] Invoked by {self.context.author} @ {now.hour}:{x}'.format(self.clean_prefix, self.invoked_with)

    def get_opening_note(self):
        return f"""```md
* All optional aurguments are wrapped with '[]'
* All mandatory aurguments are wrapped with '<>'
```
```diff
- Do NOT type these symbols when during command usage
+ {self.clean_prefix}{self.invoked_with} [command | module] for help on a command/module
+ Both [command | module] aurguments are case sensetive
```
        """

    def get_command_signature(self, command):
        return '{0.qualified_name} {0.signature}'.format(command)
    def get_command_signature_name(self, command):
        return '{0.qualified_name}'.format(command)
    def get_author_icon(self):
        return f'{self.context.author.avatar_url_as(format="png")}'
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='HELP PANEL', description=self.get_opening_note(), colour=self.COLOUR)
        description = self.context.bot.description
        if description:
            embed.description = description
        cogs = ""
        for cog in self.context.bot.cogs.values():
            # if cog == 'OwnerOnly':
            #     cog=''
            try:
                # cogs += '• '
                cogs += f'• {cog.icon}'
                cogs += ' '
                cogs += cog.qualified_name
                cogs += '\n'
            except AttributeError:
                pass

        cogs += '\n\n'
            # name = 'No Category' if cog is None else cog.qualified_name
            # filtered = await self.filter_commands(commands, sort=True)
            # if filtered:
            #     value = '\u2002'.join(f'`{c.name}`' for c in commands)
            #     if cog:
            #         value = '{0}'.format(value)


        embed.add_field(name='Enabled Modules', value=cogs, inline=False)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        cmds=""
        embed = discord.Embed(title=f'{(cog.qualified_name).upper()} MODULE', colour=self.COLOUR)
        # if cog.description:
        #     embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            cmds += f"`{(self.get_command_signature_name(command)).strip()}`"
            cmds += f" - "
            cmds += command.short_doc
            cmds += '\n'
        embed.add_field(name=f'**{cog.__doc__}**', value=cmds, inline=False)
        embed.set_thumbnail(url=cog.thumbnail)
        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        self.verify_checks=False
        embed = discord.Embed(title=self.get_command_signature(group), colour=self.COLOUR)
        if group.help:
            embed.description = group.help

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            for command in filtered:
                embed.add_field(name=self.get_command_signature(command), value=command.short_doc, inline=False)

        embed.set_thumbnail(url=group.cog.thumbnail)
        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)


    send_command_help = send_group_help

class Info(commands.Cog):

    """
This Module allows you to get data about this bot.
    """

    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = EmbedHelpCommand()
        bot.help_command.cog = self
        self.bot = bot
        self.icon = "<:tubes:715934865794662501>"
        self.thumbnail = 'https://media.discordapp.net/attachments/693832161660370945/715936504651972728/lab.png?width=499&height=499'
        self.helping = Helping()
        self.global_check = False


    @commands.command(description="Displays the average webstock latency.")
    async def ping(self, ctx):
        """
        Displays the average webstock latency.
        """
        lst=[]
        for i in range(3):
            lst.append(round(self.bot.latency*1000))


        embed=discord.Embed(title="PONG", color=0x36393E)
        embed.add_field(name=f"Average websocket latency", value=f":ping_pong: | `{lst[0]}ms`", inline=False)
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=self.helping.get_footer(ctx))
        await ctx.send(embed=embed)

    # def cog_unload(self):
    #     self.bot.help_command = self._original_help_command
def setup(bot):
    bot.add_cog(Info(bot))
