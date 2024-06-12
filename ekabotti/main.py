import discord
from dotenv import dotenv_values
from operator import itemgetter, attrgetter
from datetime import datetime, date, time, timezone, timedelta

config = dotenv_values()
logging_channel_id = int(config.get("LOGGING_CHANNEL_ID"))
posting_channel_id = int(config.get("POSTING_CHANNEL_ID"))
token = str(config.get("DISCORD_TOKEN"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print("a")
    #await channel.send("alku")
    print("b")
    dt = datetime.combine(date=date.today(), time=time.min).astimezone(tz=timezone(timedelta(hours=2), 'Europe/Helsinki'))
    print(dt)
    channel2 = await client.fetch_channel(posting_channel_id)
    first_message = None
    while first_message is None:
        async for message in channel2.history(after=dt, limit=1):
            first_message = message
    print(first_message.content)
    #channel2.send(handle_file(first_message, channel2.members))
    quit()
    
def handle_file(first_message, members):
    f = open("ekat.txt", "a")
    f.write(str(first_message.author.id)+"\n")
    f.close()
    f = open("ekat.txt", "r")
    s = f.read().splitlines()
    f.close()
    r = "EKA oli " + first_message.author.display_name + "\n\n"
    for member in members:
        r+= member.display_name + "|" + str(s.count(str(member.id))) + "\n"
    return r

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        print(message.channel.id)
        await message.channel.send('Hello!')

client.run(token)