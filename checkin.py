#!/bin/python3 -u
import os
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands
import asyncio
import mysql.connector
from datetime import date
from datetime import datetime
from datetime import timedelta

load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv('db_password'),
    database="salaseura"
)

mycursor = mydb.cursor()

@client.event
async def on_ready():
    print('checkin started on bot {0.user}'.format(client))
    await client.wait_until_ready()
    
    load_dotenv()
    guild = discord.utils.get(client.guilds, name=os.getenv('guild_name'))
    guest_role = discord.utils.get(guild.roles, name=os.getenv('guest_role'))
    probation_role = discord.utils.get(guild.roles, name=os.getenv('probation_role'))
    member_role = discord.utils.get(guild.roles, name=os.getenv('member_role'))
    mod_role = discord.utils.get(guild.roles, name=os.getenv('mod_role'))
    announce_channel = discord.utils.get(guild.channels, name=os.getenv('announce_channel'))
    commands_channel = discord.utils.get(guild.channels, name=os.getenv('commands_channel'))

    today = date.today()
    min_probation = today - timedelta(days=int(os.getenv('min_probation')))
    warn_probation = today - timedelta(days=int(os.getenv('warn_probation')))
    max_probation = today - timedelta(days=int(os.getenv('max_probation')))

    mycursor = mydb.cursor()
    mycursor.execute(str("SELECT user_id FROM members WHERE join_date='" + str(min_probation) + "'"))
    min_probation_members = mycursor.fetchall()
    mydb.commit()

    mycursor = mydb.cursor()
    mycursor.execute(str("SELECT user_id FROM members WHERE join_date='" + str(warn_probation) + "'"))
    warn_probation_members = mycursor.fetchall()
    mydb.commit()

    mycursor = mydb.cursor()
    mycursor.execute(str("SELECT user_id FROM members WHERE join_date='" + str(max_probation) + "'"))
    max_probation_members = mycursor.fetchall()
    mydb.commit()

    for member in min_probation_members:
        numeric_filter = filter(str.isdigit, str(member))
        member_numeric = "".join(numeric_filter)
        await announce_channel.send("<@!" + str(member_numeric) + "> has been on probation for " + str(os.getenv('min_probation')) + " days today and is eligible for membership.")

    for member in warn_probation_members:
        numeric_filter = filter(str.isdigit, str(member))
        member_numeric = "".join(numeric_filter)
        await announce_channel.send("<@!" + str(member_numeric) + "> has been on probation for " + str(os.getenv('warn_probation')) + " days today and is eligible for membership.")


    for member in max_probation_members:
        numeric_filter = filter(str.isdigit, str(member))
        member_numeric = "".join(numeric_filter)
        await announce_channel.send("<@!" + str(member_numeric) + "> has been on probation for " + str(os.getenv('max_probation')) + " days today and has been demoted to guest.")

        user = discord.utils.get(guild.members, id=int(member_numeric))
        await user.add_roles(guest_role)
        await user.remove_roles(probation_role)

        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM members WHERE user_id=" + str(member_numeric))
        mydb.commit()

    await client.close()

client.run(os.getenv('TOKEN'))

