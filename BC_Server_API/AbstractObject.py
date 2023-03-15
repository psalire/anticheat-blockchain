"""Abstract object."""
from abc import ABC, abstractmethod


class AbstractObject(ABC):
    """Abstract class for objects."""

    @abstractmethod
    def get_data(self):
        """Data getter."""
