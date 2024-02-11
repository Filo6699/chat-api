class PermissionError(Exception):
    """Exception raised when the user doesn't have enough privileges."""

    def __init__(self, message="Not enough privileges."):
        self.message = message
        super().__init__(self.message)


class AuthError(Exception):
    """Exception raised when the user authentication fails."""

    def __init__(self, message="Authentication failed."):
        self.message = message
        super().__init__(self.message)
