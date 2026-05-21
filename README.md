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

## Contenido pendiente

- [ ] Parte 1: Analisis (particiones, limites, preguntas al PO)
- [ ] Parte 2: Tabla de casos de prueba
- [ ] Parte 3: Implementacion TDD
- [ ] Parte 4: BDD Gherkin
- [ ] Parte 5: Pipeline CI/CD
- [ ] Parte 6: Reflexion
