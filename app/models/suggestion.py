from app import db


class Suggestion(db.Model):
    __tablename__ = 'suggestions'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')
    
    def __init__(self, title, description, user_id):
        self.title = title
        self.description = description
        self.user_id = user_id
        
    def __repr__(self):
        return f'{self.title}'
    
    def save_suggestion(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_suggestion(self):
        db.session.delete(self)
        db.session.commit()
        
    def update_suggestion(self, title, description):
        self.title = title
        self.description = description
    
    @classmethod
    def find_by_suggestion(cls, _id):
        suggestion = cls.query.filter_by(id=_id).first()
        if suggestion:
            return suggestion
        return None
    
    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'user_id': self.user_id
            }
    