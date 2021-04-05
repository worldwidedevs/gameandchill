import discord
from discord.ext import commands, tasks
import random

class Battle_Royale(commands.Cog, name="Battle Royale (br.[command])"):

  game_running = False
  memberlist = []
  podiumlist = []
  member_count = len(memberlist)

  sentlove = False

  def __init__(self, bot):
    self.bot = bot

  '''
  # Test for cog interaction
  @commands.command(pass_context=True)
  async def give_ehre(self, ctx):
    await self.bot.cogs["Ehrenbank"].add_ehre(ctx)
  '''

  async def kick(self, ctx, users):
    for user in users:
      await ctx.send(f"{user.mention} has been disqualified.")
      self.memberlist.remove(user)
      self.podiumlist.append(user)

  # Podium
  @commands.command(pass_context=True)
  async def podium(self, ctx):
    if ctx.prefix != "br.": return

    rank_count = self.member_count
    await ctx.send("Podium:")
    for player in self.podiumlist:
      await ctx.send(f"{player.mention} is placed #{rank_count}")
      rank_count -= 1

  # Disqualifizieren
  @commands.command(pass_context=True)
  async def disqualify(self, ctx):
    if ctx.prefix != "br.": return

    mentions = ctx.message.mentions
    await self.kick(ctx, mentions)

  # Create new Game
  @commands.command(pass_context=True)
  async def newbr(self, ctx):
    # if ctx.prefix != "br.": return

    self.game_running = False
    self.memberlist = []
    await ctx.send("Please use br.join if you want to join the game.")
    await ctx.send("The game will start if there are at least 10 players.")

  # Join the Game
  @commands.command(aliases=["join_battleroyale","join_battle royale"],pass_context=True)
  async def join_br(self, ctx):
    # if ctx.prefix != "br.": return

    if self.game_running == True:
      await ctx.send("The Game is already running and nobody can join anymore.")
      return
    if ctx.author not in self.memberlist:
      self.memberlist.append(ctx.author)
      self.member_count = len(self.memberlist)
      await ctx.message.add_reaction("✅")
      print(f"{ctx.author} joined the game.")
    else:
      await ctx.send("You are already in the game.")

  # Send Playerlist
  @commands.command(pass_context=True)
  async def playerlist(self, ctx):
    if ctx.prefix != "br.": return

    for member in self.memberlist:
      await ctx.send(member)

  # Start the Game
  @commands.command(pass_context=True)
  async def start_br(self, ctx):
    if ctx.prefix != "br.": return

    self.game_running = True
    await ctx.send("Starting a new Battle Royale! Better be prepared ;D")
    self.start_random_event.start(ctx)

  # Get random event daily
  @tasks.loop(hours=24)
  async def start_random_event(self, ctx):
    eventlist = [
      ["Marriage","The Chosen users have to chat everyday from now on for the next week."],
      ["Event2","If the loved one is in a call, the victim shall join after a maximum of 30min."]
      ]
    random_event = random.choice(eventlist)
    await ctx.send("The Event has been chosen:")
    embed=discord.Embed(title=random_event[0], description=random_event[1], color=0x70dbff)
    await ctx.send(embed=embed)
    func = getattr(self, "event_" + random_event[0].lower())
    await func(ctx)
  
  # All Events____________________________________________________________________________
  async def event_marriage(self, ctx):
    partner1 = random.choice(self.memberlist)
    self.memberlist.remove(partner1)
    partner2 = random.choice(self.memberlist)
    self.marriage.start(ctx, partner1, partner2)

  @tasks.loop(hours=24)
  async def marriage(self, ctx, partner1, partner2):
    if self.sentlove == False:
      await ctx.send("You have failed in your marriage and are now disqualified.")
      await self.kick(ctx, [partner1, partner2])
    else:
      self.sentlove = False
  
  async def event_event2(self, ctx):
    await ctx.send("Event 2 triggered.")


def setup(bot):
  bot.add_cog(Battle_Royale(bot))