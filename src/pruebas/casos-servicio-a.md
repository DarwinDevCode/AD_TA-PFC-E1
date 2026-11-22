# Casos y datos de prueba del servicio A

Borrador para el servicio de elegibilidad propuesto en [ADR-001](../../docs/adr/ADR-001-estilo-de-arquitectura.md). Cubre la consulta académica de RF-03 y aporta escenarios a la [matriz de pruebas](matriz-pruebas-rnf.md) para RNF-04 y RNF-10. Los casos describen observaciones de negocio y de integración. Su representación se definirá con [ADR-002](../../docs/adr/ADR-002-mecanismo-de-comunicacion.md) y el contrato de interfaz.

## Datos sintéticos

Usar la asignatura ficticia `ASIG-01`. Los promedios de carrera representan el periodo anterior en los registros simulados. Cada fila es un escenario independiente del SGA simulado.

El borrador de RF-03 propone matrícula regular, nota de la asignatura de al menos 8 y promedio del estudiante estrictamente superior al de su carrera en el periodo anterior. Estos criterios quedan sujetos a la validación del equipo. Los decimales sirven para ejercitar los límites de la comparación y se adaptarán a la precisión del contrato.

| Registro | Matrícula | Nota de la asignatura | Promedio del estudiante | Promedio de la carrera | Matrícula esperada | Nota esperada | Promedio esperado |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EST-001 | Regular | 9.25 | 8.70 | 8.20 | Cumple | Cumple | Cumple |
| EST-002 | Regular | 8.00 | 8.01 | 8.00 | Cumple | Cumple | Cumple |
| EST-003 | Regular | 7.99 | 8.70 | 8.20 | Cumple | No cumple | Cumple |
| EST-004 | Regular | 9.25 | 8.20 | 8.20 | Cumple | Cumple | No cumple |
| EST-005 | Regular | 9.25 | 8.19 | 8.20 | Cumple | Cumple | No cumple |
| EST-006 | No regular | 9.25 | 8.70 | 8.20 | No cumple | Cumple | Cumple |
| EST-007 | No regular | 7.99 | 8.20 | 8.20 | No cumple | No cumple | No cumple |
| EST-008 | Regular | Sin dato | 8.70 | 8.20 | Cumple | Dato faltante | Cumple |

## Casos de prueba

| Caso | Preparación y acción | Resultado esperado |
| --- | --- | --- |
| SA-01 · Consulta con datos completos | Cargar `EST-001` y solicitar su verificación. | Se obtienen tres resultados «Cumple» para el estudiante y la asignatura consultados. |
| SA-02 · Nota igual al mínimo | Consultar `EST-002`, con nota 8.00 y promedio del estudiante apenas superior al de la carrera. | La nota cumple el mínimo inclusivo y el promedio cumple la comparación estricta. |
| SA-03 · Nota inferior al mínimo | Consultar `EST-003`, con nota 7.99. | La nota queda como «No cumple». Matrícula y promedio siguen como «Cumple». |
| SA-04 · Promedios iguales | Consultar `EST-004`. | El promedio queda como «No cumple» porque los promedios son iguales. |
| SA-05 · Promedio inferior | Consultar `EST-005`. | El promedio queda como «No cumple». Matrícula y nota siguen como «Cumple». |
| SA-06 · Matrícula no regular | Consultar `EST-006`. | La matrícula queda como «No cumple». Nota y promedio siguen como «Cumple». |
| SA-07 · Varios requisitos incumplidos | Consultar `EST-007`. | Se pueden comprobar los tres incumplimientos en el resultado previsto por el contrato. |
| SA-08 · Dato académico incompleto | Consultar `EST-008`, cuyo registro carece de la nota de la asignatura. | Comprobar que la nota ausente queda identificada como dato faltante. El tratamiento y su representación se confirmarán con el contrato. |
| SA-09 · Estudiante sin registro | Consultar `EST-999` sin cargarlo en el SGA simulado. | Distinguir la ausencia de registro de un incumplimiento calculado a partir de datos académicos. La respuesta concreta queda pendiente del contrato. |
| SA-10 · SGA simulado indisponible y recuperado | Interrumpir el simulador, intentar consultar `EST-001`, restablecer el simulador y volver a validar. | Distinguir la indisponibilidad de una decisión académica. Al recuperar el acceso se puede volver a validar y obtener el resultado de SA-01. El responsable del reintento y su política quedan pendientes del contrato. |
| SA-11 · Lectura sin mutaciones | Capturar el estado y el registro de operaciones del SGA simulado. Ejecutar una consulta satisfactoria y una consulta sin registro. Comparar con el estado inicial. | Se observan las consultas previstas y **0 operaciones de escritura**. Los registros académicos del simulador quedan intactos (RNF-10). |

## Integración y evidencia

- Para la primera prueba entre servicios, usar SA-01 como consulta base y SA-03 como variante de incumplimiento si el contrato incluye ambos resultados.
- Comprobar la fecha de consulta donde RF-03 la haga observable una vez definido el contrato. En la prueba del flujo completo de RNF-04, comprobar en **postulaciones** que el envío queda en «Validación pendiente» y se conserva hasta su revalidación.
- Al publicar el contrato, vincular cada caso con la operación, los campos y las respuestas definitivas. Registrar por ejecución el caso, los datos usados, el resultado observado y la evidencia. Estos casos todavía están pendientes de ejecución.
