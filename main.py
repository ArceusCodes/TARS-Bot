import discord
from discord import Option
from discord.ext.commands.errors import MissingPermissions
import os
import dotenv
import random
from discord.ext import commands

dotenv.load_dotenv('token.env')
token = str(os.getenv("TOKEN"))

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"TARS is online.")

# Greet command:
@bot.slash_command(name = 'greet', description = 'Say hello to TARS')
async def hello(ctx):
    await ctx.respond(f"Hi there.")

# Purge command:
@bot.slash_command(name = 'purge', description = 'TARS will delete a selected number of messages in this channel')
@commands.has_permissions(manage_messages = True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def purge(ctx, messages: Option(int, description= "How many messages do you wish to delete?", required = True)):
    await ctx.defer()
    await ctx.channel.purge(limit = messages)
@purge.error
async def purgeerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond(':warning: You need `Manage Messages` permission in order to execute this command.')
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(error)
    else:
        raise error

# Ping command:
@bot.command(description = "Sends the bot's latency")
async def ping(ctx):
    await ctx.respond(f":gear: Latency is {bot.latency * 1000} ms.")

# Ban command:
@bot.slash_command(name = 'tarsban', description = 'TARS will ban a selected member from the server')
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: Option(discord.Member, description = 'Select a user to TARS-ban'), reason: Option(str, description = 'Any reason?', required = False)):
    if member.id == ctx.author.id:
        await ctx.respond("Are you okay, little boy? As much as I'd like to do this, banning yourself would make you look more stupid than you already are. AND, I don't want to hurt you. :)")
    elif member.guild_permissions.administrator:
        await ctx.respond(":warning: You can't ban someone with `Administrator` permission.")
    elif member.id == {bot.user}:
        await ctx.respond("Nice try but I won't fall for any of your tricks.")
    else:
        if reason == None:
            reason = f"No reason provided by {ctx.author}."
        await member.ban(reason = reason)
        await ctx.send(f":white_check_mark: Operation Successful, <@{member.id}> was banned.\nReason: {reason}\nAction taken by: <@{ctx.author.id}>")
# Ban error handling:
@ban.error
async def banerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond(':warning: You need `Ban Members` permission in order to execute this command.')
    else:
        await ctx.respond(':question: Something went wrong, please re-run the command.')
        raise error

# Kick command:
@bot.slash_command(name = 'tarskick', description = 'TARS will kick a selected member from the server')
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: Option(discord.Member, description = 'Select a user to TARS-kick'), reason: Option(str, description = 'Any reason?', required = False)):
    if member.id == ctx.author.id:
        await ctx.respond("You could just leave the server you know.")
    elif member.guild_permissions.administrator:
        await ctx.respond(":warning: You can't kick someone with `Administrator` permission.")
    elif member.id == {bot.user}:
        ctx.respond("Nice try but I won't fall for any of your tricks.")
    else:
        if reason == None:
            reason = f"No reason provided by {ctx.author}."
        else:
            await member.kick(reason = reason)
            await ctx.send(f":white_check_mark: Operation Successful, <@{member.id}> was kicked.\nReason: {reason}\nAction taken by: <@{ctx.author.id}>")
# Kick error handling:
@kick.error
async def kickerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond(':warning: You need `Kick Members` permission in order to execute this command.')
    else:
        await ctx.respond(':question: Something went wrong, please re-run the command.')
        raise error

# Help command:
@bot.slash_command(name = 'help', description = "Lists all of TARS' protocols/commands")
async def help(ctx):
    await ctx.respond("Here's a list of all my protocols and commands:\n\n**:lock:__Moderation/Maintenance, Security:__:lock:**\n> 1) `/purge`: Used to delete a selected number of messages from the channel the command is executed in.\n> 2)`/ban`: Used to ban a selected user from the server.\n> 3) `/ping`: You can call this command to check my latency.\n*More to be added soon.*\n\n**:champagne_glass:__Miscellaneous:__:champagne_glass:**\n> 1) `/greet`: Feeling friendly? Say hello to me!\n> 2) `/gtn`: Play Guess-the-Number with me, I'll pick a random number between 1 and 10 for you to guess.\n*More to be added soon.*")

# Guess-the-Number command:
@bot.command(description = 'Play Guess-the-Number with TARS')
async def gtn(ctx, guess: Option(int, description = 'Try to guess a number between 1 and 10', required = True)):
    number = random.randint(1, 10)
    if guess == number:
        await ctx.respond(f":white_check_mark: Congratulations! You guessed it.")
    else:
        await ctx.respond(f":warning: Incorrect guess, try again.", ephemeral = True)


bot.run(token)
