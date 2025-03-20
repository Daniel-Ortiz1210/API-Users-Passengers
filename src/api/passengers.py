from fastapi import APIRouter, Body, Depends, Header, Path, status, Query
from fastapi.responses import JSONResponse, Response
from peewee import IntegrityError
from pydantic import ValidationError

from src.database.repository.passengers import PassengersRepository
from src.database.connection import DatabaseConnection
from src.utils.logger import Logger
from src.schemas.responses import SuccessResponse, BadResponse, ValidationErrorResponse
from src.schemas.requests import PassengerRequestSchema
from src.utils.dependencies import JWTBearerDependencie
from src.utils.token import JWTManager

router = APIRouter(
    prefix='/passengers',
    tags=['Passengers']
)

@router.get('/')
def get_all_passengers():
    """
    Retrieve all passengers from the database. \n
    This endpoint retrieves all passengers from the database and paginates the results 
    using the FastAPI pagination extension. \n

    **Arguments** \n
        - db (Session): Database session dependency, provided by FastAPI's Depends. \n
    **Responses** \n
        - 200: A paginated list of passengers (. \n
    **Logs Levels** \n
        - INFO: Logs the start of the passenger retrieval process. \n
        - INFO: Logs the successful completion of the passenger retrieval process. \n
    """
    logger = Logger()
    
    logger.log('INFO', f"[/api/v1/passengers/] [GET] Retreiving passengers from database")

    db = DatabaseConnection()

    passenger_repo = PassengersRepository(db)

    passengers = passenger_repo.get_passengers()

    json_response = SuccessResponse(data=passengers).model_dump()

    logger.log('INFO', f"[/api/v1/passengers/] [GET] [200] Passengers retreived successfully")

    return JSONResponse(content=json_response, status_code=status.HTTP_200_OK)


@router.get('/{id}')
def get_passenger_details(
    decoded_token: str = Depends(JWTBearerDependencie()),
    id: int = Path(
        ...,
        title='passengers ID',
        description='Unique identity value for a passengers'
        )
    ):
    """
    Retrieve passenger details by ID.\n
    This endpoint retrieves the details of a passenger from the database using the provided passenger ID.\n
    It also verifies that the passenger making the request has access to the requested passenger ID.\n
    \n
    
    **Responses:** \n
        - 200: passenger details retrieved successfully.\n
        - 403: Forbidden access to passenger with the provided ID.\n
        - 404: passenger with the provided ID not found.\n
    **Log Levels:**\n
        - INFO:\n
            - Retrieving passenger with ID from database.\n
            - passenger with ID retrieved successfully.\n
        - ERROR:\n
            - passenger with ID not found.\n
            - Forbidden access to passenger with ID.\n
    """
    logger = Logger()
    
    logger.log('INFO',f"[/api/v1/passengers/{id}] [GET] Retreiving passenger with ID {id} from database")

    db = DatabaseConnection()

    passengers_repo = PassengersRepository(db)
    
    passenger = passengers_repo.get_by_email(decoded_token['email'])

    if not passenger:
        
        logger.log('ERROR', f"[/api/v1/passengers/{id}] [GET] [404] passenger with ID {id} not found")
        
        response = BadResponse(message='passenger not found')
        
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
    else:
        if passenger['id'] != id:
            
            logger.log('ERROR', f"[/api/v1/passengers/{id}] [GET] [403] Forbidden access to passenger with ID {id}")

            response = BadResponse(message='passenger logged in does not have access to this resource')
            
            return JSONResponse(content=response.model_dump(), status_code=status.HTTP_403_FORBIDDEN)
        else:
            http_response = SuccessResponse(data=passenger).model_dump()

            logger.log('INFO', f"[/api/v1/passengers/{id}] [GET] [200] passenger with ID {id} retreived successfully")
    
            return JSONResponse(content=http_response, status_code=status.HTTP_200_OK)
        

@router.post('/')
def create_passenger(
    request: dict = Body(...,json_schema_extra=PassengerRequestSchema.schema())
    ):
    """
    Create a new passenger in the database. \n
    This function handles the creation of a new passenger by validating the request body \n
    persisting the passenger data to the database, and generating a JWT token for the passenger. \n
    
    **Args:** \n
        - db (Session): Database session dependency. \n
        - request (dict): Request body containing passenger data.\n
    **Returns:** \n
        - JSONResponse: A JSON response with the status of the operation and relevant data or error messages. \n
    **Raises:** \n
        - ValidationError: If the request body validation fails. \n
        - IntegrityError: If there is a database integrity error (e.g., passenger already exists). \n
        - Exception: If there is an error generating the JWT token.
    """
    
    logger = Logger()
    
    logger.log('INFO', f"[/api/v1/passengers/] [POST] Persisting passenger to database")

    try: 
        body = PassengerRequestSchema(**request)
    except ValidationError as e:
        logger.log('ERROR', f"[/api/v1/passengers/] [POST] [400] Error validating request body")

        errors_details = e.errors()
        
        error_response = ValidationErrorResponse(details=errors_details)
        
        return JSONResponse(content=error_response.model_dump(), status_code=status.HTTP_400_BAD_REQUEST)
    
    db = DatabaseConnection()

    try:
        body_to_dict = body.model_dump()

        passenger_repository = PassengersRepository(db)
    
        new_passenger_id = passenger_repository.create(body_to_dict)
    except IntegrityError as e:
        
        logger.log('ERROR', f"[/api/v1/passengers/] [POST] [400] Error creating passenger: {str(e)}")
        
        response = BadResponse(message='passenger already exists')
        
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_400_BAD_REQUEST)
    
    try:
        jwt_manager = JWTManager()
        
        token = jwt_manager.encode(body_to_dict)
    except Exception as e:
        
        logger.log('ERROR', f"[/api/v1/passengers/] [POST] [500] Error generating token: {str(e)}")
        
        response = BadResponse(message='Possible error generating token')
        
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    http_response = SuccessResponse(data={
        'passenger': {"id": new_passenger_id, **body_to_dict},
        'token': token
    })

    logger.log('INFO', "[/api/v1/passengers/] [POST] [201] passenger created successfully")
    
    return JSONResponse(content=http_response.model_dump(), status_code=status.HTTP_201_CREATED)


@router.put('/{id}')
def update_passenger(
    decoded_token: dict = Depends(JWTBearerDependencie()), 
    id: int = Path(..., title='passenger ID', description='Unique identity value for a passenger'),
    request: dict = Body(..., json_schema_extra=PassengerRequestSchema.model_json_schema())
    ):
    """
    Update a passenger in the database.\n
    This endpoint replaces the passenger data with the provided request body for the passenger with the specified ID.\n
    It also generates a new JWT token for the updated passenger. \n

    **Args:**\n
        - db (Session): Database session dependency.\n
        - decoded_token (dict): Decoded JWT token dependency.\n
        - id (int): Unique identity value for a passenger.\n
        - request (dict): Request body containing the passenger data to update.\n
    **Returns:**\n
        - JSONResponse: JSON response with the status of the operation and any relevant data or error messages.\n
    **Raises:**\n
        - ValidationError: If the request body validation fails.\n
        - Exception: If there is an error generating the JWT token.\n
    **Logs:**\n
        - INFO: Logs the start and successful completion of the update operation.\n
        - ERROR: Logs any errors encountered during the process.\n
    **Responses:**\n
        - 400: Bad request if the request body validation fails.\n
        - 404: Not found if the passenger with the specified ID does not exist.\n
        - 403: Forbidden if the logged-in passenger does not have access to the specified resource.\n
        - 500: Internal server error if there is an error generating the JWT token.\n
        - 201: Created if the passenger is updated successfully.\n
    """
    
    logger = Logger()
    
    logger.log('INFO', f"[/api/v1/passengers/{id}] [PUT] Replacing passenger with ID {id} from database")

    try:  
        body = PassengerRequestSchema(**request)
    except ValidationError as e:
        
        logger.log('ERRO', f"[/api/v1/passengers/{id}] [PUT] [400] Error validating request body")

        errors_details = e.errors()
        
        error_response = ValidationErrorResponse(details=errors_details)
        
        return JSONResponse(content=error_response.model_dump(), status_code=status.HTTP_400_BAD_REQUEST)


    db = DatabaseConnection()

    passenger_repository = PassengersRepository(db)

    passenger = passenger_repository.get_by_email(decoded_token['email'])

    body_to_dict = body.model_dump()

    if not passenger:
        
        logger.log('ERROR', f"[/api/v1/passengers/{id}] [PUT] [404] passenger with ID {id} not found")
        
        response = BadResponse(message='passenger not found')
        
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
    else:
        if passenger["id"] != id:
            
            logger.log('ERROR', f"[/api/v1/passengers/{id}] [PUT] [403] Forbidden access to passenger with ID {id}")

            response = BadResponse(message='passenger logged in does not have access to this resource')

            return JSONResponse(content=response.model_dump(), status_code=status.HTTP_403_FORBIDDEN)
        else:
    
            updated_passenger = passenger_repository.update(id, body_to_dict)

            logger.log('INFO', f"[/api/v1/passengers/{id}] [PUT] [201] passenger with ID {id} updated successfully")

            try:
                jwt_manager = JWTManager()
                
                token = jwt_manager.encode(body_to_dict)
            except Exception as e:
                
                logger.log('ERROR', f"[/api/v1/passengers/{id}] [PUT] [500] Error generating token: {str(e)}")
                
                response = BadResponse(message='Possible error generating token')
                
                return JSONResponse(content=response.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            response = SuccessResponse(data={
                'token': token,
                'passenger': body_to_dict
                }
            )
            return JSONResponse(content=response.model_dump(), status_code=status.HTTP_201_CREATED)
        

@router.delete('/{id}')
def delete_passenger(
    decoded_token: dict = Depends(JWTBearerDependencie()),
    id: int = Path(...,title='passenger ID',description='Unique identity value for a passenger')
    ):
    """
    Deletes a passenger from the database.\n

    This endpoint deletes a passenger from the database using the provided passenger ID.\n
    It also verifies that the passenger making the request has access to the specified passenger ID.\n


    **Args:**\n
        - decoded_token (dict): The decoded JWT token containing user information.\n
        - db (Session): The database session dependency.\n
        - id (int): The unique identity value for a passenger.\n
    **Returns:**\n
        - 404 Not Found: If the passenger with the given ID does not exist.\n
        - 403 Forbidden: If the logged-in passenger does not have access to delete the specified passenger.\n
        - 204 No Content: If the passenger is successfully deleted.\n
    **Logs:**\n
        - INFO: When attempting to delete a passenger.\n
        - ERROR: If the passenger with the given ID does not exist.\n
        - ERROR: If the logged-in passenger does not have access to delete the specified passenger.\n
        - INFO: If the passenger is successfully deleted.\n
    """
    
    logger = Logger()
    
    logger.log('INFO', f"[/api/v1/passengers/{id}] [DELETE] Deleting passenger with ID {id} from database")

    db = DatabaseConnection()

    passenger_repository = PassengersRepository(db)

    passenger = passenger_repository.get_by_email(decoded_token['email'])

    if not passenger:
        
        logger.log('ERROR', f"[/api/v1/passengers/{id}] [DELETE] [404] passenger with ID {id} not found")
        
        response = BadResponse(message='passenger not found')
        
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
    else:
        if passenger["id"] != id:
            
            logger.log('ERROR', f"[/api/v1/passengers/{id}] [DELETE] [403] Forbidden access to passenger with ID {id}")

            response = BadResponse(message='passenger logged in does not have access to this resource')

            return JSONResponse(content=response.model_dump(), status_code=status.HTTP_403_FORBIDDEN)
        else:
            logger.log('INFO', f"[/api/v1/passengers/{id}] [DELETE] [204] passenger with ID {id} deleted successfully")

            passenger_repository.delete(id)

            response = SuccessResponse()

            return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/{id}/reservations')
def get_passenger_reservations(
    id: int = Path(...,title='passenger ID',description='Unique identity value for a passenger'),
    decoded_token: dict = Depends(JWTBearerDependencie()),
):
    logger = Logger()

    db = DatabaseConnection()

    passengers_repository = PassengersRepository(db)

    passenger = passengers_repository.get_by_email(decoded_token['email'])

    if not passenger:
        
        logger.log('ERROR', f"[/api/v1/passengers/{id}] [DELETE] [404] passenger with ID {id} not found")
        
        response = BadResponse(message='passenger not found')
        
        return JSONResponse(content=response.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
    else:
        if passenger["id"] != id:
            
            logger.log('ERROR', f"[/api/v1/passengers/{id}] [DELETE] [403] Forbidden access to passenger with ID {id}")

            response = BadResponse(message='passenger logged in does not have access to this resource')

            return JSONResponse(content=response.model_dump(), status_code=status.HTTP_403_FORBIDDEN)
        else:

            reservations = passengers_repository.get_reservations(id)

            db.close()

            json_response = SuccessResponse(data=reservations).model_dump()

            return JSONResponse(content=json_response, status_code=status.HTTP_200_OK)
