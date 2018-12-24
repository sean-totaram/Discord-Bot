''' 
orderBot.py
Author: twnkltoe

Order of the Fallen discord server bot

TODO:

General
 *add more features
'''

#orderBot.py
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from datetime import date
from datetime import datetime
import csv
import random

Client = discord.Client()
client = commands.Bot(command_prefix = "?")

#Predefined Variables
#   Discord
TOKEN = "NTI1NDAzNTM0ODQ2NDU5OTE3.Dv23yA.hv95Ul8Hz-P48oTc6Lezb-eAaeU"
userlist = []

#   Channels
games = ["conan-exiles", "destiny", "eso", "league-of-legends", "overwatch", 
    "path-of-exile", "r6-siege", "rocket-league", "wow"]
twnkleGames =["Arma 3", "Conan Exiles", "ESO", "GTA V", 
    "Just Cause 3", "Minecraft", "The Witcher 3", "Siege", "BF 1"]

barrensChannel = "232183982547009536"
suggestionsChannel = "525529661065658378"
orderChannel = "525530245210570753"

conanChannel = "525358403942350865"
destinyChannel = "525358246509150239"
esoChannel = "525358346983833600"
lolChannel = "525358544443146242"
overwatchChannel = "525358620368437248"
poeChannel = "525358316126339105"
r6siegeChannel = "525358709917089817"
rocketLeagueChannel = "525537148880027658"
wowChannel = "525358220613648390"

#   Roles
adminRole = "525418694755483669"
modRole = "525493523546505252"

#   Users
twnkltoeUser = "<@232183497098395650>"
holymagumboUser = "<@83729683325128704>"


#Helper functions
#   Finds difference between input date and today
def getCountdown(target):
    end = datetime.strptime(target, "%Y-%m-%d")
    today = date.today()
    return (end.date() - date.today())

#   Gets game namd and description from stored file
def getInfo(gameName):
    with open("timeTable.csv") as csvFile:
        csv_reader = csv.reader(csvFile, delimiter = ',')
        for row in csv_reader:
            if row[0] == gameName:
                #return getCountdown(row[2])
                return row

#   Sets countdown info
def setInfo(name, descr, date):
    with open("timeTable.csv", mode = 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerow([name, descr, date])

#   Checks if game has a channel
def checkGamesList(gameName):
    for game in games:
        if gameName == game:
            return True
    return False

#   Checks if author is admin
def checkAdmin(roles):
    for role in roles:
        if role.id == adminRole:
            return True
    return False

#   Checks if author is mod
def checkMod(roles):
    for role in roles:
        if role.id == modRole:
            return True
    return False

#Bot commands
#   Bot is online
@client.event
@asyncio.coroutine
def on_ready():
    print("Bot is online and connected")

#   Welcomes new members to server
@client.event
@asyncio.coroutine
def on_member_join(member):
    msg = "Welcome to the Order of the Fallen server " + str(member.mention)
    yield from client.send_message(discord.Object(
        id=barrensChannel), msg)

#   !commands
@client.event
@asyncio.coroutine 
def on_message(message):
    #gets roles for author
    roles = message.author.roles
    global userlist
    global twnkleGames

    #bot doesn't answer to self
    if message.author == client.user:
        return

    #clears text channel of all messages
    if message.content.startswith("!clear"):
        if checkAdmin(roles) or checkMod(roles):
            yield from client.purge_from(message.channel)
        else:
            msg = "Sorry {0.author.mention} you do not have permission.".format(message)
            yield from client.send_message(message.channel, msg)

    #says hello       
    if message.content.startswith("!hello"):
        msg = "Hello {0.author.mention}".format(message)
        yield from client.send_message(message.channel, msg)

    #displays creators name
    if message.content.startswith("!credit"):
        msg = "OrderBot was written in Python and created by the glorious Mr. %s for the Order of the Fallen WoW Guild" %twnkltoeUser 
        yield from client.send_message(message.channel, msg)

    #Picks a random game for me to play
    if message.content.startswith("!pickagame"):
       if ("<@" + message.author.id + ">") == twnkltoeUser:
            selectedGame = twnkleGames[random.randint(0, len(twnkleGames))]
            msg = "You should def fucking play " + selectedGame
            yield from client.send_message(message.channel, msg)
       else:
            msg = "Sorry {0.author.mention} you cant tell me what to fucking do.".format(message)
            yield from client.send_message(message.channel, msg)

    #set countdown time
    if message.content.startswith("!settime"):
        if checkAdmin(roles) or checkMod(roles):
            args = message.content.split(" ")
            setInfo(args[1], args[2], args[3])
            yield from client.send_message(message.channel, "All set")
        else:
            msg = "Sorry {0.author.mention} you do not have permission.".format(message)
            yield from client.send_message(message.channel, msg)

    #returns time till update
    if message.content.startswith("!gettime"):
        args = message.content.split(" ")
        print(args[1])
        if checkGamesList(args[1]):
            if(args[1] == "wow"):
                row = getInfo(args[1])
                time1 = getCountdown(row[2])
                msg = str(time1)[:6] + "s till " + str(row[1])
                yield from client.send_message(discord.Object(id = wowChannel), msg)
            elif(args[1] == "overwatch"):
                row = getInfo(args[1])
                time = getCountdown(row[2])
                msg = str(time)[:6] + "s till " + str(row[1])
                yield from client.send_message(discord.Object(id = overwatchChannel), msg)
        elif args[1] == "Dave":
            row = getInfo(args[1])
            time = getCountdown(row[2])
            msg = str(time[:6] + "s till" + str(row[1]))
            yield from client.send_message(discord.Object(id = barrensChannel), msg)
        else:
            msg = "Sorry {0.author.mention} we don't have that game channel".format(message)
            yield from client.send_message(message.channel, msg)

    #start game generator
    if message.content.startswith("!startgame"):
        if checkAdmin(roles) or checkMod(roles):
            if len(userlist) == 0:
                userlist.append("start")
                msg = "Collecting game names. Please use the !addgame command to add a game"
                yield from client.send_message(message.channel, msg)
            else:
                msg = "This event is already in progress"
                yield from client.send_message(message.channel, msg)
        else:
            msg = "You do not have permission to start this feature"

    #add games to random list
    if message.content.startswith("!addgame"):
        if len(userlist) > 0:
            args = message.content.split(" ")
            del args[0]
            for item in args:
                userlist.append(item)
            msg = "Games added : %s" %(" ".join(args[0:]))
            yield from client.send_message(message.channel, msg)
        else:
            msg = "Sorry {0.author.mention} this event hasn't been started yet".format(message)
            yield from client.send_message(message.channel, msg)

    #ends list collection and chooses random game
    if message.content.startswith("!endgame"):
        if checkAdmin(roles) or checkMod(roles):
            if len(userlist) > 0:
                selectedGame = userlist[random.randint(1, len(userlist))]
                userlist = []
                msg = "The selected game is " + selectedGame
                yield from client.send_message(message.channel, msg)
            else:
                msg = "Sorry {0.author.mention} this event hasn't been started yet.".format(message)
                yield from client.send_message(message.channel, msg)
        else:
            msg = "You do not have permission to end this event"
            yield from client.send_message(message.channel, msg)

client.run(TOKEN)
