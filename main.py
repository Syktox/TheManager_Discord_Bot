import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

description = '''This Shit should change the nicknames of people on the server with an command'''

load_dotenv()
intents = discord.Intents.all()
intents.members = True
intents.messages = True
member_list = []

bot = commands.Bot(command_prefix='$', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command('changeNickname')
async def changeNickame(ctx, member: discord.Member, nick: str):
    try:
        await member.edit(nick=nick)
        await ctx.send(f"Changed nickname of {member.mention}")
    except discord.Forbidden:
        print(f"Can't change the nickname of {member.name} : {member.nick}")

@bot.command('removeAllNicknames', pass_content=True)
async def removeAllNicknames(ctx):
    for server in bot.guilds:
        for member in server.members:
            await ctx.send(f"Current user: {member.name} : {member.nick} : {member.id}")
            try:
                if member.nick:
                    await member.edit(nick=None)
                    await ctx.send(f"Removed nickname from: {member.name}")
            except discord.Forbidden:
                print(f"Can't change the nickname of {member.name} : {member.nick}")
            except discord.HTTPException as e:
                print(f"Error : {e}")
             

TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)