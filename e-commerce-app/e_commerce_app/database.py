from sqlalchemy.orm import Session

from e_commerce_app.models import session_local


def get_db() -> Session:
    """This is used to load the database instance."""
    db = session_local
    try:
        yield db
    finally:
        db.close()
