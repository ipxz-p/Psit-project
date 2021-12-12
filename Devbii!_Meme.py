#918805504745152553 client
#OTE4ODA1NTA0NzQ1MTUyNTUz.YbMmTg.zaNd2jAiZ7UAw5yXnkVesmdCCnI token
#8

import discord
from discord import message
from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import os
import aiohttp
import random
import json
from requests import get

bot = commands.Bot(command_prefix='+', help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

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
        emBed = discord.Embed(title='You got this!!', color=0x66CDAA)
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
        emBed = discord.Embed(title='You got this!! Meow ˄·͈༝·͈˄', color=0x66CDAA)
        emBed.set_image(url=rdmeme)
        await ctx.channel.send(embed=emBed)

@bot.command()
async def dog(ctx):
    async with aiohttp.ClientSession() as session:
        content = []
        url = 'https://www.pinterest.ca/dogsareloveon4legs/dog-memes/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        images = soup.find_all('img')
        for image in images:
            content.append(image['src'])
        rdmeme = random.choice(content)
        emBed = discord.Embed(title='You got this!! Ruff U ´ᴥ` U', color=0x66CDAA)
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
        emBed = discord.Embed(title='You got this!!', color=0x66CDAA)
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
        emBed = discord.Embed(title='You got this!! aroom-joh', color=0x66CDAA)
        emBed.set_image(url=rdmeme)
        await ctx.channel.send(embed=emBed)


@bot.command()
async def help(ctx):#help #test #send
    emBed = discord.Embed(title='Tutorial Bot help', description='All available bot command', color=0x66CDAA)
    emBed.add_field(name='help', value='Get help command', inline=False)
    emBed.add_field(name='test', value='Respond message that you\'ve send', inline=False)
    emBed.add_field(name='send', value='Send hello message to user', inline=False)
    emBed.set_thumbnail(url='https://variety.com/wp-content/uploads/2021/07/Rick-Astley-Never-Gonna-Give-You-Up.png')
    emBed.set_footer(text='test help command', icon_url='https://variety.com/wp-content/uploads/2021/07/Rick-Astley-Never-Gonna-Give-You-Up.png')
    await ctx.channel.send(embed=emBed)


bot.run('OTE4ODA1NTA0NzQ1MTUyNTUz.YbMmTg.zaNd2jAiZ7UAw5yXnkVesmdCCnI')