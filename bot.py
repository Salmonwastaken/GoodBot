#!/usr/bin python3.7
#importing required software
import os
import discord
from dotenv import load_dotenv
import sqlite3

#Sqlite3 connection
con = sqlite3.connect('GoodBot.db')
cur = con.cursor()

# GoodBot part
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()



#runs any time a message gets sent               
@client.event
async def on_message(message):
    author = message.author.id
    channel = message.channel
    #Check if author of message is bot (bot doesn't need experience or levels.)
    
    if message.author.bot == False:
        #check if author already exists in Database
        t = (author,)
        cur.execute('SELECT EXISTS(SELECT 1 FROM experience WHERE authorID=?)', t)
        authorexist = cur.fetchone()
        #if author does exist, get current experience and add 1 experience
        if authorexist[0] == 1:
            cur.execute('SELECT experience FROM experience WHERE authorID=?', t)
            currentexp = cur.fetchone()
            newxp = currentexp[0] + 1
            varx = (newxp, author)
            cur.execute('UPDATE experience SET experience = ? WHERE authorID=? ', varx)
            con.commit()
            #janky level check, but it works and no database useage required
            modulus = newxp % 100
            level = newxp // 100
            if modulus == 0:
                await channel.send('Congrats ' + message.author.mention + ' you leveled up! Your level is now ' + str(level))
        else:
            cur.execute('INSERT INTO experience VALUES (?,0)', t)
            con.commit()   

client.run(TOKEN)