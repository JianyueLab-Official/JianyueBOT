from http.client import responses
import discord
from settings import TOKEN, default_status, default_custom_status, setting_version

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)
bot_version = "V0.0.2"
bot_build = "8"

@client.event
async def on_ready():
    print(f"目前登录身份 --> {client.user}")
    if default_status == 'idle':
        edit_status = discord.Status.idle
    elif default_status == 'online':
        edit_status = discord.Status.online
    elif default_status == 'do_not_discord':
        edit_status = discord.Status.do_not_disturb
    else:
        print("unknown Status")  
        edit_status = discord.Status.online
    game = discord.Game(default_custom_status)
    await client.change_presence(status=edit_status, activity=game)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!minecraft':
        await message.channel.send("Before you playing the server hold by JianyueLab, you need apply for whitelist")
        
    if message.content.startswith('!speak'):
        tmp = message.content.split(" ",1)
        if len(tmp) == 1:
            await message.channel.send("What do you want let me to speak?")
        else:
            await message.channel.send(tmp[1])
            
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
        elif tmp[1] == 'do_not_disturb':
            await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(' '.join(tmp[2:])))
            return
    
    if message.content == '!help':
        await message.channel.send("!status <- change bot status \n!speak <- let bot speak something. \n!statusmod <- Change bot status(online, idle, do_not_disturb)")
    
    if message.content == '!version':
        await message.channel.send("Setting File Verison: " + setting_version, "Bot Version: " + bot_version, "Bot Build: " + bot_build)
    
    else:
        await message.channel.send("Invalid Input. Please check '!help'.")
    
client.run(TOKEN)