import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)


@client.event
async def on_ready():
    print('nuts')

@client.command()
async def inspect(ctx):
    print(ctx.message.attachments)

client.run('MTA3OTA5NDczNjM4NTc0NDkyOQ.Gq4sKv.vI1HcFk8BxiazqGb9mQopdT9v4pbUXh38H3SDc')