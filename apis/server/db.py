from apis.store import database

# db instance
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()