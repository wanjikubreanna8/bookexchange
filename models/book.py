from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Book(Base):
    __tablename__ = 'books'  # ✅ correction ici

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String)

    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship("User", backref="books")

    def __repr__(self):  
        return f"<Book(id={self.id}, title='{self.title}', owner_id={self.owner_id})>"
