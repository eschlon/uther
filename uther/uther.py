import discord
import asyncio
from random import randint

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    elif message.content.startswith('!roll'):
        result = roll(message.content)
        await client.send_message(message.channel, result)


def roll(message):
    """!roll 2d10
        <number>d<sides> [+-/*] <number>d<sides> / <constant>
        5d10k2 - Keep Highest 2
        5d10l2 - Keep Lowest 2
        5d10x9 - Explode rolls that are 9 or higher
    """
    dice = message.split(' ')[1].split('d')
    n, sides = [int(d) for d in dice]
    result = []
    for _ in range(n):
        result.append(randint(1, sides))
    
    return result

client.run('TOKEN')