import discord
from discord.ext import commands
import requests
import json
import bot_events
import threading
import asyncio

bot = None
threadList = []
wake_event = asyncio.Event()

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
async def dmMe(ctx, message: str):
    await ctx.author.send(message)


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


@commands.command('dmMemberSpam')  # Muss threaded sein
async def dmMemberSpam(ctx, message: str, *members: discord.Member):
    try:
        if not members:
            await ctx.send("You have to mention at least one member!")
            return

        for member in members:
            stop_event = threading.Event()  # Event-Objekt für diesen Thread
            thread = threading.Thread(
                target=start_spam_in_thread, 
                args=(message, member, bot.loop, stop_event), 
                daemon=True
            )
            threadList.append({"thread": thread, "event": stop_event})  # Speichere Thread und Event
            thread.start()

        await ctx.send(f"Started spamming {len(members)} members.")
        
    except discord.Forbidden:
        await ctx.send("I can't send a message to one or more users. They have DMs disabled.")
    except Exception as e:
        await ctx.send("An error occurred.")
        print(f"Error: {e}")


def start_spam_in_thread(message: str, member: discord.Member, loop: asyncio.AbstractEventLoop, stop_event: threading.Event):
    try:
        asyncio.run_coroutine_threadsafe(
            spammessage_discord_member(message, member, stop_event), 
            loop
        )
    except Exception as e:
        print(f"Thread error for {member.name}: {e}")


async def spammessage_discord_member(message: str, member: discord.Member, stop_event: threading.Event):
    try:
        while not stop_event.is_set():  # Überprüfe, ob das Event gesetzt ist
            await member.send(message)
            await asyncio.sleep(1)
    except discord.Forbidden:
        print(f"DMs for {member.name} are disabled.")
    except Exception as e:
        print(f"Error with {member.name}: {e}")


@commands.command('stopAll')  # Stoppt alle Threads
async def stopAll(ctx):
    if not threadList:
        await ctx.send("No threads to stop.")
        return

    for thread_data in threadList:
        stop_event = thread_data["event"]
        thread = thread_data["thread"]
        stop_event.set()  # Signalisiere dem Thread, dass er stoppen soll
        thread.join()  # Warte, bis der Thread beendet ist

    threadList.clear()  # Liste leeren
    await ctx.send("All threads have been stopped.")


# Other commands

@commands.command('survey')
async def survey(ctx, question: str, *options):
    if len(options) < 2:
        await ctx.send("You need at least 2 options to create a Survey!")
        return
    if len(options) > 10:
        await ctx.send("You can only have up to 10 options!")
        return
    
    embed = discord.Embed(title="Survey", description=question, color=0x00ff00)
    reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    fields = [f"{reactions[i]} {option}" for i, option in enumerate(options)]
    embed.add_field(name="Options", value="\n".join(fields), inline=False)
    poll_message = await ctx.send(embed=embed)

    for i in range(len(options)):
        await poll_message.add_reaction(reactions[i])

    await wake_event.wait()
    poll_message = await ctx.fetch_message(poll_message.id)
    results = {reactions[i]: 0 for i in range(len(options))}
    for reaction in poll_message.reactions:
        if reaction.emoji in results:
            results[reaction.emoji] = reaction.count - 1

    result_text = "\n".join([f"{fields[i]}: {results[reactions[i]]} votes" for i in range(len(options))])
    await ctx.send(f"Poll Results:\n{result_text}")


@commands.command('stopSurvey')
async def stopSurvey(ctx):
    wake_event.set()