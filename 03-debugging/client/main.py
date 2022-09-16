"""client"""
import os
import random
import time
from typing import Any, Callable

import httpx
from rich.pretty import pprint

NAMESPACE = os.getenv("NAMESPACE")
API_HOST = f"devspace-example-python-simple.{NAMESPACE}.svc.cluster.local"


def get_planet_count() -> int:
    r = httpx.get(f"http://{API_HOST}/planets")

    r.raise_for_status()

    return len(r.json())


def get_people_count() -> int:
    r = httpx.get(f"http://{API_HOST}/people")

    r.raise_for_status()

    return len(r.json())


def get_planet(id_: int) -> dict[str, Any]:
    r = httpx.get(f"http://{API_HOST}/planet/{id_}")

    if not r.is_success:
        print(f"planet id {id_} not found or otherwise failed...")

        return {}

    return r.json()


def get_person(id_: int) -> dict[str, Any]:
    r = httpx.get(f"http://{API_HOST}/people/{id_}")

    if not r.is_success:
        print(f"people id {id_} not found or otherwise failed...")

        return {}

    return r.json()


def report(obj: dict[str, Any]):
    pprint(obj)


def main():
    max_planets = get_planet_count()
    max_people = get_people_count()

    choices: list[str] = ["planet", "person"]
    choice_getters: dict[str, Callable[[int], dict[str, Any]]] = {
        "planet": get_planet,
        "person": get_person
    }
    choice_max: dict[str, int] = {
        "planet": max_planets,
        "person": max_people
    }

    while True:
        choice = random.choice(choices)

        obj = choice_getters[choice](random.randint(1, choice_max[choice]))

        report(obj=obj)

        time.sleep(random.randint(1, 5))


if __name__ == "__main__":
    main()
