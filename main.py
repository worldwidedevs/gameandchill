import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

bot = commands.Bot(command_prefix = '.')

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Game('Tinder with the boys'))
  print('Bot is online.')

@bot.command()
async def load(ctx, extension):
  bot.load_extension(f'cogs.{extension}')
  await ctx.send(f'Succesfully installed extension {extension}.')

@bot.command()
async def unload(ctx, extension):
  bot.unload_extension(f'cogs.{extension}')
  await ctx.send(f'Succesfully removed extension {extension}.')

@bot.command()
async def reload(ctx, extension):
  bot.unload_extension(f'cogs.{extension}')
  bot.load_extension(f'cogs.{extension}')
  await ctx.send(f'Succesfully reloaded extension {extension}.')

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(DISCORD_TOKEN)