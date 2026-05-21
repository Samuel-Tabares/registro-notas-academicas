"""Modulo de registro de notas academicas."""
from dataclasses import dataclass


class NotaFueraDeRangoError(ValueError):
    """Se intenta crear una nota con valor fuera del rango permitido."""


@dataclass(frozen=True)
class Nota:
    materia: str
    semestre: str
    valor: float

    def __post_init__(self):
        if self.valor < 0.0 or self.valor > 5.0:
            raise NotaFueraDeRangoError(
                f"La nota {self.valor} esta fuera del rango permitido [0.0, 5.0]"
            )
