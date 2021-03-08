from app import db
from passlib.hash import pbkdf2_sha256

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    
    def __repr__(self):
        return f'{self.username}'
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        
    def save_user(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_by_user(cls, _id):
        user = cls.query.get(_id)
        if user:
            return user
        return None
    
    @classmethod
    def find_by_email(cls, _email):
        user = cls.query.filter_by(email=_email).first()
        if user:
            return user
        return None
    
    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
        
    def gen_hash(self):
        self.password = pbkdf2_sha256.hash(self.password)
    
    def verify_password(self, password):
        return pbkdf2_sha256.verify(password ,self.password)