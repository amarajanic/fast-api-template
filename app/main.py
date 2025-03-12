from typing import Union

from starlette.middleware.sessions import SessionMiddleware

from fastapi import FastAPI

from database.db import engine

from blog.router import router as blog_router

from user.router import router as user_router

from auth.router import router as auth_router

from role.router import router as role_router

from weather.router import router as weather_router

from admin.router import router as admin_router

from google_auth.router import router as google_router

from theme.router import router as theme_router

from blog.model import DbBlog

from user.model import DbUser

from role.model import DbRole

from theme.model import DbTheme

DbBlog.metadata.create_all(bind=engine)

DbUser.metadata.create_all(bind=engine)

DbRole.metadata.create_all(bind=engine)

DbTheme.metadata.create_all(bind=engine)


# from strawberry.asgi import GraphQL

# @strawberry.type
# class User:
#     name: str
#     age: int


# @strawberry.type
# class Query:
#     @strawberry.field
#     def user(self) -> User:
#         return User(name="Patrick", age=100)

# schema = strawberry.Schema(query=Query)


# graphql_app = GraphQL(schema)

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="!secret")

app.include_router(blog_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(role_router)
app.include_router(weather_router)
app.include_router(admin_router)
app.include_router(google_router)
app.include_router(theme_router)


# app.add_route("/graphql", graphql_app)
# app.add_websocket_route("/graphql", graphql_app)

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/health-check")
async def health_check():
    return {"status": "ok"}
