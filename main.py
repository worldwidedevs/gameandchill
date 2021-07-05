import discord
import os
from discord.ext import commands
import random
# from cogs import *

bot = commands.Bot(command_prefix=(".", "br.", "eb.", "ww.", "ws."))

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

@bot.event
async def on_ready():
  activities = ["Tinder with the boys", "Flirting with the Snek", "Searching for suitable bunnies", "\"Dating Sims\""]
  activity = random.choice(activities)
  await bot.change_presence(activity=discord.Game(activity))

  guild_count = 0
  
  print("\n------")
  print("Logged in as {0}\n".format(bot.user.name))
    
  for guild in bot.guilds:
    guild_count = guild_count + 1
    
  print("Bot is in " + str(guild_count) + " guild(s)")

  for guild in bot.guilds:
    print(" + {0}".format(guild.name))
    
  print("\n------")

@bot.command()
async def load(ctx, extension):
  bot.load_extension(f"cogs.{extension.lower()}")
  await ctx.send(f"Succesfully installed extension {extension}.")

@bot.command()
async def unload(ctx, extension):
  bot.unload_extension(f"cogs.{extension.lower()}")
  await ctx.send(f"Succesfully removed extension {extension}.")

@bot.command()
async def reload(ctx, extension):
  bot.unload_extension(f"cogs.{extension.lower()}")
  bot.load_extension(f"cogs.{extension.lower()}")
  await ctx.send(f"Succesfully reloaded extension {extension}.")

for filename in os.listdir("./cogs"):
  if filename.endswith(".py"):
    bot.load_extension(f"cogs.{filename[:-3]}")
    print(f"cogs.{filename[:-3]} was loaded successfully")


bot.run(DISCORD_TOKEN)