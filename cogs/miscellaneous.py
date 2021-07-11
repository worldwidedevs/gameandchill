import discord
from discord.ext import commands, tasks
import random
import os
import sys
import typing
from typing import Optional


class Miscellaneous(commands.Cog, name="Miscellaneous (misc.[command])"):

  def __init__(self, bot) -> None:
    self.bot = bot
    self.guild = None
    self.afkchannel = None
    self.temp_category = None
    self.bot_log_channel = None

  # --------SETUP-----------

  @commands.command(pass_context=True)
  async def setup(self, ctx):
    if self.guild is None:
      self.guild = ctx.guild
    if ctx.guild.afk_channel is not None:
      self.afkchannel = ctx.guild.afk_channel
      if len(self.afkchannel.members) == 0:
        await self.afkchannel.set_permissions(self.guild.default_role, view_channel=False)
      await ctx.send("Setup done!")
    else:
      await ctx.send("Setup done! If you eventually create an afk channel, think about running this command again ^^")

  @commands.command(aliases=["sc", "setcategory"], pass_context=True)
  async def set_category(self, ctx):
    if ctx.message.author.guild_permissions.administrator:
      self.temp_category = ctx.channel.category
      await ctx.send("Category set as temporary category.")
    else:
      await ctx.send("This command can only be used by an Administrator.")

  @commands.command(aliases=["clog", "log"], pass_context=True)
  async def create_bot_log_channel(self, ctx):
    if ctx.message.author.guild_permissions.administrator:
      self.bot_log_channel = await self.temp_category.create_text_channel("Bot Log Channel", reason=None)
      await ctx.send("Created logging channel.")
    else:
      await ctx.send("This command can only be used by an Administrator.")
      return
    
    await self.bot_log_channel.set_permissions(ctx.guild.default_role, send_messages=False)

  # --------TEMPORARY VOICE CHANNELS-----------

  @commands.command(aliases=["cvc", "createvc"], pass_context=True)
  async def create_voice_channel(self, ctx, channelname, userlimit: Optional[int]=None):
    if self.temp_category is None:
      await ctx.send("An Admin needs to set the category before you can create t]emporary channels in it.")
      await ctx.send("Use the command '.setcategory' aka '.sc' in the wished category to make that happen.")
      return

    useramount = len(ctx.message.mentions)
    rolementions = len(ctx.message.role_mentions)

    created_vc = await self.temp_category.create_voice_channel(str(channelname), reason=None)

    if ctx.author.voice:
      await ctx.author.move_to(created_vc)

    private = False

    if useramount != 0:
      private = True
      userlist = ctx.message.mentions
      await created_vc.set_permissions(ctx.guild.default_role, view_channel=False)
      await created_vc.set_permissions(ctx.author, view_channel=True)
      for user in userlist:
        await created_vc.set_permissions(user, view_channel=True)

    if rolementions != 0:
      private = True;
      rolelist = ctx.message.role_mentions
      await created_vc.set_permissions(ctx.guild.default_role, view_channel=False)
      await created_vc.set_permissions(ctx.author, view_channel=True)
      for role in rolelist:
        await created_vc.set_permissions(role, view_channel=True)

    if userlimit is not None:
      if userlimit > 99:
        await ctx.send("The maximum userlimit for a voice channel is 99.")
      else:
        await created_vc.edit(user_limit = userlimit)

    if private == True:
        await ctx.message.delete()

  @commands.command(aliases=["avc", "appendvc"], pass_context=True)
  async def append_voice_channel(self, ctx):
    if ctx.message.author.voice is None:
      await ctx.send("You must be in a voice channel to use this command.")
      await ctx.message.delete()
      return
    targets = ctx.message.mentions
    if len(targets) == 0:
      await ctx.send("You have to ping someone for this command to work.")
      return
    channel = ctx.message.author.voice.channel
    if channel is None:
      await ctx.send("You have to be in the voice channel to use this command.")
      return
    for user in targets:
      await channel.set_permissions(user, view_channel=True)

    await ctx.message.delete()

  @commands.command(aliases=["dvc", "detachvc"], pass_context=True)
  async def detach_voice_channel(self, ctx):
    if ctx.message.author.voice is None:
      await ctx.send("You must be in a voice channel to use this command.")
      await ctx.message.delete()
      return
    targets = ctx.message.mentions
    if len(targets) == 0:
      await ctx.send("You have to ping someone for this command to work.")
      return
    channel = ctx.message.author.voice.channel
    if channel is None:
      await ctx.send("You have to be in the voice channel to use this command.")
      return
    for user in targets:
      await channel.set_permissions(user, view_channel=False)

    await ctx.message.delete()

  # --------LISTENERS-----------

  @commands.Cog.listener()
  async def on_message(self, message):

    # --------FUCK THIS BOT-----------

    if "fuck this bot" in str(message.content).lower():
      await message.author.send("Fuck you, buddy")
      await message.author.send("https://tenor.com/view/no-u-reverse-card-anti-orders-gif-19358543")

  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):

    # --------DELETE TEMPORARY CHANNELS-----------

    if before.channel is not None:
      if before.channel.category == self.temp_category:
        if len(before.channel.members) == 0:
          await before.channel.delete()

    # --------TEMPORARILY HIDE AFK CHANNELS-----------

    if self.afkchannel is not None:
      if before.channel == self.afkchannel:
        if len(self.afkchannel.members) == 0:
          await self.afkchannel.set_permissions(self.guild.default_role, view_channel=False)
      else:
        if after.channel == self.afkchannel:
          await self.afkchannel.set_permissions(self.guild.default_role, view_channel=True)

    
    @commands.Cog.listener()
    async def on_member_join(self, member):
      dj_role = discord.utils.get(self.guild.roles, name="DJ")
      await member.add_roles(dj_role)
      await member.send_message("Hello, I'm the private Bot of the Game & Chill Server. Hope you enjoy your stay.")
      await member.send_message("If you want to know about my features, hit me up with '.help'.")
    

  # --------REMOVE ROLE-----------

  @commands.command(aliases=["rr", "removerole", "deleterole"], pass_context=True)
  async def remove_role(self, ctx, rolename):
    role = discord.utils.get(ctx.guild.roles, name=rolename)
    await ctx.author.remove_roles(role, reason=None)
    await self.bot_log_channel.send("{0} has been removed from {1}.".format(rolename, ctx.author))

  # --------ANNOUNCE UPDATE(WIP)-----------

  """
  @commands.command(aliases=["update","announceupdate","au"], pass_context=True)
  async def announce_update(self, ctx):
    # das bitte in slash command umwandeln

    embed = discord.Embed(title="Title", description="Description", color=0x3fc3e4)
    #embed.set_author(name="Author Name", url="https://Authors Link", icon_url="https://Authors Icon")
    #embed.set_thumbnail(url="https://Icon")
    embed.add_field(name="Category 1", value="Value Cat 1", inline=False)
    embed.set_footer(text="Footer text")
    await ctx.send(embed=embed)
  """

  # --------EQUAL CHANGE NICKNAME-----------
  # sadly does only not work for the owner :sob:

  @commands.command(aliases=["cn", "changename"], pass_context=True)
  @commands.bot_has_permissions(manage_nicknames=True)
  async def change_nickname(self, ctx, new_name):
    if len(new_name) >= 32:
      await ctx.send("Due to Discord's rules, the nickname can't be longer than 32 characters.")
      return

    if len(ctx.message.mentions) == 0:
        target = ctx.message.author
    else:
        target = ctx.message.mentions[0]

    if target == self.guild.owner:
      await ctx.send("Due to Discord's rules, I can't change the nickname of the server owner.")
      return

    await ctx.send("Changed Nickname from {0} to **{1}**.\nRequested by {2}.".format(target.nick, new_name, ctx.author.mention))

    # send in Logs channel
    if self.bot_log_channel is not None:
      await self.bot_log_channel.send("{0} changed nickname from **{1}** to **{2}** for {3}.".format(ctx.author.mention, target.nick, new_name, target.mention))

    await target.edit(nick=new_name)

    await ctx.message.delete()

  # --------COUNTABLE ROLES-----------

  """
  @commands.command(aliases=["scr", "setrole"], pass_context=True)
  async def set_countable_role(self, ctx, role):
    new_name = "Opossum Count: " + str(self.countable_roles)
    await role.edit(name=new_name)
  """

  # IDEEN:
  # Beim Umbenennen per Befehl, kann man für 5 EHRE (pro Buchstabe) anonym umbenennen
  # semi-automate quoting channel -> complicated/weird for users
  # countable roles -> hard to do

  # assign dj role on join -> done

def setup(bot):
    bot.add_cog(Miscellaneous(bot))