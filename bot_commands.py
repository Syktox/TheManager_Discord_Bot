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
    for member in ctx.guild.members:
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
    for server_member in ctx.guild.members:
        if server_member.nick:
            try:
                if not any(member == server_member for member in role.members):
                    await server_member.edit(nick=None)
                    await ctx.send(f"Removed nickname from: {server_member.name}")
            except discord.Forbidden:
                print(f"Can't change the nickname of {server_member.name} : {server_member.nick}")
            except discord.HTTPException as e:
                print(f"Error : {e}")

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


@commands.command('alone')
async def alone(ctx, member: discord.Member):
    if ctx.author.voice and ctx.author.voice.channel:
        voice_channel = ctx.author.voice.channel
        members = ", ".join([member.name for member in voice_channel.members])
        if not any(t in member for t in members):
            await ctx.send(f"The other person is not in a voice channel with you")
        await ctx.send(f"Users in {voice_channel.name}: {members}")
    else:
        await ctx.send("You are not connected to a voice channel!")

@commands.command('dmMe')   # only test reasons
async def dmMe(ctx):
    await ctx.author.send('I send you a message')

@commands.command('dmMember')
async def dmMember(ctx, message: str, *members: discord.Member):
    try:
        if not members:
            ctx.send("You have to mention atleast one member!")
            return
        for member in members:
            await member.send(message)
    except discord.Forbidden:
        await ctx.send(f"Ich kann {member.name} keine Nachricht senden. Der Benutzer hat DMs deaktiviert.")
    except Exception as e:
        await ctx.send("Es ist ein Fehler aufgetreten.")
        print(f"Fehler: {e}")

@commands.command('dmMemberSpam')
async def dmMemberSpam(ctx, message: str, *members: discord.Member):
    try:
        if not members:
            ctx.send("You have to mention atleast one member!")
            return
        while True:
             bot.loop.create_task(members.send(message))
    except discord.Forbidden:
        await ctx.send(f"Ich kann {members.name} keine Nachricht senden. Der Benutzer hat DMs deaktiviert.")
    except Exception as e:
        await ctx.send("Es ist ein Fehler aufgetreten.")
        print(f"Fehler: {e}")

@commands.command('stopAll')
async def stopAll(ctx):
    pass
