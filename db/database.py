import sqlite3


class Database:
    """Class for members database."""

    def __init__(self):
        """Database constructor."""
        self.db = sqlite3.connect("main.sqlite")
        self.cursor = self.db.cursor()
        self._is_code_sent = False
        self.init_table()

    def init_table(self):
        """Create table if necessary."""
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS members(
                    user_id TEXT,
                    user_mail TEXT,
                    user_code TEXT,
                    is_user_on_server INTEGER
                    )
                """)

    def add_new_member(self, member):
        """Add a new member to the database using the discord ID as user_id
        and leave mail and code empty for now."""
        # TODO
        print(f"===DEBUG: {member}")

    def update_mail(self, user, mail):
        """Update user's mail."""
        # TODO
        print(f"===DEBUG: setting an email {mail} for {user}")
        if self.is_correct_mail(mail):
            pass
        else:
            pass
        return True

    def update_code(self, user, code):
        """Update user's code for authentication."""
        # TODO
        print(f"===DEBUG: setting a code {code} for {user}")
        self.send_code_to_mail()

    def is_user_in_table(self, user):
        """Check if the user is already in our table."""
        # TODO
        print(f"===DEBUG: checking if an user {user} is in table")
        return True

    def is_correct_mail(self, mail):
        """Check if entered e-mail's domain is correct."""
        # TODO
        print(f"===DEBUG: checking if an email {mail} is correct")
        return True

    def is_code_sent(self, user):
        """Make sure the code is sent to user. And change the corresponding value in the table."""
        # TODO
        return self._is_code_sent

    def send_code_to_mail(self):
        """Send an e-mail with the code."""
        self._is_code_sent = True

    def get_code(self, user):
        """Return generated user's code from the table."""
        # TODO
        return "123"
