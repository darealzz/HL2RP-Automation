import discord
from discord.ext import commands, tasks
import time
import sys
import os
import json
from classes.helping import Helping

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.log_color = 0xb94b4b
        self.helping = Helping()


    # @tasks.loop(seconds=30)w
    # async def change_status(self):
    #     if ctx.guild.premium_subscribers == self.bot.prem_lst:
    #         return
    #     elif ctx.guild.premium_subscribers != self.bot.prem_lst:
    #         for user in ctx.guild.premium_subscribers:
    #             if user not in self.bot.prem_lst:
    #                 channel = ctx.guild.get_channel(716939038489051136)
    #                 await channel.send('new premium man')

    @commands.Cog.listener()
    async def on_ready(self):

        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"The Universal Union"))

        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('------')

        # self.change_status.start()
        # self.change_statuss.start()


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel = self.bot.get_channel(735524706656190525)
        embed=discord.Embed(color=self.log_color)
        if message.attachments:
            # embed.set_image(url=f"{message.attachments[0].url}")
            content="**{Image}**"
        else:
            content = message.content
        embed.description=f"**[NEW-MESSAGE-DELETE]**\n\n`Message-author`: {message.author.name}, {message.author.id}\n`Channel`: {message.channel.mention},\n`Message`: {content}"
        embed.set_footer(text=self.helping.get_footer(message))
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Events(bot))
