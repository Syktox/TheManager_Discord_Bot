import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from commands import *
import events

description = '''This Shit should change the nicknames of people on the server with an command'''

load_dotenv()
intents = discord.Intents.all()
intents.members = True
intents.voice_states=True
intents.message_content=True

bot = commands.Bot(command_prefix='$', description=description, intents=intents)
events.bot = bot
commands.bot = bot

for event_name in dir(events):
    if event_name.startswith("on_"):  # Nur Funktionen mit "on_" berücksichtigen
        event_func = getattr(events, event_name)
        bot.event(event_func)

bot.add_command(changeNickname)
bot.add_command(removeAllNicknames)
bot.add_command(removeAllNicknamesExceptRole)
bot.add_command(switch_join_message)
bot.add_command(switch_leave_message)

TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)