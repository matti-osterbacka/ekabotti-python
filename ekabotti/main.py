import discord
import os
from dotenv import dotenv_values
from datetime import datetime, date, time, timezone, timedelta
import time as time2
test = False # change this depending on whether running locally to test (True) from .env or live from a server's os.environ (False)
logging_channel_id = 0
posting_channel_id = 0
token = ""
if test:
    config = dotenv_values()
    logging_channel_id = int(config["LOGGING_CHANNEL_ID"])
    posting_channel_id = int(config["POSTING_CHANNEL_ID"])
    token = str(config["DISCORD_TOKEN"])
else:
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
    first_message = await fetch_first_message(channel)
    print(first_message.content)
    #clear_file()
    await message_first_to_logging_channel(first_message, channel.members)
    #write_first_into_file(first_message)
    #await channel2.send(read_stats_from_file(first_message, channel2.members))
    #print(read_stats_from_file(first_message, channel.members))
    time2.sleep(1)
    statistics = await get_statistics_from_logging_channel(first_message, channel.members)
    await channel.send(statistics)
    quit()

async def fetch_first_message(channel):
    dt = datetime.now().replace(minute=0,second=0,microsecond=0)
    first_message = None
    while first_message is None:
        async for message in channel.history(after=dt, limit=1):
            first_message = message
    print(first_message.created_at)
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

async def message_first_to_logging_channel(first_message, members):
    channel = await client.fetch_channel(logging_channel_id)
    s = {}
    for member in members:
        s[member.id] = {"score":0, "display_name":member.display_name}
    stat_message = None
    async for message in channel.history(oldest_first=False, limit=1):
        stat_message = message
    for line in stat_message.content.splitlines():
        if len(line.split("|")) != 3:
            break
        else:
            user_info = line.split("|")
            s[int(user_info[0])]["score"]= int(user_info[1])
    s[first_message.author.id]["score"] += 1
    string_to_send = ""
    for id, info in s.items():
        string_to_send += str(id) +"|"+ str(info["score"]) + "|" + info["display_name"] + "\n"
    await channel.send(string_to_send)

async def get_statistics_from_logging_channel(first_message, members):
    channel = await client.fetch_channel(logging_channel_id)
    s = {}    
    stat_message = None
    async for message in channel.history(oldest_first=False, limit=1):
        stat_message = message
    for line in stat_message.content.splitlines():
        user_info = line.split("|")
        s[int(user_info[0])]= {"display_name":user_info[2], "score":int(user_info[1])}
    string_to_send = "EKA oli " + first_message.author.display_name + "\n\n"
    for info in dict(sorted(s.items(), key=lambda item: item[1]["score"], reverse=True)).values():
        if info["score"] > 0:
            string_to_send += info["display_name"] +": "+ str(info["score"]) + "\n"
    return string_to_send


client.run(token)