class NotKenzieEmailError(Exception):
    default_message = "email precisa ser @kenzie.com"

    def __init__(self, message=None) -> None:
        self.message = message or self.default_message


def is_kenzie_domain(email: str):
    if not email.endswith("@kenzie.com"):
        raise NotKenzieEmailError
