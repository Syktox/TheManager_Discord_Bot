import discord
import datetime

bot = None
join_role_id = 415936771742892053
main_channel_id = 1328375654106009741
show_join_message = True
show_leave_message = True

async def on_ready():
    print(f'Logged in as {bot.user.name} at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

async def on_command_error(ctx, error):
        if isinstance(error, discord.ext.commands.CommandNotFound):
            await ctx.send(f"Command not found!")
        elif isinstance(error, discord.ext.commands.errors.BadBoolArgument):
            await ctx.send(f"Wrong Input! You should use True or False")
        else:
            raise error

async def on_message(message):
     if message.author == bot.user:
            return
     await bot.process_commands(message)
    
async def on_member_join(member):  
    if show_join_message:
        channel = bot.get_channel(1328375654106009741)
        if channel:
            await channel.send(f"# Hello {member.name}!")
    
    role = member.guild.get_role(join_role_id)
    if role:
        await member.add_roles(role)
        print(f"Assigned Role: Community to {member.name}")
        
async def on_member_remove(member):
    if show_leave_message:
        channel = bot.get_channel(1328375654106009741)
        if channel:
            await channel.send(f"# Goodbye {member.name}!")

