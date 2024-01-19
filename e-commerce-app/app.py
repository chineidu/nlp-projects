import uvicorn
from fastapi import FastAPI

from e_commerce_app import create_app, settings  # type: ignore

app: FastAPI = create_app()


def main() -> None:
    """This is the entrypoint."""

    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )


# Run with CLI (Recommended)
# uvicorn app:app --port 8008 --host "0.0.0.0"
