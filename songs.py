import discord
from discord.utils import get
import youtube_dl
import asyncio
from async_timeout import timeout
from functools import partial
import itertools
from discord.ext import commands

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')


    def __getitem__(self, item: str):

        return self.__getattribute__(item)

class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')


    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            data = data['entries'][0]

        await ctx.send(f'```ini\nเพิ่ม {data["title"]} เข้ามาในคิว\n```') 

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source, **ffmpeg_options), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url'], **ffmpeg_options), data=data, requester=requester)

class MusicPlayer:

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:

                async with timeout(300):
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                del [self._guild]
                return await self.destroy(self._guild)

            if not isinstance(source, YTDLSource):

                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'ไม่สามารถเล่นได้.\n'
                                        f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(f'**กำลังเล่น:** `{source.title}` ขอโดย '
                                            f'`{source.requester}`')
            await self.next.wait()

            source.cleanup()
            self.current = None

            try:
                await self.np.delete()
            except discord.HTTPException:
                pass

    async def destroy(self, guild):
        await self._guild.voice_client.disconnect()
        return self.bot.loop.create_task(self._cog.cleanup(guild))

class songAPI:
    def __init__(self):
        self.players = {}

    async def play(self, ctx,search: str):
        self.bot = ctx.bot
        self._guild = ctx.guild
        channel = ctx.author.voice.channel
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client == None:
            await ctx.channel.send("สวัสดีจ้า")
            await channel.connect()
            voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        await ctx.trigger_typing()

        _player = self.get_player(ctx)
        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await _player.queue.put(source)


    players = {}
    def get_player(self, ctx):
        try:
            player = self.players[ctx.guild.id]
        except:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player


    async def stop(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client == None:
            await ctx.channel.send("น้องไม่ได้เชื่อมต่อกับ vc")
            return

        if voice_client.channel != ctx.author.voice.channel:
            await ctx.channel.send("ตอนนี้น้องกำลังเชื่อต่อ {0}".format(voice_client.channel))
            return

        voice_client.stop()

    async def pause(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client == None:
            await ctx.channel.send("น้องไม่ได้เชื่อมต่อกับ vc")
            return

        if voice_client.channel != ctx.author.voice.channel:
            await ctx.channel.send("ตอนนี้น้องกำลังเชื่อต่อ {0}".format(voice_client.channel))
            return

        voice_client.pause()

    async def resume(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client == None:
            await ctx.channel.send("น้องไม่ได้เชื่อมต่อกับ vc")
            return

        if voice_client.channel != ctx.author.voice.channel:
            await ctx.channel.send("ตอนนี้น้องอยู่ที่ {0}".format(voice_client.channel))
            return

        voice_client.resume()

    async def leave(self, ctx):
        del self.players[ctx.guild.id]
        await ctx.voice_client.disconnect()

    async def queue(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client == None or not voice_client.is_connected():
            await ctx.channel.send("น้องไม่ได้เชื่อมต่อกับ vc", delete_after=10)
            return

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send('ไม่มีเพลงเลยซักเพลง')

        upcoming = list(itertools.islice(player.queue._queue,0,player.queue.qsize()))
        fmt = '\n'.join(f'-{_["title"]}' for _ in upcoming)
        embed = discord.Embed(title=f'รายชื่อเพลงทั้งหมด {len(upcoming)} เพลงก็คือ', description=fmt, color=0x1ABC9C , delete_after=10)
        await ctx.send(embed=embed)

    async def skip(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client == None or not voice_client.is_connected():
            await ctx.channel.send("น้องไม่ได้เชื่อมต่อกับ vc", delete_after=10)
            return

        if voice_client.is_paused():
            pass
        elif not voice_client.is_playing():
            return

        voice_client.stop()
        await ctx.send(f'**`{ctx.author}`**: ขออนุญาตเปลี่ยนเพลงน้า!')
