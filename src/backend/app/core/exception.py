from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger

def internal_server_error(exc: Exception):
    logger.error(f"An error occurred: {exc}")
    logger.exception("Exception Stack Trace:")
    error_message = "Internal server error"
    return HTTPException(status_code=500, detail=error_message)

def authentication_error(exc: Exception):
    logger.warning(f"Authentication error: {exc}")
    error_message = "Authentication failed. Please check your credentials."
    return HTTPException(status_code=401, detail=error_message)

def validation_error(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()}")
    error_details = exc.errors()
    return JSONResponse(
        status_code=422,
        content={"detail": error_details},
    )

def not_found_error(exc: Exception):
    logger.warning(f"Resource not found: {exc}")
    error_message = "The requested resource was not found."
    return HTTPException(status_code=404, detail=error_message)

def forbidden_error(exc: Exception):
    logger.warning(f"Forbidden access: {exc}")
    error_message = "You do not have permission to access this resource."
    return HTTPException(status_code=403, detail=error_message)

def bad_request_error(exc: Exception):
    logger.warning(f"Bad request: {exc}")
    error_message = "The request could not be understood or was missing required parameters."
    return HTTPException(status_code=400, detail=error_message)
