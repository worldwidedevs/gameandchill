import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import random

bot = commands.Bot(command_prefix=(".", "br.", "eb.", "ww.", "ws."))

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
  activities = ["Tinder with the boys", "Flirting with the Snek", "Searching for suitible bunnies", "\"Dating\""]
  activity = random.choice(activities)
  await bot.change_presence(activity=discord.Game(activity))

  guild_count = 0
  
  print("Logged in as")
  print(bot.user.name)
  print("")
    
  for guild in bot.guilds:
    print("{0}".format(guild.name))
    guild_count = guild_count + 1
    
  print("Bot is in " + str(guild_count) + " guilds")
  print("")
  print("Startup complete!")
  print("------")

@bot.command()
async def load(ctx, extension):
  bot.load_extension(f"cogs.{extension}")
  await ctx.send(f"Succesfully installed extension {extension}.")

@bot.command()
async def unload(ctx, extension):
  bot.unload_extension(f"cogs.{extension}")
  await ctx.send(f"Succesfully removed extension {extension}.")

@bot.command()
async def reload(ctx, extension):
  bot.unload_extension(f"cogs.{extension}")
  bot.load_extension(f"cogs.{extension}")
  await ctx.send(f"Succesfully reloaded extension {extension}.")

for filename in os.listdir("./cogs"):
  if filename.endswith(".py"):
    bot.load_extension(f"cogs.{filename[:-3]}")


bot.run(DISCORD_TOKEN)