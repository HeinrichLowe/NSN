class AddFriendException(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to add friend. Please, try again!")