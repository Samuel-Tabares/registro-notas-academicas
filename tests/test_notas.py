"""Tests unitarios para el modulo de registro de notas academicas.

Cada test esta asociado a un caso de prueba (CP-NN) de la tabla en el README.
"""
import pytest

from registro_notas.notas import Nota, NotaFueraDeRangoError


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
