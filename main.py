import os
from threading import Thread

import nextcord as discord
from nextcord.ext import commands
from flask import Flask

from utils.functions import get_prefix
from utils.pagination import Embed

bot = commands.Bot(
  case_insensitive=True,
  command_prefix=get_prefix,
  intents=discord.Intents.all()
)

@bot.event
async def on_ready():
  print("Ready!")

  bot.Embed = Embed
  bot.menus = {}

  bot.get_cog("Events").update_reddit_token.start()

for filename in os.listdir("./cogs"):
  if filename.endswith(".py"):
    bot.load_extension(f"cogs.{filename[:-3]}")

app = Flask('')

@app.route('/')
def home():
    return "Hello"

def run():
  app.run(host='0.0.0.0', port=8080)

t = Thread(target=run)
t.start()

bot.run(os.getenv("TOKEN"))