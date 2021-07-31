import os
import discord
# from pydactyl import PterodactylClient #upm package(py-dactyl)
from keep_alive import keep_alive

# save secret keys to variables
server_key = os.environ['server_key']
panel_url = os.environ['panel_url']

# connect to the discord and pterodactly clients
discord_client = discord.Client()
# server_client = PterodactylClient(panel_url, server_key)

# my_servers = server_client.client.list_servers()
# print(my_servers)

# event for when discord bot is ready
@discord_client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(discord_client))

# event for when a user sends a message
@discord_client.event
async def on_message(message):

  # check to see if the message was from the bot
  if message.author == discord_client.user:
    return
  
  if message.content.startswith('!hello'):
    await message.channel.send('Hello :)')


keep_alive()
discord_client.run(os.getenv('discord_key'))
