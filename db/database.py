import sqlite3


class Database:
    """Class for members database."""

    def __init__(self):
        """Database constructor."""
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS members(
                    user_id TEXT,
                    user_mail TEXT,
                    user_code TEXT,
                    is_user_on_server INTEGER
                    )
                """)

    def add_new_member(self):
        """Add a new member to the database using the discord ID as user_id
        and leave mail and code empty for now."""
        # TODO

    def update_mail(self, user, mail):
        """Update user's mail."""
        # TODO

    def update_code(self, user, code):
        """Update user's code for authentication."""
        # TODO
