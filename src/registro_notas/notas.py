"""Modulo de registro de notas academicas."""
from dataclasses import dataclass, field

NOTA_MINIMA = 0.0
NOTA_MAXIMA = 5.0
NOTA_APROBACION = 3.0


class NotaFueraDeRangoError(ValueError):
    """Se intenta crear una nota con valor fuera del rango permitido."""


class MateriaNoRegistradaError(LookupError):
    """Se consulta una materia que el estudiante no tiene registrada."""


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


@dataclass
class Estudiante:
    nombre: str
    notas: list[Nota] = field(default_factory=list)

    def registrar_nota(self, materia: str, semestre: str, valor: float) -> Nota:
        nota = Nota(materia=materia, semestre=semestre, valor=valor)
        self.notas.append(nota)
        return nota

    def aprueba(self, materia: str, semestre: str) -> bool:
        nota = self._buscar_nota(materia, semestre)
        return nota.valor >= NOTA_APROBACION

    def _buscar_nota(self, materia: str, semestre: str) -> Nota:
        for nota in self.notas:
            if nota.materia == materia and nota.semestre == semestre:
                return nota
        raise MateriaNoRegistradaError(
            f"El estudiante {self.nombre} no tiene registrada la materia "
            f"'{materia}' en el semestre '{semestre}'"
        )
