from datetime import timedelta
import json
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from sqlalchemy.orm import Session
from database.db import get_db
from google_auth.services import generate_tokens, validate_user

router = APIRouter(tags=["google-authentication"])


config = Config('.env')
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@router.get('/google-login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return jsonable_encoder(await oauth.google.authorize_redirect(request, redirect_uri))["_headers"]["location"]


@router.get('/google-auth')
async def auth(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user = await validate_user(db, token.get('userinfo')["email"])
        response = await generate_tokens(user, db)
        return response
    except OAuthError as error:
       raise HTTPException(status.HTTP_401_UNAUTHORIZED, error.error)


