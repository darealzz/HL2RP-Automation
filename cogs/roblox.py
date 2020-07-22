import discord
from discord.ext import commands
import time
import sys
import os
from cogs.info import EmbedHelpCommand
from classes.helping import Helping
import json
import requests
from bs4 import BeautifulSoup
import random
import asyncpg
import robloxapi
import asyncio

class Roblox(commands.Cog):

    """
This Module allows you to execute roblox related tasks.
    """

    def __init__(self, bot):
        self.bot = bot
        self.icon = "<:h2o:716315229381984257>"
        self.thumbnail = 'https://cdn.discordapp.com/attachments/714791190926458901/716315345849155634/h2o_1.png'
        self.helping = Helping()
        self.client = robloxapi.Client(cookie=None)

    async def is_verified_check(ctx):
        user = await ctx.cog.bot.pg_con.fetch("SELECT * FROM vainz_roblox WHERE discord_id = $1", ctx.author.id)
        if not user:
            embed=discord.Embed(title="You're not verified yet.", description=f'<:warningerrors:713782413381075536> Please use `{ctx.prefix}verify` to verify.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            raise discord.ext.commands.CommandNotFound
        else:
            return True


    # @commands.check(is_verified)
    # @commands.is_owner()
    @commands.command()
    async def verify(self, ctx):
        """This commands allows you to verify with the bot."""
        def check(m):
            return m.author == ctx.author

        user = await self.bot.pg_con.fetch("SELECT * FROM vainz_roblox WHERE discord_id = $1", ctx.author.id)
        if user:
            embed=discord.Embed(title="You are already verified.", description=f'<:warningerrors:713782413381075536> Please use `{ctx.prefix}getroles` to get your roles.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return

        embed=discord.Embed(title="Prompt.", description=":question: What's your Roblox username?\n\nType **cancel** to cancel.", color=0x36393e)
        # embed.add_field(name=":question:", value="What's your Roblox username?\n\nType **cancel** to cancel.", inline=False)
        embed.set_footer(text="This prompt will automatically cancel in 200 seconds.")
        await ctx.send(embed=embed)

        try:
            roblox_name = await self.bot.wait_for('message', check=check, timeout=200)
        except:
            embed=discord.Embed(title="Prompt timed out.", description=f'<:warningerrors:713782413381075536> Please use `{ctx.prefix}{ctx.command}` to restart the prompt and try again.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return

        if roblox_name.content.upper() == "CANCEL":
            embed=discord.Embed(title="Prompt was terminated.", description=f'<:check:711530148196909126> Please use `{ctx.prefix}{ctx.command}` to restart the prompt.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return


        response = requests.get(url=f"https://api.roblox.com/users/get-by-username?username={roblox_name.content}")
        json_r = response.json()
        try:
            userID = json_r['Id']
        except KeyError:
            embed=discord.Embed(title="That account was not found.", description=f'<:warningerrors:713782413381075536> Please use `{ctx.prefix}{ctx.command}` to restart the prompt and try again.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return


        words = ['dog', 'car', 'oof', 'cat', 'bad', 'cool', 'fun', 'nice', 'play', 'roblox']

        word_one = random.choice(words)
        word_two = random.choice(words)
        word_three = random.choice(words)
        word_four = random.choice(words)
        word_five = random.choice(words)


        embed = discord.Embed(title="Prompt.", description=f':question: Hello, {roblox_name.content}! To confirm that you own this Roblox account, please go here: https://www.roblox.com/my/account and put this code on your **profile or status**:\n```{word_one} {word_two} {word_three} {word_four} {word_five}```\n\nsay **done** when done.\nsay **cancel** to cancel.', color=0x36393e)
        # embed.add_field(name=":question:", value=f"Hello, {roblox_name.content}! To confirm that you own this Roblox account, please go here: https://www.roblox.com/my/account and put this code on your **profile or status**:\n```{word_one} {word_two} {word_three} {word_four} {word_five}```\n\nsay **done** when done.\nsay **cancel** to cancel.")
        embed.set_footer(text="This prompt will automatically cancel in 200 seconds.")
        embed.set_image(url='https://cdn.discordapp.com/attachments/692517225558442065/696777741919584266/verify_help.png')
        await ctx.send(embed=embed)
        try:
            global wait_for_done
            wait_for_done = await self.bot.wait_for('message', check=check, timeout=200)
        except:
            embed=discord.Embed(title="Prompt timed out.", description=f'<:warningerrors:713782413381075536> Please use `{ctx.prefix}{ctx.command}` to restart the prompt and try again.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return

        if wait_for_done.content.upper() == "DONE":
            await wait_for_done.add_reaction('<a:loading:716280480579715103>')
            pass
        elif wait_for_done.content.upper() == "CANCEL":
            embed=discord.Embed(title="Prompt was terminated.", description=f'<:check:711530148196909126> Please use `{ctx.prefix}{ctx.command}` to restart the prompt.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return

        elif wait_for_done.content.upper() not in ["DONE", "CANCEL"]:
            embed=discord.Embed(title="Please provide a valid response: `done` or `cancel`.", description=f'<:warningerrors:713782413381075536> Please use `{ctx.prefix}{ctx.command}` to restart the prompt and try again.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return

        blrub_request = requests.get(url=f'https://www.roblox.com/users/{int(userID)}/profile')
        soup = BeautifulSoup(blrub_request.text, "html.parser")
        try:
            blurb = soup.find('div', {'class': 'profile-about-content'}).pre.span.text
        except AttributeError:
            await wait_for_done.clear_reactions()
            embed=discord.Embed(title="We could not find the code on your profile.", description=f'<:warningerrors:713782413381075536> Please use `{ctx.prefix}{ctx.command}` to restart the prompt and try again.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return

        status_request = requests.get(url=f'https://www.roblox.com/users/profile/profileheader-json?userId={int(userID)}')
        status_json = status_request.json()
        status = status_json["UserStatus"]

        if blurb == f"{word_one} {word_two} {word_three} {word_four} {word_five}" or status == f"{word_one} {word_two} {word_three} {word_four} {word_five}":
            pass
        else:
            await wait_for_done.clear_reactions()

            embed=discord.Embed(title="We could not find the code on your profile.", description=f'<:warningerrors:713782413381075536> Please use `{ctx.prefix}{ctx.command}` to restart the prompt and try again.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return

        group = await self.client.get_group(7115216)
        # user_obj = await self.client.get_user_by_id(userID)
        try:
            rank = await group.get_role_in_group(userID)
        except robloxapi.utils.errors.NotFound:
            await wait_for_done.clear_reactions()

            user = await self.bot.pg_con.execute("INSERT INTO vainz_roblox (discord_id, roblox_id) VALUES ($1, $2)", ctx.author.id, userID)
            embed=discord.Embed(title="You are not in the official group.", description=f"<:warningerrors:713782413381075536> Once you join the group you can use `{ctx.prefix}getroles` to get your roles.\nhttps://www.roblox.com/groups/7115216/HL2RP#!/about", color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return

        user = await self.bot.pg_con.execute("INSERT INTO vainz_roblox (discord_id, roblox_id) VALUES ($1, $2)", ctx.author.id, userID)

        role = discord.utils.get(ctx.guild.roles, name=rank.name)
        if not role:
            await wait_for_done.clear_reactions()

            embed=discord.Embed(title="No such role exists on this discord server.", description=f'<:warningerrors:713782413381075536> Please contact a server administrator and request that a role be created called `{rank.name}`.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return
        await wait_for_done.clear_reactions()

        verified = ctx.guild.get_role(733743233154416641)

        try:
            await ctx.author.add_roles(role, verified)
            await ctx.author.edit(nick=f'{roblox_name.content}')
        except discord.errors.Forbidden:
            embed=discord.Embed(title="I lack the permissions to change your roles.", description=f'<:warningerrors:713782413381075536> Please contact a server administrator and request that you get the `{rank.name}` role & your nickname be changed to `{roblox_name.content}`, verification was completed.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return
        embed=discord.Embed(title="Verification has been completed successfully.", description=f'<:check:711530148196909126> Please use `{ctx.prefix}help` to get a full list of commands.', color=0x36393E)
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
        await ctx.send(embed=embed)


    @commands.check(is_verified_check)
    @commands.command()
    async def delverify(self, ctx):
        """Deletes the verification binded to your discord ID."""

        await self.bot.pg_con.execute("DELETE FROM roblox WHERE discord_id = $1", ctx.author.id)

        embed=discord.Embed(title="Verification bind deleted successfully.", description=f"<:check:711530148196909126> Use `{ctx.prefix}verify` to reverify.", color=0x36393E)
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
        await ctx.send(embed=embed)
        return


    @commands.check(is_verified_check)
    @commands.command()
    async def getroles(self, ctx):
        """Updates users discord roleset to group rank."""
        wait_for_done = ctx.message
        await wait_for_done.add_reaction('<a:loading:716280480579715103>')
        user = await self.bot.pg_con.fetchrow("SELECT roblox_id FROM vainz_roblox WHERE discord_id = $1", ctx.author.id)

        user_obj = await self.client.get_user_by_id(user['roblox_id'])
        group = await self.client.get_group(7115216)
        verified = ctx.guild.get_role(733743233154416641)


        try:
            rank = await group.get_role_in_group(user['roblox_id'])
        except robloxapi.utils.errors.NotFound:

            rolelst = []
            for role in ctx.author.roles:
                rolelst.append(role)
            group_roles = await group.get_group_roles()
            for group_role in group_roles:
                try:
                    role = discord.utils.get(ctx.guild.roles, name=group_role.name)
                    if role in rolelst:
                        await ctx.author.remove_roles(role)
                except:
                    pass

            classD = ctx.guild.get_role(735524451378266174)
            await wait_for_done.clear_reactions()
            try:
                await ctx.author.add_roles(classD, verified)
                await ctx.author.edit(nick=f'{user_obj.name}')
            except discord.errors.Forbidden:
                await wait_for_done.clear_reactions()
                embed=discord.Embed(title="I lack the permissions to change your roles.", description=f'<:warningerrors:713782413381075536> Please contact a server administrator and request that you get the `{rank.name}` role & your nickname be changed to `{user_obj.name}`.', color=0x36393E)
                embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
                await ctx.send(embed=embed)
                return

            embed=discord.Embed(title="Oh no! You've left the official group.", description=f"<:warningerrors:713782413381075536> Once you rejoin the group you can use `{ctx.prefix}getroles` to get your roles.\nhlox.com/gttps://www.robroups/7115216/CMB-THE-UNIVERSAL-UNION#!/about\nFor now, I have given you the `{classD.name}` role.", color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return

        d_role = discord.utils.get(ctx.guild.roles, name=rank.name)
        if not d_role and rank.name == 'Development Team':
            d_role = discord.utils.get(ctx.guild.roles, name='Site Engineers')
            try:
                await ctx.author.edit(nick=f'{user_obj.name}')
            except discord.errors.Forbidden:
                await wait_for_done.clear_reactions()
                embed=discord.Embed(title="I lack the permissions to change your roles.", description=f'<:warningerrors:713782413381075536> Please contact a server administrator and request that you get the `{rank.name}` role & your nickname be changed to `{user_obj.name}`.', color=0x36393E)
                embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
                await ctx.send(embed=embed)
                return
        if not d_role:
            # await wait_for_done.clear_reactions()
            await wait_for_done.clear_reactions()
            embed=discord.Embed(title="No such role exists on this discord server.", description=f'<:warningerrors:713782413381075536> Please contact a server administrator and request that a role be created called `{rank.name}`.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return

        rolelst = []
        for role in ctx.author.roles:
            rolelst.append(role)
        if d_role in rolelst:
            group_roles = await group.get_group_roles()
            for group_role in group_roles:
                try:
                    role = discord.utils.get(ctx.guild.roles, name=group_role.name)
                    if role in rolelst:
                        await ctx.author.remove_roles(role)
                except:
                    pass
            # try:
            await ctx.author.add_roles(d_role)
            # except:
                # pass

            await wait_for_done.clear_reactions()
            embed=discord.Embed(title="No new group roles to add.", description=f'<:check:711530148196909126> Use `{ctx.prefix}help` to get a full list of roles.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return

        rolelst = []
        for role in ctx.author.roles:
            rolelst.append(role)
        group_roles = await group.get_group_roles()
        for group_role in group_roles:
            try:
                role = discord.utils.get(ctx.guild.roles, name=group_role.name)
                if role in rolelst:
                    await ctx.author.remove_roles(role)
            except:
                pass

        try:
            await ctx.author.add_roles(d_role, verified)
            await ctx.author.edit(nick=f'{user_obj.name}')
        except discord.errors.Forbidden:
            await wait_for_done.clear_reactions()
            embed=discord.Embed(title="I lack the permissions to change your roles.", description=f'<:warningerrors:713782413381075536> Please contact a server administrator and request that you get the `{rank.name}` role & your nickname be changed to `{user_obj.name}`.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return
        await wait_for_done.clear_reactions()
        embed=discord.Embed(title="Roles applied successfully.", description=f"<:check:711530148196909126> I've added `{d_role.name}` to your roleset.", color=0x36393E)
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
        await ctx.send(embed=embed)
        return


def setup(bot):
    bot.add_cog(Roblox(bot))
