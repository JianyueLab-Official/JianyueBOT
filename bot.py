# imports
import os
import random

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

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
bot_version = "v0.1.3"
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
            f"""
            ## Domain Registrar
            **TLD**: {result['domain']} **| Order**: {result['order']}
            ### 1st:
            - **Registrar**: {result['reg_1']}
            - **Currency**: {result['currency_1']}
            - **New**: {result['new_1']}
            - **Renew**: {result['renew_1']}
            - **Transfer**: {result['transfer_1']}
            - **Registrar Website**: {result['reg_web_1']}
            ### 2nd:
            - **Registrar**: {result['reg_2']}
            - **Currency**: {result['currency_2']}
            - **New**: {result['new_2']}
            - **Renew**: {result['renew_2']}
            - **Transfer**: {result['transfer_2']}
            - **Registrar Website**: {result['reg_web_2']}
            ### 3rd:
            - **Registrar**: {result['reg_3']}
            - **Currency**: {result['currency_3']}
            - **New**: {result['new_3']}
            - **Renew**: {result['renew_3']}
            - **Transfer**: {result['transfer_3']}
            - **Registrar Website**: {result['reg_web_3']}
            ### 4th:
            - **Registrar**: {result['reg_4']}
            - **Currency**: {result['currency_4']}
            - **New**: {result['new_4']}
            - **Renew**: {result['renew_4']}
            - **Transfer**: {result['transfer_4']}
            - **Registrar Website**: {result['reg_web_4']}
            ### 5th:
            - **Registrar**: {result['reg_4']}
            - **Currency**: {result['currency_4']}
            - **New**: {result['new_4']}
            - **Renew**: {result['renew_4']}
            - **Transfer**: {result['transfer_4']}
            - **Registrar Website**: {result['reg_web_4']}
            """
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
            f"""
            ## Domain Registrar
            **Registrar**: {result['reg']} **| Registrar Website**: {result['reg_web']} **| Order**: {result['order']}
            ### 1st:
            **Domain**: {result['domain_1']}
            **New**: {result['new_1']}
            **Renew**: {result['renew_1']}
            **Transfer**: {result['transfer_1']}
            **Currency**: {result['currency_1']}
            ### 2nd:
            **Domain**: {result['domain_2']}
            **New**: {result['new_2']}
            **Renew**: {result['renew_2']}
            **Transfer**: {result['transfer_2']}
            **Currency**: {result['currency_2']}
            ### 3rd:
            **Domain**: {result['domain_3']}
            **New**: {result['new_3']}
            **Renew**: {result['renew_3']}
            **Transfer**: {result['transfer_3']}
            **Currency**: {result['currency_3']}
            ### 4th:
            **Domain**: {result['domain_4']}
            **New**: {result['new_4']}
            **Renew**: {result['renew_4']}
            **Transfer**: {result['transfer_4']}
            **Currency**: {result['currency_4']}
            ### 5th:
            **Domain**: {result['domain_5']}
            **New**: {result['new_5']}
            **Renew**: {result['renew_5']}
            **Transfer**: {result['transfer_5']}
            **Currency**: {result['currency_5']}
            """
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


# /info
@client.tree.command(name='info', description="Some information about this bot")
async def version(interaction: discord.Interaction):
    await interaction.response.send_message(
        """
        ## JianyueBot
        This bot was developed by [JianyueLab](https://eke.vin). 
        If you have any questions or require assistance, please contact @jianyuehugo.
        - **Github Repo**: https://github.com/jianyuelab/jianyuebot
        - **Bot Version:** {bot_version}
        - **Bot Build:** {bot_build}
        - **Settings Version:** {setting_version}
        - **Build Type:** {bot_type}
        """,
        ephemeral=True
    )


client.run(TOKEN)
