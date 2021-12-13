from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=False, nullable=False)
    source_name = db.Column(db.String, nullable=False)
    published = db.Column(db.DateTime, nullable=True)

    def __repr__(self): # тут пишем как будет отображатся при печати 
        return f'News.title:{self.title}'


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    authors = db.Column(db.String, nullable=False)

    def __repr__(self): # тут пишем как будет отображатся при печати 
        return f'User.id:{self.title}'

