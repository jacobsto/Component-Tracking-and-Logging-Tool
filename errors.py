# Custom errors to cleanly handle problems.

class AppError(Exception):
    # Base error for the application.
    pass

class ValidationError(AppError):
    # Raised when input is invalid.
    pass

class NotFoundError(AppError):
    # Raised when a requested component does not exist.
    pass

class StorageError(AppError):
    # Raised when saving/loading fails.
    pass