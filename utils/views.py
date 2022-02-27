import datetime as dt

import nextcord as discord
from nextcord.ext import menus

from utils import functions, resources


class CommentMenu(menus.ButtonMenu):
    def __init__(self, author, bot, post):
        super().__init__(disable_buttons_after=True)
        self.author = author
        self.bot = bot
        self.post = post
        self.index = 0

    async def get_comment(self, page):
        post, comment = functions.get_comment(
            f"https://oauth.reddit.com{self.post.permalink}", self.index, self.bot)

        embed = await resources.default.embed(
            embed=True,
            author_name=comment.author,
            title=post.title,
            description=comment.body,
            thumbnail_url=self.author.display_avatar.url,
            footer_text=f"r/{comment.subreddit} • 👍{comment.ups} • 💬{comment.replies}",
            timestamp=dt.datetime.now()
        )

        return embed

    async def send_initial_message(self, ctx, channel):
        embed = await self.get_comment(self.index)
        return await ctx.reply(embed=embed, view=self)

    @discord.ui.button(emoji="<:cross:906925217828446268>", style=discord.ButtonStyle.danger)
    async def on_cancel(self, button, interaction):
        await self.stop()

        await interaction.message.delete()

    @discord.ui.button(emoji="<:right:907828453859028992>")
    async def on_next_comment(self, button, interaction):
        self.index += 1

        embed = await self.get_comment(self.index)
        return await self.message.edit(embed=embed)


class Dropdown(discord.ui.Select):
    def __init__(self, author, bot, post):
        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(
                label='Comments', description="Read the post\'s comments", emoji='📪')
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Select an option',
                         min_values=1, max_values=1, options=options)
        self.author = author
        self.bot = bot
        self.post = post
        self.comments = None

    async def callback(self, interaction: discord.Interaction):
        self.comments = CommentMenu(self.author, self.bot, self.post)
        await self.comments.start(await self.bot.get_context(interaction.message))

    def change_post(self, post):
        self.post = post


class PageMenu(menus.ButtonMenu):
    def __init__(self, author, bot, post, page):
        super().__init__(disable_buttons_after=False)
        self.author = author
        self.bot = bot
        self.post = post
        self.page = page

        self.dropdown = Dropdown(self.author, self.bot, self.post)

        self.add_item(self.dropdown)

    async def get_page_embed(self, page):
        description = functions.get_selftext_page(self.post.selftext, page)
        url = self.post.url

        embed = await resources.default.embed(
            embed=True,
            author_name=f"{self.author.name}#{self.author.discriminator}",
            author_icon_url=self.author.display_avatar.url,
            title=self.post.title,
            description=description,
            image_url=url if "i.redd.it" in url else "",
            footer_text=f"r/{self.post.subreddit} • 👍{self.post.ups}",
            timestamp=dt.datetime.now()
        )

        return embed

    async def send_initial_message(self, ctx, channel):
        embed = await self.get_page_embed(self.page)
        return await channel.send(embed=embed, view=self)

    @discord.ui.button(label="Prev. Page")
    async def on_prev_page(self, button, interaction):
        if self.page == 0:
            self.page = round((len(self.post.selftext) + 438) / 1750) - 1

        else:
            self.page -= 1

        embed = await self.get_page_embed(self.page)
        await self.message.edit(embed=embed)

    @discord.ui.button(label="Next Page")
    async def on_next_page(self, button, interaction):
        last_page = round((len(self.post.selftext) + 438) / 1750) - 1

        if self.page == last_page:
            self.page = 0

        else:
            self.page += 1

        embed = await self.get_page_embed(self.page)
        await self.message.edit(embed=embed)

    @discord.ui.button(emoji="<:right:907828453859028992>")
    async def on_next_post(self, button, interaction):
        self.post = functions.get_post(
            subreddit=self.post.subreddit, bot=self.bot)
        self.page = 0

        embed = await self.get_page_embed(self.page)
        await self.message.edit(embed=embed)

        self.dropdown.change_post(self.post)
