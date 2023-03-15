"""Handles Player logic."""
from uuid import uuid4, UUID
from AbstractObject import AbstractObject
from RequestModels import PostPlayerRequest
from PlayerPositionModels import Coordinates


class PlayerObject(AbstractObject):
    """Player facade."""
    
    def __init__(self, player_request: PostPlayerRequest, session_id: UUID):
        """Initialize values and do validation."""
        self.session_id = session_id

        self.player_id = getattr(player_request, 'player_id', None)
        if self.player_id is None or self.player_id == '':
            self.player_id = uuid4()

        self.coord = getattr(player_request, 'position', None)
        if self.coord is None:
            self.coord = Coordinates()

    def get_data(self):
        """Data getter."""
        return {
            "session": self.session_id,
            "player_id": self.get_player_id(),
            "position": self.get_coord(),
        }

    def get_coord(self):
        """Coord getter."""
        return self.coord

    def get_player_id(self):
        """player_id getter."""
        return self.player_id
