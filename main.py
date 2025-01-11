import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

description = '''This Shit should change the nicknames of people on the server with an command'''

load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix='$', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='change')
@commands.has_permissions(manage_nicknames=True)
async def change(ctx, member: discord.Member, new_nickname: str):
    try:
        old_nickname = member.nick or member.name  # Fallback to username if no nickname is set
        await member.edit(nick=new_nickname)
        await ctx.send(f"Changed nickname for {old_nickname} to {new_nickname}.")
    except discord.Forbidden:
        await ctx.send("I do not have permission to change this member's nickname.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command('changeAll')
async def changeAll(ctx, occurrences , new_nickname: str):


    pass


TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)