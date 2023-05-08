from pydantic import BaseModel, Field

class Error(BaseModel): 
    status_code: int | None = None
    message: str | None = Field(description="Descriptive error message")