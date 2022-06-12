from datetime import datetime


class Message:
    def __init__(self, **kwargs) -> None:
        self.id: int = kwargs.pop("id", None)
        self.channel_id: int = kwargs.pop("channel_id", None)
        self.author_id: int = kwargs.pop("author_id", None)
        self.content: str = kwargs.pop("content", None)
        self.created_at: datetime = kwargs.pop("created_at", None)

    def to_json(self) -> dict:
        """Convert to json."""
        return {
            "id": str(self.id),
            "channel_id": str(self.channel_id),
            "content": str(self.content),
            "author_id": str(self.author_id),
            "created_at": str(self.created_at.timestamp())
        }
