class PermissionError(Exception):
    """Exception raised when the user doesn't have enough privileges."""

    def __init__(self, message="Not enough privileges."):
        self.message = message
        super().__init__(self.message)
