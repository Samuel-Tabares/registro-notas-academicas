# Registro de Notas Academicas

Modulo de registro de notas academicas para la Universidad Regional del Sur.
Entrega del primer parcial de la asignatura Pruebas de Software (Semestre V).

## Tecnologia elegida

- **Lenguaje:** Python 3.12
- **Gestor de dependencias y entorno:** [uv](https://github.com/astral-sh/uv)
- **Test unitario:** pytest + pytest-cov
- **BDD:** pytest-bdd (Gherkin)
- **CI/CD:** GitHub Actions

**Por que esta combinacion:** `uv` instala dependencias en milisegundos y produce un lockfile reproducible, lo cual mantiene el pipeline CI rapido y deterministico. `pytest-bdd` corre los escenarios Gherkin en el mismo runner que los tests unitarios, asi un solo comando ejecuta TDD y BDD juntos y la cobertura cubre ambos.

## Como ejecutar localmente

```bash
uv sync
uv run pytest --cov=src/registro_notas --cov-report=term-missing
```

## Estructura del repositorio

```
registro-notas-academicas/
├── .github/workflows/ci.yml      # Pipeline CI/CD
├── src/registro_notas/
│   └── notas.py                  # Logica de dominio
├── tests/
│   ├── test_notas.py             # Tests TDD unitarios
│   ├── features/notas.feature    # Escenarios Gherkin
│   └── step_defs/                # Step definitions BDD
├── pyproject.toml
└── README.md
```

---

## Parte 1 — Analisis de testing

Este analisis se hizo **antes** de escribir cualquier test o codigo. Es evidencia de haber pensado como tester antes de teclear.

### 1.1 Particiones de equivalencia — Requerimiento 1 (nota entre 0.0 y 5.0)

| # | Particion | Rango que cubre | Valor representativo | Resultado esperado |
|---|---|---|---|---|
| P1 | Invalida — por debajo del minimo | `valor < 0.0` | `-1.5` | Error: nota fuera de rango |
| P2 | Valida — zona de reprobacion | `0.0 <= valor < 3.0` | `2.0` | Nota aceptada, reprueba |
| P3 | Valida — zona de aprobacion | `3.0 <= valor <= 5.0` | `4.2` | Nota aceptada, aprueba |
| P4 | Invalida — por encima del maximo | `valor > 5.0` | `5.5` | Error: nota fuera de rango |
| P5 | Invalida — tipo no numerico | cualquier no-numero | `"cinco"` | Error: tipo invalido |

Razon de incluir P5: los inputs reales pueden llegar como strings desde un formulario; cubrir esa frontera evita errores silenciosos en produccion.

### 1.2 Analisis de valores limite — Requerimiento 1

Para cada borde del rango `[0.0, 5.0]` se prueban tres valores: justo antes, el limite exacto, justo despues.

| Valor | Dentro del rango | Resultado esperado |
|---|---|---|
| `-0.1` | No | Error: nota fuera de rango |
| `0.0` | Si (limite inferior exacto) | Nota aceptada |
| `0.1` | Si | Nota aceptada |
| `4.9` | Si | Nota aceptada |
| `5.0` | Si (limite superior exacto) | Nota aceptada |
| `5.1` | No | Error: nota fuera de rango |

Adicionalmente, para el limite de aprobacion del Requerimiento 2 (`>= 3.0`):

| Valor | Resultado esperado |
|---|---|
| `2.9` | Reprueba |
| `3.0` | Aprueba (limite exacto) |
| `3.1` | Aprueba |

### 1.3 Preguntas al Product Owner — Requerimiento 4 (no duplicar nota)

**Pregunta 1:** ¿Que formato identifica un "semestre"? ¿Es un string libre (`"2026-1"`, `"2026A"`), un entero correlativo o un objeto con año + periodo?

*Por que impacta los casos de prueba:* la clave de unicidad usada para detectar duplicados depende de esto. Si el semestre es un string libre, los tests deben cubrir variaciones de capitalizacion y espacios (¿`"2026-1"` y `"2026-1 "` son el mismo semestre?). Si es un objeto estructurado, los tests deben validar igualdad por valor, no por referencia.

**Pregunta 2:** Cuando se intenta registrar una nota duplicada, ¿el sistema debe rechazar la operacion completa o sobreescribir la nota anterior (con o sin auditoria)?

*Por que impacta los casos de prueba:* el enunciado dice "lanzar un error claro", lo cual implica rechazo. Pero hay que confirmar si despues del error el estado del estudiante queda inalterado. Esto define un test critico: tras una excepcion, `len(estudiante.notas)` debe seguir igual y la nota original debe permanecer intacta.

**Pregunta 3 (bonus):** ¿Que debe devolver el calculo de promedio si el estudiante no tiene notas registradas? ¿Cero, `None`, o un error?

*Por que impacta los casos de prueba:* es una decision de diseño que cambia el comportamiento esperado en un caso borde obligatorio (estudiante sin notas, exigido por la Parte 2 del enunciado). Asumo **lanzar un error** porque devolver `0.0` confundiria con "reprobado total" y devolver `None` rompe el tipado.

---
