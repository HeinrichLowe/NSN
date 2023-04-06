class FindUserException(Exception):
    def __init__(self) -> None:
        super().__init__("No user found.")