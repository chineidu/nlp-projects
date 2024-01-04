from typing import Any
from sqlalchemy import insert


from rich.console import Console
from db import User, session


console = Console()

new_users: list[dict[str, Any]] = [
    {"name": "spongebob", "fullname": "Spongebob Squarepants"},
    {"name": "sandy", "fullname": "Sandy Cheeks"},
    {"name": "patrick", "fullname": "Patrick Star"},
    {"name": "squidward", "fullname": "Squidward Tentacles"},
    {"name": "ehkrabs", "fullname": "Eugene H. Krabs"},
]

# Bulk Insert
try:
    users = session.scalars(insert(User).returning(User), new_users)
    session.commit()
    console.print(users.all())
    console.print("User inserted successfully!", style="green")

except Exception as err:
    console.print(f"Error inserting user: {err}", style="red")
    session.rollback()  # Rollback changes on error
