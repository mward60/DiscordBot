from discord import app_commands, Interaction, Intents, Client 

def log_bot_guild_presence(discord_client: Client) -> None:
    """ Logs Ivy Bot's guild presence

    Args:
        discord_client (Client): Discord client
    """
    for guild in discord_client.guilds:
        print(f'{discord_client.user.name} is connected to {guild.name}.')
        print(f'Server Members ({len(guild.members)}):')
        
        for member in guild.members:
            print(f'- {member.name}')