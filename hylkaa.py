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
    print('hylkaa started on bot {0.user}'.format(client))
    
@client.command()
async def hylkaa(ctx, user: discord.Member):
    load_dotenv()
    guest_role = discord.utils.get(ctx.guild.roles, name=os.getenv('guest_role'))
    probation_role = discord.utils.get(ctx.guild.roles, name=os.getenv('probation_role'))
    member_role = discord.utils.get(ctx.guild.roles, name=os.getenv('member_role'))
    member_role2 = discord.utils.get(ctx.guild.roles, name=os.getenv('member_role2'))
    member_role3 = discord.utils.get(ctx.guild.roles, name=os.getenv('member_role3'))
    mod_role = discord.utils.get(ctx.guild.roles, name=os.getenv('mod_role'))
    announce_channel = discord.utils.get(ctx.guild.channels, name=os.getenv('announce_channel'))
    commands_channel = discord.utils.get(ctx.guild.channels, name=os.getenv('commands_channel'))
    today=date.today()
    
    if ctx.channel == commands_channel:
        if mod_role in ctx.author.roles:
            if probation_role in user.roles:
                await user.remove_roles(probation_role)
                await user.add_roles(guest_role)
                await ctx.send("<@!" + str(user.id) + "> taken off probation and returned to guest rank on " + str(today.strftime("%d.%m.%y")))
        
                mycursor = mydb.cursor()
                mycursor.execute("DELETE FROM members WHERE user_id=" + str(user.id))
                mydb.commit()
            else:
                await ctx.send("Error. This command can only be used on users with " + str(probation_role) + " role.")
        else:
            await ctx.send("Error. This command can only be used by users with <@&" + str(mod_role.id) + "> role.")
    else:
        await ctx.send("Error. This command can only be used in <#" + str(commands_channel.id) + ">.")


@hylkaa.error
async def hylkaa_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Usage: !hylkaa @user")


client.run(os.getenv('TOKEN'))

