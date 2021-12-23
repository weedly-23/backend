from weedly_app.db.db import Base, engine
from sqlalchemy import Column, Integer, String, DateTime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class News(Base):
    __tablename__ = "news"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    source_name = Column(String, nullable=False)
    published = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Статья '{self.title}', автор {self.author}, опубликовано: {self.published}.>"


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    authors = Column(String, nullable=False)

    def __repr__(self):
        return f"<User ID: {self.id}>"


if __name__ == "__main__":
    """Run this module if you want to create given tables in a DB."""
    Base.metadata.create_all(bind=engine)