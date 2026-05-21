Feature: Registro de notas academicas
  Como registrador academico de la Universidad Regional del Sur
  Quiero registrar las notas de los estudiantes y consultar su rendimiento
  Para informar de forma confiable quien aprueba o reprueba cada materia
  y conocer el promedio academico de cada estudiante.

  Background:
    Given existe el estudiante "Ana Perez" sin notas registradas

  @smoke @critical
  Scenario: Un estudiante aprueba cuando obtiene la nota minima de aprobacion
    When registro la nota 3.0 en la materia "Algebra" del semestre "2026-1"
    Then el estudiante aprueba la materia "Algebra" del semestre "2026-1"

  @critical
  Scenario Outline: Decision de aprobacion segun la nota obtenida
    When registro la nota <nota> en la materia "Calculo" del semestre "2026-1"
    Then la decision de aprobacion para "Calculo" en "2026-1" es <decision>

    Examples:
      | nota | decision |
      | 1.5  | reprueba |
      | 2.9  | reprueba |
      | 3.0  | aprueba  |
      | 3.1  | aprueba  |
      | 4.5  | aprueba  |
      | 5.0  | aprueba  |

  @regression
  Scenario: Calcular el promedio del estudiante con varias notas
    When registro la nota 3.0 en la materia "Calculo" del semestre "2026-1"
    And registro la nota 4.0 en la materia "Algebra" del semestre "2026-1"
    And registro la nota 5.0 en la materia "Fisica" del semestre "2026-1"
    Then el promedio del estudiante es 4.0

  @regression @critical
  Scenario: Consultar el promedio cuando el estudiante no tiene notas falla con error claro
    When intento consultar el promedio del estudiante
    Then el sistema responde con el error "SinNotasError"

  @critical
  Scenario: No se permite registrar dos notas para la misma materia en el mismo semestre
    Given el estudiante ya tiene una nota de 4.0 en la materia "Calculo" del semestre "2026-1"
    When intento registrar la nota 3.5 en la materia "Calculo" del semestre "2026-1"
    Then el sistema responde con el error "NotaDuplicadaError"
    And el estudiante mantiene solo 1 nota registrada

  @regression
  Scenario: Si permite registrar la misma materia en un semestre distinto
    Given el estudiante ya tiene una nota de 3.0 en la materia "Calculo" del semestre "2026-1"
    When registro la nota 4.0 en la materia "Calculo" del semestre "2026-2"
    Then el estudiante tiene 2 notas registradas
