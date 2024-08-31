# imports
import random

import discord
from discord import app_commands
from discord.ext import commands

from scripts import *

load_dotenv('.env')

TOKEN = os.getenv('TOKEN')
default_custom_status = os.getenv('default_custom_status')
default_status = os.getenv('default_status')
default_version = os.getenv('default_version')
setting_version = os.getenv('setting_version')

# 固定不变
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

# 版本号
bot_version = "v0.1.4"
bot_build = "1"
bot_type = "Release Build"


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
        print("Unknown Status")
        edit_status = discord.Status.online
    # 自定义状态的内容
    game = discord.Game(default_custom_status)
    await client.change_presence(status=edit_status, activity=game)
    # 同步命令 并输出
    try:
        synced = await client.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


# /say [things_to_say]
@client.tree.command(name="say", description="Let bot say something.")
@app_commands.describe(things_to_say="What should I say?")
async def say(interaction: discord.Interaction, things_to_say: str):
    await interaction.response.send_message(f"{things_to_say}")


# /status [choice] [custom]
@client.tree.command(name="status", description="Change the status")
@app_commands.choices(
    choices=[
        app_commands.Choice(name="Online", value="online"),
        app_commands.Choice(name="idle", value="idle"),
        app_commands.Choice(name="Do Not Disturb", value="dnd"),
    ]
)
async def status(interaction: discord.Interaction, choices: app_commands.Choice[str], *, custom_status_message: str):
    if choices.value == "online":
        changed_status = discord.Status.online
    elif choices.value == "idle":
        changed_status = discord.Status.idle
    elif choices.value == "dnd":
        changed_status = discord.Status.dnd
    else:
        await interaction.response.send_message(f"Unknown Status. Please specify 'online', 'idle', 'Do Not Disturb'",
                                                ephemeral=True)
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
@app_commands.choices(
    country=[
        app_commands.Choice(name='Japan', value='JP'),
    ]
)
async def zipcode(interaction: discord.Interaction, country: app_commands.Choice[str], zipcodes: str):
    await interaction.response.defer(ephemeral=True)
    if country.value == 'JP':
        result = search_zipcode_jp(zipcodes)
        if result is None:
            await interaction.followup.send(f"Invalid Zipcode.")
        else:
            await interaction.followup.send(
                f"""
                **Prefecture 都道府県:** {result['address1']} {result['kana1']}
                **City 市区町村:** {result['address2']} {result['kana2']}
                **Town 町域:** {result['address3']} {result['kana3']}
                """
            )
    if country.value == 'CN':
        result = "Unavaliable"
        if result is None:
            await interaction.followup.send(f"Invalid Zipcode.")
        else:
            await interaction.followup.send(f"Address: {result}")
    else:
        await interaction.followup.send(f'Invalid Country.')

    return


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
            description=f"This is the Result of {ipaddress}"
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
            description=f"This is the Result of {ipaddress}"
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
@client.tree.command(name='domain', description='Find the cheapest domain registrar')
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
    else:
        await interaction.followup.send(
            "## Domain Registrar"
            f"\n**TLD**: {result['domain']} **| Order**: {result['order']}"
            "\n### 1st:"
            f"\n- **Registrar**: {result['reg_1']}"
            f"\n- **Currency**: {result['currency_1']}"
            f"\n- **New**: {result['new_1']}"
            f"\n- **Renew**: {result['renew_1']}"
            f"\n- **Transfer**: {result['transfer_1']}"
            f"\n- **Registrar Website**: {result['reg_web_1']}"
            "\n### 2nd:"
            f"\n- **Registrar**: {result['reg_2']}"
            f"\n- **Currency**: {result['currency_2']}"
            f"\n- **New**: {result['new_2']}"
            f"\n- **Renew**: {result['renew_2']}"
            f"\n- **Transfer**: {result['transfer_2']}"
            f"\n- **Registrar Website**: {result['reg_web_2']}"
            "\n### 3rd:"
            f"\n- **Registrar**: {result['reg_3']}"
            f"\n- **Currency**: {result['currency_3']}"
            f"\n- **New**: {result['new_3']}"
            f"\n- **Renew**: {result['renew_3']}"
            f"\n- **Transfer**: {result['transfer_3']}"
            f"\n- **Registrar Website**: {result['reg_web_3']}"
            "\n### 4th:"
            f"\n- **Registrar**: {result['reg_4']}"
            f"\n- **Currency**: {result['currency_4']}"
            f"\n- **New**: {result['new_4']}"
            f"\n- **Renew**: {result['renew_4']}"
            f"\n- **Transfer**: {result['transfer_4']}"
            f"\n- **Registrar Website**: {result['reg_web_4']}"
            "\n### 5th:"
            f"\n- **Registrar**: {result['reg_5']}"
            f"\n- **Currency**: {result['currency_5']}"
            f"\n- **New**: {result['new_5']}"
            f"\n- **Renew**: {result['renew_5']}"
            f"\n- **Transfer**: {result['transfer_5']}"
            f"\n- **Registrar Website**: {result['reg_web_5']}"
        )

    return


# /registrars
@client.tree.command(name='registrars', description='Find the cheapest domain registrar')
@app_commands.choices(
    order=[
        app_commands.Choice(name='New', value='new'),
        app_commands.Choice(name='Renew', value='renew'),
        app_commands.Choice(name='Transfer', value='transfer'),
    ],
)
async def registrars(interaction: discord.Interaction, registrar: str, order: app_commands.Choice[str]):
    await interaction.response.defer(ephemeral=True)
    result = registrar_search(registrar, order)
    if result is None:
        await interaction.followup.send(f"Invalid input or Inter Error")
        return
    else:
        await interaction.followup.send(
            "## Domain Registrar"
            f"\n**Registrar**: {result['reg']} **| Registrar Website**: {result['reg_web']} **| Order**: {result['order']}"
            "\n### 1st:"
            f"\n**Domain**: {result['domain_1']}"
            f"\n**New**: {result['new_1']}"
            f"\n**Renew**: {result['renew_1']}"
            f"\n**Transfer**: {result['transfer_1']}"
            f"\n**Currency**: {result['currency_1']}"
            "\n### 2nd:"
            f"\n**Domain**: {result['domain_2']}"
            f"\n**New**: {result['new_2']}"
            f"\n**Renew**: {result['renew_2']}"
            f"\n**Transfer**: {result['transfer_2']}"
            f"\n**Currency**: {result['currency_2']}"
            "\n### 3rd:"
            f"\n**Domain**: {result['domain_3']}"
            f"\n**New**: {result['new_3']}"
            f"\n**Renew**: {result['renew_3']}"
            f"\n**Transfer**: {result['transfer_3']}"
            f"\n**Currency**: {result['currency_3']}"
            "\n### 4th:"
            f"\n**Domain**: {result['domain_4']}"
            f"\n**New**: {result['new_4']}"
            f"\n**Renew**: {result['renew_4']}"
            f"\n**Transfer**: {result['transfer_4']}"
            f"\n**Currency**: {result['currency_4']}"
            "\n### 5th:"
            f"\n**Domain**: {result['domain_5']}"
            f"\n**New**: {result['new_5']}"
            f"\n**Renew**: {result['renew_5']}"
            f"\n**Transfer**: {result['transfer_5']}"
            f"\n**Currency**: {result['currency_5']}"
        )
        return


# Minecraft server detection
@client.tree.command(name='mcserver', description='Get debug and details of a minecraft server')
@app_commands.choices(
    server_type=[
        app_commands.Choice(name='Java', value='java'),
        app_commands.Choice(name='Bedrock', value='bedrock'),
    ]
)
async def mcserver(interaction: discord.Interaction, server_type: app_commands.Choice[str], ipaddress: str):
    await interaction.response.defer(ephemeral=True)
    result = minecraftServer(server_type, ipaddress)
    if result is None:
        await interaction.followup.send("Invalid Input / Server Type")
    else:
        embed = discord.Embed(
            colour=discord.Colour.dark_grey(),
            title="Minecraft Server",
            description=f"This is the Result of {ipaddress}"
        )
        embed.add_field(name='Actual IP address', value=result['ip'])
        embed.add_field(name='Server Listening Port', value=result['port'])
        embed.add_field(name='Hostname', value=result['hostname'])
        embed.add_field(name='Game Version', value=result['version'])
        embed.add_field(name='MOTD', value=result['motd'])
        embed.add_field(name='Ping', value=result['ping'])
        embed.add_field(name='SRV Record', value=result['srv'])
        embed.add_field(name='Player', value=f"{result['player']} / {result['maxPlayer']}")

        await interaction.followup.send(embed=embed)
    return


# /bincheck
@client.tree.command(name='bincheck', description="Check a card issuer and country")
async def bincheck(interaction: discord.Interaction, bin_code: int):
    await interaction.response.defer(ephemeral=True)
    result = bin_check_request(bin_code)

    if result is None:
        await interaction.followup.send("Request Error or BIN code doesn't exist")
    else:
        embed = discord.Embed(
            colour=discord.Colour.dark_grey(),
            title="BinCheck",
            description=f"The result of {bin_code}"
        )
        embed.add_field(name='Valid', value=result['valid'])
        embed.add_field(name='Brand', value=result['brand'])
        embed.add_field(name='Type', value=result['type'])
        embed.add_field(name='Level', value=result['level'])
        embed.add_field(name='Commercial', value=result['is_commercial'])
        embed.add_field(name='Prepaid', value=result['is_prepaid'])
        embed.add_field(name='Currency', value=result['currency'])
        embed.add_field(name='Country', value=result['country'])
        embed.add_field(name='Flag', value=result['flag'])
        embed.add_field(name='Issuer', value=result['issuer'])

        await interaction.followup.send(embed=embed, ephemeral=True)
    return


# /info
@client.tree.command(name='info', description="Some information about this bot")
async def version(interaction: discord.Interaction):
    await interaction.response.send_message(
        "## JianyueBot"
        "\nThis bot was developed by [JianyueLab](https://awa.ms)."
        "\nIf you have any questions or require assistance, please contact @jianyuehugo."
        "\n- **GitHub Repo**: https://github.com/jianyuelab/jianyuebot"
        f"\n- **Bot Version:** {bot_version}"
        f"\n- **Bot Build:** {bot_build}"
        f"\n- **Settings Version:** {setting_version}"
        f"\n- **Build Type:** {[bot_type]}",
        ephemeral=True
    )


client.run(TOKEN)
