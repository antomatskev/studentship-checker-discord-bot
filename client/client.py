"""Class for bot client."""

import discord
from discord.ext import commands


class BotClient(discord.Client):
    """Bot client."""

    async def on_ready(self):
        print("Bot is ready")

    async def on_member_join(self, member):
        print(f"{member} has joined the server!")

    async def on_member_remove(self, member):
        print(f"{member} has left the server!")
