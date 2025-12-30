from enum import Enum
from pydantic import BaseModel


class EngineeringApp(str, Enum):
    """
    Supported engineering applications.
    """

    ASPEN_PLUS = "aspen-plus"
    HYSYS = "hysys"


class ResponseStatus(str, Enum):
    SUCCESS = "success"
    FAIL = "fail"


class PromptRequest(BaseModel):
    """
    Input sent by the client.
    """

    engineering_app: EngineeringApp
    user_query: str


class PromptResponse(BaseModel):
    """
    Output returned to the client.
    """

    status: ResponseStatus
    commands: list[str]
    message: str = ""
