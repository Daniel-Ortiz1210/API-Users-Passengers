from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.utils.token import JWTManager


class JWTBearerDependencie(HTTPBearer):
    """
    JWTBearerDependencie is a custom dependency class that extends HTTPBearer for handling JWT authentication.
    Methods:
    --------
    __init__(self, auto_error: bool = True):
        Initializes the JWTBearerDependencie with an optional auto_error parameter.
    __call__(self, req: Request):
        Asynchronously processes the incoming request to extract and decode the JWT token.
        Raises an HTTPException with status code 401 if the token is invalid or decoding fails.
    Parameters:
    -----------
    auto_error : bool, optional
        If set to True, automatically raises an HTTPException for authentication errors (default is True).
    Returns:
    --------
    decoded_token : dict
        The decoded JWT token if authentication is successful.
    """

    def __init__(self, auto_error: bool = True):
        super(JWTBearerDependencie, self).__init__(auto_error=auto_error)

    async def __call__(self, req: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearerDependencie, self).__call__(req)
        
        try:
            decoded_token = JWTManager().decode(credentials.credentials)
        except ValueError as error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': error.__str__()})
    
        return decoded_token
