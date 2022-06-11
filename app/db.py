from datetime import datetime
from psycopg2._psycopg import connection, cursor
import typing

from app.models.message import Message
from app.models.text_channel import TextChannel
from app.models.user import User
from snowflake import SnowflakeGenerator


snowflakes = SnowflakeGenerator(42)


class Database:
    def __init__(self, db: connection):
        """Init a database manager class."""
        self.db = db
        self.setup_database()

    def setup_database(self) -> None:
        """Create database tables."""
        with self.db.cursor() as cur:
            cur: cursor
            for statement in open("setup.sql", "r").read().split(";")[:-1]:
                cur.execute(statement, [])
            self.db.commit()

    def get_user(self, **kwargs) -> User:
        """Get user from the database."""
        condition = []
        values = []
        for x in kwargs.keys():
            condition.append(f"{x}=%s")
            values.append(kwargs[x])
        req = f"SELECT * FROM users WHERE {' AND '.join(condition)};"
        with self.db.cursor() as cur:
            cur: cursor
            cur.execute(req, values)
            data = cur.fetchone()
        if data:
            return User(
                id=data[0],
                username=data[1],
                avatar_hash=data[2],
                password_hash=data[3],
                created_at=data[4],
                locale=data[5],
            )
    
    def modify_user(self, user: User) -> User:
        """Modify an existing user."""
        with self.db.cursor() as cur:
            cur: cursor
            cur.execute(
                f"UPDATE users SET username=%s, password_hash=%s WHERE id=%s;",
                (user.username, user.password_hash, user.id)
            )
            self.db.commit()
        return user

    def create_user(self, user: User) -> User:
        """Create and save a new user."""
        new_id = next(snowflakes)
        user.id = new_id
        user.created_at = datetime.now()
        args = ("id", "username", "role", "password_hash", "created_at")
        with self.db.cursor() as cur:
            cur: cursor
            cur.execute(
                f"INSERT INTO users({','.join(args)}) VALUES (%s,%s,%s,%s,%s);",
                (new_id, user.username, user.role, user.password_hash, user.created_at),
            )
            self.db.commit()
        return user

    def create_text_channel(self, channel: TextChannel) -> TextChannel:
        """Create and save a text channel."""
        new_id = next(snowflakes)
        channel.id = new_id
        channel.created_at = datetime.now()
        args = ("id", "name", "description", "created_at")
        with self.db.cursor() as cur:
            cur: cursor
            cur.execute(
                f"INSERT INTO text_channels({','.join(args)}) VALUES (%s,%s,%s,%s);",
                (new_id, channel.name, channel.description, channel.created_at),
            )
            self.db.commit()
        return channel

    def get_text_channel(self, **kwargs) -> TextChannel:
        """Get text channel from the database."""
        condition = []
        values = []
        for x in kwargs.keys():
            condition.append(f"{x}=%s")
            values.append(kwargs[x])
        req = f"SELECT * FROM text_channels WHERE {' AND '.join(condition)}"
        print(req)
        with self.db.cursor() as cur:
            cur: cursor
            cur.execute(req, values)
            data = cur.fetchone()
        print(data)
        if data:
            return TextChannel(
                id=data[0], name=data[1], description=data[2], created_at=data[3]
            )

    def get_all_text_channels(self) -> typing.List[TextChannel]:
        """Get list of all text channels."""
        with self.db.cursor() as cur:
            cur: cursor
            cur.execute("SELECT * FROM text_channels;")
            data = cur.fetchall()
        if data:
            return [
                TextChannel(id=x[0], name=x[1], description=x[2], created_at=x[3])
                for x in data
            ]

    def modify_text_channel(self, channel: TextChannel) -> None:
        """Modify a text channel."""
        with self.db.cursor() as cur:
            cur: cursor
            cur.execute(
                "UPDATE text_channels SET name=%s, description=%s WHERE id=%s;",
                (channel.name, channel.description, channel.id),
            )
            self.db.commit()

    def delete_text_channels(self, **kwargs) -> None:
        """Delete a text channel from the database."""
        condition = []
        values = []
        for x in kwargs.keys():
            condition.append(f"{x}=%s")
            values.append(kwargs[x])
        req = f"DELETE FROM text_channels WHERE {' AND '.join(condition)};"
        print(req)
        with self.db.cursor() as cur:
            cur: cursor
            cur.execute(req, values)
            self.db.commit()

    def create_message(self, message: Message) -> None:
        """Create and save a message."""
        new_id = next(snowflakes)
        args = ("id", "author_id", "channel_id", "content", "created_at")
        message.id = new_id
        message.created_at = datetime.now()
        with self.db.cursor() as cur:
            cur: cursor
            cur.execute(
                f"INSERT INTO messages({','.join(args)}) VALUES (%s,%s,%s,%s,%s);",
                (new_id, message.author_id, message.channel_id, message.content, message.created_at),
            )
            self.db.commit()
        return message

    def get_messages(self, **kwargs) -> typing.List[Message]:
        """Get messages from the database."""
        condition = []
        values = []
        for x in kwargs.keys():
            condition.append(f"{x}=%s")
            values.append(kwargs[x])
        req = f"SELECT * FROM messages WHERE {' AND '.join(condition)};"
        print(req)
        with self.db.cursor() as cur:
            cur: cursor
            cur.execute(req, values)
            data = cur.fetchall()
        if data:
            return [
                Message(
                    id=x[0], channel_id=x[1], author_id=x[2], content=x[3], created_at=x[4]
                )
                for x in data
            ]

    def modify_message(self, message: Message) -> None:
        """Modify a message."""
        with self.db.cursor() as cur:
            cur: cursor
            cur.execute(
                "UPDATE messages SET content=%s WHERE id=%s;",
                (message.content, message.id),
            )
            self.db.commit()

    def delete_messages(self, **kwargs) -> None:
        """Create and save a message."""
        condition = []
        values = []
        for x in kwargs.keys():
            condition.append(f"{x}=%s")
            values.append(kwargs[x])
        req = f"DELETE FROM messages WHERE {' AND '.join(condition)}"
        print(req)
        with self.db.cursor() as cur:
            cur: cursor
            cur.execute(req, values)
            self.db.commit()
