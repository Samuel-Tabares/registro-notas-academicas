"""Step definitions para los escenarios BDD de registro de notas."""
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from registro_notas.notas import Estudiante, NotaDuplicadaError, SinNotasError

FEATURE_FILE = (
    Path(__file__).parent.parent / "features" / "notas.feature"
)

scenarios(str(FEATURE_FILE))


@pytest.fixture
def contexto() -> dict:
    return {"estudiante": None, "error": None}


# --- Given ---

@given(parsers.parse('existe el estudiante "{nombre}" sin notas registradas'))
def crear_estudiante(contexto, nombre):
    contexto["estudiante"] = Estudiante(nombre=nombre)


@given(
    parsers.parse(
        'el estudiante ya tiene una nota de {valor:f} en la materia '
        '"{materia}" del semestre "{semestre}"'
    )
)
def estudiante_con_nota_previa(contexto, valor, materia, semestre):
    contexto["estudiante"].registrar_nota(
        materia=materia, semestre=semestre, valor=valor
    )


# --- When ---

@when(
    parsers.parse(
        'registro la nota {valor:f} en la materia "{materia}" del semestre '
        '"{semestre}"'
    )
)
def registrar_nota(contexto, valor, materia, semestre):
    try:
        contexto["estudiante"].registrar_nota(
            materia=materia, semestre=semestre, valor=valor
        )
    except NotaDuplicadaError as exc:
        contexto["error"] = exc


@when(
    parsers.parse(
        'intento registrar la nota {valor:f} en la materia "{materia}" del '
        'semestre "{semestre}"'
    )
)
def intentar_registrar_nota(contexto, valor, materia, semestre):
    try:
        contexto["estudiante"].registrar_nota(
            materia=materia, semestre=semestre, valor=valor
        )
    except NotaDuplicadaError as exc:
        contexto["error"] = exc


@when("intento consultar el promedio del estudiante")
def intentar_promedio(contexto):
    try:
        contexto["estudiante"].promedio()
    except SinNotasError as exc:
        contexto["error"] = exc


# --- Then ---

@then(
    parsers.parse(
        'el estudiante aprueba la materia "{materia}" del semestre "{semestre}"'
    )
)
def verificar_aprueba(contexto, materia, semestre):
    assert contexto["estudiante"].aprueba(materia=materia, semestre=semestre) is True


@then(
    parsers.parse(
        'la decision de aprobacion para "{materia}" en "{semestre}" es {decision}'
    )
)
def verificar_decision(contexto, materia, semestre, decision):
    aprueba = contexto["estudiante"].aprueba(materia=materia, semestre=semestre)
    esperado = decision.strip() == "aprueba"
    assert aprueba is esperado, (
        f'Se esperaba "{decision}" pero el sistema devolvio aprueba={aprueba}'
    )


@then(parsers.parse("el promedio del estudiante es {esperado:f}"))
def verificar_promedio(contexto, esperado):
    assert contexto["estudiante"].promedio() == pytest.approx(esperado)


@then(parsers.parse('el sistema responde con el error "{nombre_error}"'))
def verificar_error(contexto, nombre_error):
    assert contexto["error"] is not None, "Se esperaba un error pero no se capturo ninguno"
    assert type(contexto["error"]).__name__ == nombre_error


@then(parsers.parse("el estudiante mantiene solo {cantidad:d} nota registrada"))
def verificar_cantidad_de_notas_singular(contexto, cantidad):
    assert len(contexto["estudiante"].notas) == cantidad


@then(parsers.parse("el estudiante tiene {cantidad:d} notas registradas"))
def verificar_cantidad_de_notas(contexto, cantidad):
    assert len(contexto["estudiante"].notas) == cantidad
