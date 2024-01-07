from typing import Any

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from e_commerce_app.config import settings

root_router = APIRouter()


body_template: str = """
            <html>
                <body style='padding: 15px;'>
                    <h1>{} App</h1>
                    <div>
                    Check the docs: <a href='{}/docs'>here</a>
                    </div>
                </body>
            </html>
    """


@root_router.get("/")
async def index() -> Any:
    """This is the homepage."""

    body: str = body_template.format(settings.PROJECT_NAME, settings.API_VERSION_STR)  # type: ignore
    return HTMLResponse(content=body)


@root_router.get(f"/health")
async def health() -> dict[str, Any]:
    """This is used for health check."""

    return {
        "message": f"{settings.PROJECT_NAME} app is working properly!",  # type: ignore
        "version": settings.API_FLOAT_VERSION,  # type: ignore
        "status": "success",
    }
