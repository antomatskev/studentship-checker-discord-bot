"""Class for bot client."""
import random

import discord

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
        self.db.add_new_member(member)

    async def on_member_remove(self, member):
        print(f"===DEBUG: {member} has left the server!")

    async def on_message(self, message):
        if message.author == self.user:
            return
        else:  # Private messages.
            if type(message.channel) is discord.channel.DMChannel:
                print(f"===DEBUG: Message object: {message}")
                print(f"===DEBUG: Message content: {message.content}")
                print(f"===DEBUG: Message author: {message.author}")
                if self.db.is_user_in_table(message.author):
                    if self.db.is_code_sent(message.author):
                        if self.db.get_code(message.author) == self.clean_message(message.content):
                            await message.author.send("You look like a student. Welcome aboard.")
                            self.accept_user()
                    if not self.db.update_mail(message.author, message.content):
                        await message.author.send("Your e-mail looks incorrect. Try again.")
                    else:
                        code = self.generate_code()
                        self.db.update_code(message.author, code)
                        await message.author.send("I've sent you a code. Enter it.")
                        print(f"===DEBUG: Generated code: {code}")
                else:
                    await message.author.send("Seems that you aren`t registered jet. Enter your school e-mail. I'll send you a confirmation code.")
                    self.db.add_new_member(message.author)

    def generate_code(self):
        """Generate verification code."""
        alphabet = list('1234567890QWERTYUIOPASDFGHJKLZXCVBNM')
        return "".join(map(lambda x: random.choice(alphabet), (["0"] * 32)))

    @staticmethod
    def clean_message(msg):
        """Eliminate all non-digits and non-uppercase letters."""
        alphabet = list('1234567890QWERTYUIOPASDFGHJKLZXCVBNM')
        return "".join([x for x in msg if x in alphabet])

    def accept_user(self):
        """Accepting user, changing the role etc."""
        # TODO
