"""This module is used for authentication to the API.

Author: Chinedu Ezeofor
"""

from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session
from typeguard import typechecked

from e_commerce_app.models import get_db
from e_commerce_app.utils.credentials import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
)
from e_commerce_app.utils.crud import (
    authenticate_user,
)
from e_commerce_app.v1.schemas import token_schema

auth_router = APIRouter(prefix="/authqw", tags=["auth"])

# OAuth2PasswordBearer is used to get the token from the request headers.
# It sends the request to the tokenUrl endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


db_dependency = Annotated[Session, Depends(get_db)]
auth_dependency = Annotated[str, Depends(oauth2_scheme)]


@typechecked
def create_access_token(username: str, user_id: int, expires_delta: timedelta) -> str:
    """This generates a string as an access token."""

    to_encode: dict[str, Any] = {"sub": username, "id": user_id}
    expire: datetime = datetime.now(timezone.utc) + expires_delta

    # Update the data with the expiration timedelta
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


@typechecked
@auth_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> token_schema.Token:
    user: Optional[dict[str, Any]] = authenticate_user(
        username=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        username=user.username,  # type: ignore
        user_id=user.id,  # type: ignore
        expires_delta=access_token_expires,
    )

    return token_schema.Token({"access_token": access_token, "token_type": "bearer"})


# @typechecked
# async def get_current_user(
#     db: db_dependency, token: auth_dependency
# ) -> Union[HTTPException, Any]:
#     """This authenticates and returns the current user by sending a request to
#     `login_for_access_token`."""

#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         payload: dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: int = payload.get("id")
#         username: str = payload.get("sub")

#         if user_id is None or username is None:
#             raise credentials_exception
#         token_data = token_schema.TokenData(user_id=user_id, username=username)

#     except JWTError:
#         raise credentials_exception

#     user: Optional[dict[str, Any]] = get_customer_by_email(db=db, username=token_data.username)

#     if user is None:
#         raise credentials_exception

#     return user


# user_dependency = Annotated[
#     dict[str, db_schema.CustomersSchemaInDB], Depends(get_current_user)
# ]


# @typechecked
# @auth_router.get("/users")
# async def get_users(db: db_dependency, _: user_dependency) -> dict[str, User]:  # type: ignore
#     return db


# ================================================================================
from e_commerce_app.utils.crud import get_password_hash, verify_password

username: str = "adam1"
user_id: int = 2
plain_password: str = "12345abc"

hashed_password: str = get_password_hash(password=plain_password)
is_valid: bool = verify_password(plain_password=plain_password, hashed_password=hashed_password)


# result: Optional[dict[str, Any]] = get_customer_by_username(
#     db=db, username=username, password=plain_password
# )
# result: Optional[dict[str, Any]] = get_customer(db=db, id=1)
# result = authenticate_user(username=username, password=plain_password)
# access_token_expires: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
# result: str = create_access_token(
#     username=username, user_id=user_id, expires_delta=access_token_expires
# )


# print(is_valid)
