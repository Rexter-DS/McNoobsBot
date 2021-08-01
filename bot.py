import os
import discord
import urllib.request
from dotenv import load_dotenv
from pydactyl import PterodactylClient #upm package(py-dactyl)
from discord.ext import commands, tasks

# load environment variables from .env
load_dotenv()

# save secret keys to variables
server_id = os.environ['SERVER_ID']
server_key = os.environ['SERVER_KEY']
panel_url = os.environ['PANEL_URL']

# connect to the discord and pterodactly clients
server_client = PterodactylClient(panel_url, server_key)

# ----------------------------------------------- helper functions ----------------------------------------------------------------

# get the latest log from the server
def get_logs():
  latest_log_url = server_client.client.download_file(server_id, '/logs/latest.log')
  response = urllib.request.urlopen(latest_log_url)
  data = response.read()
  
  return data.decode('utf-8')

@tasks.loop(seconds=5.0)
async def check_server(ctx, option):
  # get current server state
  server_utilization = server_client.client.get_server_utilization(server_id)
  current_state = server_utilization.get('current_state')

  if ((option == 'start' or option == 'restart') and current_state == 'running'):
    await ctx.send('current state of server: ' + current_state)
    check_server.cancel()
  elif ((option == 'stop' or option == 'kill') and current_state == 'offline'):
    await ctx.send('current state of server: ' + current_state)
    check_server.cancel()

# -----------------------------------------------  BOT STUFF -----------------------------------------------------------------------

# set the command prefix to be $
bot = commands.Bot(command_prefix='$')

# event check for when discord bot is ready
@bot.event
async def on_ready():
  print('Logged in as')
  print(bot.user.name)
  print(bot.user.id)

# ----------------------------------------------- command functions ----------------------------------------------------------------

# command for checking the list of players online
@bot.command(name='list', brief='Returns the list of current online players', description='Returns the list of current online players')
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
    check_server.start(ctx, option)
  else:
    await ctx.send('Invalid option. If you need help, type $help power.')

# command for checking the state of the server
@bot.command()
async def state(ctx):
  # check the current state of the server
  server_utilization = server_client.client.get_server_utilization(server_id)
  await ctx.send('current state of server: ' + server_utilization.get('current_state'))

# start the bot
bot.run(os.getenv('DISCORD_KEY'))
