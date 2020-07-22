import discord
from discord.ext import commands
import time
import sys
import os
import datetime


class Helping():

    def __init__(self):
        self.now = datetime.datetime.now()

    def get_time_in_gmt(self):

        if len(str(self.now.minute)) == 1:
            x = f"0{self.now.minute}"
        else:
            x = self.now.minute

        return f'{self.now.hour}:{x}'

    def get_footer(self, ctx):
        return f'[-] Invoked by {ctx.author} @ {self.get_time_in_gmt()}'
