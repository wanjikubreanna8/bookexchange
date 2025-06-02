from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime

class ExchangeRequest(Base):
    __tablename__ = 'exchange_requests'  # ✅ corrigé

    id = Column(Integer, primary_key=True)
    status = Column(String, default='Pending', nullable=False)  # ✅ valeur par défaut
    timestamp = Column(DateTime, default=datetime.utcnow)  # ✅ date de création

    requester_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)

    requester = relationship("User", backref="sent_requests")
    book = relationship("Book", backref="requests")

    def __repr__(self):
        return (
            f"<ExchangeRequest(id={self.id}, book_id={self.book_id}, "
            f"requester_id={self.requester_id}, status='{self.status}')>"
        )
