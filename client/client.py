"""Class for bot client."""

import discord

from client.mail import Mail
from code import Code
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
            if type(message.channel) is discord.channel.DMChannel:
                print(f"===DEBUG: Message object: {message}")
                print(f"===DEBUG: Message content: {message.content}")
                print(f"===DEBUG: Message author: {user}")
                if self.db.is_user_in_table(user):
                    if self.db.is_code_sent(user):
                        if self.db.get_user_code(user) == self.clean_message(message.content):
                            await user.send("You look like a student. Welcome aboard.")
                            self.accept_user()
                    if not self.db.update_user_mail(user,
                                                    message.content):  # TODO: FIX: this check comes again after entering the code.
                        await user.send("Your e-mail looks incorrect. Try again.")
                    else:
                        code = Code().generate_code()
                        self.db.update_user_code(user, code)
                        mail = self.db.get_user_mail(user)
                        print(f"===DEBUG: mail for {user} from DB is {mail}")
                        Mail(user, mail).send_code_to_mail(mail, code)
                        await user.send("I've sent you a code. Enter it.")
                        print(f"===DEBUG: Generated code: {code}")
                else:
                    await user.send(
                        "Seems that you aren`t registered jet. Enter your school e-mail. I'll send you a confirmation code.")
                    self.db.add_new_user(user)

    @staticmethod
    def clean_message(msg):
        """Eliminate all non-digits and non-uppercase letters."""
        alphabet = list('1234567890QWERTYUIOPASDFGHJKLZXCVBNM')
        return "".join([x for x in msg if x in alphabet])

    def accept_user(self):
        """Accepting user, changing the role etc."""
        # TODO
