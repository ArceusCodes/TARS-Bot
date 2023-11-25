import discord
import mysql.connector as sql
from discord import Option
from discord.ext.commands.errors import MissingPermissions
import os
import dotenv
import random
from discord.ext import commands
import datetime
from datetime import timedelta
from discord.ui import Select, View

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
    await ctx.respond(f"Hi there!", ephemeral=True)


# Purge command:
@bot.slash_command(name='purge', description='TARS will delete a selected number of messages in this channel')
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def purge(ctx, messages: Option(int, description="How many messages do you wish to delete?", required=True)):
    await ctx.defer()
    await ctx.channel.purge(limit=messages)
    embed = discord.Embed(
        description='<:tars_success:1055919701001252945> Channel purged.',
        color=discord.Colour.blurple()
    )
    await ctx.send(embed=embed)


# Purge error handling:
@purge.error
async def purgeerror(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            description='<:tars_error:1055912274835034194> You need `Manage Messages` permission in order to execute this command.',
            color=discord.Colour.from_rgb(232, 17, 35)
        )
        await ctx.respond(embed=embed, ephemeral=True)
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(error)
    else:
        raise error


# Ping command:
@bot.command(description="Sends the bot's latency")
async def ping(ctx):
    embed = discord.Embed(
        description=f"<:tars_gear:1055914499581943859> Latency is {bot.latency * 1000} ms.",
        color=discord.Colour.blurple()
    )
    await ctx.respond(embed=embed, ephemeral=True)


# Case command:
password = str(os.getenv("DB"))
db = sql.connect(host="localhost", user="Arceus", password=password, database="cases")

@bot.slash_command(name='file-case', description='TARS will log said user into the server watchlist.')
@commands.has_permissions(moderate_members=True)
async def filecase(ctx: discord.ApplicationContext, member: discord.Member, reason: str):
    time = str(datetime.datetime.utcnow())
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO all_cases VALUES (%s, %s, %s, %s)",
        (member.id, ctx.author.id, reason, time)
    )
    cursor.close()
    db.commit()
    embed = discord.Embed(
        description='<:tars_success:1055919701001252945> TARS has filed a case on the mentioned user.',
        color=discord.Colour.blurple()
    )
    await ctx.respond(embed=embed)


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
            description="<:tars_error:1055912274835034194> You can't ban someone with `Administrator` permission.",
            color=discord.Colour.from_rgb(232, 17, 35)
        )
        await ctx.respond(embed=embed)
    else:
        if reason == None:
            reason = f"No reason provided by {ctx.author}."
        await member.ban(reason=reason)
        embed = discord.Embed(
            description=f"<:tars_success:1055919701001252945> Operation Successful, <@{member.id}> was banned.\nReason: {reason}\nAction taken by: <@{ctx.author.id}>",
            color=discord.Colour.blurple()
        )
        await ctx.send(embed=embed)


# Ban error handling:
@ban.error
async def banerror(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            description='<:tars_error:1055912274835034194> You need `Ban Members` permission in order to execute this command.',
            color=discord.Colour.from_rgb(232, 17, 35)
        )
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            description='<:tars_question:1055912854743699597> Something went wrong, please re-run the command.',
            color=discord.Colour.dark_red()
        )
        await ctx.respond(embed=embed)
        raise error


# Unban command:
@bot.slash_command(name='unban',
                   description="TARS will unban a selected user and they'll be allowed to join the server")
@commands.has_permissions(ban_members=True)
async def unban(ctx,
                user: Option(discord.Member, description='Enter the ID of the user you wish to unban',
                             required=True)):
    await ctx.guild.unban(user)
    embed = discord.Embed(
        description=f"<:tars_success:1055919701001252945> Operation Successful, <@{user.id}> was unbanned.\nAction taken by: <@{ctx.author.id}>",
        color=discord.Colour.blurple()
    )
    await ctx.send(embed=embed)


# Kick command:
@bot.slash_command(name='tarskick', description='TARS will kick a selected member from the server')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: Option(discord.Member, description='Select a user to TARS-kick'),
               reason: Option(str, description='Any reason?', required=False)):
    if member.id == ctx.author.id:
        await ctx.respond("You could just leave the server you know.")
    elif member.guild_permissions.administrator:
        embed = discord.Embed(
            description="<:tars_error:1055912274835034194> You can't kick someone with `Administrator` permission.",
            color=discord.Colour.from_rgb(232, 17, 35)
        )
        await ctx.respond(embed=embed)
    else:
        if reason == None:
            reason = f"No reason provided by {ctx.author}."
        else:
            await member.kick(reason=reason)
            embed = discord.Embed(
                description=f"<:tars_success:1055919701001252945> Operation Successful, <@{member.id}> was kicked.\nReason: {reason}\nAction taken by: <@{ctx.author.id}>",
                color=discord.Colour.blurple()
            )
            await ctx.send(embed=embed)


# Kick error handling:
@kick.error
async def kickerror(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            description='<:tars_error:1055912274835034194> You need `Kick Members` permission in order to execute this command.',
            color=discord.Colour.from_rgb(232, 17, 35)
        )
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            description='<:tars_question:1055912854743699597> Something went wrong, please re-run the command.',
            color=discord.Colour.from_rgb(232, 17, 35)
        )
        await ctx.respond(embed=embed)
        raise error


# Timeout command:
@bot.slash_command(name='tarstimeout', description='TARS will timeout a selected member for a specified time')
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: Option(discord.Member, description='Select a user to TARS-timeout'),
                  reason: Option(str, description='Any reason?', required=False),
                  days: Option(int, default=0, required=False),
                  hours: Option(int, default=0, required=False),
                  minutes: Option(int, default=0, required=False),
                  seconds: Option(int, default=0, required=False)):
    if member.id == ctx.author.id:
        await ctx.respond("You can't timeout yourself. Instead, try shutting up.")
    elif member.guild_permissions.moderate_members or member.guild_permissions.administrator:
        embed = discord.Embed(
            description="<:tars_error:1055912274835034194> You can't timeout a moderator or someone with `Administrator` permission.",
            color=discord.Colour.from_rgb(232, 17, 35)
        )
        await ctx.respond(embed=embed)
    else:
        duration = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        if reason == None:
            reason = 'None.'
        await member.timeout_for(duration, reason=reason)
        embed = discord.Embed(
            description=f"<:tars_success:1055919701001252945> Operation Successful, <@{member.id}> was timeout for {days} day(s), {hours} hour(s), {minutes} minute(s), and {seconds} second(s).\nReason: {reason}\nAction taken by: <@{ctx.author.id}>",
            color=discord.Colour.blurple()
        )
        await ctx.send(embed=embed)


# Timeout error handling:
@timeout.error
async def timeouterror(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            description='<:tars_error:1055912274835034194> You need `Moderate Members` permission or higher in order to execute this command.',
            color=discord.Colour.from_rgb(232, 17, 35)
        )
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            description='<:tars_question:1055912854743699597> Something went wrong, please re-run the command.',
            color=discord.Colour.from_rgb(232, 17, 35)
        )
        await ctx.respond(embed=embed)
        raise error


# Lockdown command:
@bot.slash_command(name='lock', description='TARS will lock the selected channel down for everyone')
@commands.has_permissions(moderate_members=True)
async def lock(ctx, channel: Option(discord.TextChannel, description='Select a channel to lock down'),
               role: Option(discord.Role, description='Select a role to lock the selected channel for'),
               reason: Option(str, description='Any reason?', required=False)):
    await channel.set_permissions(target=role, send_messages=False)
    embed = discord.Embed(
        description=f'<:tars_success:1055919701001252945> This channel has been locked for {role}.\nReason: {reason}',
        color=discord.Colour.blurple()
    )
    await ctx.respond(embed=embed)


# Lockdown error handling:
@lock.error
async def lockdownerror(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            description='<:tars_error:1055912274835034194> You need `Moderate Members` permission or higher in order to execute this command.',
            color=discord.Colour.from_rgb(232, 17, 35)
        )
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        raise error


# Unlock command:
@bot.slash_command(name='unlock', description='TARS will unlock the selected text channel')
@commands.has_permissions(moderate_members=True)
async def unlock(ctx, channel: Option(discord.TextChannel),
                 role: Option(discord.Role, description='Select a role to unlock the channel for')):
    await channel.set_permissions(target=role, send_messages=True)
    embed = discord.Embed(
        description='<:tars_success:1055919701001252945> Channel unlocked.',
        color=discord.Color.blurple()
    )
    await ctx.respond(embed=embed)


# Unlock error handling:
@unlock.error
async def unlockerror(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            description='<:tars_error:1055912274835034194> You need `Moderate Members` permission or higher in order to execute this command.',
            color=discord.Colour.from_rgb(232, 17, 35)
        )
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        raise error


# Help command:
@bot.slash_command(name='help', description="Lists all of TARS' protocols and commands")
async def help(ctx):
    selectmenu = Select(
        options=[
            discord.SelectOption(label='Moderation & Security',
                                 emoji="<:tars_moderation:1055908963717222410>",
                                 description='Click here to see all my moderation commands'),
            discord.SelectOption(label='Miscellaneous',
                                 emoji='<:tars_misc:1056221154865582110>',
                                 description='Click here to see all my miscellaneous commands')
        ])

    async def callback(interaction):
        if interaction.user.id != ctx.author.id:
            raise error
        if selectmenu.values[0] == 'Moderation & Security':
            embed = discord.Embed(
                description="<:tars_moderation:1055908963717222410> **__Moderation Commands__** <:tars_moderation:1055908963717222410>",
                color=discord.Colour.blurple()
            )
            embed.add_field(name='<:dot:1056245841070915714> `/purge`:',
                            value='Used to purge a selected number of messages from the channel the command is executed in.',
                            inline=False)
            embed.add_field(name='<:dot:1056245841070915714> `/tarstimeout`:',
                            value='TARS will timeout a selected user for a selected number of time (providing reason and time is optional).',
                            inline=False)
            embed.add_field(name='<:dot:1056245841070915714> `/lock`',
                            value='TARS will lock a selected text channel for everyone. This will remove `Send_Messages` permission from everyone for that text channel.',
                            inline=False)
            embed.add_field(name='<:dot:1056245841070915714> ` /unlock`',
                            value='TARS will unlock a selected channel for everyone and they will be allowed to send messages.')
            embed.add_field(name='<:dot:1056245841070915714> `/tarskick`:',
                            value='TARS will kick a selected user from the server for a given reason (reason is optional).',
                            inline=False)
            embed.add_field(name='<:dot:1056245841070915714> `/tarsban`:',
                            value='TARS will ban a selected user from the server for a provided reason (optional).',
                            inline=False)
            embed.add_field(name='<:dot:1056245841070915714> `/ping`:',
                            value="*This command is mainly made for the dev team.* Shows the bot's latency.",
                            inline=False)
            embed.add_field(name='<:dot:1056245841070915714> `/unban`:',
                            value='TARS will unban a user from the server. Enter the numeric ID of the user you wish to unban.',
                            inline=False)
            await interaction.response.send_message('You chose: **Moderation & Security**',
                                                    embed=embed,
                                                    ephemeral=True)

        elif selectmenu.values[0] == 'Miscellaneous':
            embed = discord.Embed(
                description="<:tars_misc:1056221154865582110> **__Miscellaneous Commands__** <:tars_misc:1056221154865582110>",
                color=discord.Colour.blurple()
            )
            embed.add_field(name='<:dot:1056245841070915714> `/greet`:',
                            value='Feeling friendly? Say hi to TARS using this command!',
                            inline=False)
            embed.add_field(name='<:dot:1056245841070915714> `/gtn`:',
                            value='Play Guess-the-Number with TARS. TARS will ask you to enter your guess as you run the `/gtn` command. The number is chosen randomly by TARS and it lies between 1 and 10.',
                            inline=False)
            await interaction.response.send_message("You chose: **Miscellaneous**",
                                                    embed=embed,
                                                    ephemeral=True)

    selectmenu.callback = callback
    view = View()
    view.add_item(selectmenu)
    await ctx.respond("Select the specific type of commands you're looking for below:",
                      view=view)


# Guess-the-Number command:
@bot.command(description='Play Guess-the-Number with TARS')
async def gtn(ctx, guess: Option(int, description='Try to guess a number between 1 and 10', required=True)):
    number = random.randint(1, 10)
    if guess == number:
        embed = discord.Embed(
            description=f"<:tars_success:1055919701001252945> Congratulations! You guessed it.",
            color=discord.Colour.blurple()
        )
        await ctx.respond(embed=embed)
    else:
        embed = discord.Embed(
            description=f"<:tars_error:1055912274835034194> Incorrect guess, try again.",
            color=discord.Colour.from_rgb(232, 17, 35)
        )
        await ctx.respond(embed=embed, ephemeral=True)


bot.run(token)
