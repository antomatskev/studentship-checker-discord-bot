import random


class Code:
    """Class for code, which is sent by mail and checked by the bot."""

    def __init__(self):
        """."""

    def generate_code(self):
        """Generate verification code."""
        alphabet = list('1234567890QWERTYUIOPASDFGHJKLZXCVBNM')
        return "".join(map(lambda x: random.choice(alphabet), (["0"] * 32)))
