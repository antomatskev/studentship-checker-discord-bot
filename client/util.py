class Util:

    def get_data(self):
        """Get data from local file."""
        try:
            with open("tkn") as f:
                lines = f.readlines()
        except IOError:
            print("Token file not found.")
        return lines

    def get_token(self):
        """Get a token from a local file content."""
        return self.get_data()[0]

    def get_mail(self):
        """Get sending mail data from a local file content."""
        pwd = self.get_data()[2].split("=")[1]
        addr = self.get_data()[3].split("=")[1]
        return addr, pwd
