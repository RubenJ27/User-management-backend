from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from jose import jwt
from schema.user__auth_schema import AuthUser, AuthUserCreateSchema, Token
from auth.auth import (
    get_password_hash, oauth2_scheme, ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_active_user
)
from database.database import get_db

app = FastAPI()
router = APIRouter()

@router.post("/token", response_model=Token, include_in_schema=False)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), conn = Depends(get_db)):
    user = authenticate_user(conn, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/auth", response_model=AuthUser, include_in_schema=False)
def create_user_endpoint(user: AuthUserCreateSchema, conn = Depends(get_db)):
    hashed_password = get_password_hash(user.hashed_password)
    db_user = {
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "hashed_password": hashed_password,
        "disabled": False,
    }
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO auth_users (username, full_name, email, hashed_password, disabled) VALUES (%s, %s, %s, %s, %s) RETURNING *",
            (db_user["username"], db_user["full_name"], db_user["email"], db_user["hashed_password"], db_user["disabled"]),
        )
        conn.commit()
        return cursor.fetchone()

# Custom documentation routes with authentication
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(token: str = Depends(oauth2_scheme)):
    return get_swagger_ui_html(openapi_url=app.openapi_url, title=app.title + " - Docs", oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url)

@app.get("/docs/oauth2-redirect", include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()