from datetime import datetime
import typing


class TextChannel:
    def __init__(self, **kwargs):
        """Init a new User object.

        Parameters
        ==========
        id: int
            Channel ID
        name: str
            Channel name
        description: Union[str, None]
            Channel description
        created_at: datetime
            Channel creation date
        """
        self.id: int = kwargs.pop("id", None)
        self.name: str = kwargs.pop("name", None)
        self.description: typing.Union[str, None] = kwargs.pop("description", None)
        self.created_at: datetime = kwargs.pop("created_at", None)

    def to_json(self) -> typing.Dict:
        """Convert to json."""
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.timestamp(),
        }
