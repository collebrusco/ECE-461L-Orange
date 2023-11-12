# Define types of exception

class ConflictError(Exception): # Conflict
    pass

class InvalidRequestError(Exception): # Bad Request
    pass

class UnauthorizedError(Exception): # Unauthorized User
    pass