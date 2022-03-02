import nextcord as discord
from nextcord.ext import commands, tasks

import check
from utils import resources
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

  # Commands

  @commands.command(name="aeval", brief="eval async functions!")
  @check.has_user_id(394320584089010179)
  async def _aeval(self, ctx, *, exp):
    try:
      resp = await eval(exp)

      await resources.default.embed(
        msg=ctx.message,
        title="Code evaluted!",
        description=f"```py\n{resp}\n```"
      )

    except Exception as err:
      await resources.error.embed(
        msg=ctx.message,
        title="ERROR!",
        description=f"```py\n{err}\n```"
      )

  @commands.command(name="eval", brief="eval normal functions!")
  @check.has_user_id(394320584089010179)
  async def _eval(self, ctx, *, exp):
    try:
      resp = eval(exp)

      await resources.default.embed(
        msg=ctx.message,
        title="Code evaluted!",
        description=f"```py\n{resp}\n```"
      )

    except Exception as err:
      await resources.error.embed(
        msg=ctx.message,
        title="ERROR!",
        description=f"```py\n{err}\n```"
      )

def setup(bot):
  bot.add_cog(Events(bot))