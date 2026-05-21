"""Modulo de registro de notas academicas."""
from dataclasses import dataclass, field

NOTA_MINIMA = 0.0
NOTA_MAXIMA = 5.0
NOTA_APROBACION = 3.0


class NotaFueraDeRangoError(ValueError):
    """Se intenta crear una nota con valor fuera del rango permitido."""


class MateriaNoRegistradaError(LookupError):
    """Se consulta una materia que el estudiante no tiene registrada."""


class SinNotasError(ValueError):
    """Se intenta calcular el promedio de un estudiante sin notas registradas."""


class NotaDuplicadaError(ValueError):
    """Ya existe una nota registrada para la misma materia en el mismo semestre."""


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

    def corresponde_a(self, materia: str, semestre: str) -> bool:
        return self.materia == materia and self.semestre == semestre


@dataclass
class Estudiante:
    nombre: str
    notas: list[Nota] = field(default_factory=list)

    def registrar_nota(self, materia: str, semestre: str, valor: float) -> Nota:
        if self._buscar(materia, semestre) is not None:
            raise NotaDuplicadaError(
                f"Ya existe una nota para la materia '{materia}' en el "
                f"semestre '{semestre}' del estudiante {self.nombre}"
            )
        nota = Nota(materia=materia, semestre=semestre, valor=valor)
        self.notas.append(nota)
        return nota

    def aprueba(self, materia: str, semestre: str) -> bool:
        nota = self._buscar(materia, semestre)
        if nota is None:
            raise MateriaNoRegistradaError(
                f"El estudiante {self.nombre} no tiene registrada la materia "
                f"'{materia}' en el semestre '{semestre}'"
            )
        return nota.valor >= NOTA_APROBACION

    def promedio(self) -> float:
        if not self.notas:
            raise SinNotasError(
                f"El estudiante {self.nombre} no tiene notas registradas"
            )
        return sum(n.valor for n in self.notas) / len(self.notas)

    def _buscar(self, materia: str, semestre: str) -> Nota | None:
        return next(
            (n for n in self.notas if n.corresponde_a(materia, semestre)),
            None,
        )
