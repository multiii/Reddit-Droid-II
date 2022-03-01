import nextcord as discord
from nextcord.ext import commands, tasks

from utils.functions import get_numbers_from_str, get_reddit_token, send_post

class Events(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # Tasks

  @tasks.loop(hours=2)
  async def update_reddit_token(self):
    TOKEN, headers = get_reddit_token()

    self.bot.reddit_token = TOKEN
    self.bot.reddit_headers = headers

  # Listeners

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandNotFound):
      return

    raise error

  @commands.Cog.listener()
  async def on_message(self, msg: discord.Message):
    if msg.author.bot or msg.content == "":
      return

    ctx = await self.bot.get_context(msg)
    prefix = ctx.prefix

    if prefix is None:
      return
    
    args = msg.content.lower().split()

    if get_numbers_from_str(prefix) == str(self.bot.user.id):
      subreddit = args[1].strip()

    else:
      subreddit = args[0].split(prefix)[1].strip()

    if self.bot.get_command(subreddit) is None:
      await send_post(ctx=ctx, author=msg.author, subreddit=subreddit)      

def setup(bot):
  bot.add_cog(Events(bot))