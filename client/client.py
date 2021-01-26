"""Class for bot client."""

import discord

from client.talk import Talk
from db.database import Database
from db.user import User, UserState


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
        user = User(member, self.db)
        if self.db.add_new_user(member):
            await member.send("Hey! Enter your school e-mail. I'll send you a confirmation code.")
            user.change_state(UserState.NAME_IN_DB)
        else:
            await member.send("Welcome back!")
            # TODO: specify message based on user's state.

    async def on_member_remove(self, member):
        print(f"===DEBUG: {member} has left the server!")

    async def on_message(self, message):
        user = message.author
        if user == self.user:
            return
        else:  # Private messages.
            await Talk(self.db, user).talk_to_user(message, user)
