"""Player position Models."""
from typing import Union, List, Literal
from pydantic import BaseModel


class Coordinates(BaseModel):
    """Position coordinates."""

    x: Union[int, None] = None
    y: Union[int, None] = None
    z: Union[int, None] = None


class CoordinateValidation(BaseModel):
    """Single coordinate validation parameters."""

    operand: Literal['gt', 'gte', 'lt', 'lte', 'eq', 'ne']
    coordinates: Coordinates


class CoordinatesValidation(BaseModel):
    """Position coordinates validation parameters."""

    x: List[CoordinateValidation] = []
    y: List[CoordinateValidation] = []
    z: List[CoordinateValidation] = []