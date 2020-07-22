from __future__ import annotations
import discord
from discord.ext import commands
import time
import sys
import os
import datetime
from classes.helping import Helping
import json

class Moderation(commands.Cog):

    """
This Module allows moderators to enforce preset rules.
    """

    def __init__(self, bot):
        self.bot = bot
        self.icon = "<:dnastrand:716637671518240799>"
        self.thumbnail = 'https://cdn.discordapp.com/attachments/714791190926458901/716637965711048754/dna_1.png'
        self.helping = Helping()
        self.color = 0x2be97d
        self.log_color = 0xb94b4b

    # def cog_check(self, ctx):
    #        return ctx.author.id == 433293211436580874


    @commands.command()
    @commands.has_any_role(733571861841051709, 733713902281687040, 733719737435160586)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks a guild member from the server."""


        if not reason:
            reason = 'No reason was provided.'

        try:
            await member.kick(reason=reason)
        except:
            embed=discord.Embed(title="I lack the permissions to execute this request.", description=f'<:warningerrors:713782413381075536> Please **`do not`** attempt to kick an administrator.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return

        embed=discord.Embed(description=f"<:check:711530148196909126> Kicked `{member}` for `{reason}`", color=self.color)
        await ctx.send(embed=embed, delete_after=10)

        try:
            await ctx.message.delete(delay=10)
        except:
            pass


        channel = ctx.guild.get_channel(733740815092023326)

        embed=discord.Embed(description=f"**[NEW-KICK]** {member}, {member.id}\n\n`Moderator`: {ctx.author},\n`Reason`: {reason}", color=self.log_color)
        embed.set_footer(text=self.helping.get_footer(ctx))
        await channel.send(embed=embed)

    @commands.command()
    @commands.has_any_role(733571861841051709, 733713902281687040, 733719737435160586)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Bans a guild member from the server."""


        if not reason:
            reason = 'No reason was provided.'

        try:
            await member.ban(reason=reason)
        except discord.errors.Forbidden:
            embed=discord.Embed(title="I lack the permissions to execute this request.", description=f'<:warningerrors:713782413381075536> Please **`do not`** attempt to ban an administrator.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return

        embed=discord.Embed(description=f"<:check:711530148196909126> Banned `{member}` for `{reason}`", color=self.color)
        await ctx.send(embed=embed, delete_after=10)

        try:
            await ctx.message.delete(delay=10)
        except:
            pass


        channel = ctx.guild.get_channel(733740815092023326)

        embed=discord.Embed(description=f"**[NEW-BAN]** {member}, {member.id}\n\n`Moderator`: {ctx.author},\n`Reason`: {reason}", color=self.log_color)
        embed.set_footer(text=self.helping.get_footer(ctx))
        await channel.send(embed=embed)

    @commands.command()
    @commands.has_any_role(733571861841051709, 733713902281687040, 733719737435160586)
    async def unban(self, ctx, member: int, *, reason=None):
        """Unbans a guild member from the server."""


        if not reason:
            reason = 'No reason was provided.'

        try:
            member = await self.bot.fetch_user(member)
        except discord.ext.commands.errors.BadArgument:
            embed=discord.Embed(title="You did not pass a valid user ID.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}{ctx.command}` to try again.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return
        await ctx.guild.unban(member, reason=reason)

        embed=discord.Embed(description=f"<:check:711530148196909126> Unbanned `{member.name}` for `{reason}`", color=self.color)
        await ctx.send(embed=embed, delete_after=10)

        try:
            await ctx.message.delete(delay=10)
        except:
            pass


        channel = ctx.guild.get_channel(733740815092023326)

        embed=discord.Embed(description=f"**[NEW-UNBAN]** {member.name}, {member.id}\n\n`Moderator`: {ctx.author},\n`Reason`: {reason}", color=self.log_color)
        embed.set_footer(text=self.helping.get_footer(ctx))
        await channel.send(embed=embed)



    @commands.command()
    @commands.has_any_role(733571861841051709, 733713902281687040, 733719737435160586)
    async def warn(self, ctx, member: discord.Member, *, reason):
        """Warns a guild member for the given reason."""
        await self.bot.pg_con.execute(f"INSERT INTO warnings_vain (mod_id, actioned_id, reason) VALUES ($1, $2, '{reason}')", ctx.author.id, member.id)

        embed=discord.Embed(description=f"<:check:711530148196909126> Warned `{member.name}` for `{reason}`", color=self.color)
        await ctx.send(embed=embed, delete_after=10)

        try:
            await ctx.message.delete(delay=10)
        except:
            pass

        channel = ctx.guild.get_channel(733740815092023326)

        embed=discord.Embed(description=f"**[NEW-WARN]** {member.name}, {member.id}\n\n`Moderator`: {ctx.author},\n`Reason`: {reason}", color=self.log_color)
        embed.set_footer(text=self.helping.get_footer(ctx))
        await channel.send(embed=embed)

    @commands.command()
    @commands.has_any_role(733571861841051709, 733713902281687040, 733719737435160586)
    async def warnings(self, ctx, member: discord.Member):
        """Shows all warnings for a guild member."""
        actions = await self.bot.pg_con.fetch("SELECT * FROM warnings_vain WHERE actioned_id = $1", member.id)

        embed=discord.Embed(color=self.color)
        warnings=f"**`{len(actions)}`** Warnings found for {member};\n\n" if len(actions) != 0 else f"**`{len(actions)}`** Warnings where found for {member}\n\n"
        for i in actions:
            warnings+="```json\n"
            warnings+=f"Moderator-ID: {i['mod_id']}\n"
            warnings+=f'Reason: "{i["reason"]}"\n'
            warnings+=f"Unique-ID: {i['warning_id']}```\n\n"

        embed.description=warnings
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_any_role(733571861841051709, 733713902281687040, 733719737435160586)
    async def purge(self, ctx, num: int):
        """Purges X ammount of messages."""

        if num > 500 or num < 0:
            return await ctx.send("`Invalid amount, Maximum is 500.`")
        num = num + 1
        deleted = await ctx.channel.purge(limit=num, check=None)
        num = num - 1
        await ctx.send(f'`Deleted {num} messages for you.`', delete_after=10)

        channel = ctx.guild.get_channel(733740815092023326)

        embed=discord.Embed(description=f"**[NEW-PURGE]**\n\n`Moderator`: {ctx.author},\n`Ammount`: {num}\n`Channel`: {ctx.channel.mention}", color=self.log_color)
        embed.set_footer(text=self.helping.get_footer(ctx))
        await channel.send(embed=embed)

    @commands.command()
    @commands.has_any_role(733571861841051709, 733713902281687040, 733719737435160586)
    async def mute(self, ctx, member: discord.Member):
        """Mutes a guild member."""

        Muted = discord.utils.get(member.guild.roles, name='Muted')
        try:
            await member.add_roles(Muted)
        except discord.errors.Forbidden:
            embed=discord.Embed(title="I lack the permissions to execute this request.", description=f'<:warningerrors:713782413381075536> Please **`do not`** attempt to mute an administrator.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return
        embed=discord.Embed(description=f"<:check:711530148196909126> Muted `{member.name}`", color=self.color)
        await ctx.send(embed=embed, delete_after=10)

        try:
            await ctx.message.delete(delay=10)
        except:
            pass

        channel = ctx.guild.get_channel(733740815092023326)

        embed=discord.Embed(description=f"**[NEW-MUTE]**\n\n`Moderator`: {ctx.author},\n`Muted`: {member}, {member.id}", color=self.log_color)
        embed.set_footer(text=self.helping.get_footer(ctx))
        await channel.send(embed=embed)

    @commands.command()
    @commands.has_any_role(733571861841051709, 733713902281687040, 733719737435160586)
    async def unmute(self, ctx, member: discord.Member):
        """Unmutes a guild member."""

        Muted = discord.utils.get(member.guild.roles, name='Muted')
        try:
            await member.remove_roles(Muted)
        except discord.errors.Forbidden:
            embed=discord.Embed(title="I lack the permissions to execute this request.", description=f'<:warningerrors:713782413381075536> Please **`do not`** attempt to mute an administrator.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return
        embed=discord.Embed(description=f"<:check:711530148196909126> Unmuted `{member.name}`", color=self.color)
        await ctx.send(embed=embed, delete_after=10)

        try:
            await ctx.message.delete(delay=10)
        except:
            pass

        channel = ctx.guild.get_channel(733740815092023326)

        embed=discord.Embed(description=f"**[NEW-UNMUTE]**\n\n`Moderator`: {ctx.author},\n`Muted`: {member}, {member.id}", color=self.log_color)
        embed.set_footer(text=self.helping.get_footer(ctx))
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))
