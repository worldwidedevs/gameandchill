import discord
from discord.ext import commands, tasks
import random

class Whos_the_Spy(commands.Cog, name="Who's the Spy (ws.[command])"):

  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(pass_context=True)
  async def play(self, ctx):
    if ctx.prefix != "ws.": return

    self.add_ehre(ctx, ctx.author, 5)
  


def setup(bot):
  bot.add_cog(Whos_the_Spy(bot))