"""Modulo de registro de notas academicas."""
from dataclasses import dataclass

NOTA_MINIMA = 0.0
NOTA_MAXIMA = 5.0


class NotaFueraDeRangoError(ValueError):
    """Se intenta crear una nota con valor fuera del rango permitido."""


@dataclass(frozen=True)
class Nota:
    materia: str
    semestre: str
    valor: float

    def __post_init__(self):
        if not NOTA_MINIMA <= self.valor <= NOTA_MAXIMA:
            raise NotaFueraDeRangoError(
                f"La nota {self.valor} esta fuera del rango permitido "
                f"[{NOTA_MINIMA}, {NOTA_MAXIMA}]"
            )
