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
    owner = discord.utils.get(ctx.guild.members, name=os.getenv('owner_name'))

    if ctx.author == owner:
        env_file = open(".env", "w")
        env_file.write(str(env_new))
        env_file.close()
        await ctx.send("New .env text:")
        env_file = open(".env", "r")
        await ctx.send(str(env_file.read()))
        env_file.close()
    else:
        if owner:
            await ctx.send("Error. This command can only be used by <@!" + str(owner.id) + ">")
        else:
            await ctx.send("Error. This command can onnly be used by the owner. Owner not found. Did they change names?")


@env_edit.error
async def env_edit_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Usage: !env_edit <text>")
        env_file = open(".env", "r")
        await ctx.send("Current .env text:\n" + str(env_file.read()))
        env_file.close()

client.run(os.getenv('TOKEN'))

