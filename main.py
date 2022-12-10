import discord
from discord import Option
from discord.ext.commands.errors import MissingPermissions
import os
import dotenv
import random
from discord.ext import commands
from datetime import timedelta

dotenv.load_dotenv('token.env')
token = str(os.getenv("TOKEN"))


class Tars(discord.Bot):
    def __init__(self):
        super().__init__(
            intents=discord.Intents.all(),
            activity=discord.Activity(type=discord.ActivityType.watching, name="you.")
        )

    async def on_ready(self):
        print(f"Logged in as {self.user} | Ping: {round(self.latency * 1000)}!")
        print("--------------------------")


bot = Tars()


# Greet command:
@bot.slash_command(name='greet', description='Say hello to TARS')
async def hello(ctx):
    await ctx.respond(f"Hi there.", ephemeral=True)


# Purge command:
@bot.slash_command(name='purge', description='TARS will delete a selected number of messages in this channel')
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def purge(ctx, messages: Option(int, description="How many messages do you wish to delete?", required=True)):
    await ctx.defer()
    await ctx.channel.purge(limit=messages)
    embed = discord.Embed(
        description = ':white_check_mark: Message(s) purged.',
        color = discord.Colour.blurple()
    )
    await ctx.send(embed = embed)

#Purge error handling:
@purge.error
async def purgeerror(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            description= ':warning: You need `Manage Messages` permission in order to execute this command.',
            color = discord.Colour.blurple()
        )
        await ctx.respond(embed= embed, ephemeral= True)
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(error)
    else:
        raise error


# Ping command:
@bot.command(description="Sends the bot's latency")
async def ping(ctx):
    embed = discord.Embed(
        description = f":gear: Latency is {bot.latency * 1000} ms.",
        color = discord.Colour.blurple()
    )
    await ctx.respond(embed = embed, ephemeral= True)


# Ban command:
@bot.slash_command(name='tarsban', description='TARS will ban a selected member from the server')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: Option(discord.Member, description='Select a user to TARS-ban'),
              reason: Option(str, description='Any reason?', required=False)):
    if member.id == ctx.author.id:
        await ctx.respond(
            "Are you okay, little boy? As much as I'd like to do this, banning yourself would make you look more stupid than you already are. AND, I don't want to hurt you. :)")
    elif member.guild_permissions.administrator:
        embed = discord.Embed(
            description=":warning: You can't ban someone with `Administrator` permission.",
            color = discord.Colour.blurple()
        )
        await ctx.respond(embed = embed)
    elif member.id == {bot.user.id}:
        await ctx.respond("Nice try but I won't fall for any of your tricks.")
    else:
        if reason == None:
            reason = f"No reason provided by {ctx.author}."
        await member.ban(reason=reason)
        embed = discord.Embed(
            description=  f":white_check_mark: Operation Successful, <@{member.id}> was banned.\nReason: {reason}\nAction taken by: <@{ctx.author.id}>",
            color = discord.Colour.blurple()
        )
        await ctx.send(embed = embed)

# Ban error handling:
@ban.error
async def banerror(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            description = ':warning: You need `Ban Members` permission in order to execute this command.',
            color = discord.Colour.blurple()
        )
        await ctx.respond(embed = embed, ephemeral= True)
    else:
        embed = discord.Embed(
            description= ':question: Something went wrong, please re-run the command.',
            color = discord.Colour.blurple()
        )
        await ctx.respond(embed = embed)
        raise error


# Kick command:
@bot.slash_command(name='tarskick', description='TARS will kick a selected member from the server')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: Option(discord.Member, description='Select a user to TARS-kick'),
               reason: Option(str, description='Any reason?', required=False)):
    if member.id == ctx.author.id:
        await ctx.respond("You could just leave the server you know.")
    elif member.guild_permissions.administrator:
        embed = discord.Embed(
            description= ":warning: You can't kick someone with `Administrator` permission.",
            color = discord.Colour.blurple()
        )
        await ctx.respond(embed = embed)
    elif member.id == {bot.user}:
        ctx.respond("Nice try but I won't fall for any of your tricks.")
    else:
        if reason == None:
            reason = f"No reason provided by {ctx.author}."
        else:
            await member.kick(reason=reason)
            embed = discord.Embed(
                description= f":white_check_mark: Operation Successful, <@{member.id}> was kicked.\nReason: {reason}\nAction taken by: <@{ctx.author.id}>",
                color = discord.Colour.blurple()
            )
            await ctx.send(embed = embed)

# Kick error handling:
@kick.error
async def kickerror(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            description= ':warning: You need `Kick Members` permission in order to execute this command.',
            color = discord.Colour.blurple()
        )
        await ctx.respond(embed = embed, ephemeral= True)
    else:
        embed = discord.Embed(
            description= ':question: Something went wrong, please re-run the command.',
            color = discord.Colour.blurple()
        )
        await ctx.respond(embed = embed)
        raise error


# Timeout command:
@bot.slash_command(name='tarstimeout', description='TARS will timeout a selected member for a specified time')
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: Option(discord.Member, description='Select a user to TARS-timeout'),
                  reason: Option(str, description='Any reason?', required=False),
                  days: Option(int, default=0, required=False), hours: Option(int, default=0, required=False),
                  minutes: Option(int, default=0, required=False), seconds: Option(int, default=0, required=False)):
    if member.id == ctx.author.id:
        await ctx.respond("You can't timeout yourself. Instead, try shutting up.")
    elif member.guild_permissions.moderate_members or member.guild_permissions.administrator:
        embed = discord.Embed(
            description= ":warning: You can't timeout a moderator or someone with `Administrator` permission.",
            color = discord.Colour.blurple()
        )
        ctx.respond(embed = embed)
    elif member.id == {bot.user}:
        ctx.respond("Nice try but I won't fall for any of your tricks.")

    if days == None:
        days = 0
    elif hours == None:
        hours = 0
    elif minutes == None:
        minutes = 0
    elif seconds == None:
        seconds = 0
    duration = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds, )
    if reason == None:
        await member.timeout_for(duration)
        embed = discord.Embed(
            description=  f":white_check_mark: Operation Successful, <@{member.id}> was timeout for {days} day(s), {hours} hour(s), {minutes} minute(s), and {seconds} second(s).\nReason: None\nAction taken by: <@{ctx.author.id}>",
            color = discord.Colour.blurple()
        )
        await ctx.send(embed = embed)
    else:
        await member.timeout_for(duration, reason=reason)
        embed = discord.Embed(
            description=  f":white_check_mark: Operation Successful, <@{member.id}> was timeout for {days} day(s), {hours} hour(s), {minutes} minute(s), and {seconds} second(s).\nReason: {reason}\nAction taken by: <@{ctx.author.id}>",
            color = discord.Colour.blurple()
        )
        await ctx.send(embed = embed)

# Timeout error handling:
@timeout.error
async def timeouterror(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            description= ':warning: You need `Moderate Members` permission or higher in order to execute this command.',
            color = discord.Colour.blurple()
        )
        await ctx.respond(embed = embed, ephemeral= True)
    else:
        embed = discord.Embed(
            description=':question: Something went wrong, please re-run the command.',
            color=discord.Colour.blurple()
        )
        await ctx.respond(embed=embed)
        raise error


# Help command:
@bot.slash_command(name='help', description="Lists all of TARS' protocols/commands")
async def help(ctx):
    embed = discord.Embed(
        title = 'Commands & Protocols',
        description = "Here's a list of all my commands and protocols that you can use.",
        color = discord.Colour.blurple()
    )
    embed.add_field(name = '**__:lock: Moderation & Security :lock: :__**', value = 'This section provides all the information about all moderation commands TARS provides (more commands under development and will be added soon).', inline=False)
    embed.add_field(name = '`/purge`:', value = 'Used to purge a selected number of messages from the channel the command is executed in.', inline= False)
    embed.add_field(name = '`/tarstimeout`:', value = 'TARS will timeout a selected user for a selected number of time (providing reason and time is optional).', inline= False)
    embed.add_field(name = '`/tarskick`:', value = 'TARS will kick a selected user from the server for a given reason (reason is optional).', inline= False)
    embed.add_field(name = '`/tarsban`:', value = 'TARS will ban a selected user from the server for a provided reason (optional).', inline= False)
    embed.add_field(name = '`/ping`:', value = "*This command is mainly made for the dev team.* Shows the bot's latency.", inline= False)

    embed.add_field(name = ':robot:', value = '**------------------------------------------------------------------**' , inline = False)

    embed.add_field(name = '**__:champagne_glass: Miscellaneous :champagne_glass: :__**', value = 'This section provides all the information about all miscellaneous commands TARS offers.', inline = False)
    embed.add_field(name = '`/greet`:', value = 'Feeling friendly? Say hi to TARS using this command!', inline = False)
    embed.add_field(name = '`/gtn`:', value = 'Play Guess-the-Number with TARS. TARS will ask you to enter your guess as you run the `/gtn` command. The number is chosen randomly by TARS and it lies between 1 and 10.', inline = False)

    embed.add_field(name=':robot:', value = '**------------------------------------------------------------------**', inline=False)

    embed.set_footer(text = 'To be updated from time to time.')
    embed.set_thumbnail(url='https://img.buzzfeed.com/buzzfeed-static/static/2018-03/12/6/asset/buzzfeed-prod-fastlane-01/sub-buzz-27470-1520850106-8.jpg?downsize=600:*&output-format=auto&output-quality=auto')
    await ctx.respond(embed=embed)


# Guess-the-Number command:
@bot.command(description='Play Guess-the-Number with TARS')
async def gtn(ctx, guess: Option(int, description='Try to guess a number between 1 and 10', required=True)):
    number = random.randint(1, 10)
    if guess == number:
        embed = discord.Embed(
            description= f":white_check_mark: Congratulations! You guessed it.",
            color = discord.Colour.blurple()
        )
        await ctx.respond(embed = embed)
    else:
        embed = discord.Embed(
            description= f":warning: Incorrect guess, try again.",
            color = discord.Colour.blurple()
        )
        await ctx.respond(embed = embed, ephemeral=True)



bot.run(token)
