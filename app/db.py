from datetime import datetime
from psycopg2._psycopg import connection, cursor
import typing
from random import randint
from app.models.message import Message
from app.models.channel import Channel
from app.models.user import User
from snowflake import SnowflakeGenerator


snowflakes = SnowflakeGenerator(42)


class Database:
    def __init__(self, db: connection):
        """Init a database manager class."""
        self.connection = db
        self.setup_database()

    def setup_database(self) -> None:
        """Create database tables."""
        with self.connection.cursor() as cur:
            cur: cursor
            for statement in open("setup.sql", "r").read().split(";")[:-1]:
                cur.execute(statement, [])
            self.connection.commit()

    def get_user(self, **kwargs) -> User:
        """Get user from the database."""
        condition = []
        values = []
        for x in kwargs.keys():
            condition.append(f"{x}=%s")
            values.append(kwargs[x])
        req = f"SELECT * FROM users WHERE {' AND '.join(condition)};"
        with self.connection.cursor() as cur:
            cur: cursor
            cur.execute(req, values)
            data = cur.fetchone()
        if data:
            return User(
                id=data[0],
                username=data[1],
                role=data[2],
                password_hash=data[3],
                created_at=data[4],
                locale=data[5],
                discriminator=data[6]
            )

    def modify_user(self, user: User) -> User:
        """Modify an existing user."""
        with self.connection.cursor() as cur:
            cur: cursor
            cur.execute(
                f"UPDATE users SET username=%s, role=%s, password_hash=%s, locale_code=%s, discriminator=%s WHERE id=%s;",
                (user.username, user.role, user.password_hash, user.locale, user.discriminator, user.id),
            )
            self.connection.commit()
        return user

    def generate_discrim(self):
        """Generate a discriminator."""
        d = ''
        for _ in range(4):
            d += str(randint(0, 9))
        return d

    def create_user(self, user: User, ignore_admin_limit=False) -> User:
        """Create and save a new user."""
        new_id = str(next(snowflakes))
        user.id = new_id
        user.discriminator = self.generate_discrim()
        # very stupid solution !!!!!!!!!!
        while self.get_user(username=user.username, discriminator=user.discriminator):
            user.discriminator = self.generate_discrim()
        user.created_at = datetime.now()
        args = ("id", "username", "password_hash", "created_at", "role", "discriminator")
        if not ignore_admin_limit and user.role == 'admin':
            raise ValueError('Cannot create another admin user.')
        with self.connection.cursor() as cur:
            cur: cursor
            cur.execute(
                f"INSERT INTO users({','.join(args)}) VALUES (%s,%s,%s,%s,%s,%s);",
                (new_id, user.username, user.password_hash, user.created_at, user.role, user.discriminator),
            )
            self.connection.commit()
        return user

    def create_channel(self, channel: Channel) -> Channel:
        """Create and save a channel."""
        new_id = str(next(snowflakes))
        channel.id = new_id
        channel.created_at = datetime.now()
        args = ("id", "name", "topic", "created_at", "type")
        with self.connection.cursor() as cur:
            cur: cursor
            cur.execute(
                f"INSERT INTO channels({','.join(args)}) VALUES (%s,%s,%s,%s,%s);",
                (new_id, channel.name, channel.topic, channel.created_at, channel.type),
            )
            self.connection.commit()
        return channel

    def get_channel(self, **kwargs) -> Channel:
        """Get channel from the database."""
        condition = []
        values = []
        for x in kwargs.keys():
            condition.append(f"{x}=%s")
            values.append(kwargs[x])
        req = f"SELECT * FROM channels WHERE {' AND '.join(condition)}"
        with self.connection.cursor() as cur:
            cur: cursor
            cur.execute(req, values)
            data = cur.fetchone()
        if data:
            return Channel(
                id=data[0], name=data[1], topic=data[2], created_at=data[3], type=data[4]
            )

    def get_all_channels(self) -> typing.List[Channel]:
        """Get list of all channels."""
        with self.connection.cursor() as cur:
            cur: cursor
            cur.execute("SELECT * FROM channels;")
            data = cur.fetchall()
        if data:
            return [
                Channel(id=x[0], name=x[1], topic=x[2], created_at=x[3], type=x[4])
                for x in data
            ]

    def modify_channel(self, channel: Channel) -> None:
        """Modify a channel."""
        with self.connection.cursor() as cur:
            cur: cursor
            cur.execute(
                "UPDATE channels SET name=%s, topic=%s WHERE id=%s;",
                (channel.name, channel.topic, channel.id),
            )
            self.connection.commit()

    def delete_channels(self, **kwargs) -> None:
        """Delete a channel from the database."""
        condition = []
        values = []
        for x in kwargs.keys():
            condition.append(f"{x}=%s")
            values.append(kwargs[x])
        req = f"DELETE FROM channels WHERE {' AND '.join(condition)};"
        with self.connection.cursor() as cur:
            cur: cursor
            cur.execute(req, values)
            self.connection.commit()

    def create_message(self, message: Message) -> None:
        """Create and save a message."""
        new_id = str(next(snowflakes))
        args = ("id", "author_id", "channel_id", "content", "created_at")
        message.id = new_id
        message.created_at = datetime.now()
        with self.connection.cursor() as cur:
            cur: cursor
            cur.execute(
                f"INSERT INTO messages({','.join(args)}) VALUES (%s,%s,%s,%s,%s);",
                (
                    new_id,
                    message.author.id,
                    message.channel.id,
                    message.content,
                    message.created_at,
                ),
            )
            self.connection.commit()
        return message

    def get_messages(self, **kwargs) -> typing.List[Message]:
        """Get messages from the database."""
        condition = []
        values = []
        for x in kwargs.keys():
            condition.append(f"{x}=%s")
            values.append(kwargs[x])
        req = f"SELECT * FROM messages WHERE {' AND '.join(condition)};"
        with self.connection.cursor() as cur:
            cur: cursor
            cur.execute(req, values)
            data = cur.fetchall()
        if data:
            return [
                Message(
                    id=x[0],
                    channel=self.get_channel(id=x[1]),
                    author=self.get_user(id=x[2]),
                    content=x[3],
                    created_at=x[4],
                )
                for x in data
            ]

    def modify_message(self, message: Message) -> None:
        """Modify a message."""
        with self.connection.cursor() as cur:
            cur: cursor
            cur.execute(
                "UPDATE messages SET content=%s WHERE id=%s;",
                (message.content, message.id),
            )
            self.connection.commit()

    def delete_messages(self, **kwargs) -> None:
        """Delete message(s) based on given parameters."""
        condition = []
        values = []
        for x in kwargs.keys():
            condition.append(f"{x}=%s")
            values.append(kwargs[x])
        req = f"DELETE FROM messages WHERE {' AND '.join(condition)}"
        with self.connection.cursor() as cur:
            cur: cursor
            cur.execute(req, values)
            self.connection.commit()
