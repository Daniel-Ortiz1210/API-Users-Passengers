import jwt
from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta
from src.utils.config import Config

settings = Config()
class TokenBaseManager(ABC):
    """
    TokenBaseManager is an abstract base class that serves as an interface for token generation and decoding.

    Methods
    -------
    encode(body: dict) -> str
        Abstract method to encode a dictionary into a token string.
    decode(token: str) -> dict
        Abstract method to decode a token string back into a dictionary.
    """
    """Interface for token generation"""

    @abstractmethod
    def encode(self, body: dict) -> str:
        pass

    @abstractmethod
    def decode(self, token: str) -> dict:
        pass

class JWTManager(TokenBaseManager):
    """
    JWTManager is responsible for encoding and decoding JSON Web Tokens (JWT).
    Attributes:
        secret_key (str): The secret key used to encode and decode the JWT.
        algorithm (str): The algorithm used for encoding the JWT. Default is 'HS256'.
        expiration_in_minutes (int): The expiration time of the token in minutes. Default is 10 minutes.
    Methods:
        encode(data: dict) -> str:
            Encodes the given data into a JWT with an expiration time.
        decode(token: str) -> dict:
            Decodes the given JWT and returns the payload data.
    """
    def __init__(
        self,
        secret_key: str = settings.token_secret_key,
        algorithm: str = settings.token_algorithm,
        expiration_in_minutes: int = settings.token_expiration_in_minutes
        ):
            self.secret_key = secret_key
            self.algorithm = algorithm
            self.expiration_in_minutes = expiration_in_minutes

    def encode(self, data: dict):
        """
        Encodes the given data into a JWT token.

        Args:
            data (dict): The data to be encoded into the token.

        Returns:
            str: The encoded JWT token.
        """
        try:
            payload = {
                **data,
                'exp': datetime.now(tz=timezone.utc) + timedelta(minutes=self.expiration_in_minutes)
            }
            
            token = jwt.encode(
                payload,
                key=self.secret_key,
                algorithm=self.algorithm
                )
        except Exception as e:
            raise ValueError(f"{e}")
        return token

    def decode(self, token):
        """
        Decodes a JWT token using the specified secret key and algorithm.
        Args:
            token (str): The JWT token to decode.
        Returns:
            dict: The decoded token payload.
        Raises:
            jwt.ExpiredSignatureError: If the token has expired.
            jwt.InvalidTokenError: If the token is invalid for any reason.
        """
        try:
            decoded_token = jwt.decode(
            token, key=self.secret_key,
            algorithms=[self.algorithm],
            verify=True
            )
        except jwt.exceptions.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.exceptions.InvalidTokenError:
            raise ValueError("Invalid token")
        
        return decoded_token
