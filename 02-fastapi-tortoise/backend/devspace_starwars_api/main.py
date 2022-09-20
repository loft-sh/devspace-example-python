"""devspace_starwars_api.main"""
from fastapi import FastAPI

from tortoise.contrib.fastapi import register_tortoise

from .routes import people, planets

app = FastAPI(title="Hello, DevSpace and StarWars!")
app.include_router(people.router)
app.include_router(planets.router)


POSTGRES_USER = "postgres"
POSTGRES_PASS = "password"
POSTGRES_DB = "starwars"

register_tortoise(
    app,
    db_url=f"postgres://{POSTGRES_USER}:{POSTGRES_PASS}@localhost:5432/{POSTGRES_DB}",
    modules={"models": ["devspace_starwars_api.db.models"]},
    generate_schemas=False,
    add_exception_handlers=True,
)
