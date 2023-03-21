import mentry
import msearch
import os
import discord
from discord.ext import commands

filepath = os.environ.get('MEMEDATAFILEPATH')
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)


@client.event
async def on_ready():
    print('Ready to eat memes', client.user)


@client.command()
async def archive(ctx, *tags):
    tags = list(tags)
    if 'tags' in tags:
        title = ' '.join(tags[:tags.index('tags')])
        tags = tags[tags.index('tags'):]
    else:
        title = ' '.join(tags)
    if not str(ctx.message.attachments[-1]).endswith('mp4'):
        await ctx.send('Get this shit outta here I only like mp4s')
        return
    entry = mentry.Entry(str(ctx.message.attachments[-1]),title,' '.join(tags))
    if entry.save_to_database():
        await ctx.send('Saved')
        return
    await ctx.send('Did not save this shit bro')


@client.command()
async def search(ctx, *inquiry):
    inquiry = list(inquiry)
    if 'tags' in inquiry:
        results = msearch.Search(' '.join(inquiry[:inquiry.index('tags')]),inquiry[inquiry.index('tags')+1:]).search()
        print(results)
        file = discord.File(rf'{filepath}\{results[0][0]}.mp4')
        print('rees',results[0][0])
        try:
            await ctx.send(file=file, content=f'Found {results[0][1]}. Other results: {" , ".join([i[1] for i in results[1:]])}')
            return
        except:
            await ctx.send('File too big to send sending the next best result')
            results.pop(0)
            file = discord.File(rf'{filepath}\{results[0][0]}.mp4')
            try:
                await ctx.send(file=file, content=f'Found {results[0][1]}. Other results: {" , ".join([i[1] for i in results[1:]])}')
                return
            except:
                pass
        await ctx.send('all these files are too damn big')
    else:
        results = msearch.Search(' '.join(inquiry)).search()
        print(results)
        file = discord.File(rf'{filepath}\{results[0][0]}.mp4')
        print('res',results[0][0])
        try:
            await ctx.send(file=file, content=f'Found {results[0][1]}. Other results: {" , ".join([i[1] for i in results[1:]])}')
            return
        except:
            while len(results) > 0:
                await ctx.send('File too big to send sending the next best result')
                results.pop(0)
                file = discord.File(rf'{filepath}\{results[0][0]}.mp4')
                try:
                    await ctx.send(file=file, content=f'Found {results[0][1]}. Other results: {" , ".join([i[1] for i in results[1:]])}')
                    return
                except:
                    pass
        await ctx.send('all these files are too damn big')


@client.command()
async def searchtext(ctx, *text):
    text = list(text)
    results = msearch.Search(' '.join(text)).by_speech()
    print(results)
    file = discord.File(rf'{filepath}\{results[0][1][0]}.mp4')
    await ctx.send(file=file, content=f'Found {results[0][1][1]}. Other results from speech to text: {" , ".join([i[1][1] for i in results[1:]])}')
client.run('')

# TODO : get rid of this aids and compress the videos
