# Casos y datos de prueba del servicio A

Plan de pruebas de la interacción I-05 para RF-03, RNF-04 y RNF-10. La referencia es el [contrato OpenAPI de elegibilidad](../contrato/elegibilidad-v1.yaml), versión `1.0.0-propuesto`. La implementación y la ejecución quedan pendientes de la aprobación del [ADR-002](../../docs/adr/ADR-002-mecanismo-de-comunicacion.md).

## Operaciones y comprobaciones comunes

- Base local propuesta `http://localhost:8081/api/v1`.
- Salud: `GET /salud` (operación `consultarSalud`).
- Elegibilidad: `GET /estudiantes/{estudianteId}/elegibilidad?asignatura=ASIG-01` (operación `consultarElegibilidad`). `estudianteId` va en la ruta y `asignatura` es obligatoria en la consulta, salvo en el caso que comprueba su ausencia.
- En cada respuesta `200` de elegibilidad, comprobar el cuerpo JSON contra `ResultadoElegibilidad`: identificadores solicitados, `fechaConsulta` válida en UTC según ISO 8601, `estadoGeneral`, y los resultados y valores de `requisitos.matricula`, `requisitos.nota` y `requisitos.promedio`. En `nota.minimo` verificar `8.00` y en `promedio.promedioCarrera` el promedio del periodo anterior.
- En los errores de elegibilidad, verificar el esquema `Error`: `codigo` esperado, `mensaje` de texto y `fechaConsulta` en UTC. Los escenarios de error se distinguen por el código HTTP y `codigo`.

## Datos sintéticos del SGA

Usar la asignatura ficticia `ASIG-01`. Los valores numéricos se expresan con dos decimales en los datos de prueba. Comparar el valor después de leer el JSON como número, ya que `8.00` y `8` son el mismo valor numérico.

| Registro | Matrícula | Nota | Promedio del estudiante | Promedio de la carrera | Resultado de matrícula | Resultado de nota | Resultado de promedio | Estado general |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EST-001 | `REGULAR` | 9.25 | 8.70 | 8.20 | `CUMPLE` | `CUMPLE` | `CUMPLE` | `ELEGIBLE` |
| EST-002 | `REGULAR` | 8.00 | 8.01 | 8.00 | `CUMPLE` | `CUMPLE` | `CUMPLE` | `ELEGIBLE` |
| EST-003 | `REGULAR` | 7.99 | 8.70 | 8.20 | `CUMPLE` | `NO_CUMPLE` | `CUMPLE` | `NO_ELEGIBLE` |
| EST-004 | `REGULAR` | 9.25 | 8.20 | 8.20 | `CUMPLE` | `CUMPLE` | `NO_CUMPLE` | `NO_ELEGIBLE` |
| EST-005 | `REGULAR` | 9.25 | 8.19 | 8.20 | `CUMPLE` | `CUMPLE` | `NO_CUMPLE` | `NO_ELEGIBLE` |
| EST-006 | `NO_REGULAR` | 9.25 | 8.70 | 8.20 | `NO_CUMPLE` | `CUMPLE` | `CUMPLE` | `NO_ELEGIBLE` |
| EST-007 | `NO_REGULAR` | 7.99 | 8.20 | 8.20 | `NO_CUMPLE` | `NO_CUMPLE` | `NO_CUMPLE` | `NO_ELEGIBLE` |
| EST-008 | `REGULAR` | `null` | 8.70 | 8.20 | `CUMPLE` | `DATO_FALTANTE` | `CUMPLE` | `INCOMPLETO` |
| EST-009 | `NO_REGULAR` | `null` | 8.70 | 8.20 | `NO_CUMPLE` | `DATO_FALTANTE` | `CUMPLE` | `NO_ELEGIBLE` |

## Casos de prueba

Para SA-01 a SA-09 y SA-14 se usa la operación de elegibilidad con la asignatura `ASIG-01`. En los casos `200` se comprueba la respuesta completa contra la fila correspondiente de los datos sintéticos.

| Caso | Preparación y acción | Resultado esperado |
| --- | --- | --- |
| SA-01 · Datos completos | Consultar `EST-001`. | `200 ELEGIBLE`. Los tres requisitos tienen resultado `CUMPLE`. |
| SA-02 · Nota igual al mínimo | Consultar `EST-002`. | `200 ELEGIBLE`. La nota 8.00 cumple el mínimo inclusivo y el promedio 8.01 supera 8.00. |
| SA-03 · Nota inferior al mínimo | Consultar `EST-003`. | `200 NO_ELEGIBLE`. Solo la nota tiene resultado `NO_CUMPLE`. |
| SA-04 · Promedios iguales | Consultar `EST-004`. | `200 NO_ELEGIBLE`. Un promedio igual al de la carrera tiene resultado `NO_CUMPLE`. |
| SA-05 · Promedio inferior | Consultar `EST-005`. | `200 NO_ELEGIBLE`. Solo el promedio tiene resultado `NO_CUMPLE`. |
| SA-06 · Matrícula no regular | Consultar `EST-006`. | `200 NO_ELEGIBLE`. La matrícula tiene valor `NO_REGULAR` y resultado `NO_CUMPLE`. |
| SA-07 · Varios incumplimientos | Consultar `EST-007`. | `200 NO_ELEGIBLE`. Los tres requisitos tienen resultado `NO_CUMPLE`. |
| SA-08 · Dato faltante | Consultar `EST-008`, cuyo registro carece de nota. | `200 INCOMPLETO`. La nota tiene valor `null` y resultado `DATO_FALTANTE`. |
| SA-09 · Estudiante sin registro | Consultar `EST-999` con el SGA simulado disponible y sin cargar ese estudiante. | `404` con código `ESTUDIANTE_NO_ENCONTRADO`. |
| SA-10 · SGA indisponible y recuperación | Consultar `EST-001` con una demora del SGA mayor a 2 s. Repetir con conexión rechazada. Restaurar el simulador y volver a consultar. | Ambas fallas devuelven `503` con código `SGA_NO_DISPONIBLE`. En la demora se activa el límite de 2 s de elegibilidad. Si aparece `Retry-After`, verificar que expresa segundos enteros. Tras la recuperación se obtiene el `200 ELEGIBLE` de SA-01. |
| SA-11 · Solo lectura | Registrar las operaciones del SGA simulado antes de ejecutar SA-01 y SA-09. Comparar su estado antes y después. | Se observan las consultas esperadas, **0 escrituras** y los registros del simulador quedan intactos. |
| SA-12 · Salud | Con el servicio A en ejecución, llamar a `GET /salud`. | `200` con cuerpo JSON `{"estado":"OK"}`. |
| SA-13 · Asignatura ausente | Llamar a `GET /estudiantes/EST-001/elegibilidad` sin el parámetro `asignatura`. | `400` con código `PARAMETRO_INVALIDO`. El contrato también prevé `400` para un formato inválido. Queda por concretar ese caso porque el parámetro se define como cadena sin un patrón. |
| SA-14 · Incumplimiento con un dato faltante | Consultar `EST-009`. | `200 NO_ELEGIBLE`. El incumplimiento de matrícula prevalece sobre la nota faltante. |

## Integración con postulaciones y evidencia

- Demostración inicial: ejecutar SA-01 y SA-03 desde postulaciones y verificar que B recibe los resultados del servicio A. Usar la [matriz de RNF](matriz-pruebas-rnf.md) para vincular SA-10 con RNF-04 y SA-11 con RNF-10.
- RNF-04: en la prueba entre ambos servicios, verificar que B espera hasta 3 s. Ante `503`, conexión rechazada o tiempo agotado, B conserva la postulación en «Validación pendiente» y reintenta cada 60 s. Comprobar por separado que un `200` tras recuperarse el SGA y un `404` tras una nueva consulta detienen el reintento.
- Por cada ejecución, guardar caso, versión del contrato, solicitud, estado HTTP, respuesta, tiempo medido cuando corresponda y resultado observado. La evidencia de ejecución se registrará cuando estén implementados los servicios.
