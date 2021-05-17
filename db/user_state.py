import enum


class UserState(enum.Enum):
    """User's state in authentication process."""
    NEWBIE = 0
    NAME_IN_DB = 1
    MAIL_IN_DB = 2
    CODE_GENERATED = 3
    CODE_SENT = 4
    CONFIRMED = 5
