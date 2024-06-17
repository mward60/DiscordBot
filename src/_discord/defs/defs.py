from discord import app_commands, Intents, Client

intents = Intents.default()
discord_client = Client(intents = Intents.all())
command_tree = app_commands.CommandTree(discord_client)