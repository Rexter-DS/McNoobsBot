import os
from dotenv import load_dotenv
from pydactyl import PterodactylClient #upm package(py-dactyl)
from discord.ext import commands

# load environment variables from .env
load_dotenv()

# save secret keys to variables
server_id = os.environ['SERVER_ID']
server_key = os.environ['SERVER_KEY']
panel_url = os.environ['PANEL_URL']

# connect to the discord and pterodactly clients
server_client = PterodactylClient(panel_url, server_key)

# set the command prefix to be $
bot = commands.Bot(command_prefix='$')

# event check for when discord bot is ready
@bot.event
async def on_ready():
  print('Logged in as')
  print(bot.user.name)
  print(bot.user.id)

# command for sending power actions to server
@bot.command()
async def power(ctx, option):
  # check if option is one of these signals
  if (option == 'start' or option == 'restart' or option == 'stop' or option == 'kill'):
    # send the signal to the server
    server_client.client.send_power_action(server_id, option)
    await ctx.send('sending ' + option + ' signal to server')

    # check the current state of the server
    server_utilization = server_client.client.get_server_utilization(server_id)
    await ctx.send('current state of server: ' + server_utilization.get('current_state'))
  elif (option == 'help'):
    # send user instructions
    await ctx.send('Options: start, restart, stop, kill. Example: $power start.')
  else:
    # send user that the option they typed is invalid
    await ctx.send('Invalid option. If you need help, type $power help.')

# command for checking the state of the server
@bot.command()
async def state(ctx):
  # check the current state of the server
  server_utilization = server_client.client.get_server_utilization(server_id)
  await ctx.send('current state of server: ' + server_utilization.get('current_state'))

# start the bot
bot.run(os.getenv('DISCORD_KEY'))
