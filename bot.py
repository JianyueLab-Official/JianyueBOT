# imports
import discord
from discord.ext import commands
from discord import app_commands
from settings import TOKEN, default_custom_status, default_status, setting_version
import random
from scripts.zipcode import search_zipcode_jp
from scripts.ipdetails import ipdetails
from scripts.iplocations import iplocations
from scripts.domainreg import cheapest

# 固定不变
intents = discord.Intents.all() 
client = commands.Bot(command_prefix='!', intents=intents)

# 版本号
bot_version = "v0.1.2"
bot_build = "1"
bot_type = "Dev Build"

# 启动之后
@client.event
async def on_ready():
    # 终端输出
    print("Bot is ready for use!")
    # 从配置文件中获取设定的状态
    if default_status == 'idle':
        edit_status = discord.Status.idle
    elif default_status == 'online':
        edit_status = discord.Status.online
    elif default_status == 'do_not_disturb':
        edit_status = discord.Status.dnd
    else:
        print("unknown Status")  
        edit_status = discord.Status.online
    # 自定义状态的内容
    game = discord.Game(default_custom_status)
    await client.change_presence(status=edit_status, activity=game)
    #同步命令 并输出
    try:
        synced = await client.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    
# /say [things_to_say]
@client.tree.command(name="say", description="Let bot say something.")
@app_commands.describe(things_to_say = "What should I say?")
async def say(interaction: discord.Interaction, things_to_say: str):
    await interaction.response.send_message(f"{things_to_say}")

# /status [choice] [custom]
@client.tree.command(name="status", description="Change the status")
@app_commands.choices(choices=[
    app_commands.Choice(name="Online", value="online"),
    app_commands.Choice(name="idle", value="idle"),
    app_commands.Choice(name="Do Not Disturb", value="dnd"),
])
async def status(interaction: discord.Interaction, choices: app_commands.Choice[str], *, custom_status_message: str):
        if choices.value == "online":
            changed_status = discord.Status.online
        elif choices.value == "idle":
            changed_status = discord.Status.idle
        elif choices.value == "dnd":
            changed_status = discord.Status.dnd
        else:
            await interaction.response.send_message(f"Unknown Status. Please specify 'online', 'idle', 'Do Not Disturb'", ephemeral=True)
            return
        
        game = discord.Game(custom_status_message)
        await client.change_presence(status=changed_status, activity=game)
        await interaction.response.send_message(f"Status Updated!", ephemeral=True)

# /roll 
@client.tree.command(name='roll', description='Roll a dice.')
async def roll(interaction: discord.Interaction):
    number = random.randint(1, 6)
    await interaction.response.send_message(f"Number is {number}")

# /zipcode [country] [zipcode]
@client.tree.command(name='zipcode', description='search address from zipcode')
@app_commands.choices(country=[
    app_commands.Choice(name='China', value='CN'),
    app_commands.Choice(name='Japan', value='JP'),
])
async def zipcode(interaction: discord.Interaction, country: app_commands.Choice[str], zipcode: str):
    await interaction.response.defer(ephemeral=True)
    if country.value == 'JP':
        result = search_zipcode_jp(zipcode)
        if result is None:
            await interaction.followup.send(f"Invalid Zipcode.")
            return
        else:
            await interaction.followup.send(f"**Prefecture 都道府県:** {result['address1']} {result['kana1']}\n**City 市区町村:** {result['address2']} {result['kana2']}\n**Town 町域:** {result['address3']} {result['kana3']}")
            return
    if country.value == 'CN':
        result = "Unavaliable"
        if result is None:
            await interaction.followup.send(f"Invalid Zipcode.")
            return
        else:
            await interaction.followup.send(f"Address: {result}")
            return
    else: 
        await interaction.followup.send(f'Invalid Country.')
        
# /ipdetails
@client.tree.command(name='ipdetail', description="Show the details from IP address")
async def ipdetail(interaction: discord.Interaction, ipaddress: str):
    await interaction.response.defer(ephemeral=True)
    result = ipdetails(ipaddress)
    if result is None:
        await interaction.followup.send(f"Invalid IP address or Inter Error")
        return
    else:
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title="IP Detail",
            description=(f"This is the Result of {ipaddress}")
        )
        embed.add_field(name='IP address', value=result['ip'])
        embed.add_field(name='IP number', value=result['ip_number'])
        embed.add_field(name='IP version', value=result['ip_version'])
        embed.add_field(name='IP country name', value=result['country_name'])
        embed.add_field(name='IP country code', value=result['country_code2'])
        embed.add_field(name='IP ISP', value=result['isp'])
        embed.add_field(name='IP response_code', value=result['response_code'])
        embed.add_field(name='IP response_message', value=result['response_message'])
        
        await interaction.followup.send(embed=embed)
        return
    
# /iplocation
@client.tree.command(name='iplocation', description="Show the Geolocation from IP address")
async def iplocation(interaction: discord.Interaction, ipaddress: str):
    await interaction.response.defer(ephemeral=True)
    result = iplocations(ipaddress)
    if result is None:
        await interaction.followup.send(f"Invalid IP address or Inter Error")
        return
    else:
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title="IP Location",
            description=(f"This is the Result of {ipaddress}")
        )
        embed.add_field(name='Query', value=result['query'])
        embed.add_field(name='Timezone', value=result['timezone'])
        embed.add_field(name='Country', value=result['country'])
        embed.add_field(name='City', value=result['city'])
        embed.add_field(name='ISP', value=result['isp'])
        embed.add_field(name='org', value=result['org'])
        embed.add_field(name='ASN', value=result['as'])

        await interaction.followup.send(embed=embed)
        return

# /domain
@client.tree.command(name='domain', description='Find the cheapest domain register')
@app_commands.choices(
    order=[
    app_commands.Choice(name='New', value='new'),
    app_commands.Choice(name='Renew', value='renew'),
    app_commands.Choice(name='Transfer', value='transfer'),
    ]
)
async def domain(interaction: discord.Interaction, tld: str, order: app_commands.Choice[str]):
    await interaction.response.defer(ephemeral=True)
    result = cheapest(tld, str(order))
    if result is None:
        await interaction.followup.send(f"Invalid input or Inter Error")
        return
    else:
        await interaction.followup.send(
            "## Domain Registrar"
            f"\n**TLD**: {result['domain']} **| Order**: {result['order']}"
            "\n### 1st: "
            f"\n- **Registrar**: {result['reg_1']}"
            f"\n- **Currency**: {result['currency_1']}"
            f"\n- **New**: {result['new_1']}"
            f"\n- **Renew**: {result['renew_1']}"
            f"\n- **Transfer**: {result['transfer_1']}"
            f"\n- **Registrar Website**: {result['reg_web_1']}"
            "\n### 2nd: "
            f"\n- **Registrar**: {result['reg_2']}"
            f"\n- **Currency**: {result['currency_2']}"
            f"\n- **New**: {result['new_2']}"
            f"\n- **Renew**: {result['renew_2']}"
            f"\n- **Transfer**: {result['transfer_2']}"
            f"\n- **Registrar Website**: {result['reg_web_2']}"
            "\n### 3rd: "
            f"\n- **Registrar**: {result['reg_3']}"
            f"\n- **Currency**: {result['currency_3']}"
            f"\n- **New**: {result['new_3']}"
            f"\n- **Renew**: {result['renew_3']}"
            f"\n- **Transfer**: {result['transfer_3']}"
            f"\n- **Registrar Website**: {result['reg_web_3']}"
            "\n### 4th: "
            f"\n- **Registrar**: {result['reg_4']}"
            f"\n- **Currency**: {result['currency_4']}"
            f"\n- **New**: {result['new_4']}"
            f"\n- **Renew**: {result['renew_4']}"
            f"\n- **Transfer**: {result['transfer_4']}"
            f"\n- **Registrar Website**: {result['reg_web_4']}"
            "\n### 5th: "
            f"\n- **Registrar**: {result['reg_4']}"
            f"\n- **Currency**: {result['currency_4']}"
            f"\n- **New**: {result['new_4']}"
            f"\n- **Renew**: {result['renew_4']}"
            f"\n- **Transfer**: {result['transfer_4']}"
            f"\n- **Registrar Website**: {result['reg_web_4']}"
            )

        return

# /version
@client.tree.command(name='version', description="Print the version of the bot")
async def version(interaction: discord.Interaction):
    await interaction.response.send_message(f"**Bot Version:** {bot_version}\n**Bot Build:** {bot_build}\n**Settings Version:** {setting_version}\n**Build Type:** {bot_type}", ephemeral=True)

# /help
@client.tree.command(name='help', description='Guild of use this bot.')
async def version(interaction: discord.Interaction):
    await interaction.response.send_message(f"- `/say [message]` let bot send a message."
                                            "\n- `/roll` Roll a dice"
                                            "\n- `/ipdetails [IP address]` Get detail information of an ipaddress"
                                            "\n- `/zipcode [Country] [zipcode]` Search address from zipcode"
                                            "\n- `/status [Status] [Custom Status]` Change Bot's status. "
                                            "\n- `/version` Print the version of this bot."
                                            "\n- `/help` Show the help of using this bot.",
                                            ephemeral=True)

client.run(TOKEN)
