import discord

from client.mail import Mail
from db.code import Code


class Talk:
    """Class responsible for talks with users."""

    def __init__(self, db, user):
        """."""
        self._db = db
        self._user = user

    async def talk_to_user(self, message, user):
        if type(message.channel) is discord.channel.DMChannel:
            print(f"===DEBUG: Message object: {message}")
            print(f"===DEBUG: Message content: {message.content}")
            print(f"===DEBUG: Message author: {user}")
            # TODO: make the conversation to work with user's state.
            if self._db.is_user_in_table(user):
                if self._db.is_code_sent(user):
                    if self._db.get_user_code(user) == self.clean_message(message.content):
                        await user.send("You look like a student. Welcome aboard.")
                        self.accept_user()
                if not self._db.update_user_mail(user,
                                                 message.content):  # TODO: FIX: this check comes again after entering the code.
                    await user.send("Your e-mail looks incorrect. Try again.")
                else:
                    code = Code().generate_code()
                    self._db.update_user_code(user, code)
                    mail = self._db.get_user_mail(user)
                    print(f"===DEBUG: mail for {user} from DB is {mail}")
                    Mail(user, mail).send_code_to_mail(mail, code)
                    await user.send("I've sent you a code. Enter it.")
                    print(f"===DEBUG: Generated code: {code}")
            else:
                await user.send(
                    "Seems that you aren`t registered jet. Enter your school e-mail. I'll send you a confirmation code.")
                self._db.add_new_user(user)

    @staticmethod
    def clean_message(msg):
        """Eliminate all non-digits and non-uppercase letters."""
        alphabet = list('1234567890QWERTYUIOPASDFGHJKLZXCVBNM')
        return "".join([x for x in msg if x in alphabet])

    def accept_user(self):
        """Accepting user, changing the role etc."""
        # TODO
