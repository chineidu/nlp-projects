# type: ignore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from e_commerce_app.config import settings


def create_app() -> FastAPI:
    """This is used to create the app and add routers."""

    # ==== Included to avoid calling this multiple times. ====
    from e_commerce_app.v1.auth.jwt_auth import auth_router
    from e_commerce_app.v1.routes.customers import customer_router
    from e_commerce_app.v1.routes.health import root_router
    from e_commerce_app.v1.routes.orders import orders_router
    from e_commerce_app.v1.routes.products import products_router

    app: FastAPI = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"/{settings.API_VERSION_STR}/openapi.json",
        docs_url=f"/{settings.API_VERSION_STR}/docs",
        redoc_url=f"/{settings.API_VERSION_STR}/redoc",
        version=settings.API_FLOAT_VERSION,
    )
    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Add routers
    app.include_router(root_router)
    app.include_router(customer_router, prefix=f"/{settings.API_VERSION_STR}")
    app.include_router(products_router, prefix=f"/{settings.API_VERSION_STR}")
    app.include_router(orders_router, prefix=f"/{settings.API_VERSION_STR}")
    app.include_router(auth_router, prefix=f"/{settings.API_VERSION_STR}")

    return app
