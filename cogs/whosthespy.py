import discord
from discord.ext import commands, tasks
import random
import os
import sys
import typingimport discord
from discord.ext import commands, tasks
import random
import os
import sys
import typing

class Whos_the_Spy(commands.Cog, name="Who's the Spy (ws.[command])"):
  
  gamerunning = False
  thumbsup = 1
  thumbsdown = 1
  spy = None
  membercount = None
  location = None

  locations = [
    ["Restaurant","https://i.ibb.co/0qkC1Zm/restaurant-wts.jpg", # 7 Roles
    "Manager","Restaurant Critic","Waiter","Pianist","Guest","Wine Waiter","Kitchen Assistant"],
    ["Casino","https://i.ibb.co/7r4DZzR/casino-wts.jpg", # 8 Roles !eine fehlt noch
    "Cheater","Security Guard","Barkeeper","Dealer","Bouncer","Groupier","Escort Lady","Manager"],
    ["Beach","https://i.ibb.co/j645RYh/beach-wts.jpg", # 7 Roles
    "Thief","Beach Vendor (Strandverkäufer)","Vacationer (Urlauber)","Lifeguard","Surfer","Diver","Animator"],
    ["Luxury Yacht","https://i.ibb.co/3YqN28b/yacht-wts.jpg", # 10 Roles
    "Passanger","Captain","Cook","Cleaning Member","Receptionist","Sailor","Barkeeper","Tour Guide","Steward","Musician"],
    ["Submarine","https://i.ibb.co/rvmhDGv/submarine-wts.jpg", # 5 Roles
    "Electrician","Captain","Sailor","Security Guard","Weapons Manager","Cook"],
    ["University","https://i.ibb.co/Bgj2HgH/university-wts.jpg", # 8 Roles
    "Tutor","College Student","Librarian","Psychologist","Dean (Dekan)","Professor","Student Advisor (Studienberater)","Visitor"],
    ["Embassy", "https://ibb.co/YDf56nj", # 7 Roles
    "Refugee (Flüchtling)","Tourist","Security Guard","Diplomat","Secretary","Chauffeur","Ambassador"],
    ["Wellness Temple","", # 7 Roles
    "Stylist","Cosmetician (Kosmetiker)","Guest","Hairdresser (Friseur)","Masseur","Manicurist (Nageldesigner)","Cleaning Person (Reinigungskraft)"],
    ["Hotel","", # 7 Roles
    "Barkeeper","Guest","Bellhop (Page)","Doorman (Portier)","Manager","Maid (Zimmermädchen)","Receptionist"],
    ["Hospital","", # 7 Roles
    "Nurse (Krankenschwester)","Patient","Male Nurse (Pfleger)","Pathologist","Internist","Assistant Doctor (Assistenzarzt)","Surgeon (Chirurg)"],
    ["Workshop","", # 7 Roles
    "Car Mechanic (KFZ-Mechaniker)","Executive Director (Geschäftsführer)","Receptionist (Empfangsdame)","Service Engineer (Servicetechniker)","Spengler","Biker","Motorist (Autofahrer)"]
  ]

  def __init__(self, bot):
    self.bot = bot

  def geterror(self, e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return exc_type, fname, exc_tb.tb_lineno

  def delkeys(self):
    gamerunning = False
    thumbsup = 1
    thumbsdown = 1
    spy = None
    membercount = None
    location = None

  @commands.command(pass_context=True)
  async def play(self, ctx, debug: typing.Optional[str] = None):
    if ctx.prefix != "ws.": return
    elif self.gamerunning == True: return
    channel_id = str(ctx.channel.id)
    
    text = ""
    for location in self.locations:
      if self.locations.index(location) == len(self.locations)-1:
        location = location[0]
        text = text + location + "."
      else:
        location = location[0]
        text = text + location + ", "

    author = ctx.author
    try:
      voice_channel = author.voice.channel.id
      voice_members = author.voice.channel.members
    except AttributeError:
      await ctx.send("You can only start a game while you're on a server, in a voice channel together with your friends.")
      return

    print(voice_members)
    
    for member in voice_members: # Bot im Channel -> removen
      if member.bot == True:
        voice_members.remove(member)

    await ctx.send("Starting the game! You'll be receiving your roles via DM shortly.")
    print(voice_members)
    self.membercount = len(voice_members)

    max_players = len(self.locations[0])-2
    if debug != "debug":
      if  self.membercount > max_players:
        await ctx.send(f"The maximum amount of players is {max_players}.")
        return
      elif self.membercount < 4:
        await ctx.send("The minimum amount of players is 4.")
        return              

    roleset = random.choice(self.locations)
    location = roleset[0]
    self.location = location
    roleset.remove(location)
    image = roleset[0]
    roleset.remove(image)
    spy = random.randint(0,self.membercount-1)

    # Direct messages to members
    for member in voice_members:
      try:
        if voice_members.index(member) == spy:
          channel = await member.create_dm()
          self.spy = member
          embed=discord.Embed(title="Who's the Spy?", description="A new game has started! Here's your role:", color=0xffe600)
          embed.add_field(name="Location", value="Find it out", inline=True)
          embed.add_field(name="Role", value="Spy", inline=True)
          embed.add_field(name="Possible locations", value=text, inline=False)
          embed.set_footer(text="Type .guess [location] in the server channel where you started the game to guess the location.")
          await channel.send(embed=embed)
        else:
          role = random.choice(roleset)
          roleset.remove(role)
          channel = await member.create_dm()
          embed=discord.Embed(title="Who's the Spy?", description="A new game has started! Here's your role:", color=0xffe600)
          embed.set_thumbnail(url=image)
          embed.add_field(name="Location", value=location, inline=True)
          embed.add_field(name="Role", value=role, inline=True)
          embed.set_footer(text="Type .vote [user] in the server channel where you started the game to vote out the spy.")
          await channel.send(embed=embed)
      except Exception as e:
        await ctx.send("The DM couldn't be sent to everyone. Check if someone blocked the bot.")
        print(f"Exception while sending DMs - {e} - Details: {self.geterror(e)}")
        return

    await ctx.send(f"**The game starts now!** We're starting with: {random.choice(voice_members).mention}. Ask someone a question!")


  @commands.command(pass_context=True)
  async def vote(self, ctx):
    if ctx.prefix != "ws.": return
    elif self.gamerunning == True: return
    channel_id = str(ctx.channel.id)

    mentioned = ctx.message.mentions[0]

    voting = await ctx.send(f"{ctx.author.mention} voted for {mentioned.mention}. React to vote with 👍 or 👎.")
    await voting.add_reaction("👍")
    await voting.add_reaction("👎")
    voting = await ctx.channel.fetch_message(voting.id)

    @commands.event
    async def on_reaction_add(reaction, user):
      channel_id = str(ctx.channel.id)
      
      if user.id == mentioned.id:
        return
      if reaction.message.id != voting.id:
        return
      elif reaction.emoji == "👍":
        self.thumbsup += 1
      elif reaction.emoji == "👎":
        self.thumbsdown += 1

      if self.thumbsdown >= 2:
        await ctx.send("Voting failed.")
        await voting.delete()
      elif self.thumbsup >= self.membercount:
        if mentioned.id == self.spy:
          await ctx.send(f"{self.spy.mention} was the spy!\nThe Crew wins!")
          await voting.delete()
          self.delkeys()
        else:
          await ctx.send(f"{mentioned.mention} was not the spy! The real spy was {self.spy.mention}.")
          await voting.delete()
          self.delkeys()

  @commands.command(pass_context=True)
  async def guess(self, ctx, guessed_location):
    if ctx.prefix != "ws.": return
    elif self.gamerunning == True: return
    channel_id = str(ctx.channel.id)

    location = self.location

    if ctx.author == self.spy:
        if guessed_location.lower() != location.lwer():
            await ctx.send(f"**{guessed_location} is not right!** The real location was {location}. The crew wins!")
            self.delkeys()
        else:
            await ctx.send(f"**{guessed_location} is right!** The spy wins!")
            self.delkeys()


def setup(bot):
  bot.add_cog(Whos_the_Spy(bot))