from fastapi import APIRouter, Body, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.schemas.requests import Login
from src.schemas.responses import ValidationErrorResponse, SuccessResponse, BadResponse
from src.utils.token import JWTManager
from src.database.connection import DatabaseConnection
from src.utils.logger import Logger
from src.database.repository.passengers import PassengersRepository

router = APIRouter(prefix='/auth', tags=['Authentication'])

@router.post('/login')
def login(
    credentials: dict = Body(
        ...,
        title='Customers Credentiales for login',
        json_schema_extra=Login.schema()
        ),
    ):
    """
    Authenticates a user based on provided credentials.\n
    **Args:** \n
        credentials (dict): A dictionary containing the user's login credentials.\n
        db (Session): Database session dependency.\n
    **Returns:**\n
        - 200 OK: If the user is authenticated successfully, returns a token.\n
        - 400 Bad Request: If there is a validation error in the request body.\n
        - 401 Unauthorized: If the user is not found or the password is invalid.\n
        - 404 Not Found: If the user is not found.\n
        - 500 Internal Server Error: If there is an error generating the token.\n
    """

    logger = Logger()
    logger.log('INFO', f"[/api/v1/auth/login] [POST] Authenticating user with credentials {credentials}")

    try:
        credentials = Login(**credentials)
    except ValidationError as e:
        logger.log('ERROR', f"[/api/v1/auth/login] [POST] [400] Error validating request body")
        errors_details = e.errors()

        response = ValidationErrorResponse(details=errors_details)

        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_400_BAD_REQUEST)

    db = DatabaseConnection()
    customer_repository = PassengersRepository(db)
    customer = customer_repository.get_by_email(credentials.email)

    if not customer:
        logger.log('ERROR', f"[/api/v1/auth/login] [POST] [401] User not found")
        
        response = BadResponse(message='Customer not found')
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
    else:
        if not customer["password"] == credentials.password:
            logger.log('ERROR', f"[/api/v1/auth/login] [POST] [401] Invalid password")
            
            response = BadResponse(message='Invalid password')
            return JSONResponse(content=response.model_dump(), status_code=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                token_manager = JWTManager()
                token = token_manager.encode(credentials.model_dump())
            except Exception as e:
                logger.log('ERROR', f"[/api/v1/auth/login] [POST] [500] Error generating token: {str(e)}")
                
                response = BadResponse(message='Possible error generating token')
                return JSONResponse(content=response.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

            http_response = SuccessResponse(data={'token': token})

            logger.log('INFO', f"[/api/v1/auth/login] [POST] [200] User authenticated successfully")
            
            return JSONResponse(content=http_response.model_dump(), status_code=status.HTTP_200_OK) 
