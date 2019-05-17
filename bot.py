import discord
from discord.ext import commands
import asyncio
import datetime
from itertools import cycle

client = discord.Client(max_messages=100000, status=discord.Status.dnd)

TOKEN = 'INSET TOKEN HERE'
log=INSERT LOG CHANNEL ID HERE

@client.event
async def on_ready():
	#indicates bot is live
	print("My botty is ready")

#This method logs the messages sent to a file, this is optional and may be removed if unnecessary
@client.event
async def on_message(message):
	f = open("log.txt", "a+")
	f.write(str(message.author) + " has said " + message.content + " in " + str(message.channel) + " at " + str(message.created_at) + "\n")
	f.close()

#This method logs messages deleted to the log channel specified above
@client.event
async def on_message_delete(message):
	embed = discord.Embed(title = "Message Deleted!", color=0xff69b4)
	embed.add_field(name="User", value = str(message.author) + "\n", inline=False)
	if not message.attachments:
		embed.add_field(name="Message", value = message.content + "\n", inline=False)
	else:
		embed.add_field(name="Message", value = message.content + "\n" + message.attachments[0].url, inline=False)
	channel = client.get_channel(log)
	await channel.send(embed=embed)

#This method logs messages edited, both before and after, to the log channel specified above
@client.event
async def on_message_edit(beforeMessage, afterMessage):
	embed = discord.Embed(title = "Message Edited!", description=str(beforeMessage.author) + " has edited their message!", color=0xff69b4)
	embed.add_field(name="Original message", value = " " + beforeMessage.content, inline=False)
	embed.add_field(name="Date created", value = str(beforeMessage.created_at), inline=False)
	embed.add_field(name="Edited message", value = " " + afterMessage.content, inline=False)
	embed.add_field(name="Date edited", value = str(afterMessage.edited_at), inline=False)
	channel = client.get_channel(log)
	await channel.send(embed=embed)

#This method logs a member joining the server
@client.event
async def on_member_join(member):
	embed = discord.Embed(title = "Member Joined", color=0xff69b4)
	embed.add_field(name="User Joined", value=member.mention + " has joined " + member.guild.name, inline=False)
	channel = client.get_channel(log)
	await channel.send(embed=embed)

#This method logs a member leaving a server
@client.event
async def on_member_remove(member):
	embed = discord.Embed(title = "Member Left", color=0xff69b4)
	embed.add_field(name="User Left", value=member.mention + " has left " + member.guild.name, inline=False)
	channel = client.get_channel(log)
	await channel.send(embed=embed)

#this method deletes the logs in the log channel to be compliant with CoC
async def log_cleanup():
	await client.wait_until_ready()
	channel = client.get_channel(log)
	while(True):
		async for messages in channel.history(limit=300):
			if(datetime.datetime.now().timestamp() - messages.created_at.timestamp() > 86400):
				await messages.delete()

async def bot_presence():
	await client.wait_until_ready()
	games = [enter strings here]
	msgs = cycle(games)
	print("test")
	while(True):
		current_status = next(msgs)
		print(current_status)
		await client.change_presence(activity=discord.Game(name=current_status))
		await asyncio.sleep(120)

client.loop.create_task(log_cleanup())
client.loop.create_task(bot_presence())
client.run(TOKEN)

