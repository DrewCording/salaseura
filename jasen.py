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
    print('jasen started on bot {0.user}'.format(client))
    
@client.command()
async def jasen(ctx, user: discord.Member):
    guest_role = discord.utils.get(ctx.guild.roles, name=os.getenv('guest_role'))
    probation_role = discord.utils.get(ctx.guild.roles, name=os.getenv('probation_role'))
    member_role = discord.utils.get(ctx.guild.roles, name=os.getenv('member_role'))
    mod_role = discord.utils.get(ctx.guild.roles, name=os.getenv('mod_role'))
    announce_channel = discord.utils.get(ctx.guild.channels, name=os.getenv('announce_channel'))
    commands_channel = discord.utils.get(ctx.guild.channels, name=os.getenv('commands_channel'))
    
    if ctx.channel == commands_channel:
        if mod_role in ctx.author.roles:
            if probation_role in user.roles:
                await user.remove_roles(probation_role)
                await user.add_roles(member_role)
                await ctx.send("<@!" + str(user.id) + "> taken off probation and given membership on " + str(date.today()))
        
                mycursor = mydb.cursor()
                mycursor.execute("DELETE FROM members WHERE user_id=" + str(user.id))
                mydb.commit()
            else:
                await ctx.send("Error. This command can only be used on users with " + str(probation_role) + " role.")
        else:
            await ctx.send("Error. This command can only be used by users with " + str(mod_role) + " role.")
    else:
        await ctx.send("Error. This command can only be used in <#" + str(commands_channel.id) + ">.")


@jasen.error
async def jasen_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Usage: !jasen @user")


client.run(os.getenv('TOKEN'))

