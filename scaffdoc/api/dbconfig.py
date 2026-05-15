from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = ''
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

with engine.connect() as conn:
    conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
    conn.commit()