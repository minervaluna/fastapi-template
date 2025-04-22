# app/core/exceptions.py
from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status


class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print('validation_exception_handler')
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "参数校验失败",
            "data": exc.errors(),
        },
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    print('http_exception_handler')
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None,
        }
    )

async def generic_exception_handler(request: Request, exc: Exception):
    print('generic_exception_handler')
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "Internal Server Error",
            "data": None,
        }
    )
