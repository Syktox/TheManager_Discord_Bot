import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import bot_commands
import bot_events

description = '''This Shit should change the nicknames of people on the server with an command'''

load_dotenv()
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$', description=description, intents=intents)
bot_events.bot = bot
bot_commands.bot = bot

for event_name in dir(bot_events):
    if event_name.startswith("on_"):
        event_func = getattr(bot_events, event_name)
        bot.event(event_func)

for command_name in dir(bot_commands):
    command_func = getattr(bot_commands, command_name)
    if isinstance(command_func, commands.Command):
        bot.add_command(command_func)

TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)