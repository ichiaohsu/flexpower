import uvicorn
from fastapi import FastAPI, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.server import routers, trade

from app.store.schemas import Base

from app.store import database

Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Trades API",
    version="0.1.0",
)

app.include_router(routers.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(trade.Error(status_code=status.HTTP_400_BAD_REQUEST, message=str(exc.errors())))
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)