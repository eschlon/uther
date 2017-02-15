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
    elif message.content.startswith('/rf'):
        result = fluid(message.content)
        await client.send_message(message.channel, success_text)

def fluid(message):
    """Example: /rf d7 t6 p6
    Syntax: /rf d<n1> t<n2> p<n3>, where
    n1 = number of dice rolled
    n2 = threshold: the minimum number to be considered a success
    n3 = bonus pips: can be added across all failed rolls, if this will create additional successes
    """
    dice = message.split('d')[1].split(' ')[0]
    dice = int(dice)
    threshold = message.split('t')[1].split(' ')[0]
    threshold = int(threshold)
    pips = message.split('p')[1].split(' ')[0]
    pips = int(pips)
    result = []
    for _ in range(dice):
        result.append(randint(1, 10))

    result.sort(reverse = True)

    success_count = 0

    NatSuccess = []
    PipSuccess = []
    Failures =[]

    for r in result:
        margin = r - threshold
        if margin >= 0:
            success_count += 1
            NatSuccess.append(r)
        elif pips + margin >= 0:
            pips += margin
            PipSuccess.append(r)
            success_count += 1
        else:
            Failures.append(r)

    TotalDice = NatSuccess + PipSuccess + Failures

    if success_count != 1 and pips != 1:
        success_text = '{} successes with {} pips remaining:\n{}'.format(success_count, pips, TotalDice)
    elif success_count == 1 and pips != 1:
        success_text = '1 success with {} pips remaining:\n{}'.format(pips, TotalDice)
    elif success_count != 1 and pips == 1:
        success_text = '{} successes with 1 pip remaining:\n{}'.format(success_count, TotalDice)
    else:
        success_text = '1 successes with 1 pip remaining:\n{}'.format(TotalDice)

    return success_text


client.run('TOKEN')
