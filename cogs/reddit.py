import nextcord as discord
from nextcord.ext import commands

from utils.functions import send_post

class Reddit(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @discord.slash_command(
    name="subreddit",
    description="view posts from any subreddit!",
  )
  async def slash_subreddit(
    self,
    inter: discord.Interaction,
    subreddit: str = discord.SlashOption(name="subreddit", description="The subreddit to view posts from")
  ):
    await send_post(inter=inter, author=inter.user, subreddit=subreddit)

  @commands.command(
    name="<subreddit>",
    brief="view posts from any subreddit!",
    help="r/<subreddit>"
  )
  async def _subreddit(self, ctx):
    """Function to create command. Actual command is executed through on_message event."""

def setup(bot):
  bot.add_cog(Reddit(bot))