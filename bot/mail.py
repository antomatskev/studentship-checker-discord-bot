import yagmail

from main.configurations_util import ConfigurationsUtil
from bot.validator import MailValidator


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
