
import discord
from discord.ext import commands
import googletrans
from googletrans import Translator
from songs import songAPI
from discord.utils import get
import asyncio
import os
import aiohttp
import random
import json
import requests
from requests import get
from bs4 import BeautifulSoup


bot = commands.Bot(command_prefix='\\', help_command=None)

@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name=f"\help"))

@bot.command()
async def translate(ctx):
    t = Translator()
    a = t.translate(ctx, dest="hi")
    print(a.text)


@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason=None):
    embed = discord.Embed(title="Kick user", description="`%s` You are engraved on our memory forever."%(member), color=0x5865F2)
    embed.set_author(name = 'buh bye~', icon_url = 'https://cdn.discordapp.com/emojis/786631842710159411.gif?size=64')
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
    await ctx.channel.send(embed=embed)
    await member.kick(reason=reason)

@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason=None):
    embed = discord.Embed(title="Ban user", description="`%s` Omae wa mou shindeiru!!"%(member), color=0x5865F2)
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
        embed = discord.Embed(title="Unban user", description="`%s` I'm so sorry but not my fault."%(user), color=0x5865F2)
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
    embed = discord.Embed(title="You can\'t type in this channel", color=0x5865F2)
    embed.set_author(name = 'Devbii! Lock', icon_url = 'https://cdn.discordapp.com/emojis/786631852931940382.gif?size=64')
    embed.set_image(url = 'https://gifimage.net/wp-content/uploads/2018/11/thinking-emoji-gif-transparent-2.gif')
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.channel.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_channels = True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    embed = discord.Embed(title="You can type in this channel", color=0x5865F2)
    embed.set_author(name = 'Devbii! Unlock', icon_url="https://cdn.discordapp.com/emojis/785476061738827796.gif?size=64")
    embed.set_image(url = 'https://c.tenor.com/cAppw2WmFSoAAAAi/long-livethe-blob-its-all-good.gif')
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
    await ctx.channel.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title=":x: Invalid command used.", description= ":white_small_square: Use `\help` to see a list of all commands.", color=0xff0000)
        await ctx.channel.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title=":x: You can't use this `command.`", description= "You don't have permissions to use this command.", color=0xff0000)
        await ctx.channel.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=":x: Try again", color=0xff0000)
        await ctx.channel.send(embed=embed)
    if isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=":thinking: Who?", color=0xff0000, description= "I can't find that member. try again")
        await ctx.channel.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Devbii!'s Command List", description=":white_small_square: Prefix `\\`", color=0x5865F2)
    embed.add_field(name=':wrench: Administrator', value="> `kick`, `ban`, `unban`, `lock`, `unlock`, `clear`" , inline = False)
    embed.add_field(name=':guitar: Music', value="> `play`, `pause`, `resume`, `leave`, `skip`, `queue`", inline = False)
    embed.add_field(name=':mag: Translate', value="> `tr`, `langcode`", inline = False)
    embed.add_field(name=':rofl: Meme', value="> `meme`, `cat`, `dog`, `alpaca`, `hamster`", inline=0)
    embed.add_field(name=':keyboard: Wrong Word',value="> `re`" , inline=0)
    embed.add_field(name=':lips: Text To Speech',value="> `tts`" , inline=0)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
    await ctx.channel.send(embed=embed)

songsearch = songAPI()


@bot.command()
async def tr(ctx, lang, *, thing):
    translator = Translator()
    translation = translator.translate(thing, dest=lang)
    embed=discord.Embed(title=' ',description=' ',color=0x5865F2)#    embed.add_field(name='Text', value='**`{}`**'.format(thing), inline=True)
    embed.add_field(name=lang.upper(), value='**`{}`**'.format(translation.text), inline=True)
    embed.set_author(name="Devbii! Translate", icon_url='https://media.giphy.com/media/HVofJOWFXGpDX4xeg1/giphy.gif')
    embed.set_footer(icon_url = ctx.author.avatar_url,text="Requested by: {}".format(ctx.author))
    await ctx.send(embed=embed)

@bot.command()
async def re(ctx, *, word):
    show = ': '
    countt = ''
    my_eng = ['1','2','3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '?', 'a', 's'\
    'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '//', '!', '@', '#', '$', '%', '^', '&', '*', '(', \
    '_', '+', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"', 'Z', 'X', 'C',
    'V', 'B', 'N', 'M', '<', '>', '?']
    my_th = ['+', '๑', '๒', '๓', '๔', 'ู', '฿', '๕', '๖', '๗', '๘', '๙', '๐', '"', 'ฎ', 'ฑ', 'ธ', 'ํ', '๊', 'ณ' , 'ฯ', 'ญ', 'ฐ',
    ',', 'ฤ', 'ฆ', 'ฏ', 'โ', 'ฌ', '็', '๋', 'ษ', 'ศ', 'ซ', '.', '(', ')', 'ฉ', 'ฮ', 'ฺ', '์', '?', 'ฒ', 'ฬ', 'ฦ', 'ๅ', '/', '-', 'ภ',\
    'ถ', 'ุ', 'ึ', 'ค','ต', 'จ', 'ข', 'ช', 'ๆ', 'ไ', 'ำ', 'พ', 'ะ', 'ั', 'ี', 'ร', 'น', 'ย', 'บ', 'ล', 'ฃ', 'ฟ', 'ห', 'ก','ด', \
    'เ', '้', '่', 'า', 'ส', 'ว', 'ง', 'ผ', 'ป', 'แ', 'อ', 'ิ', 'ื', 'ท', 'ม', 'ใ', 'ฝ']
    my_dictionary_eng = {' ':' ', '1':'ๅ','2':'/','3':'-','4':'ภ','5':'ถ','6':'ุ','7':'ึ','8':'ค','9':'ต','0':'จ','-':'ข','=':'ช',\
        'q':'ๆ','w':'ไ','e':'ำ','r':'พ','t':'ะ','y':'ั','u':'ี','i':'ร', 'o':'น','p':'ย','[':'บ',']':'ล','\\':'ฃ','a':'ฟ','s':'ห',\
        'd':'ก','f':'ด','g':'เ','h':'้','j':'่','k':'า','l':'ส',';':'ว','\'':'ง', 'z':'ผ', 'x':'ป', 'c':'แ', 'v':'อ', 'b':'ิ',\
        'n':'ื', 'm':'ท', ',':'ม','.':'ใ', '/':'ฝ',\
        '!':'+', '@':'๑', '#':'๒', '$':'๓', '%':'๔', '^':'ู', '&':'฿', '*':'๕', '(':'๖', ')':'๗', '_':'๘', '+':'๙',\
        'Q':'๐', 'W':'\"', 'E':'ฎ', 'R':'ฑ', 'T':'ธ', 'Y':'ํ', 'U':'๊', 'I':'ณ', 'O':'ฯ', 'P':'ญ', '{':'ฐ', '}':',', '|':'ฅ',\
        'A':'ฤ', 'S':'ฆ', 'D':'ฏ', 'F':'โ', 'G':'ฌ', 'H':'็', 'J':'๋','K':'ษ', 'L':'ศ', ':':'ซ', '\"':'.', 'Z':'(', \
        'X':')', 'C':'ฉ', 'V':'ฮ', 'B':'ฺ', 'N':'์', 'M':'?', '<':'ฒ', '>':'ฬ', '?':'ฦ'}
    my_dictionary_th = dict([(value, key) for key, value in my_dictionary_eng.items()])
    for i in word:
        if i in my_eng:
            countt += 'e'
        if i in my_th:
            countt += 't'
    if countt.count('e') > countt.count('t'):
        for i in word:
            show += my_dictionary_eng[i]
    elif countt.count('e') < countt.count('t'):
        for i in word:
            show += my_dictionary_th[i]
    embed = discord.Embed(title=word, description=show, color=0x5865F2)
    embed.set_author(name="Devbii! PIMPID", icon_url='https://media.giphy.com/media/11BbGyhVmk4iLS/giphy.gif')
    embed.set_footer(icon_url = ctx.author.avatar_url,text="Requested by: {}".format(ctx.author))
    await ctx.send(embed=embed)


@bot.command()
async def langcode(ctx):
    embed1 = discord.Embed(title='Code (1)', color=0x5865F2)
    embed1.set_author(name = 'Devbii! Language Code', icon_url = 'https://media.giphy.com/media/HVofJOWFXGpDX4xeg1/giphy.gif')
    embed1.add_field(name='af', value='Afrikaans')
    embed1.add_field(name='ar', value='Arabic')
    embed1.add_field(name='az', value='Azeri (Latin)')
    embed1.add_field(name='be', value='Belarusian')
    embed1.add_field(name='bg', value='Bulgarian')
    embed1.add_field(name='ca', value='Catalan')
    embed1.add_field(name='cs', value='Czech')
    embed1.add_field(name='cy', value='Welsh')
    embed1.add_field(name='da', value='Danish')
    embed1.add_field(name='de', value='German')
    embed1.add_field(name='el', value='Greek')
    embed1.add_field(name='en', value='English')
    embed1.add_field(name='eo', value='Esperanto')
    embed1.add_field(name='es', value='Spanish')
    embed1.add_field(name='et', value='Estonian')
    embed1.add_field(name='eu', value='Basque')
    embed1.add_field(name='fa', value='Farsi')
    embed1.add_field(name='fi', value='Finnish')
    embed1.add_field(name='fr', value='French')
    embed1.add_field(name='gl', value='Galician')
    embed1.add_field(name='gu', value='Gujarati')
    embed1.add_field(name='he', value='Hebrew')
    embed1.add_field(name='hi', value='Hindi')
    embed1.add_field(name='hr', value='Croatian')
    embed2 = discord.Embed(title='Code (2)', color=0x5865F2)
    embed2.add_field(name='hu', value='Hungarian')
    embed2.add_field(name='hy', value='Armenian')
    embed2.add_field(name='id', value='Indonesian')
    embed2.add_field(name='is', value='Icelandic')
    embed2.add_field(name='it', value='Italian')
    embed2.add_field(name='ja', value='Japanese')
    embed2.add_field(name='ka', value='Georgian')
    embed2.add_field(name='kk', value='Kazakh')
    embed2.add_field(name='kn', value='Kannada')
    embed2.add_field(name='ko', value='Korean')
    embed2.add_field(name='ky', value='Kyrgyz')
    embed2.add_field(name='lt', value='Lithuanian')
    embed2.add_field(name='lv', value='Latvian')
    embed2.add_field(name='mi', value='Maori')
    embed2.add_field(name='mk', value='Macedonian')
    embed2.add_field(name='mn', value='Mongolian')
    embed2.add_field(name='ms', value='Malay')
    embed2.add_field(name='mt', value='Maltese')
    embed2.add_field(name='nl', value='Dutch')
    embed2.add_field(name='pa', value='Punjabi')
    embed2.add_field(name='pl', value='Polish')
    embed2.add_field(name='ps', value='Pashto')
    embed2.add_field(name='pt', value='Portuguese')
    embed2.add_field(name='ro', value='Romanian')
    embed3 = discord.Embed(title='Code (3)', color=0x5865F2)
    embed3.add_field(name='ru', value='Russian')
    embed3.add_field(name='sk', value='Slovak')
    embed3.add_field(name='sl', value='Slovenian')
    embed3.add_field(name='sq', value='Albanian')
    embed3.add_field(name='sv', value='Swedish')
    embed3.add_field(name='sw', value='Swahili')
    embed3.add_field(name='ta', value='Tamil')
    embed3.add_field(name='te', value='Telugu')
    embed3.add_field(name='th', value='Thailand')
    embed3.add_field(name='tl', value='Tagalog')
    embed3.add_field(name='tr', value='Turkish')
    embed3.add_field(name='uk', value='Ukrainian')
    embed3.add_field(name='ur', value='Urdu')
    embed3.add_field(name='uz', value='Uzbek (Latin)')
    embed3.add_field(name='vi', value='Vietnamese')
    embed3.add_field(name='xh', value='Xhosa')
    embed3.add_field(name='zh-CN', value='Chinese')
    embed3.add_field(name='zu', value='Zulu')
    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)
    await ctx.send(embed=embed3)

@bot.command()
async def meme(ctx):
    async with aiohttp.ClientSession() as session:
        content = []
        url = 'https://www.pinterest.com/daemewz/memes/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        images = soup.find_all('img')
        for image in images:
            content.append(image['src'])
        rdmeme = random.choice(content)
        emBed = discord.Embed(title='You got this!!', color=0x5865F2)
        emBed.set_image(url=rdmeme)
        await ctx.channel.send(embed=emBed)

@bot.command()
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        content = []
        url = 'https://www.pinterest.com/abcaom123/meme-cat/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        images = soup.find_all('img')
        for image in images:
            content.append(image['src'])
        rdmeme = random.choice(content)
        emBed = discord.Embed(title='You got this!! Meow ˄·͈༝·͈˄', color=0x5865F2)
        emBed.set_image(url=rdmeme)
        await ctx.channel.send(embed=emBed)

@bot.command()
async def dog(ctx):
    async with aiohttp.ClientSession() as session:
        content = []
        url = 'https://www.pinterest.com/jrvm1027/funny-dog-faces/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        images = soup.find_all('img')
        for image in images:
            content.append(image['src'])
        rdmeme = random.choice(content)
        emBed = discord.Embed(title='You got this!! Ruff U ´ᴥ` U', color=0x5865F2)
        emBed.set_image(url=rdmeme)
        await ctx.channel.send(embed=emBed)

@bot.command()
async def hamster(ctx):
    async with aiohttp.ClientSession() as session:
        content = []
        url = 'https://www.pinterest.com/unicornamelia24/hamster-memes/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        images = soup.find_all('img')
        for image in images:
            content.append(image['src'])
        rdmeme = random.choice(content)
        emBed = discord.Embed(title='You got this!!', color=0x5865F2)
        emBed.set_image(url=rdmeme)
        await ctx.channel.send(embed=emBed)

@bot.command()
async def alpaca(ctx):
    async with aiohttp.ClientSession() as session:
        content = []
        url = 'https://www.pinterest.com/rongsupanprompon/%E0%B8%AD%E0%B8%A3%E0%B8%A1%E0%B9%80%E0%B8%88%E0%B8%B2%E0%B8%B0/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        images = soup.find_all('img')
        for image in images:
            content.append(image['src'])
        rdmeme = random.choice(content)
        emBed = discord.Embed(title='You got this!! aroom-joh', color=0x5865F2)
        emBed.set_image(url=rdmeme)
        await ctx.channel.send(embed=emBed)

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def tts(ctx, *, thing):
    channel = ctx.author.voice.channel
    if (ctx.voice_client):
        await ctx.send(thing, tts=True)
    else:
        await channel.connect()
        await ctx.send(thing, tts=True)

@bot.command()
async def play(ctx,* ,search: str):
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

@bot.event
async def on_message(message):
    await bot.process_commands(message)

bot.run(input())
#input your token
