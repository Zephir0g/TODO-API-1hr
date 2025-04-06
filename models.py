from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    is_done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Task('{self.title}', '{self.is_done}')"