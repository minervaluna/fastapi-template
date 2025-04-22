# app/main.py
import json
import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from app.api.main import api_router
from app.core.config import settings
from app.core.database import engine, Base
from app.core.exceptions import generic_exception_handler, validation_exception_handler, http_exception_handler

app = FastAPI(
    title=settings.PROJECT_NAME,
)

# Automatically create database tables (tables are created based on models upon the first launch)
Base.metadata.create_all(bind=engine)

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler: HTTPException and all uncaptured exceptions
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


# Global middleware: Uniform JSON output format
@app.middleware("http")
async def add_custom_response_format(request: Request, call_next):
    response = await call_next(request)

    # Handle json result...
    if "application/json" in response.headers.get("content-type", ""):
        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        try:
            original_data = json.loads(body)
        except Exception:
            original_data = body.decode()

        # Return itself if it's already the uniform structure.
        if isinstance(original_data, dict) \
                and set(original_data.keys()) == {"code", "message", "data"}:
            return JSONResponse(content=original_data, status_code=response.status_code)

        # Otherwise, wrap it...
        wrapped = {
            "code": response.status_code,
            "message": "Success" if response.status_code < 400 else "Failure",
            "data": original_data,
        }
        return JSONResponse(content=wrapped, status_code=response.status_code)

    return response


# Introduce all routes and specify the prefix path...
app.include_router(api_router, prefix=settings.API_ROUTE_PREFIX)

# Supports pagination
add_pagination(app)

# logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
