"""devspace_starwars_api.dependencies"""
from pydantic import BaseModel


class Status(BaseModel):
    message: str
