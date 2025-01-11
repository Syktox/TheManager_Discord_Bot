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
async def changeAll(ctx, occurrences: str , new_nickname: str):
    for server in bot.guilds:
        for member in server.members:
            member_list.append(member)
            if member.nick == "Maike4Seven ":
                member.nick = None
                await ctx.send(f"changed {member.name}s nickname back")
            await ctx.send(f"{member.id} : {member} : {member.nick} : {member.name}")
        

TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)