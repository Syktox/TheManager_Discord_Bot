import discord
import datetime

bot = None
show_join_message = True
show_leave_message = True

async def on_ready():
    print(f'Logged in as {bot.user.name} at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

async def on_message(message):
     if message.author == bot.user:
            return
     await bot.process_commands(message)

async def on_member_join(ctx, member):
        if show_join_message:
            channel = member.guild.system_channel
            if channel:
                await channel.send(f"Hello {member.name}!")

async def on_member_remove(ctx, member):
    if show_leave_message:
        channel = member.guild.system_channel
        if channel:
            await channel.send(f"Goodbye {member.name}")

