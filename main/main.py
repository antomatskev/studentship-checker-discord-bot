"""Main file to start the whole bot."""

import discord
from discord.ext import commands

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix=".", intents=intents)


@client.event
async def on_ready():
    print("Bot is ready")


@client.event
async def on_member_join(member):
    print(f"{member} has joined the server!")


@client.event
async def on_member_remove(member):
    print(f"{member} has left the server!")


client.run("NzkwNDU1MjgyNjgwODU2NTk4.X-A22Q.wFy3IO7TTOE_fm1h10kkzTpRaVU")
