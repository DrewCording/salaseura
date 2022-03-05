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

    today = date.today()
    min_probation = today - timedelta(days=int(os.getenv('min_probation')))
    max_probation = today - timedelta(days=int(os.getenv('max_probation')))

    mycursor = mydb.cursor()
    #mycursor.execute(str("SELECT user_id FROM members WHERE join_date='" + str(min_probation) + "'"))
    mycursor.execute(str("SELECT user_id FROM members WHERE join_date='" + str(today) + "'"))
    min_probation_members = mycursor.fetchall()
    mydb.commit()

    mycursor = mydb.cursor()
    mycursor.execute(str("SELECT user_id FROM members WHERE join_date='" + str(max_probation) + "'"))
    max_probation_members = mycursor.fetchall()
    mydb.commit()

    for member in min_probation_members:
        print(member)

    await client.close()

client.run(os.getenv('TOKEN'))

