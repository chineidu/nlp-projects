# from sqlalchemy.orm import Session

# from e_commerce_app.models import session_local
# from e_commerce_app.logger_config import logger

# def get_db() -> Session:
#     """This is used to load the database instance."""
#     db = session_local
#     try:
#         logger.info("Database loaded!")
#         yield db
#     finally:
#         db.close()
