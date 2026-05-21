"""Tests unitarios para el modulo de registro de notas academicas.

Cada test esta asociado a un caso de prueba (CP-NN) de la tabla en el README.
"""
import pytest

from registro_notas.notas import (
    Estudiante,
    MateriaNoRegistradaError,
    Nota,
    NotaFueraDeRangoError,
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
