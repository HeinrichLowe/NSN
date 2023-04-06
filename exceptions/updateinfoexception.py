class UpdateInfoException(Exception):
    def __init__(self) -> None:
        super().__init__("Something is go wrong. Please, try again!")