# . . . Imports . . . #

import pydantic
from typing import Dict, List, Optional, Union

import nextcord as discord

from utils import functions

# . . . Imports . . . #


class Resource:
    __slots__ = ("_color", "_emote")

    def __init__(self, *args, **kwargs) -> None:
        self._color = kwargs.get("color")
        self._emote = kwargs.get("emote")

    @property
    def color(self):
        return self._color

    @property
    def emote(self):
        return self._emote

    async def embed(self, *args, **kwargs) -> Union[discord.Message, discord.Embed]:
        if kwargs.get("emoji") is not None:
            title = f'{kwargs.get("emoji")}・'

        elif self.emote is not None:
            title = f'{self.emote}・'

        else:
            title = ""

        title += functions.clean_none(kwargs.get("title"))

        embed = discord.Embed(
            title=title,
            description=functions.clean_none(kwargs.get("description")),
            color=self.color if kwargs.get(
                "color") is None else kwargs.get("color")
        )

        if kwargs.get("timestamp") is not None:
            embed.timestamp = kwargs.get("timestamp")

        embed.set_thumbnail(url=functions.clean_none(
            kwargs.get("thumbnail_url")))
        embed.set_image(url=functions.clean_none(kwargs.get("image_url")))

        embed.set_author(icon_url=functions.clean_none(kwargs.get(
            "author_icon_url")), name=functions.clean_none(kwargs.get("author_name")))

        embed.set_footer(icon_url=functions.clean_none(kwargs.get(
            "footer_icon_url")), text=functions.clean_none(kwargs.get("footer_text")))

        if kwargs.get("field_names") is not None:
            for name, value in zip(kwargs.get("field_names"), kwargs.get("field_values")):
                embed.add_field(name=name, value=value,
                                inline=kwargs.get("inline"))

        if kwargs.get("embed") is not None:
            return embed

        if isinstance(kwargs.get("msg"), discord.abc.Messageable):
            return await kwargs["msg"].send(content=functions.clean_none(kwargs.get("content")), embed=embed, delete_after=kwargs.get("delete_after"), view=kwargs.get("view"))

        if kwargs.get("reply"):
            return await kwargs["msg"].reply(content=functions.clean_none(kwargs.get("content")), embed=embed, delete_after=kwargs.get("delete_after"), view=kwargs.get("view"))

        return await kwargs["msg"].channel.send(content=functions.clean_none(kwargs.get("content")), embed=embed, delete_after=kwargs.get("delete_after"), view=kwargs.get("view"))

# Basic Colors


default_c = 0x2F3136
error_c = 0xFF6347

# Special Colors


# Basic Emotes


# Special Emotes

alert_e = "<:alert:935890334003658793>"

# Resource Objects

default = Resource(color=default_c)
error = Resource(color=error_c)

# Classes


class Comment(pydantic.BaseModel):
    author: str
    title: Optional[str]
    body: str
    subreddit: str
    ups: int
    replies: Dict


class Post(pydantic.BaseModel):
    author: str
    title: str
    selftext: str
    subreddit: str
    permalink: str
    url: Optional[str]
    ups: int
    over_18: bool
