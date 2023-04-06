class SignUpException(Exception):
    def __init__(self) -> None:
        super().__init__("This email or username is already in use. Please, Try again!")