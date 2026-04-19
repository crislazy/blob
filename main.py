# ==== main.py ====
# BLOB - A Discord Bot

import discord
from discord.ext import commands
import random
import config

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    if config.CUSTOM_STATUS:
        activity = None

        if config.STATUS_TYPE == "playing":
            activity = discord.Game(name=config.STATUS_TEXT)
        elif config.STATUS_TYPE == "watching":
            activity = discord.Activity(type=discord.ActivityType.watching, name=config.STATUS_TEXT)
        elif config.STATUS_TYPE == "listening":
            activity = discord.Activity(type=discord.ActivityType.listening, name=config.STATUS_TEXT)

        await bot.change_presence(activity=activity)

#Welcome Message Announcement
@bot.event
async def on_member_join(member):
    if not config.ENABLE_WELCOME_MESSAGE:
        return
    channel = bot.get_channel(config.welcome_channel_id)
    if config.AUTO_ROLE: 
        role = member.guild.get_role(config.member_role_id)
        if role:
            await member.add_roles(role)
    if channel:
        msg = random.choice(config.welcome_messages).format(user=member.mention)
        await channel.send(msg)

#Goodbye Message Announcement
@bot.event
async def on_member_remove(member):
    if not config.ENABLE_GOODBYE_MESSAGE:
        return
    channel = bot.get_channel(config.welcome_channel_id)

    if channel is None:
        return

    try:
        msg = random.choice(config.goodbye_messages).format(user=member.name)
        await channel.send(msg)
    except discord.Forbidden:
        print("Bot cannot send messages in this channel")

#Ping-Pong
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong {round(bot.latency * 1000)}ms")

#Kick
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"{member} has been kicked. Reason: {reason}")
    except discord.Forbidden:
        await ctx.send("User had no perms")
    except Exception as e:
        await ctx.send(f"Error: {e}")
    await ctx.message.delete()

#Ban
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"{member} has been banned. Reason: {reason}")
    except discord.Forbidden:
        await ctx.send("User had no perms")
    except Exception as e:
        await ctx.send(f"Error: {e}")
    await ctx.message.delete()

#Get a response on ping
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if config.PING_RESPOND and bot.user in message.mentions:
        await message.channel.send(random.choice(config.blob_messages))

    await bot.process_commands(message)

#Send a message as bot
@bot.command()
async def s(ctx, channel_id: int, *, message):
    if not config.SEND_AS_BOT:
        await ctx.send("❌ This feature is disabled.")
        return
    # check roles
    if not any(role.id in config.mod_roles_id for role in ctx.author.roles):
        await ctx.message.delete()
        return

    channel = bot.get_channel(channel_id)
    if channel is None:
        await ctx.send("Channel not found.")
        return

    await channel.send(message)

#User info
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    if not config.ENABLE_USERINFO:
        return
    member = member or ctx.author
    await ctx.send(f"User: {member}\nID: {member.id}\nJoined: {member.joined_at}")

#8Ball
@bot.command()
async def ball(ctx):
    if not config.ENABLE_8BALL:
        return
    await ctx.send(f"🎱 {random.choice(config.ballresponse)}")

#Random cat
@bot.command()
async def cat(ctx):
    if not config.ENABLE_CAT:
        return
    await ctx.send("https://cataas.com/cat")

#Help
@bot.command()
async def help(ctx):
    if not config.HELP_COMMAND:
        return
    await ctx.send("""
    🛠 Commands:
    !userinfo - see info about an user
    !ball - random 8ball
    !ping - check latency
    !cat - random cat
    !kick - kick a user (mods only)
    !ban - ban a user (mods only)
    !s - send message as bot (mods only)
    !help - THIS COMMAND
    """)

#In case of error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to do that.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing arguments.")
    elif isinstance(error, commands.CommandNotFound):
        return
    else:
        await ctx.send("❌ Something went wrong.")
        print(error)

bot.run(config.bot_secret)