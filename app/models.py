from database_init import db

class Tasks(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key = True)
    task_type = db.Column(db.String(120), nullable = False)
    task_value = db.Column(db.String(120), nullable = False)
    task_result = db.Column(db.String(120), nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls):
        return [t.__dict__ for t in cls.query.all()]
