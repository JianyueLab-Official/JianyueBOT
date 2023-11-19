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
    
    if message.content == '!help':
        await message.channel.send("This is a help message.")
   
client.run('MTE3NTQzMDYxODk5NDE4MDIwNg.GLaTtn.SxXOMfkmu1XMMzL6nQreW1NmMogD8lSNOTfNOM')