"""devspace_starwars_api.routes.person"""
from typing import List

from fastapi import HTTPException, APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError

from ..dependencies import Status
from ..db.models import Person, Person_Pydantic, PersonIn_Pydantic


router = APIRouter()


@router.get("/people", response_model=List[Person_Pydantic])
async def get_people():
    return await Person_Pydantic.from_queryset(Person.all())


@router.post("/people", response_model=Person_Pydantic)
async def create_person(person: PersonIn_Pydantic):
    user_obj = await Person.create(**person.dict(exclude_unset=True))
    return await Person_Pydantic.from_tortoise_orm(user_obj)


@router.get("/people/{person_id}", response_model=Person_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_person(person_id: int):
    return await Person_Pydantic.from_queryset_single(Person.get(id=person_id))


@router.put("/people/{person_id}", response_model=Person_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_person(person_id: int, user: PersonIn_Pydantic):
    await Person.filter(id=person_id).update(**user.dict(exclude_unset=True))
    return await Person_Pydantic.from_queryset_single(Person.get(id=person_id))


@router.delete("/people/{person_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_person(person_id: int):
    deleted_count = await Person.filter(id=person_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Person {person_id} not found")
    return Status(message=f"Deleted person {person_id}")
