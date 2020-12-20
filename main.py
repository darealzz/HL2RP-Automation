import discord
from discord.ext import commands, tasks
import random
import os
import itertools
from cogs.info import EmbedHelpCommand
import asyncpg


bot = commands.Bot(command_prefix=['!'], case_insensetive=True, help_command=EmbedHelpCommand())
# bot.prem_lst = ctx.guild.premium_subscribers
bot.epic_count = 0

async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(host="localhost", database="postgres", user="postgres", password="Bestmate69")



for filename in os.listdir('./events'):
    if filename.endswith('.py'):
        bot.load_extension(f"events.{filename[:-3]}")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")




bot.load_extension('jishaku')

bot.loop.run_until_complete(create_db_pool())
bot.run('env')
