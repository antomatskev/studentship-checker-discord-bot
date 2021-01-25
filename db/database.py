import sqlite3

import discord

from client.mail import Mail


class Database:
    """Class for members database."""

    def __init__(self):
        """Database constructor."""
        self.db = sqlite3.connect("main.sqlite")
        self.cursor = self.db.cursor()
        self.init_table()

    def init_table(self):
        """Create table if necessary."""
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS members(
                    user_id TEXT PRIMARY KEY UNIQUE,
                    user_mail TEXT UNIQUE,
                    user_code TEXT UNIQUE,
                    is_user_on_server INTEGER,
                    is_code_sent INTEGER
                    )
                """)
        self.db.commit()

    def add_new_member(self, member: discord.User.id):
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

    def update_mail(self, user, mail):
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

    def update_code(self, user, code):
        """Update user's code for authentication."""
        print(f"===DEBUG: setting a code {code} for {user}")
        self.cursor.execute(f"""
            UPDATE members
            SET user_code = '{code}'
            WHERE user_id = '{user}'
        """)
        # TODO: create separate method for retrieving a mail.
        self.cursor.execute(f"""
            SELECT user_mail FROM members
            WHERE user_id='{user}'
        """)
        mail = self.cursor.fetchone()[0]
        print(f"===DEBUG: mail for {user} from DB is {mail}")
        Mail(user, mail).send_code_to_mail(mail, code)
        self.db.commit()

    def is_user_in_table(self, user):
        """Check if the user is already in our table."""
        print(f"===DEBUG: checking if an user {user} is in table")
        self.cursor.execute(f"""
            SELECT * FROM members WHERE EXISTS 
            (SELECT user_id FROM members WHERE user_id = '{user}')
        """)
        return self.cursor.fetchone()

    def code_was_sent(self, user):
        """Updating is_code_sent field in database to 1"""
        self.cursor.execute(f"""
                UPDATE members SET is_code_sent = 1 WHERE user_id = '{user}'
            """)
        self.db.commit()

    def is_code_sent(self, user):
        """Make sure the code is sent to user. And change the corresponding value in the table."""
        self.cursor.execute(f"""
                SELECT is_code_sent FROM members WHERE user_id = '{user}'
            """)
        return self.cursor.fetchone()[0]

    def get_code(self, user):
        """Return generated user's code from the table."""
        self.cursor.execute(f"""
                SELECT user_code FROM members WHERE user_id = '{user}'
            """)
        return self.cursor.fetchone()[0]
