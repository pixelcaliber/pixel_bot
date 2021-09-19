import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
client = discord.Client()

sad_words = ["sad","sorrow","tragic","cheerless", "unhappy", "sorrowful","dejected","regretful","depressed","downcast","miserable","downhearted","down","despondent","despairing","disconsolate","out of sorts", "desolate","bowed down","wretched","glum","gloomy","doleful","dismal","blue","melancholy","melancholic","low-spirited","mournful", "woeful", "woebegone", "forlorn","crestfallen","broken-hearted","heartbroken","inconsolable","grief-stricken"]

starter_encourage = ["Cheer up!", "You are doing awesome!", "Keep fighting!", "Stay strong!"]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
   response = requests.get("https://zenquotes.io/api/random")
   json_data = json.loads(response.text)
   quote = json_data[0]['q'] + " \n-" + json_data[0]['a']
   return(quote)

def update_encouragements(encouraging_messsage):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_messsage)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_messsage]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event

async def on_ready():
 print('Hey! We have loged in as {0.user}'.format(client))

@client.event
async def on_message(message):
   if message.author == client.user:
     return

   msg = message.content

   if message.content.startswith('$hello'):
    # await message.channel.send('Hello !')
    print('Hey! {0.user}'.format(client))
   if message.content.startswith('hi'):
    await message.channel.send('Hello!')
   if message.content.startswith('bue'):
    await message.channel.send('bue bue!')
   if message.content.startswith('$how u doing'):
    await message.channel.send('I am doing great. How abt u? Do Read my bio if u r more curious abt me!')
 
   if message.content.startswith('$quote'):
     quote = get_quote()
     await message.channel.send(quote)

   if db["responding"]:
    options = starter_encourage
    if "encouragements" in db.keys():
      options.extend(db["encouragements"])

   if any(word in msg for word in sad_words):
     await message.channel.send(random.choice(options))

   if msg.startswith("$new"):
     encouraging_messsage = msg.split("$new ", 1)[1]
     update_encouragements(encouraging_messsage)
     await message.channel.send("New Message added.")

   if msg.startswith("$del"):
     encouragements = []
     if "encouragements" in db.keys():
       encouragements = db["encouragements"]
       index = int(msg.split("$del", 1)[1])
       index = index - 1
       delete_encouragement(index)
      #  encouragements = db["enco  uragements"]
       await message.channel.send(encouragements)

   if msg.startswith("$lists"):
       encouragements = []
       if "encouragements" in db.keys():
         encouragements = db["encouragements"]
       await message.channel.send(encouragements)
       
   if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getenv('token'))