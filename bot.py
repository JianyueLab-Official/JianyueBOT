from http.client import responses
import discord

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print(f"目前登录身份 --> {client.user}")
    game = discord.Game('!help')
    await client.change_presence(status=discord.Status.idle, activity=game)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == '!jianyuelab':
        await message.channel.send("JianyueLab is a organization gathered with a group of people who are liking developing, servers, locallize and etc.")
    
    if message.content == '!minecraft':
        await message.channel.send("Before you playing the server hold by JianyueLab, you need apply for whitelist")
        
    if message.content.startswith('!speak'):
        tmp = message.content.split(" ",1)
        if len(tmp) == 1:
            await message.channel.send("What do you want let me to speak?")
        else:
            await message.channel.send(tmp[1])
        
    if message.content.startswith('!changestatus'):
        tmp = message.content.split(" ",1)
        if len(tmp) == 1:
            await message.channel.send("What do you want to change?")
        else:
            game = discord.Game(tmp[1])
            await client.change_presence(status=discord.Status.idle, activity=game)
    
    if message.content == '!help':
        await message.channel.send("!jianyuelab <- Explain what is JianyueLab \n !changestatus <- change bot status \n !speak <- let bot speak something.")
   
client.run('MTE3NTQzMDYxODk5NDE4MDIwNg.GLaTtn.SxXOMfkmu1XMMzL6nQreW1NmMogD8lSNOTfNOM')