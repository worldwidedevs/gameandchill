import discord
from discord.ext import commands, tasks
import random

class Battle_Royale(commands.Cog):

  game_running = False
  Memberlist = []
  podium = []
  member_count = len(Memberlist)

  sentlove = False

  def __init__(self, bot):
    self.bot = bot

  # Test for cog interaction
  @commands.command(pass_context=True)
  async def give_ehre(self, ctx):
    self.bot.ehrenbank.add_ehre(ctx, ctx.author, 5)

  # Podium
  @commands.command(pass_context=True)
  async def brpodium(self, ctx):
    rank_count = self.member_count
    await ctx.send('Podium:')
    for player in self.podium:
      await ctx.send(f'{player.mention} is placed #{rank_count}')
      rank_count -= 1

  # Disqualifizieren
  @commands.command(pass_context=True)
  async def brdisqualify(self, ctx):
    mentions = ctx.message.mentions
    for member in mentions:
      await ctx.send(f'{member.mention} has been disqualified.')
      self.podium.append(member)
      self.Memberlist.remove(member)

  # Create new Game
  @commands.command(pass_context=True)
  async def newbr(self, ctx):
    self.game_running = False
    self.Memberlist = []
    await ctx.send('Please say .joinbr if you want to join the game.')
    await ctx.send('The game will start if there are at least 10 players.')

  # Join the Game
  @commands.command(pass_context=True)
  async def joinbr(self, ctx):
    if self.game_running == True:
      await ctx.send('The Game is already running and nobody can join anymore.')
      return
    if ctx.author not in self.Memberlist:
      self.Memberlist.append(ctx.author)
      self.member_count = len(self.Memberlist)
      await ctx.message.add_reaction('✅')
      print(f'{ctx.author} joined the game.')
    else:
      await ctx.send('You are already in the game.')

  # Send Playerlist
  @commands.command(pass_context=True)
  async def brplayerlist(self, ctx):
    for member in self.Memberlist:
      await ctx.send(member)

  # Start the Game
  @commands.command(aliases=['sbr','start br','start battle royale'], pass_context=True)
  async def start_battle_royale(self, ctx):
    self.game_running = True
    await ctx.send('Starting a new Battle Royale! Better be prepared ;D')
    self.start_random_event.start(ctx)

  # Get random event daily
  @tasks.loop(hours=24)
  async def start_random_event(self, ctx):
    eventlist = [
      ['Marriage','The Chosen users have to chat everyday from now on for the next week.'],
      ['Event2','If the loved one is in a call, the victim shall join after a maximum of 30min.']
      ]
    random_event = random.choice(eventlist)
    await ctx.send('The Event has been chosen:')
    embed=discord.Embed(title=random_event[0], description=random_event[1], color=0x70dbff)
    await ctx.send(embed=embed)
    func = getattr(self, 'event_' + random_event[0].lower())
    await func(ctx)
  
  # All Events____________________________________________________________________________
  async def event_marriage(self, ctx):
    # pick 2 random users
    partner1 = random.choice(self.MemberList)
    self.MemberList.remove(partner1)
    partner2 = random.choice(self.MemberList)
    self.marriage.start(ctx, partner1, partner2)

  @tasks.loop(hours=24)
  async def marriage(self, ctx, partner1, partner2):
    if self.sentlove == False:
      await ctx.send('You have failed in your marriage and are now disqualified.')
      self.podium.append(partner1)
      self.Memberlist.remove(partner1)
      self.podium.append(partner2)
      self.Memberlist.remove(partner2)
    else:
      self.sentlove = False
  
  async def event_event2(self, ctx):
    await ctx.send('Event 2 triggered.')


def setup(bot):
  bot.add_cog(Battle_Royale(bot))