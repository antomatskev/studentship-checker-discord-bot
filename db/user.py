import enum


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
