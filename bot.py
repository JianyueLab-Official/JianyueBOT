from http.client import responses
import discord
from settings import TOKEN, default_status, default_custom_status, setting_version
from help import help_message

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)
bot_version = "v0.0.2"
bot_build = "10 fix"

@client.event
async def on_ready():
    print(f"目前登录身份 --> {client.user}")
    if default_status == 'idle':
        edit_status = discord.Status.idle
    elif default_status == 'online':
        edit_status = discord.Status.online
    elif default_status == 'do_not_disturb':
        edit_status = discord.Status.dnd
    else:
        print("unknown Status")  
        edit_status = discord.Status.online
    game = discord.Game(default_custom_status)
    await client.change_presence(status=edit_status, activity=game)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!speak'):
        tmp = message.content.split(" ",1)
        if len(tmp) == 1:
            await message.channel.send("What do you want let me to speak?")
            return
        else:
            await message.channel.send(tmp[1])
            return
            
    if message.content.startswith('!status'):
        tmp = message.content.split(" ")
        if len(tmp) == 1:
            await message.channel.send("What do you want to change?")
        elif tmp[1] == 'online':
            await client.change_presence(status=discord.Status.online, activity=discord.Game(' '.join(tmp[2:])))
            return
        elif tmp[1] == 'idle':
            await client.change_presence(status=discord.Status.idle, activity=discord.Game(' '.join(tmp[2:])))
            return
        elif tmp[1] == 'dnd':
            await client.change_presence(status=discord.Status.dnd, activity=discord.Game(' '.join(tmp[2:])))
            return
        else:
            await message.channel.send("Invalid Input. Check '!help' to correct it.")
            return
    
    if message.content == '!help':
        await message.channel.send(help_message)
        return
    
    if message.content == '!version':
        await message.channel.send("**Setting File Version:** " + str(setting_version) + "\n**Bot Version:** " + str(bot_version) + "\n**Bot Build:** " + str(bot_build))
        return
    
    else:
        await message.channel.send("Invalid Input. Please check '!help'.")
    
client.run(TOKEN)