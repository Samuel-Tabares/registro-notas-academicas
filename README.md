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

## Parte 2 — Tabla formal de casos de prueba

Estos casos son la guia que cualquier tester del equipo podria ejecutar manualmente, independientemente del codigo. Cada caso tiene su test automatizado correspondiente en `tests/test_notas.py`.

Distribucion: **15 casos** (minimo exigido = 12), repartidos 4/4/3/4 entre los cuatro requerimientos.

| ID | Req | Descripcion | Precondicion | Datos de entrada | Pasos | Resultado esperado | Tipo |
|---|---|---|---|---|---|---|---|
| CP-01 | R1 | Registrar nota dentro del rango valido en zona de aprobacion | Estudiante existe sin notas | materia="Calculo", semestre="2026-1", valor=4.2 | 1) Crear Nota 2) registrar_nota() | Nota agregada al estudiante | Positivo |
| CP-02 | R1 | Registrar nota en el limite inferior exacto | Estudiante existe | valor=0.0 | 1) Crear Nota con valor 0.0 | Nota aceptada sin error | Borde |
| CP-03 | R1 | Registrar nota en el limite superior exacto | Estudiante existe | valor=5.0 | 1) Crear Nota con valor 5.0 | Nota aceptada sin error | Borde |
| CP-04 | R1 | Rechazar nota por debajo del minimo | Estudiante existe | valor=-0.1 | 1) Intentar crear Nota | Lanza NotaFueraDeRangoError | Negativo |
| CP-05 | R1 | Rechazar nota por encima del maximo | Estudiante existe | valor=5.1 | 1) Intentar crear Nota | Lanza NotaFueraDeRangoError | Negativo |
| CP-06 | R2 | Aprobar con nota justo en el limite | Nota registrada con 3.0 | materia="Algebra", semestre="2026-1" | 1) aprueba(materia, semestre) | Devuelve True | Borde |
| CP-07 | R2 | Reprobar con nota justo debajo del limite | Nota registrada con 2.9 | materia="Algebra", semestre="2026-1" | 1) aprueba(materia, semestre) | Devuelve False | Borde |
| CP-08 | R2 | Aprobar con nota claramente sobre el limite | Nota registrada con 4.5 | materia="Algebra", semestre="2026-1" | 1) aprueba(materia, semestre) | Devuelve True | Positivo |
| CP-09 | R2 | Consultar aprobacion de materia no registrada | Estudiante sin esa materia | materia="Fisica", semestre="2026-1" | 1) aprueba(materia, semestre) | Lanza error materia no encontrada | Negativo |
| CP-10 | R3 | Calcular promedio con varias notas | 3 notas: 3.0, 4.0, 5.0 | n/a | 1) promedio() | Devuelve 4.0 | Positivo |
| CP-11 | R3 | Calcular promedio con una sola nota | 1 nota: 3.5 | n/a | 1) promedio() | Devuelve 3.5 | Positivo |
| CP-12 | R3 | Calcular promedio sin notas registradas | Estudiante recien creado | n/a | 1) promedio() | Lanza SinNotasError | Negativo |
| CP-13 | R4 | Registrar dos notas en la misma materia y semestre | Ya existe nota ("Calculo","2026-1",4.0) | nueva nota ("Calculo","2026-1",3.5) | 1) registrar_nota() | Lanza NotaDuplicadaError | Negativo |
| CP-14 | R4 | Misma materia en semestre diferente debe permitirse | Existe ("Calculo","2026-1",3.0) | nueva nota ("Calculo","2026-2",4.0) | 1) registrar_nota() | Ambas notas almacenadas | Positivo |
| CP-15 | R4 | El estado del estudiante no cambia tras error de duplicado | Existe ("Calculo","2026-1",4.0) | nueva nota ("Calculo","2026-1",2.0) | 1) registrar_nota() esperando excepcion 2) verificar lista de notas | Lista de notas sin cambios, nota original intacta con valor 4.0 | Negativo |

---

## Parte 3 — Ciclo TDD evidenciado en los commits

El historial de Git muestra el ciclo Red-Green-Refactor aplicado a los cuatro requerimientos. Cada commit lleva un prefijo explicito:

- `test(reqN): RED` — se escriben los tests sin implementar la logica.
- `feat(reqN): GREEN` — implementacion minima para que los tests pasen.
- `refactor(...)` — mejoras de codigo manteniendo tests verdes.

Total: **17 commits** documentando la evolucion del trabajo (minimo exigido = 10).

### Reporte de cobertura

Salida de `uv run pytest --cov=src/registro_notas --cov-report=term-missing`:

```
======================= test session starts =========================
collected 26 items

tests/step_defs/test_notas_steps.py ...........            [ 42%]
tests/test_notas.py ...............                        [100%]

================================ tests coverage ================================
______________ coverage: platform darwin, python 3.12.13-final-0 _______________

Name                             Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------------
src/registro_notas/__init__.py       0      0      0      0   100%
src/registro_notas/notas.py         39      0      8      0   100%
----------------------------------------------------------------------------
TOTAL                               39      0      8      0   100%
============================== 26 passed in 0.08s ==============================
```

**Cobertura final: 100%** (umbral exigido por el enunciado: 85%, gate del CI: 80%).

---

## Parte 4 — BDD

El archivo [`tests/features/notas.feature`](tests/features/notas.feature) contiene los escenarios escritos en lenguaje de negocio. Cumple:

- Narrativa `Feature` con rol del usuario (registrador academico) y proposito.
- `Background` reutilizado en todos los escenarios.
- 6 escenarios entre los requerimientos 2, 3 y 4.
- 1 `Scenario Outline` con tabla `Examples` de 6 combinaciones para la decision de aprobacion.
- 2 escenarios de error con resultado esperado claro (`SinNotasError` y `NotaDuplicadaError`).
- Tags `@smoke`, `@critical`, `@regression` en cada escenario, registrados como markers en `pyproject.toml`.

Los step definitions estan en [`tests/step_defs/test_notas_steps.py`](tests/step_defs/test_notas_steps.py) y conectan cada paso del Gherkin con la misma API de produccion usada por los tests unitarios.

---

## Parte 5 — Pipeline CI/CD

El workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml) corre en cada push y PR a `main`:

1. Checkout
2. Instalacion de `uv` con cache
3. Python 3.12
4. `uv sync --frozen` (usa el lockfile)
5. `pytest` ejecutando tests unitarios y BDD juntos con cobertura
6. Falla si la cobertura baja del 80%
7. Sube `coverage.xml` como artifact

El pipeline esta en verde en [Actions del repositorio](https://github.com/Samuel-Tabares/registro-notas-academicas/actions).

---

## Parte 6 — Reflexion

**Diseñar los casos antes vs. programar directo.** Cuando arranque a escribir la tabla de casos en la Parte 2, me obligue a pensar en escenarios que probablemente habria pasado por alto si hubiera empezado por el codigo: el caso CP-15 (verificar que el estado no cambia tras un error de duplicado) salio justamente de la pregunta 2 al PO. Si hubiera escrito primero la implementacion, lo natural habria sido crear la `Nota` y *despues* validar si ya existia — lo cual habria contaminado el estado del estudiante con la excepcion del rango antes de detectar el duplicado. La tabla me sirvio como contrato mental: antes de programar ya sabia que necesitaba un orden de validaciones especifico y que ese orden era testeable.

**Lo mas dificil del TDD y la tentacion de saltarse pasos.** El paso REFACTOR fue donde mas senti la tentacion de saltar adelante. Despues del GREEN del Requerimiento 4 todo funcionaba y los 15 tests pasaban; mover codigo para consolidar `_existe_nota` y `_buscar_nota` en un solo helper se sintio como un riesgo innecesario. La disciplina de hacer ese commit aparte, con tests corriendo antes y despues, fue lo que dio el valor real: el diff del refactor quedo aislado y auditable, mientras que si lo hubiera mezclado con el GREEN nadie habria podido ver que la implementacion minima era distinta del codigo limpio final. Tambien me costo no implementar mas funciones de las que cada test pedia — por ejemplo, en el GREEN del Req2 tuve que resistir agregar `promedio()` y `registrar_nota` con validacion de duplicados porque "ya estaba ahi"; ceñirme a lo minimo y dejarlo para sus propios ciclos RED-GREEN despues hizo que cada commit cuente una sola historia.
