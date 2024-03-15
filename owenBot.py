import pandas as pd
import numpy as np
import os
from project_script import *
import yt_dlp

user_last_message_time = {}

###################################################################################
'''                            datascience stuff                                '''
###################################################################################

def artist_count(artist):
    '''returns count of artists in artist list'''
    artist = artist.lower()
    if artist in all_artist_list_lower:
        #artist_count_list = pd.Series(all_artist_list_lower).value_counts()
        #artist_count_list.columns = ['Artist', 'Count']
        return artist_count_list.get(artist)
    else:
        return None

def get_artist_albums(artist):
    '''makes new table with album - artist column and returns a list of that column joined by \n format'''
    rave_useralbum = raw_rave_albums.drop('Album', axis=1)
    rave_useralbum['Album - Artist'] = rave_with_useralbum
    rave_useralbum['lower artist'] = all_artist_list_lower
    albums = rave_useralbum[rave_useralbum['lower artist'] == artist.lower()]['Album - Artist']
    return '\n'.join(albums.tolist())

user_list = ['Moonlit Warrior Ortvgal', 'Nate', 'Swegify', 'gabriel', 'hobo',
       'terriyaki', 'z33p', 'zym', 'Kaotic', 'Theo', 'owen', 'jwebb',
       'lego', 'liv', 'DCDUKE', 'glootte', 'gregory', '*ant', 'Bacchus',
       'terry', 'Ciel', 'Tomato', 'Ultra', 'Clock', 'HondaS2000', 'oliver',
       'corphish', 'jahquavious', 'kylebruh', 'seraphiel', 'BigToz',
       'Don-Q', 'Luihi', 'Tattertoff', 'terry j', 'Lele', 'aliyah', 'big',
       'Armani', 'Trinity', 'julia', 'lemon', 'Damon', 'TatterToff',
       'gogurt', 'land_on', 'Райан К (???)']

user_list_lower = [word.lower() for word in user_list]

user_submit_count = [14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 11, 11, 11, 10, 10, 10,
        9,  8,  8,  7,  7,  7,  6,  6,  6,  5,  5,  5,  5,  4,  4,  4,  4,
        4,  3,  3,  3,  2,  2,  2,  2,  1,  1,  1,  1,  1]

def user_submits(user):
    '''returns count of user's submits given user'''
    user_lower = user.lower()
    if user_lower in user_list_lower:
        return user_submit_count[user_list_lower.index(user_lower)]
    else:
        return None

###################################################################################
'''                                commands                                     '''
###################################################################################

import discord
from discord.ext import commands
import discord
import yt_dlp

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot_prefix = "r!"
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

'''@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif 'rave' in message.content.lower():
        await message.channel.send('hey')'''

@bot.command()
async def user(ctx, *, data=None):
    '''returns information about a user'''
    if data == None:
        await ctx.send('Enter the Discord username of the person you would like to view info about.')
    else:
        if data.lower() in user_list_lower:
            user_submit = user_submits(data)
            await ctx.send(data + ' has submitted ' + str(user_submit) + ' album(s) in the Rave album swaps.')
        else:
            await ctx.send('User "' + data + '" either has not submitted an album or doesn\'t exist')

@bot.command()
async def artist(ctx, *, data=None):
    '''returns information about an artist'''
    if data == None:
        await ctx.send('Enter the artist/band you would like to view info about (ex: r!artist Alex G).')
    else:
        if data.lower() in all_artist_list_lower:
            await ctx.send('```' + data + ' has been submitted ' + str(artist_count(data)) + ' time(s) in the Rave album swaps.\n\nAlbums submitted by ' + data + ':\n\n' + str(get_artist_albums(data)) + '```')
        else:
            await ctx.send('Artist "' + data + '" either has not been submitted or doesn\'t exist')

@bot.command()
async def userlist(ctx):
    '''returns a list of users who have submitted'''
    nice_list = ', '.join(user_list)
    await ctx.send('__Users that have submitted albums in album swaps:__\n' + str(nice_list))

@bot.command()
async def topusers(ctx):
    '''returns top 10 users with most submits'''
    nice_list = ', '.join(user_list[:10])
    await ctx.send('__Top ten users with most album swap submits:__\n' + str(nice_list))

is_enabled = False

@bot.command()
async def toggle(ctx):
    '''toggles the bot's ability to judge zeep's posts'''
    global is_enabled
    is_enabled = not is_enabled
    print('Toggle command called')
    await ctx.send(f"zeep's posts will {'now' if is_enabled else 'not'} be judged")

@bot.command()
async def join(ctx):
    """Joins the voice channel of the user who invoked the command"""
    if ctx.author.voice is None:
        await ctx.send("ur not in a vc dumbass")
        return

    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)

    await ctx.send(f"get fucking ready {voice_channel}")

@bot.command()
async def leave(ctx):
    """Leaves the voice channel that the bot is currently in"""
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("BYEEEEEEE")
    else:
        await ctx.send("?????????")

@bot.command()
async def play(ctx, url=None, volume:float=0.1, loop:bool=True):
    """Plays from a url (almost anything yt_dlp supports)"""
    if url is None:
        await ctx.send("put a url")
        return

    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("erm.")
            return
    else:
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    vc = ctx.voice_client

    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        vc.play(discord.FFmpegPCMAudio(url2, **FFMPEG_OPTIONS), after=lambda e: loop and ctx.invoke(bot.get_command('play'), url=url, volume=volume, loop=loop))
        vc.is_playing()
        await ctx.send("Now playing: " + info['title'])

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author.name == '.z33p' and is_enabled and message.attachments:
        upvote_emoji = discord.utils.get(bot.emojis, name="upvote")
        downvote_emoji = discord.utils.get(bot.emojis, name="downvote")
        await message.add_reaction(upvote_emoji)
        await message.add_reaction(downvote_emoji)
    await bot.process_commands(message)


bot.run('...')
