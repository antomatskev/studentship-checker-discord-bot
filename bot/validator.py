class MailValidator:
    """Class for checking if the mail address is valid."""

    def __init__(self, mail):
        """."""
        self._mail = mail

    def is_correct_mail(self):
        """Check if entered e-mail's domain is correct."""
        print(f"===DEBUG: checking if an email {self._mail} is correct")
        return self._mail.endswith("ttu.ee") or self._mail.endswith("taltech.ee")
