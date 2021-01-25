"""Class for bot client."""

import discord

from client.talk import Talk
from db.database import Database


class BotClient(discord.Client):
    """Bot client."""

    def __init__(self, command_prefix, intents):
        """Constructor."""
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.db = Database()

    async def on_ready(self):
        print("===DEBUG: Bot is ready")

    async def on_member_join(self, member):
        print(f"===DEBUG: {member} has joined the server!")
        await member.send("Hey! Enter your school e-mail. I'll send you a confirmation code.")
        # TODO: switch with sending a message, so we could specify the message to send for already existing users.
        self.db.add_new_user(member)

    async def on_member_remove(self, member):
        print(f"===DEBUG: {member} has left the server!")

    async def on_message(self, message):
        user = message.author
        if user == self.user:
            return
        else:  # Private messages.
            await Talk(self.db, user).talk_to_user(message, user)
