from sqlalchemy import select, delete


from rich.console import Console
from db import User, session


console = Console()

# Joins
# stmt = insert(User).values(name="jude", fullname="Jude Bags")
# session.execute(stmt)


stmt = delete(User).where(User.name == "patrick")
session.execute(stmt)
session.commit()

users = session.execute(select(User)).all()

# for row in users:
console.print(users)
# console.print(users)


# # Update
# try:
#     users = session.query(User).all()
#     console.print(users)
#     console.print("User inserted successfully!", style="green")
#     session.commit()

# except Exception as err:
#     console.print(f"Error inserting user: {err}", style="red")
#     session.rollback()  # Rollback changes on error
