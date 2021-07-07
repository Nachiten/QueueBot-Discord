import os
import discord

client = discord.Client()
token = os.environ['TOKEN']

@client.event
async def on_ready():
  print('We have logged in as {0.user}'
  .format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')

  if message.content.startswith('!miNombre'):
    await message.channel.send(message)

client.run(token)