from enum import Enum


class Result(Enum):  # Fixe le score d'un match a des valeurs fixes pour éviter les erreurs
    Win = 1.0
    Loose = 0.0
    Draw = 0.5
