import discord
from discord.ext import commands, tasks
import random
import os
import sys
import typing

class Miscellaneous(commands.Cog, name="Miscellaneous (misc.[command])"):

  created_vc = None

  # @commands.command(aliases=["setv"])

  @commands.command(aliases=["cvc","createvc"], pass_context=True)
  async def create_voice_channel(self, ctx):
    useramount = len(ctx.message.mentions)
    # take channel name from context
    
    created_vc = await create_voice_channel(ctx.message, reason=None, category="859483668816068608")
    if useramount == 0:
      pass
      #channel öffentlich
    else:
      pass
      #channel privat
      userlist = ctx.message.mentions
    await ctx.delete() 

  if (created_vc.members = 0):
    await created_vc.delete()

# await create_role(*, reason=None, **fields)


# .cvc Große Versammlung @Lewd Firefox @Oleex @Vince Voyeur sitzt am Stoyeur -> privat auf Rolle für gepingte members
# .cvc Große Versammlung -> öffentlich