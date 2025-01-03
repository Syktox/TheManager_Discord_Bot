import discord
from dotenv import load_dotenv
import os

load_dotenv()
intents = discord.Intents.default()
intents.voice_states=True
intents.message_content=True
client = discord.Client(command_prefix='$', intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

TOKEN = os.getenv('TOKEN')
client.run(TOKEN)