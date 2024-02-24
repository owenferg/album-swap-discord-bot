import discord
from discord.ext import commands
import pandas as pd
import numpy as np
import os
from project_script import *

user_last_message_time = {}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot_prefix = "r!"
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

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

#FIXME MAKE HELP COMMAND

'''@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif 'rave' in message.content.lower():
        await message.channel.send('**__Rave.__**')
'''
discord_token = 'example' # paste discord token
bot.run(discord_token)
