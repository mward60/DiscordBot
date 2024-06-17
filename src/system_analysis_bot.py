#!/usr/bin/env python3

from _discord.token.discord_token import *
from _discord.guild.guild import *
from _discord.defs.defs import *
from _discord.events.events import on_ready
from _discord.commands.tree_commands import bot_roll_dice

def main() -> int:
    """ Main entry point for discord bot application

    Returns:
        int: Returns 0 on successful execution of program
    """

    print("Connecting to IvyBot on discord client ... \r\n")
    discord_client.run(TOKEN)
    return 0

if __name__ == "__main__":
    main()