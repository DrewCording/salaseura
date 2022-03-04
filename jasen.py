#!/bin/python3 -u
import os
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands
import asyncio
import mysql.connector

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
    print('jasen started on bot {0.user}'.format(client))
    
@client.command()
async def jasen(ctx, user: discord.Member):
    #Code goes here


@jasen.error
async def jasen_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Usage: !jasen @user")


client.run(os.getenv('TOKEN'))

