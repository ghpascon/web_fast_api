from app.db.session import Base, SessionLocal,engine
from contextlib import contextmanager


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    from app import models 
    Base.metadata.create_all(bind=engine)
