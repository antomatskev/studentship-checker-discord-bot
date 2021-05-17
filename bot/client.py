"""Class for bot bot."""

import discord

from bot.talk import Talk
from db.database import Database
from db.user import User, UserState


# class BotClient(discord.Client):
#     """Bot bot."""
#
#     def __init__(self, command_prefix, intents):
#         """Constructor."""
#         super().__init__(command_prefix=command_prefix, intents=intents)
#         self.db = Database()
#
#     async def on_ready(self):
#         print("===DEBUG: Bot is ready")
#
#     async def on_member_join(self, member):
#         print(f"===DEBUG: {member} has joined the server!")
#         user = User(member, self.db)
#         if user.state() == UserState.NEWBIE and self.db.add_new_user(member):
#             await member.send("Hey! Enter your school e-mail. I'll send you a confirmation code.")
#             user.change_state(UserState.NAME_IN_DB)
#         else:
#             await member.send("Welcome back!")
#             if user.state() == UserState.NAME_IN_DB:
#                 await member.send("Enter your school e-mail. I'll send you a confirmation code.")
#             elif user.state() == UserState.MAIL_IN_DB:
#                 await member.send("I'm generating a confirmation code for you...")
#                 # await Talk(self.db, user).generate_and_mail_code(user)
#             elif user.state() == UserState.CODE_GENERATED:
#                 await member.send("Code generated!")
#             elif user.state() == UserState.CODE_SENT:
#                 await member.send("Check your e-mail for the confirmation code.")
#             elif user.state() == UserState.CONFIRMED:
#                 await member.send("You are already confirmed.")
#
#     async def on_member_remove(self, member):
#         print(f"===DEBUG: {member} has left the server!")
#
#     async def on_message(self, message):
#         user = message.author
#         if user == self.user:
#             return
#         else:  # Private messages.
#             await Talk(self.db, user).talk_to_user(message, user)
