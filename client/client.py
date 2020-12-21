"""Class for bot client."""

import discord


class BotClient(discord.Client):
    """Bot client."""

    async def on_ready(self):
        print("Bot is ready")

    async def on_member_join(self, member):
        print(f"{member} has joined the server!")
        await member.send("Hey!")

    async def on_member_remove(self, member):
        print(f"{member} has left the server!")

    async def on_message(self, message):
        if message.author == self.user:
            return
        else:  # Private messages.
            if type(message.channel) is discord.channel.DMChannel:
                print(message.content)
