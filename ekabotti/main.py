import discord
import os
from dotenv import dotenv_values
from datetime import datetime, date, time, timezone, timedelta

config = dotenv_values()
logging_channel_id = int(os.environ.get("LOGGING_CHANNEL_ID"))
posting_channel_id = int(os.environ.get("POSTING_CHANNEL_ID"))
token = str(os.environ.get("DISCORD_TOKEN"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True
#intents.read_message_history = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print("a")
    #await channel.send("alku")
    print("b")
    channel = await client.fetch_channel(posting_channel_id)
    first_message = await fetch_first_message(False, channel)
    print(first_message.content)
    #clear_file()
    await message_first_to_logging_channel(first_message)    
    #write_first_into_file(first_message)
    #await channel2.send(read_stats_from_file(first_message, channel2.members))
    #print(read_stats_from_file(first_message, channel.members))
    print(await get_statistics_from_logging_channel(first_message, channel.members))
    quit()

async def fetch_first_message(test, channel):
    dt = datetime.combine(date=date.today(), time=time.min).astimezone(tz=timezone(timedelta(hours=2), 'Europe/Helsinki'))
    print(dt.now())
    if test:
        dt = datetime.combine(date=date.fromisoformat("2024-06-18"), time=time.min).astimezone(tz=timezone(timedelta(hours=2), 'Europe/Helsinki'))
    first_message = None
    while first_message is None:
        async for message in channel.history(after=dt, limit=1):
            first_message = message
    return first_message
        

def write_first_into_file(first_message):
    f = open("ekat.txt", "a")
    f.write(str(first_message.author.id)+"\n")
    f.close()

def read_stats_from_file(first_message, members):
    f = open("ekat.txt", "r")
    s = f.read().splitlines()
    f.close()
    r = "EKA oli " + first_message.author.display_name + "\n\n"
    for member in members:
        r+= member.display_name + "|" + str(s.count(str(member.id))) + "\n"
    return r

def clear_file():
   f = open("ekat.txt", "w")
   f.close()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        print(message.channel.id)
        await message.channel.send('Hello!')

async def message_first_to_logging_channel(first_message):
    channel = await client.fetch_channel(logging_channel_id)
    await channel.send(first_message.author.id)

async def get_statistics_from_logging_channel(first_message, members):
    channel = await client.fetch_channel(logging_channel_id)
    s = []
    async for message in channel.history():
        s.append(message.content)
    r = "EKA oli " + first_message.author.display_name + "\n\n"
    for member in members:
        r+= member.display_name + "|" + str(s.count(str(member.id))) + "\n"
    return r


client.run(token)