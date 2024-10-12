import os


class Secret:
    def get_secret():
        return os.environ["SECRET"]
