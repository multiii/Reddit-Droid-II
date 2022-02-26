from nextcord.ext import commands
from nextcord.ext.commands import CheckFailure
from typing import Union, Iterable


class NotEqualArgs(CheckFailure):
    """Exception raised when a certain number of args haven't been passed for a command.
    This inherits from :exc:`CheckFailure`.
    Parameters
    -----------
    a: :class:`int`
        The number of args to have been passed
    """

    def __init__(self, a: int):
        self.a = a
        super().__init__(
            f"{a} Args have to be passed while using this Command for it to work.")


class NotEnoughArgs(CheckFailure):
    """Exception raised when the number of args passed for a command are less than the number of args needed.
    This inherits from :exc:`CheckFailure`.
    Parameters
    -----------
    a: :class:`int`
        The least number of args to have been passed
    """

    def __init__(self, a):
        self.a = a
        super().__init__(
            f"Atleast {a} Args have to be passed while using this Command for it to work.")


class MissingID(CheckFailure):
    """Exception raised when the Author, Channel or Guild ID of the Command isn't equal to a certain ID or IDs from a list.
    This inherits from :exc:`CheckFailure`.
    Parameters
    -----------
    id: Union[:class:`int`, Iterable[:class:`int`]]
        The ID which was required
    id_type: :class: `str`
        The type of ID required (Author/User, Channel or Guild)
    """

    def __init__(self, id: Union[int, Iterable[int]], id_type: str):
        self.id = id
        self.id_type = id_type
        if type(id) == int:
            super().__init__(
                f"The {id_type} ID should be equal to {id} for the Command to work.")
        else:
            super().__init__(
                f"The {id_type} ID should be equal to an ID in {id} for the Command to work.")


class MissingName(CheckFailure):
    """Exception raised when the Author, Channel or Guild Name of the Command isn't equal to a certain Name or Names from a list.
    This inherits from :exc:`CheckFailure`.
    Parameters
    -----------
    name: Union[:class:`str`, Iterable[:class:`str`]]
        The ID which was required
    name_type: :class: `str`
        The type of ID required (Author/User, Channel or Guild)
    """

    def __init__(self, name: Union[str, Iterable[str]], name_type: str):
        self.name = name
        self.name_type = name_type
        if type(id) == str:
            super().__init__(
                f"The {name_type} Name should be equal to {name} for the Command to work.")
        else:
            super().__init__(
                f"The {name_type} Name should be equal to a Name in {name} for the Command to work.")


class NotGuildOwner(CheckFailure):
    """Exception raised when the Message Author is not the Owner of the Guild.
    This inherits from :exc:`CheckFailure`
    """
    pass


class GuildOwner(CheckFailure):
    """Exception raised when the Message Author is the Owner of the Guild.
    This inherits from :exc:`CheckFailure`
    """
    pass


def is_guild_owner():
    """Checks if the Command Author is the Guild Owner"""
    def predicate(ctx) -> bool:
        if ctx.author.id == ctx.guild.owner_id:
            return True
        raise NotGuildOwner("The Command Author does not own the Server.")
    return commands.check(predicate)


def is_not_guild_owner():
    """Checks if the Command Author is not the Guild Owner"""
    def predicate(ctx) -> bool:
        if ctx.author.id != ctx.guild.owner_id:
            return True
        raise GuildOwner("The Command Author owns the Server.")
    return commands.check(predicate)


def has_user_id(id: int):
    """Checks if the Command Author's ID is the same as the ID passed into the function"""
    def predicate(ctx) -> bool:
        if ctx.author.id == id:
            return True
        raise MissingID(id, "Author")
    return commands.check(predicate)


def has_channel_id(id: int):
    """Checks if the Command Channel's ID is the same as the ID passed into the function"""
    def predicate(ctx) -> bool:
        if ctx.channel.id == id:
            return True
        raise MissingID(id, "Channel")
    return commands.check(predicate)


def has_guild_id(id: int):
    """Checks if the Command Guild's ID is the same as the ID passed into the function"""
    def predicate(ctx) -> bool:
        if ctx.guild.id == id:
            return True
        raise MissingID(id, "Guild")
    return commands.check(predicate)


def has_user_id_in(ids: Iterable[int]):
    """Checks if the Command Author's ID is the same as any ID in the Iterable Object (List, Tuple, etc) passed into the function"""
    def predicate(ctx) -> bool:
        for id in ids:
            if ctx.author.id == id:
                return True
        raise MissingID(ids, "Author")
    return commands.check(predicate)


def has_channel_id_in(ids: Iterable[int]):
    """Checks if the Command Channel's ID is the same as any ID in the Iterable Object (List, Tuple, etc) passed into the function"""
    def predicate(ctx) -> bool:
        for id in ids:
            if ctx.channel.id == id:
                return True
        raise MissingID(ids, "Channel")
    return commands.check(predicate)


def has_guild_id_in(ids: Iterable[int]):
    """Checks if the Command Guild's ID is the same as any ID in the Iterable Object (List, Tuple, etc) passed into the function"""
    def predicate(ctx) -> bool:
        for id in ids:
            if ctx.guild.id == id:
                return True
        raise MissingID(ids, "Guild")
    return commands.check(predicate)


def has_user_name(name: str):
    """Checks if the Command Author's Name is the same as the Name passed into the function"""
    def predicate(ctx) -> bool:
        if ctx.author.name == name:
            return True
        raise MissingName(name, "Author")
    return commands.check(predicate)


def has_channel_name(name: str):
    """Checks if the Command Channel's Name is the same as the Name passed into the function"""
    def predicate(ctx) -> bool:
        if ctx.channel.name == name:
            return True
        raise MissingName(name, "Channel")
    return commands.check(predicate)


def has_guild_name(name: str):
    """Checks if the Command Guild's Name is the same as the Name passed into the function"""
    def predicate(ctx) -> bool:
        if ctx.guild.name == name:
            return True
        raise MissingName(name, "Guild")
    return commands.check(predicate)


def has_user_name_in(names: Iterable[str]):
    """Checks if the Command Author's Name is the same as any Name in the Iterable Object (List, Tuple, etc) passed into the function"""
    def predicate(ctx) -> bool:
        for name in names:
            if ctx.author.name == name:
                return True
        raise MissingName(names, "Author")
    return commands.check(predicate)


def has_channel_name_in(names: Iterable[str]):
    """Checks if the Command Channel's Name is the same as any Name in the Iterable Object (List, Tuple, etc) passed into the function"""
    def predicate(ctx) -> bool:
        for name in names:
            if ctx.channel.name == name:
                return True
        raise MissingName(names, "Channel")
    return commands.check(predicate)


def has_guild_name_in(names: Iterable[str]):
    """Checks if the Command Guild's Name is the same as any Name in the Iterable Object (List, Tuple, etc) passed into the function"""
    def predicate(ctx) -> bool:
        for name in names:
            if ctx.guild.name == name:
                return True
        raise MissingName(names, "Guild")
    return commands.check(predicate)


def has_args(number: int):
    """Checks if the Number of Args in the Command passed is equal to the Number passed into this function (Context is considered to be an Arg)"""
    def predicate(ctx) -> bool:
        if len(ctx.message.content.split()) == number:
            return True
        raise NotEqualArgs(number)
    return commands.check(predicate)


def has_args_atleast(number: int):
    """Checks if the Number of Args in the Command passed is greater than or equal to the Number passed into this function (Context is considered to be an Arg)"""
    def predicate(ctx) -> bool:
        if len(ctx.message.content.split()) >= number:
            return True
        raise NotEnoughArgs(number)
    return commands.check(predicate)