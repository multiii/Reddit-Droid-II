import itertools
import math

import nextcord as discord
from nextcord.ext import commands

from utils import functions, pagination, resources

class CustomHelpCommand(commands.HelpCommand):
    if resources.default.emote is not None:
      title = f"{resources.default.emote}・"

    else:
      title = ""

    title += "Main Menu!"

    def __init__(self):
        super().__init__(
            command_attrs={"help": "Show help about the bot, a command, or a category."}
        )

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(str(error.original))

    def make_page_embed(self, commands, title=title, description=discord.Embed.Empty):
        embed = self.context.bot.Embed(color=resources.default.color)

        embed.title = title
        embed.description = description

        for command in commands:
            signature = self.clean_prefix + command.qualified_name + " "

            if command.help is not None:
              signature += (
                command.help
              )

            else:
              signature += (
                command.signature
              )

            value = None

            if command.brief:
              value = command.brief
            
            elif command.description:
              value = command.description

            embed.add_field(
                name=signature,
                value=value or "No help found...",
                inline=False,
            )

        return embed

    def make_default_embed(self, cogs, title=title, description=discord.Embed.Empty):
        embed = self.context.bot.Embed(color=resources.default.color)

        embed.title = title
        embed.description = description

        ctx = self.context

        counter = 0
        for cog in cogs:
            cog, description, command_list = cog

            if cog.qualified_name == "Events":
              continue

            embed.add_field(name=f"{cog.qualified_name.capitalize()} | `{ctx.clean_prefix}help {cog.qualified_name}`", value=' '.join(f'`{command.qualified_name}`' for command in cog.walk_commands()), inline=False)
            counter += 1

        return embed

    async def send_bot_help(self, mapping):
        ctx = self.context
        ctx.invoked_with = "help"
        bot = ctx.bot

        def get_category(command):
            cog = command.cog
            return cog.qualified_name if cog is not None else "\u200bNo Category"

        embed_pages = []
        total = 0

        filtered = await self.filter_commands(bot.commands, sort=True, key=get_category)

        for cog_name, _commands in itertools.groupby(filtered, key=get_category):
            if cog_name == "Events":
              continue
              
            _commands = sorted(_commands, key=lambda c: c.name)

            if len(_commands) == 0:
                continue

            total += len(_commands)
            cog = bot.get_cog(cog_name)
            description = (
                (cog and cog.description)
                if (cog and cog.description) is not None
                else discord.Embed.Empty
            )
            embed_pages.append((cog, description, _commands))

        async def get_page(source, menu, pidx):
            cogs = embed_pages[
                min(len(embed_pages) - 1, pidx * 6) : min(len(embed_pages) - 1, pidx * 6 + 6)
            ]

            embed = self.make_default_embed(
                cogs,
                title=self.title,
                description=(
                    f"""
                  {resources.alert_e} **Info:**
                  
                  > **•** A bot that allows you to browse through reddit, on discord!
                  > **•** Inspired by Reddit Droid - {await ctx.bot.fetch_user(807097314907783178)}
                  > **•** Version: Beta 0.4

                  > **•** Made by {await ctx.bot.fetch_user(394320584089010179)}
                  
                  Access my help menu: `{ctx.clean_prefix}help`
                  Learn more about a command: `{ctx.clean_prefix}help <command>`"""
                ),
            )

            return embed

        pages = pagination.ContinuablePages(
            pagination.FunctionPageSource(math.ceil(len(embed_pages) / 6), get_page)
        )
        ctx.bot.menus[ctx.author.id] = pages
        await pages.start(ctx)

    async def send_cog_help(self, cog):
        ctx = self.context
        ctx.invoked_with = "help"
        bot = ctx.bot

        filtered = await self.filter_commands(cog.get_commands(), sort=True)

        embed = self.make_page_embed(
            filtered,
            title="" + (cog and cog.qualified_name or "Other"),
            description=discord.Embed.Empty if cog is None else cog.description,
        )

        await ctx.send(embed=embed)

    async def send_group_help(self, group):
        ctx = self.context
        ctx.invoked_with = "help"
        bot = ctx.bot

        subcommands = group.commands
        if len(subcommands) == 0:
            return await self.send_command_help(group)

        filtered = await self.filter_commands(subcommands, sort=True)

        description = None

        if group.help:
          description = ""

        else:
          if group.brief:
            description = group.brief

        embed = self.make_page_embed(
            filtered,
            title=group.qualified_name,
            description=description if description is not None else "No help found...",
        )

        if group.help:
          embed.add_field(name=f"{ctx.clean_prefix}{group.qualified_name} {group.help}", value=group.brief)

        await ctx.send(embed=embed)

    async def send_command_help(self, command):
        embed = self.context.bot.Embed(color=resources.default.color)
        embed.title = "" + command.qualified_name

        if command.description:
            embed.description = f"{command.description}\n\n{command.help}"
        else:
            embed.description = command.brief or "No help found..."

        embed.add_field(name="Usage", value=self.get_command_signature(command) if not command.help else command.help)

        if len(command.aliases) != 0:
          embed.add_field(name="Aliases", value=" | ".join([f'`{alias}`' for alias in command.aliases]))

        await self.context.send(embed=embed)


def setup(bot):
    bot.old_help_command = bot.help_command
    bot.help_command = CustomHelpCommand()


def teardown(bot):
    bot.help_command = bot.old_help_command