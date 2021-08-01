import os
import urllib.request
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

# helper functions
def get_logs():
  latest_log_url = server_client.client.download_file(server_id, '/logs/latest.log')
  response = urllib.request.urlopen(latest_log_url)
  data = response.read()
  
  return data.decode('utf-8')

# -----------------------------------------------  BOT STUFF -----------------------------------------------------------------------

# set the command prefix to be $
bot = commands.Bot(command_prefix='$')

# event check for when discord bot is ready
@bot.event
async def on_ready():
  print('Logged in as')
  print(bot.user.name)
  print(bot.user.id)

@bot.command()
async def list(ctx):
  # send the /list command to the server
  server_client.client.send_console_command(server_id, '/list')

  # get the latest log and split it by lines
  log = get_logs()
  log_list = log.splitlines()

  # get the last line and break it up
  last_line = log_list.pop()
  last_line_list = last_line.split(' ', 3)

  # send to server
  await ctx.send(last_line_list[3])

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
