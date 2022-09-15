"""devspace_starwars_api.db.models"""
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Planet(models.Model):
    """Planet DB Model"""

    class Meta:
        table = "planets"

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128)
    rotation_period = fields.IntField(null=True)
    orbital_period = fields.IntField(null=True)
    diameter = fields.IntField(null=True)
    climate = fields.CharField(max_length=128, null=True)
    gravity = fields.CharField(max_length=128, null=True)
    terrain = fields.CharField(max_length=128, null=True)
    surface_water = fields.CharField(max_length=128, null=True)
    population = fields.BigIntField(null=True)
    created_date = fields.DatetimeField(auto_now_add=True)
    updated_date = fields.DatetimeField(auto_now=True)
    url = fields.CharField(max_length=128)


Planet_Pydantic = pydantic_model_creator(Planet, name="Planet")
PlanetIn_Pydantic = pydantic_model_creator(Planet, name="Planet", exclude_readonly=True)


class Person(models.Model):
    """Person DB Model"""

    class Meta:
        table = "people"

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128)
    height = fields.IntField(null=True)
    mass = fields.IntField(null=True)
    hair_color = fields.CharField(max_length=128, null=True)
    skin_color = fields.CharField(max_length=128, null=True)
    eye_color = fields.CharField(max_length=128, null=True)
    birth_year = fields.CharField(max_length=128, null=True)
    gender = fields.CharField(max_length=32, null=True)
    planet_id = fields.IntField(null=True)
    created_date = fields.DatetimeField(auto_now_add=True)
    updated_date = fields.DatetimeField(auto_now=True)
    url = fields.CharField(max_length=128)


Person_Pydantic = pydantic_model_creator(Person, name="Person")
PersonIn_Pydantic = pydantic_model_creator(Person, name="Person", exclude_readonly=True)
