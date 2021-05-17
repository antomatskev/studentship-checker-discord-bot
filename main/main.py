"""Main file to start the whole bot."""
import enum
import logging
import sqlite3

import discord
import yagmail

# from bot.client import BotClient
# from bot.mail import Mail
# from bot.talk import Talk
from configurations_util import ConfigurationsUtil
# Set up logging
from db.code import Code


# from db.database import Database


# from db.user_state import UserState


class BotClient(discord.Client):
    """Bot bot."""

    def __init__(self, command_prefix, intents):
        """Constructor."""
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.db = Database()

    async def on_ready(self):
        print("===DEBUG: Bot is ready")

    async def on_member_join(self, member):
        print(f"===DEBUG: {member} has joined the server!")
        user = User(member, self.db)
        if user.state() == UserState.NEWBIE and self.db.add_new_user(member):
            await member.send("Hey! Enter your school e-mail. I'll send you a confirmation code.")
            user.change_state(UserState.NAME_IN_DB)
        else:
            await member.send("Welcome back!")
            if user.state() == UserState.NAME_IN_DB:
                await member.send("Enter your school e-mail. I'll send you a confirmation code.")
            elif user.state() == UserState.MAIL_IN_DB:
                await member.send("I'm generating a confirmation code for you...")
                # await Talk(self.db, user).generate_and_mail_code(user)
            elif user.state() == UserState.CODE_GENERATED:
                await member.send("Code generated!")
            elif user.state() == UserState.CODE_SENT:
                await member.send("Check your e-mail for the confirmation code.")
            elif user.state() == UserState.CONFIRMED:
                await member.send("You are already confirmed.")

    async def on_member_remove(self, member):
        print(f"===DEBUG: {member} has left the server!")

    async def on_message(self, message):
        user = message.author
        if user == self.user:
            return
        else:  # Private messages.
            await Talk(self.db, user).talk_to_user(message, user)


class Talk:
    """Class responsible for talks with users."""

    def __init__(self, db, user):
        """."""
        self._db = db
        self._user = user
        self._usr = User(user, db)

    async def talk_to_user(self, message, user):
        if type(message.channel) is discord.channel.DMChannel:
            print(f"===DEBUG: Message object: {message}")
            print(f"===DEBUG: Message content: {message.content}")
            print(f"===DEBUG: Message author: {user}")
            # TODO: make the conversation to work with user's state.
            if self._usr.state() == UserState.NEWBIE or self._usr.state() == UserState.NAME_IN_DB:
                if self._db.update_user_mail(user, message.content):
                    self._usr.change_state(UserState.MAIL_IN_DB)
                    await self.generate_and_mail_code(user)
                else:
                    await user.send("Your school e-mail looks incorrect. Try again.")
            elif self._usr.state() == UserState.MAIL_IN_DB or self._usr.state() == UserState.CODE_GENERATED or self._usr.state() == UserState.CODE_SENT:
                if self._db.get_user_code(user) == self.clean_message(message.content):
                    await user.send("You look like a student. Welcome aboard.")
                    await self.accept_user(user)
                else:
                    await user.send("Wrong code. Check your school e-mail and try again.")

            # if self._db.is_user_in_table(user):
            #     if self._db.is_code_sent(user):
            #         if self._db.get_user_code(user) == self.clean_message(message.content):
            #             await user.send("You look like a student. Welcome aboard.")
            #             self.accept_user()
            #     if not self._db.update_user_mail(user,
            #                                      message.content):  # TODO: FIX: this check comes again after entering the code.
            #         await user.send("Your e-mail looks incorrect. Try again.")
            #     else:
            #         await self.generate_and_mail_code(user)
            else:
                await user.send(
                    "Seems that you aren`t registered yet. Enter your school e-mail. I'll send you a confirmation code.")
                self._db.add_new_user(user)

    async def accept_user(self, user):
        """Accepting user, changing the role etc."""
        # TODO
        self._db.set_user_confirmed(user.name())
        jun = discord.utils.get(user.name().server.roles, name="джун")
        stud = discord.utils.get(user.name().server.roles, name="студент")
        intern = discord.utils.get(user.name().server.roles, name="стажёр")
        await client.add_roles(user.name(), jun)
        await client.add_roles(user.name(), stud)
        await client.remove_roles(user.name(), intern)

    async def generate_and_mail_code(self, user):
        code = Code().generate_code()
        self._db.update_user_code(user, code)
        self._usr.change_state(UserState.CODE_GENERATED)
        mail = self._db.get_user_mail(user)
        print(f"===DEBUG: mail for {user} from DB is {mail}")
        Mail(user, mail).send_code_to_mail(mail, code)
        self._usr.change_state(UserState.CODE_SENT)
        await user.send("I've sent you a code. Enter it.")
        print(f"===DEBUG: Generated code: {code}")

    @staticmethod
    def clean_message(msg):
        """Eliminate all non-digits and non-uppercase letters."""
        alphabet = list('1234567890QWERTYUIOPASDFGHJKLZXCVBNM')
        return "".join([x for x in msg if x in alphabet])


class Mail:
    """Class for mail, which can be composed and sent."""

    def __init__(self, user, address):
        """."""
        self._user = user
        self._address = address

    def get_address(self):
        """."""
        return self._address

    def send_code_to_mail(self, user_mail, code):
        """Send an e-mail with the code."""
        body = f"""Hey!
        Here is your discord server's code:

            {code}

        Tell it to the Studentship Checker bot."""
        # Only gmail account can be used. Need to provide user (example -> something@gmail.com) and APP password.
        usr, pwd = ConfigurationsUtil().get_mail()
        if usr and pwd:
            yag = yagmail.SMTP(usr, pwd)
        else:
            yag = yagmail.SMTP(user_mail="", password="")
        yag.send(
            to=user_mail,
            subject="Studentship Checker code",
            contents=body,
        )

    def is_correct(self):
        """Check if the mail address is correct."""
        return MailValidator(self._address).is_correct_mail()


class User:
    """Represents discord user."""

    def __init__(self, name, db):
        """."""
        self._name = name
        self._db = db
        self._state = self.determine_state()

    def change_state(self, state):
        """Change state."""
        self._state = state

    def determine_state(self):
        """Determine user's state basing on DB data."""
        # TODO: most probably this will be slow, so will need to refactor.
        ret = UserState.NEWBIE
        if self._db.is_user_in_table(self._name):
            ret = UserState.NAME_IN_DB
            if self._db.get_user_mail(self._name):
                ret = UserState.MAIL_IN_DB
                if self._db.is_code_sent(self._name):
                    ret = UserState.CODE_SENT
                    if self._db.is_user_confirmed(self._name):
                        ret = UserState.CONFIRMED
        return ret

    def name(self):
        return self._name

    def state(self):
        return self._state

    def is_name_in_db(self):
        return self._state == UserState.NAME_IN_DB

    def is_mail_in_db(self):
        return self._state == UserState.MAIL_IN_DB

    def is_code_generated(self):
        return self._state == UserState.CODE_GENERATED

    def is_code_sent(self):
        return self._state == UserState.CODE_SENT

    def is_confirmed(self):
        return self._state == UserState.CONFIRMED


class UserState(enum.Enum):
    """User's state in authentication process."""
    NEWBIE = 0
    NAME_IN_DB = 1
    MAIL_IN_DB = 2
    CODE_GENERATED = 3
    CODE_SENT = 4
    CONFIRMED = 5


class MailValidator:
    """Class for checking if the mail address is valid."""

    def __init__(self, mail):
        """."""
        self._mail = mail

    def is_correct_mail(self):
        """Check if entered e-mail's domain is correct."""
        print(f"===DEBUG: checking if an email {self._mail} is correct")
        return self._mail.endswith("ttu.ee") or self._mail.endswith("taltech.ee")


class Database:
    """Class for members database."""

    def __init__(self):
        """Database constructor."""
        self.db = sqlite3.connect("main.sqlite")
        self.cursor = self.db.cursor()
        self.init_table()

    def init_table(self):
        """Create table if necessary."""
        # TODO: check if is_user_on_server is needed at all.
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS members(
                    user_id TEXT PRIMARY KEY UNIQUE,
                    user_mail TEXT UNIQUE,
                    user_code TEXT UNIQUE,
                    is_user_on_server INTEGER,
                    is_code_sent INTEGER,
                    is_user_confirmed INTEGER
                    )
                """)
        self.db.commit()

    def add_new_user(self, member: discord.User.id):
        """Add a new member to the database using the discord ID as user_id
        and leave mail and code empty for now."""
        ret = False
        try:
            self.cursor.execute(f"""
                INSERT INTO members(user_id, is_code_sent)
                VALUES ('{member}', 0)
            """)
            ret = True
        except sqlite3.IntegrityError:
            print(f"===DEBUG: {member} is already in the DB!")
        self.db.commit()
        print(f"===DEBUG: {member}")
        self.cursor.execute("""SELECT * FROM members""")
        print(f"===DEBUG: {self.cursor.fetchone()}")
        return ret

    def update_user_mail(self, user, mail):
        """Update user's mail."""
        print(f"===DEBUG: setting an email {mail} for {user}")
        ret = Mail(user, mail).is_correct()
        if ret:
            self.cursor.execute(f"""
                UPDATE members
                SET user_mail = '{mail}'
                WHERE user_id = '{user}'
            """)
            self.db.commit()
        return ret

    def update_user_code(self, user, code):
        """Update user's code for authentication."""
        print(f"===DEBUG: setting a code {code} for {user}")
        self.cursor.execute(f"""
            UPDATE members
            SET user_code = '{code}'
            WHERE user_id = '{user}'
        """)
        mail = self.get_user_mail(user)
        print(f"===DEBUG: mail for {user} from DB is {mail}")
        Mail(user, mail).send_code_to_mail(mail, code)

    def get_user_mail(self, user):
        self.cursor.execute(f"""
            SELECT user_mail FROM members
            WHERE user_id='{user}'
        """)
        mail = self.cursor.fetchone()[0]
        return mail

    def is_user_in_table(self, user):
        """Check if the user is already in our table."""
        print(f"===DEBUG: checking if an user {user} is in table")
        self.cursor.execute(f"""
            SELECT * FROM members WHERE EXISTS 
            (SELECT user_id FROM members WHERE user_id = '{user}')
        """)
        return self.cursor.fetchone()

    def set_code_was_sent(self, user):
        """Updating is_code_sent field in database to 1"""
        self.cursor.execute(f"""
                UPDATE members SET is_code_sent = 1 WHERE user_id = '{user}'
            """)
        self.db.commit()

    def set_user_confirmed(self, user):
        """Updating is_user_confirmed field in database to 1"""
        self.cursor.execute(f"""
                UPDATE members SET is_user_confirmed = 1 WHERE user_id = '{user}'
            """)
        self.db.commit()

    def is_code_sent(self, user):
        """Make sure the code is sent to user. And change the corresponding value in the table."""
        self.cursor.execute(f"""
                SELECT is_code_sent FROM members WHERE user_id = '{user}'
            """)
        return self.cursor.fetchone()[0]

    def is_user_confirmed(self, user):
        """Make sure the user is confirmed."""
        self.cursor.execute(f"""
                SELECT is_user_confirmed FROM members WHERE user_id = '{user}'
            """)
        return self.cursor.fetchone()[0]

    def get_user_code(self, user):
        """Return generated user's code from the table."""
        self.cursor.execute(f"""
                SELECT user_code FROM members WHERE user_id = '{user}'
            """)
        return self.cursor.fetchone()[0]


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = BotClient(command_prefix=".", intents=intents)
client.run(ConfigurationsUtil().get_token())

# async def accept_user(self, user):
#     """Accepting user, changing the role etc."""
#     # TODO
#     self._db.set_user_confirmed(user.name())
#     jun = discord.utils.get(user.name().server.roles, name="джун")
#     stud = discord.utils.get(user.name().server.roles, name="студент")
#     intern = discord.utils.get(user.name().server.roles, name="стажёр")
#     await client.add_roles(user.name(), jun)
#     await client.add_roles(user.name(), stud)
#     await client.remove_roles(user.name(), intern)
