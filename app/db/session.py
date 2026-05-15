from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.config import DATABASE_URL

engine = create_engine(str(DATABASE_URL))

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)