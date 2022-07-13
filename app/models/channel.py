from datetime import datetime
import typing


class Channel:
    def __init__(self, **kwargs):
        """Init a new Channel object.

        Parameters
        ==========
        id: str
            Channel ID
        name: str
            Channel name
        type: str
            Channel type ('text', 'category')
        topic: Union[str, None]
            Channel description
        created_at: datetime
            Channel creation date
        parent_id: str
            Parent category channel ID
        """
        self.id: str = kwargs.pop("id", None)
        self.name: str = kwargs.pop("name", None)
        self.type: str = kwargs.pop("type", None)
        self.topic: typing.Union[str, None] = kwargs.pop("topic", None)
        self.created_at: datetime = kwargs.pop("created_at", None)
        self.parent_id: str = kwargs.pop("parent_id", None)

    def to_json(self) -> typing.Dict:
        """Convert to json."""
        return {
            "id": self.id,
            "name": self.name,
            "topic": self.topic,
            "created_at": self.created_at.strftime("%c"),
            "parent_id": self.parent_id,
        }
