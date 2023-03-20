"""pydantic Response Models."""
from typing import Any, Literal, Union, Optional
from pydantic import BaseModel


class ResponseModel(BaseModel):
    """Response Model following the JSend standard."""

    status: Literal['success', 'error']
    data: Any = None


class SuccessResponseModel(ResponseModel):
    """Success Response Model."""

    status: Literal['success'] = 'success'


class ErrorResponseModel(ResponseModel):
    """Error Response Model."""

    status: Literal['error'] = 'error'
    error: str = 'Failure'

class WSResponseModel(BaseModel):
    """Websocket Response model."""

    action: str
    response: Optional[Union[dict, SuccessResponseModel, ErrorResponseModel]]
