import discord
from discord.ext import commands, tasks
import random
import os
import sys
import typing

class Miscellaneous(commands.Cog, name="Miscellaneous (misc.[command])"):

  def __init__(self, bot):
    self.bot = bot
    self.temp_channel = self.bot.get_channel(859483668816068608)
    self.guild = self.bot.get_guild(792840014152466432)
    self.created_vc = None       
    self.temp_category = None    # Paul guck hier mal drüber, bin mir unsicher, aber discordserver
  # hat gesagt ich soll das so ungefähr machen (hab aber nicht durchgeblickt), siehe Zeile 55
  # ich sollte irgendwas mit bot.temp_category = ... machen oder so, ganz weird
  # folgendes sollte ich machen:
  """
  Need to keep track of a variable between functions? No problem!

  :warning: Careful what you name it though, else you might overwrite something :warning: 

  Just add it to your commands.Bot or discord.Client instance like so:
  bot = commands.Bot(...)
  bot.my_variable = 0

  async def foo():
      bot.my_variable += 1

  # In a cog
  @commands.command()
  async def counter(self,ctx):
      await ctx.send("Current Counter is at {}".format(ctx.bot.my_variable))

  This also allows you to access this from other cogs/extensions/functions. Anywhere you have access to the bot instance
  """

  @commands.command(aliases=["cvc","createvc"], pass_context=True)
  async def create_voice_channel(self, ctx, channelname):
    # global temp_category

    useramount = len(ctx.message.mentions)
    rolementions = len(ctx.message.role_mentions)
    self.temp_category = ctx.message.channel.category

    created_vc = await self.temp_category.create_voice_channel(str(channelname), reason=None)
    # await ctx.send("Created channel '{0}'".format(str(channelname)))

    if ctx.author.voice:
      await ctx.author.move_to(created_vc)


    private = False

    if useramount != 0:
      private = True;
      userlist = ctx.message.mentions
      await created_vc.set_permissions(ctx.guild.default_role, view_channel=False)
      for user in userlist:
        await created_vc.set_permissions(user, view_channel=True)

    if rolementions != 0:
      private = True;
      rolelist = ctx.message.role_mentions
      await created_vc.set_permissions(ctx.guild.default_role, view_channel=False)
      for role in rolelist:
        await created_vc.set_permissions(role, view_channel=True)

    if private == True:
      await ctx.message.delete()

  
  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    #if temp_category == None:
     # return

    if before.channel != None:
      if before.channel.category == self.temp_category:
        if len(before.channel.members) == 0:
          await before.channel.delete()


  @commands.Cog.listener()
  async def on_message(self, message):
    if "fuck this bot" in str(message.content).lower():
      await message.author.send("Fuck you, buddy")
      await message.author.send("https://tenor.com/view/backyardigans-tpose-spinning-spin-3d-gif-20282400")

  @commands.command(aliases=["rr","removerole","deleterole"], pass_context=True)
  async def remove_role(self, ctx, rolename):
    role = discord.utils.get(ctx.guild.roles, name=rolename)
    await ctx.author.remove_roles(role, reason=None)  

  @commands.command(aliases=["update","announceupdate","au"], pass_context=True)
  async def announce_update(self, ctx):
    # das bitte in slash command umwandeln

    embed = discord.Embed(title="Title", description="Description", color=0x3fc3e4)
    #embed.set_author(name="Author Name", url="https://Authors Link", icon_url="https://Authors Icon")
    #embed.set_thumbnail(url="https://Icon")
    embed.add_field(name="Category 1", value="Value Cat 1", inline=False)
    embed.set_footer(text="Footer text")
    await ctx.send(embed=embed)


def setup(bot):
  bot.add_cog(Miscellaneous(bot))