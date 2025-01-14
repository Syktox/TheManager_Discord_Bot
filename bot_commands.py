import string
import discord
from discord.ext import commands
import requests
import json
import bot_events

bot = None

# Event commands

@commands.command('switch_join_message')
async def switch_join_message(ctx, changed: bool):
    bot_events.show_join_message = changed
    await ctx.send(f"Show new member message has been set to: {bot_events.show_join_message}")

@commands.command('switch_leave_message')
async def switch_leave_message(ctx, changed: bool):
    bot_events.show_leave_message = changed
    await ctx.send(f"Leave message has been set to: {bot_events.show_leave_message}")

@commands.command('check_join_message_status')
async def check_join_message_status(ctx):
    await ctx.send(f"Join messages are set to: {bot_events.show_join_message}")

@commands.command('check_leave_message_status')
async def check_leave_message_status(ctx):
    await ctx.send(f"Leave message are set to: {bot_events.show_leave_message}")

# Joke command

@commands.command('joke')
async def joke(ctx):
    joke_url = "https://jokes-always.p.rapidapi.com/family"
    headers = {
        "x-rapidapi-key": "26a2dd88d8msha7adc935319e071p1d680fjsna2c3a5194d08",
        "x-rapidapi-host": "jokes-always.p.rapidapi.com"
    }
    response = requests.get(joke_url, headers=headers)
    await ctx.send(json.loads(response.text)['data'])

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

@commands.command('changeAllNicknamesInRole')
async def changeAllNicknamesInRole(ctx, role: discord.guild.Role, str):
    for member in role.members:
        try:
            await member.edit(nick=str)
            await ctx.send(f"Changed all members with {role.name} to {str}")
        except discord.Forbidden:
            print(f"Can't change the nickname of {member.name} : {member.nick}")
        except discord.HTTPException as e:
            print(f"Error : {e}")