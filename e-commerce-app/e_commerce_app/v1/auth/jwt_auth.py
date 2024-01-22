"""This module is used for authentication to the API.

Author: Chinedu Ezeofor
"""

from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typeguard import typechecked

from e_commerce_app.models import get_db
from e_commerce_app.utils.credentials import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
)
from e_commerce_app.utils.crud import authenticate_user, get_customer_by_username
from e_commerce_app.v1.schemas import token_schema

auth_router = APIRouter(prefix="/auth", tags=["auth"])

# OAuth2PasswordBearer is used to get the token from the request headers.
# It sends the request to the tokenUrl endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

db_dependency = Annotated[Session, Depends(get_db)]
token_dependency = Annotated[str, Depends(oauth2_scheme)]


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
    _token: dict[str, Any] = {"access_token": access_token, "token_type": "bearer"}

    return token_schema.Token(**_token)


@typechecked
async def get_current_user(db: db_dependency, token: token_dependency) -> Union[HTTPException, Any]:
    """This authenticates and returns the current user by sending a request to
    `login_for_access_token`."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload: dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[int] = payload.get("id")
        username: Optional[str] = payload.get("sub")

        if user_id is None or username is None:
            raise credentials_exception

        token_data = token_schema.TokenData(user_id=user_id, username=username)

    except JWTError:
        raise credentials_exception

    user = get_customer_by_username(db=db, username=token_data.username)  # type: ignore

    if user is None:
        raise credentials_exception

    return user
