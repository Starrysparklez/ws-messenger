from datetime import datetime
from .channel import Channel
from .user import User


class Message:
    def __init__(self, **kwargs) -> None:
        self.id: str = kwargs.pop("id", None)
        self.channel: Channel = kwargs.pop("channel", None)
        self.author: User = kwargs.pop("author", None)
        self.content: str = kwargs.pop("content", None)
        self.created_at: datetime = kwargs.pop("created_at", None)

    def to_json(self) -> dict:
        """Convert to json."""
        # send empty user template if message author is unknown
        if not self.author:
            print("no author for message", self.id)
            self.author = User(role='deleted')
        return {
            "id": self.id,
            "channel": self.channel.to_json(),
            "content": str(self.content),
            "author": self.author.to_json(),
            "created_at": self.created_at.strftime("%c")
        }
