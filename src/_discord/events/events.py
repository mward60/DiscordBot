
from ..defs.defs import *
from ..guild.guild import *
from discord import Game, Status

@discord_client.event
async def on_ready() -> None:
    """ Sets the bot to "Playing Dungeons and Dragons"
    """

    print("Setting bot activity...")

    dnd_discord_game = Game(name = "Dungeons and Dragons", type = 3)

    await discord_client.change_presence(activity = dnd_discord_game, status = Status.idle)
    print(f"Bot activity set to {dnd_discord_game}.")
    
    # 
    for guild in discord_client.guilds:
        command_tree.copy_global_to(guild = guild)
        await command_tree.sync(guild = guild)
    
    log_bot_guild_presence(discord_client)