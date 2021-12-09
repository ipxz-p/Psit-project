# 895275996314501140 CLIENT ID
# ODk1Mjc1OTk2MzE0NTAxMTQw.YV2Mvg.HQL5M4DrhK_VKxWU96A9gE0HGes Token
# 8 Permissions
#OTEyMzU2NjYxMTU3NTkzMTA4.YZuwWg.DelY4knxmnIxX0JpiVgNclZiK7o fix
import discord
from discord.ext import commands
import googletrans
from googletrans import Translator
from songs import songAPI
bot = commands.Bot(command_prefix='\\', help_command=None)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('\\help'))
    print(f"logged in as {bot.user}")

@bot.command()
async def translate(ctx):
    t = Translator()
    a = t.translate(ctx, dest="hi")
    print(a.text)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Command List", description=":white_small_square: Prefix `\\`", color=0x13f2f2)
    # embed.set_image(url = '')
    embed.add_field(name=':wrench: Administrator', value="> `\\kick @member`, `\\ban @member`, `\\unban @member`", inline = False)
    embed.add_field(name=':guitar: Music', value="> `\\p song name or link`, `\\pause`, `\\resume`, `\\leave`, `\\skip`, `\\queue`", inline = False)
    embed.add_field(name=':black_joker: Horoscope', value="> `\\hlove`, `\\hhealth`, `\\hstudy`, `\\hfinance`", inline = False)
    embed.add_field(name=':rofl: Meme', value="> kick, ban, unban")
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
    await ctx.channel.send(embed=embed)

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
    embed=discord.Embed(title=' ',description=' ',color=0x52adeb)#    embed.add_field(name='Text', value='**`{}`**'.format(thing), inline=True)
    embed.add_field(name=lang.upper(), value='**`{}`**'.format(translation.text), inline=True)
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
    await member.kick(reason=reason)

@bot.event
async def on_message(message):
    await bot.process_commands(message)
bot.run("ODk1Mjc1OTk2MzE0NTAxMTQw.YV2Mvg.HQL5M4DrhK_VKxWU96A9gE0HGes")
