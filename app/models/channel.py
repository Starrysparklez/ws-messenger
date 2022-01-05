from .. import db

class TextChannel(db.Model):
    __tablename__ = 'textchannels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True)
    title = db.Column(db.String(64))

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title
        }
