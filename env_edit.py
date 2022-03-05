#!/bin/python3 -u
import os
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands
import asyncio
from datetime import date

load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('env_edit started on bot {0.user}'.format(client))
    
@client.command()
async def env_edit(ctx, env_new):
    #code goes here


@env_edit.error
async def env_edit_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Usage: !env_edit <text>")


client.run(os.getenv('TOKEN'))

