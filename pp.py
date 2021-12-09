#895321854556930099 client id
#ODk1MzIxODU0NTU2OTMwMDk5.YV23dA.7kBkE9FcOcMl7k8LdnoENasEZJU Token
#534723950656 permission int

import discord
from discord.utils import get
from discord.ext import commands
from datetime import datetime, timedelta
from songs import songAPI




bot = commands.Bot(command_prefix='?',help_command=None)

songsearch = songAPI()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

import requests
from googletrans import Translator

@bot.command()
async def tr(ctx, lang, *, thing):
    translator = Translator()
    translation = translator.translate(thing, dest=lang)
    embed=discord.Embed(title=' ',description=' ',color=0x52adeb)
    embed.add_field(name='Input', value='**`{}`**'.format(thing.capitalize()), inline=True)
    embed.add_field(name='Translated', value='**`{}`**'.format(translation.text.capitalize()), inline=True)
    embed.set_author(name="Devbii! Translate", icon_url='https://media.giphy.com/media/HVofJOWFXGpDX4xeg1/giphy.gif')
    embed.set_footer(icon_url = ctx.author.avatar_url,text="Requested by: {}".format(ctx.author))
    await ctx.send(embed=embed)


@bot.command()
async def p(ctx,* ,search: str):
    await songsearch.play(ctx, search)

@bot.command()
async def stop(ctx):
    await songsearch.stop(ctx)

@bot.command()
async def pause(ctx):
    await songsearch.pause(ctx)

@bot.command()
async def resume(ctx):
    await songsearch.resume(ctx)

@bot.command()
async def leave(ctx):
    await songsearch.leave(ctx)

@bot.command()
async def queue(ctx):
    await songsearch.queue(ctx)

@bot.command()
async def skip(ctx):
    await songsearch.skip(ctx)


@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason=None):
    embed = discord.Embed(title="Kick user", description="`%s` You are engraved on our memory forever."%(member), color=0x13f2f2)
    embed.set_author(name = 'buh bye~', icon_url = 'https://cdn.discordapp.com/emojis/786631842710159411.gif?size=64')
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
    await ctx.channel.send(embed=embed)
    await member.kick(reason=reason)

@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason=None):
    embed = discord.Embed(title="Ban user", description="`%s` Omae wa mou shindeiru!!"%(member), color=0x13f2f2)
    embed.set_author(name = 'You got this!!', icon_url = 'https://cdn.discordapp.com/emojis/785477060679958578.gif?size=64')
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
    await ctx.channel.send(embed=embed)
    await member.ban(reason=reason)

@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban in banned_users:
        user = ban.user
        embed = discord.Embed(title="Unban user", description="`%s` I'm so sorry but not my fault."%(user), color=0x13f2f2)
        embed.set_author(name = 'Welcome back homie.', icon_url = 'https://cdn.discordapp.com/emojis/786631852931940382.gif?size=64')
        embed.set_thumbnail(url = user.avatar_url)
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.channel.send(embed=embed)
            await ctx.guild.unban(user)
            return

@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount=0):
    await ctx.channel.purge(limit=amount)

@bot.command()
@commands.has_permissions(manage_channels = True)
async def lock(ctx):
    embed = discord.Embed(title="Locked room", color=0x13f2f2)
    embed.set_author(name = 'ไม่ให้พิมพ์เเน้ววววว', icon_url = 'https://cdn.discordapp.com/emojis/786631852931940382.gif?size=64')
    embed.set_image(url = 'https://gifimage.net/wp-content/uploads/2018/11/thinking-emoji-gif-transparent-2.gif')
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.channel.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_channels = True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send('พิมพ์ได้เเย้ววววว')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title=":x: Invalid command used.", description= ":white_small_square: Use `\help` to see a list of all commands.", color=0xff0000)
        await ctx.channel.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title=":x: You can't use this `command.`", description= "You don't have permissions to use this command.", color=0xff0000)
        await ctx.channel.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=":x: Try again", color=0xff0000, description= "Type `\help` to see command list. for correct usage")
        await ctx.channel.send(embed=embed)
    if isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=":thinking: Who?", color=0xff0000, description= "I can't find that member. try again")
        await ctx.channel.send(embed=embed)

@bot.event
async def on_message(message):
    await bot.process_commands(message)
bot.run("ODk1MzIxODU0NTU2OTMwMDk5.YV23dA.7kBkE9FcOcMl7k8LdnoENasEZJU")
