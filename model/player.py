"""Création d'un programme ayant pour but d'organiser un tournoi d'échec
"""
from datetime import date

from controllers_files.gender import Gender
from pydantic import BaseModel, PositiveInt
from pydantic.types import conint, constr


class Player(BaseModel):  # Défini les paramètres auxquels un joueur doit se conformer
    lastname: constr(strict=True, regex="^[A-Za-z '\-éèàçê]{2,25}$")
    firstname: constr(strict=True, regex="^[A-Za-z '\-éèàçê]{2,25}$")
    birthdate: date
    rank: conint(strict=True, gt=0, lt=3000)
    sexe: Gender
    id: PositiveInt

    def __str__(self) -> str:
        return f'{self.lastname.upper()} {self.firstname} ({self.rank})'
