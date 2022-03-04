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
    print('tulokas started on bot {0.user}'.format(client))
    
@client.command()
async def tulokas(ctx, user: discord.Member):
    guest_role = discord.utils.get(ctx.guild.roles, name=os.getenv('guest_role'))
    probation_role = discord.utils.get(ctx.guild.roles, name=os.getenv('probation_role'))
    member_role = discord.utils.get(ctx.guild.roles, name=os.getenv('member_role'))
    announce_channel = discord.utils.get(ctx.guild.channels, name=os.getenv('announce_channel'))
    commands_channel = discord.utils.get(ctx.guild.channels, name=os.getenv('commands_channel'))

    print(guest_role)
    print(probation_role)
    print(member_role)
    print(announce_channel)
    print(commannds_channel)



@tulokas.error
async def tulokas_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Usage: !tulokas @user")


client.run(os.getenv('TOKEN'))

