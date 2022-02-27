import os
import random
import requests
from typing import Dict, Union

import nextcord as discord
from nextcord.ext import commands
from tinydb import TinyDB, Query

from utils import resources, views
from utils.storage import YAMLStorage

User = Query()

db = TinyDB("database.yaml", storage=YAMLStorage)

pr = db.table("prefix")


def get_prefix(bot, message):
    if message.guild is None:
        return commands.when_mentioned_or("r/")(bot, message)

    if not bool(pr.get(User.id == message.guild.id)):
        return commands.when_mentioned_or("r/")(bot, message)

    return commands.when_mentioned_or(pr.get(User.id == message.guild.id)["prefix"])(bot, message)


def clean_none(arg, datatype: type = str) -> str:
    match = {str: "", int: 0, bool: False}

    if arg is None:
        return match[datatype]
    return arg


def get_numbers_from_str(string: str):
    new_string = ""

    for char in string:
        if ord(char) >= 48 and ord(char) <= 57:
            new_string += char

    return new_string


def get_reddit_token():
    app_id = os.getenv("RedditAppID")
    secret = os.getenv("RedditSecret")

    auth = requests.auth.HTTPBasicAuth(app_id, secret)

    reddit_username = 'Multi_76'
    reddit_password = os.getenv("RedditPassword")

    data = {
        'grant_type': 'password',
        'username': reddit_username,
        'password': reddit_password
    }

    headers = {'User-Agent': 'Tutorial2/0.0.1'}

    res = requests.post(
        'https://www.reddit.com/api/v1/access_token',
        auth=auth,
        data=data,
        headers=headers
    )

    return res.json()['access_token'], headers


def get_post(subreddit: str, bot: commands.Bot) -> Dict:
    headers = {**bot.reddit_headers, **
               {'Authorization': f"bearer {bot.reddit_token}"}}

    res = requests.get(
        f'https://oauth.reddit.com/r/{subreddit}/hot.json?sort=new&limit=100', headers=headers).json()
    print(len(res['data']['children']))

    post_dict = random.choice(res['data']['children'])['data']

    return resources.Post(**post_dict)


def get_comment(url: str, index: int, bot: commands.Bot):
    headers = {**bot.reddit_headers, **
               {'Authorization': f"bearer {bot.reddit_token}"}}

    res = requests.get(url, headers=headers).json()

    post_dict = res[0]["data"]["children"][0]["data"]
    comment_dict = res[1]["data"]["children"][index]["data"]

    return resources.Post(**post_dict), resources.Comment(**comment_dict)


def get_selftext_page(selftext: str, page: int = 0) -> str:
    if selftext == "":
        return ""

    if len(selftext) <= 1750:
        return selftext

    description = selftext[1750 * page: 1750 * (page + 1)]

    if len(selftext) > 1750 * (page + 1):
        description += "..."

    return f"{description}\n\n**Page {page + 1} of {round((len(selftext) + 438) / 1750)}**"


async def send_post(ctx: commands.Context, author: Union[discord.User, discord.Member], subreddit: str) -> None:
    post = get_post(subreddit=subreddit, bot=ctx.bot)

    if post["over_18"]:
        if not ctx.channel.nsfw:
            return await resources.error.embed(
                msg=ctx.message,
                title="Sorry it's NSFW!",
                description="Please retry this command in an NSFW channel.",
                image_url="https://i.imgur.com/oe4iK5i.gif")

    await views.PageMenu(ctx.author, ctx.bot, post, 0).start(ctx)
