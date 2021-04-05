import discord
from discord.ext import commands, tasks
import random

class Ehrenbank(commands.Cog):

  Kontos = []

  def __init__(self, bot):
    self.bot = bot
  
  def add_ehre(self, ctx, user, amount):
    ctx.send(f'{amount}Ehre has been added to {user}s Konto') # Ehre zu users Konto adden
  
  @commands.command(pass_context=True)
  async def claim(self, ctx):
    self.add_ehre(ctx, ctx.author, 5)
  


def setup(bot):
  bot.add_cog(Ehrenbank(bot))