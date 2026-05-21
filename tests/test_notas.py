"""Tests unitarios para el modulo de registro de notas academicas.

Cada test esta asociado a un caso de prueba (CP-NN) de la tabla en el README.
"""
import pytest

from registro_notas.notas import (
    Estudiante,
    MateriaNoRegistradaError,
    Nota,
    NotaDuplicadaError,
    NotaFueraDeRangoError,
    SinNotasError,
)


class TestNotaRangoValido:
    """Requerimiento 1: la nota debe estar entre 0.0 y 5.0."""

    def test_cp01_nota_dentro_del_rango_se_acepta(self):
        nota = Nota(materia="Calculo", semestre="2026-1", valor=4.2)
        assert nota.valor == 4.2

    def test_cp02_nota_en_limite_inferior_exacto_se_acepta(self):
        nota = Nota(materia="Algebra", semestre="2026-1", valor=0.0)
        assert nota.valor == 0.0

    def test_cp03_nota_en_limite_superior_exacto_se_acepta(self):
        nota = Nota(materia="Algebra", semestre="2026-1", valor=5.0)
        assert nota.valor == 5.0

    def test_cp04_nota_por_debajo_del_minimo_lanza_error(self):
        with pytest.raises(NotaFueraDeRangoError):
            Nota(materia="Algebra", semestre="2026-1", valor=-0.1)

    def test_cp05_nota_por_encima_del_maximo_lanza_error(self):
        with pytest.raises(NotaFueraDeRangoError):
            Nota(materia="Algebra", semestre="2026-1", valor=5.1)


class TestAprobacion:
    """Requerimiento 2: aprueba con nota >= 3.0."""

    def test_cp06_aprueba_con_nota_en_el_limite_3_0(self):
        estudiante = Estudiante(nombre="Ana Perez")
        estudiante.registrar_nota(materia="Algebra", semestre="2026-1", valor=3.0)
        assert estudiante.aprueba(materia="Algebra", semestre="2026-1") is True

    def test_cp07_reprueba_con_nota_justo_debajo_del_limite(self):
        estudiante = Estudiante(nombre="Ana Perez")
        estudiante.registrar_nota(materia="Algebra", semestre="2026-1", valor=2.9)
        assert estudiante.aprueba(materia="Algebra", semestre="2026-1") is False

    def test_cp08_aprueba_con_nota_claramente_sobre_el_limite(self):
        estudiante = Estudiante(nombre="Ana Perez")
        estudiante.registrar_nota(materia="Algebra", semestre="2026-1", valor=4.5)
        assert estudiante.aprueba(materia="Algebra", semestre="2026-1") is True

    def test_cp09_consultar_materia_no_registrada_lanza_error(self):
        estudiante = Estudiante(nombre="Ana Perez")
        with pytest.raises(MateriaNoRegistradaError):
            estudiante.aprueba(materia="Fisica", semestre="2026-1")


class TestPromedio:
    """Requerimiento 3: calcular promedio de todas las notas."""

    def test_cp10_promedio_de_varias_notas(self):
        estudiante = Estudiante(nombre="Ana Perez")
        estudiante.registrar_nota(materia="Calculo", semestre="2026-1", valor=3.0)
        estudiante.registrar_nota(materia="Algebra", semestre="2026-1", valor=4.0)
        estudiante.registrar_nota(materia="Fisica", semestre="2026-1", valor=5.0)
        assert estudiante.promedio() == 4.0

    def test_cp11_promedio_con_una_sola_nota(self):
        estudiante = Estudiante(nombre="Ana Perez")
        estudiante.registrar_nota(materia="Calculo", semestre="2026-1", valor=3.5)
        assert estudiante.promedio() == 3.5

    def test_cp12_promedio_sin_notas_lanza_error(self):
        estudiante = Estudiante(nombre="Ana Perez")
        with pytest.raises(SinNotasError):
            estudiante.promedio()


class TestNoDuplicarNota:
    """Requerimiento 4: no permitir dos notas para la misma materia y semestre."""

    def test_cp13_registrar_duplicado_lanza_error(self):
        estudiante = Estudiante(nombre="Ana Perez")
        estudiante.registrar_nota(materia="Calculo", semestre="2026-1", valor=4.0)
        with pytest.raises(NotaDuplicadaError):
            estudiante.registrar_nota(materia="Calculo", semestre="2026-1", valor=3.5)

    def test_cp14_misma_materia_en_semestre_diferente_se_permite(self):
        estudiante = Estudiante(nombre="Ana Perez")
        estudiante.registrar_nota(materia="Calculo", semestre="2026-1", valor=3.0)
        estudiante.registrar_nota(materia="Calculo", semestre="2026-2", valor=4.0)
        assert len(estudiante.notas) == 2

    def test_cp15_estado_no_cambia_tras_error_de_duplicado(self):
        estudiante = Estudiante(nombre="Ana Perez")
        estudiante.registrar_nota(materia="Calculo", semestre="2026-1", valor=4.0)
        with pytest.raises(NotaDuplicadaError):
            estudiante.registrar_nota(materia="Calculo", semestre="2026-1", valor=2.0)
        assert len(estudiante.notas) == 1
        assert estudiante.notas[0].valor == 4.0
