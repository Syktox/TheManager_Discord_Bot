import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

description = '''This Shit should Change the Nicknames of people on the server with an ez command'''

load_dotenv()
intents = discord.Intents.default()
client = commands.Bot(command_prefix='$', description=description, intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command(name='change')
async def change(ctx, string: str):
    """Change Nicknames"""
    await print('test')

TOKEN = os.getenv('TOKEN')
client.run(TOKEN)