import os
import discord
from dotenv import load_dotenv
from pydactyl import PterodactylClient #upm package(py-dactyl)
# from keep_alive import keep_alive

# load environment variables from .env
load_dotenv()

# save secret keys to variables
server_key = os.environ['SERVER_KEY']
panel_url = os.environ['PANEL_URL']

# connect to the discord and pterodactly clients
discord_client = discord.Client()
server_client = PterodactylClient(panel_url, server_key)

print('hello')
print(discord_client)
print(server_client)

# event for when discord bot is ready
@discord_client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(discord_client))

# functions for commands
async def hello(message):
  await message.channel.send('Hello :)')
  return

async def hi(message):
  await message.channel.send('Hi :)')
  return

# event for when a user sends a message
@discord_client.event
async def on_message(message):

  # check to see if the message was from the bot
  if message.author == discord_client.user:
    return
  
  if message.content.startswith('!'):
    await hello(message)
  
discord_client.run(os.getenv('DISCORD_KEY'))
