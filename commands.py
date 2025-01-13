import discord
from discord.ext import commands
import events

bot = None

# Event commands

@commands.command('switch_join_message')
async def switch_join_message(ctx, changed: bool):
    events.show_join_message = changed
    await ctx.send(f"Show new member message has been set to: {events.show_join_message}")

@commands.command('switch_leave_message')
async def switch_leave_message(ctx, changed: bool):
    events.show_leave_message = changed
    await ctx.send(f"Leave message has been set to: {events.show_leave_message}")





# Nickname commands

@commands.command('changeNickname')
async def changeNickname(ctx, member: discord.Member, nick: str):
    try:
        await member.edit(nick=nick)
        await ctx.send(f"Changed nickname of {member.mention}")
    except discord.Forbidden:
        print(f"Can't change the nickname of {member.name} : {member.nick}")

@commands.command('removeAllNicknames', pass_content=True)
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

@commands.command('removeAllNicknamesExceptRole')
async def removeAllNicknamesExceptRole(ctx, role: discord.guild.Role):
    await ctx.send(f"Role {role.name} avalable")