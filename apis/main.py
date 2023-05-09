import uvicorn
from fastapi import FastAPI, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from apis.server import routers, error

from apis.store.schemas import Base

from apis.store import database

Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Trades API",
    version="0.1.0",
)

app.include_router(routers.router)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(error.Error(status_code=status.HTTP_400_BAD_REQUEST, message=str(exc.errors())))
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)