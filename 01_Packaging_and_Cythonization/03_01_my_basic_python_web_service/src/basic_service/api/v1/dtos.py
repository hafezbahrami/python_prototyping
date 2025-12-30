from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    environment: str


class EchoRequest(BaseModel):
    message: str


class EchoResponse(BaseModel):
    echoed_message: str
