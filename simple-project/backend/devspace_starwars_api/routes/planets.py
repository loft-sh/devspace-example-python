"""devspace_starwars_api.routes.planet"""
from typing import List

from fastapi import HTTPException, APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError

from ..dependencies import Status
from ..db.models import Planet, Planet_Pydantic, PlanetIn_Pydantic


router = APIRouter()


@router.get("/planets", response_model=List[Planet_Pydantic])
async def get_planets():
    return await Planet_Pydantic.from_queryset(Planet.all())


@router.post("/planet", response_model=Planet_Pydantic)
async def create_planet(planet: PlanetIn_Pydantic):
    user_obj = await Planet.create(**planet.dict(exclude_unset=True))
    return await Planet_Pydantic.from_tortoise_orm(user_obj)


@router.get("/planet/{planet_id}", response_model=Planet_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_planet(planet_id: int):
    return await Planet_Pydantic.from_queryset_single(Planet.get(id=planet_id))


@router.put("/planet/{planet_id}", response_model=Planet_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_planet(planet_id: int, user: PlanetIn_Pydantic):
    await Planet.filter(id=planet_id).update(**user.dict(exclude_unset=True))
    return await Planet_Pydantic.from_queryset_single(Planet.get(id=planet_id))


@router.delete("/planet/{planet_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_planet(planet_id: int):
    deleted_count = await Planet.filter(id=planet_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Planet {planet_id} not found")
    return Status(message=f"Deleted planet {planet_id}")
