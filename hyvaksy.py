#!/bin/python3 -u
import os
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands
import asyncio
import mysql.connector
from datetime import date

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
    print('hyvaksy started on bot {0.user}'.format(client))
    
@client.command()
async def hyvaksy(ctx, user: discord.Member):
    load_dotenv()
    guest_role = discord.utils.get(ctx.guild.roles, name=os.getenv('guest_role'))
    probation_role = discord.utils.get(ctx.guild.roles, name=os.getenv('probation_role'))
    member_role = discord.utils.get(ctx.guild.roles, name=os.getenv('member_role'))
    mod_role = discord.utils.get(ctx.guild.roles, name=os.getenv('mod_role'))
    announce_channel = discord.utils.get(ctx.guild.channels, name=os.getenv('announce_channel'))
    commands_channel = discord.utils.get(ctx.guild.channels, name=os.getenv('commands_channel'))
    today = date.today()
    
    if ctx.channel == commands_channel:
        if mod_role in ctx.author.roles:
            if guest_role in user.roles:
                await user.remove_roles(guest_role)
                await user.add_roles(probation_role)
                await ctx.send("<@!" + str(user.id) + "> on asetettu Tulokkaaksi " + str(today.strftime("%d.%m.%y")))
        
                mycursor = mydb.cursor()
                sql = "INSERT INTO members (user_id, discord_tag, join_date) VALUES (%s, %s, %s)"
                val = (user.id, str(user), date.today())
                mycursor.execute(sql, val)
                mydb.commit()
            else:
                await ctx.send("Virhe! Tätä komentoa voi käyttää vain käyttäjiin, joilla on " + str(guest_role) + " -rooli.")
        else:
            await ctx.send("Virhe! Tätä komentoa voi käyttää vain käyttäjät, joilla on <@&" + str(mod_role.id) + "> -rooli.")
    else:
        await ctx.send("Virhe! Tätä komentoa voi käyttää vain kanavalla <#" + str(commands_channel.id) + ">.")

@hyvaksy.error
async def hyvaksy(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Käyttö: !hyvaksy @user")


client.run(os.getenv('TOKEN'))

