from db.connection import session
from models.base import Base
from db.connection import engine
from models.user import User
from models.book import Book
from models.exchange_request import ExchangeRequest
from datetime import datetime

# Recreate tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Clear session
session.query(ExchangeRequest).delete()
session.query(Book).delete()
session.query(User).delete()

# Users
u1 = User(name="Alice", email="alice@example.com", location="Nairobi")
u2 = User(name="Bob", email="bob@example.com", location="Mombasa")

# Books
b1 = Book(title="1984", author="George Orwell", genre="Dystopia", owner=u1)
b2 = Book(title="The Alchemist", author="Paulo Coelho", genre="Adventure", owner=u2)
b3 = Book(title="Sapiens", author="Yuval Noah Harari", genre="History", owner=u1)

# Exchange Request: Bob demande "Sapiens" to Alice
r1 = ExchangeRequest(requester=u2, book=b3, status="Pending")

# Add to session
session.add_all([u1, u2, b1, b2, b3, r1])
session.commit()

print(" Database seeded with test data.")