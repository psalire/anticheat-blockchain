"""pydantic Request Models."""
from PlayerPositionModels import Coordinates, CoordinateValidation
from typing import Union, List, Optional, Literal
from uuid import UUID
from pydantic import BaseModel, Json


class PostSessionRequest(BaseModel):
    """Create a session."""

    session_id: Union[UUID, str, None] = None


class PostPlayerRequest(BaseModel):
    """Create a player."""

    player_id: Union[UUID, str, None] = None
    position: Optional[Coordinates]


class PostPlayerPositionRequest(BaseModel):
    """Create a player."""

    coordinates: Coordinates


class PostPositionValidationRule(BaseModel):
    """Post single validation rule."""

    rule: CoordinateValidation


class PutSessionDataBatch(BaseModel):
    """Put session data."""

    int_key: Optional[str] = None
    bool_key: Optional[str] = None
    string_key: Optional[str] = None
    int_data: List[int] = []
    bool_data: List[bool] = []
    string_data: List[str] = []


class PutSessionData(BaseModel):
    """Put session data."""

    data: Union[List[int],List[bool],List[str]] = []


class PutSessionDataValidationRule(BaseModel):
    """Put session data."""

    data: Union[int,bool,str]
    operand: Literal["eq","ne","lt","gt","lte","gte"]


class PutSessionValidationRule(BaseModel):
    """Put session validation rule."""

    type: str
    key: str
    vals: Union[List[int],List[bool],List[str]] = []
    operand: str


class PostValidationSchema(BaseModel):
    """Post validation schema."""

    validation_schema: Json
