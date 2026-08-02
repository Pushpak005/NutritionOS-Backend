from pydantic import BaseModel, Field


class ProfileSetupRequest(BaseModel):

    age: int = Field(..., ge=13, le=120)

    gender: str

    height: int = Field(..., ge=80, le=250)

    weight: int = Field(..., ge=20, le=350)


class ProfileSetupResponse(BaseModel):

    success: bool

    message: str