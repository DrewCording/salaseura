#!/bin/python3 -u
import os
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands
import asyncio
import mysql.connector
from time inport datetime

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
    print('tulokas started on bot {0.user}'.format(client))


async def checkin():
	await client.wait_until_ready()
    try:
        #Code goes here

        break;

	except: 
		print("Checkin crashed at " datetime.now())


client.loop.create_task(checkin())
client.run(os.getenv('TOKEN'))

