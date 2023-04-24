from mods import mentry
from mods import msearch
from mods import mdatabase
import os
import discord
from discord.ext import commands
import re

filepath = os.environ.get('MEMEDATAFILEPATH')
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)



@client.event
async def on_ready():
    print('Ready to eat memes NEW', client.user)


@client.command()
async def archive(ctx, *tags):
    if len(tags) > 200:
        return
    tags = list(tags)
    if re.search("^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+", tags[0]):
        link = tags.pop(0)
    else:
        link = str(ctx.message.attachments[-1])
    if 'tags' in tags:
        title = ' '.join(tags[:tags.index('tags')])
        tags = tags[tags.index('tags'):]
    else:
        title = ' '.join(tags)
    try:
        if not str(ctx.message.attachments[-1]).endswith('mp4'):
            await ctx.send('Get this shit outta here I only like mp4s')
            return
    except IndexError:
        pass
    entry = mentry.Entry(link,title,' '.join(tags))
    if entry.save_to_database():
        await ctx.send('Saved')
        return
    await ctx.send('Did not save this shit bro')



@client.command()
async def search(ctx, *inquiry):
    if len(inquiry) > 200:
        return
    inquiry = list(inquiry)
    if 'tags' in inquiry:
        results = msearch.Search(' '.join(inquiry[:inquiry.index('tags')]),inquiry[inquiry.index('tags')+1:]).search()
        print(results)
        file = discord.File(rf'{filepath}\{results[0][0]}.mp4')
        print('rees',results[0][0])
        await ctx.send(file=file, content=f'Found {results[0][1]}. Other results: {" , ".join([i[1] for i in results[1:]])}')
        return
    else:
        results = msearch.Search(' '.join(inquiry)).search()
        file = discord.File(rf'{filepath}\{results[0][0]}.mp4')
        embed = discord.Embed(title=results[0][1],description=results[0][3],color=discord.Color.brand_green())
        embed.set_footer(text=f'Other results: {" , ".join([i[1] for i in results[1:]])}')
        await ctx.send(embed=embed,file=file)




@client.command()
async def searchtext(ctx, *text):
    if len(text) > 200:
        return
    text = list(text)
    results = msearch.Search(' '.join(text)).by_speech()
    file = discord.File(rf'{filepath}/{results[0][1][0]}.mp4')
    await ctx.send(file=file, content=f'Found {results[0][1][1]}. Other results from speech to text: {" , ".join([i[1][1] for i in results[1:]])}')

client.run('MTA3OTA5NDczNjM4NTc0NDkyOQ.GhXQ8Q.8zwMRWA4KtWNibAmOam3efXfxToowudIrS6NbM')

# TODO : get rid of this aids and compress the videos
