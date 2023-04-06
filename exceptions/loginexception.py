class LoginException(Exception):
    def __init__(self) -> None:
        super().__init__("Username or Password incorrect. Please, try again!")