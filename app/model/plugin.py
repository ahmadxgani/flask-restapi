from app import db
from datetime import datetime
from app.model.user import User

class Plugin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fitur = db.Column(db.String(130), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey(User.id))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", backref="user_id")
    
    def __repr__(self):
        return '<Plugin {}>'.format(self.fitur)