import discord
import datetime
import sqlite3
import os

client = discord.Client()
guildID = 943321200950669374
sqliteConnection = sqlite3.connect('times.db')#doesn't exist yet
cursor = sqliteConnection.cursor()

@client.event
async def on_ready():
    print("{} has connected to Discord!".format(client.user))
    for guild in client.guilds:
        print("{} with id {}".format(guild.name, guild.id))

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send("Hi {}, welcome to the timecheck server".format(member.name))
    await member.dm_channel.send("Message format: \n !<iso8601 time>:<lecture name>:<lateness in minutes OR N/A>")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if len(message.content) == 0:
        return
    if message.content[0] == "!":
        if message.content == "!help":
            await message.channel.send("Message format: \n !<iso8601 time>:<lecture name>:<lateness in minutes OR N/A>")
        elif message.content == "!times":
            cursor.execute("""SELECT * FROM times""")
            rows = cursor.fetchall()
            for row in rows:
                await message.channel.send(row)
            await message.channel.send("done")
        else:
            args = message.content[1:].split(":")
            try:
                dto = datetime.datetime.strptime(args[0], "%d/%m/%Y")
            except:
                if message.author.id == 908744046057521192:
                    await message.channel.send("just stop")
                await message.channel.send("Can't parse date :( pls try again")
                return
            cursor.execute("""INSERT INTO times VALUES ({}, '{}', '{}') """.format(dto.timestamp(), args[1], args[2]))
            sqliteConnection.commit()
            await message.channel.send("Success maybe idk")
client.run(os.getEnv(bot_token, default=False))
