from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite database connection
engine = create_engine("sqlite:///bookexchange.db")
Session = sessionmaker(bind=engine)
session = Session()