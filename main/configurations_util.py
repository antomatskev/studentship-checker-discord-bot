class ConfigurationsUtil:

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
        file_data = self.get_data()
        pwd = file_data[2]
        addr = file_data[3]
        return addr, pwd
