class UsernameTooLongException(Exception):
    def __str__(self):
        return "Username too long, must be at most 36 characters"

class UsernameTooShortException(Exception):
    def __str__(self):
        return "Username too short, must be at least 3 characters"


class UsernameTakenException(Exception):
    def __str__(self):
        return "Username was taken"


class WeakPasswordException(Exception):
    def __str__(self):
        return "Password must be at least 12 characters long, and contain uppercase leters, lowercase letters numbers numbers and symbols"
