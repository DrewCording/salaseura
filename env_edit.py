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
    load_dotenv()
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
            await ctx.send("Virhe! Tätä komentoa voi käyttää vain <@!" + str(owner.id) + ">")
        else:
            await ctx.send("Virhe! Tätä komentoa voi käyttää vain omistaja. Häntä ei löytynyt, onko nimi vaihtunut?")


@env_edit.error
async def env_edit_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        owner = discord.utils.get(ctx.guild.members, name=os.getenv('owner_name'))

        if ctx.author == owner:
            await ctx.send("Käyttö: !env_edit <teksti>")
            env_file = open(".env", "r")
            await ctx.send("Tämänhetkinen .env teksti:\n" + str(env_file.read()))
            env_file.close()
        else:
            if owner:
                await ctx.send("Virhe! Tätä komentoa voi käyttää vain <@!" + str(owner.id) + ">")
            else:
                await ctx.send("Virhe! Tätä komentoa voi käyttää vain omistaja. Häntä ei löytynyt, onko nimi vaihtunut?")


client.run(os.getenv('TOKEN'))

