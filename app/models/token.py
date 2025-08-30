from app.extensions import db
from datetime import datetime,timezone

class TokenBlockList(db.Model):
    __tablename__ = "TokenBlockList"
    id = db.Column(db.Integer,primary_key=True)
    jti = db.Column(db.String(),nullable=True)
    created_at = db.Column(db.DateTime(), default = datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Token {self.jti}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def deleteBlockList(self):
        db.session.delete(self)
        db.session.commit()  