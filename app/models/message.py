from .. import db

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer)
    content = db.Column(db.String(1024))
    author_id = db.Column(db.Integer)

    def to_json(self):
        return {
            "id": self.id,
            "channel_id": self.channel_id,
            "content": self.content,
            "author_id": self.author_id
        }
