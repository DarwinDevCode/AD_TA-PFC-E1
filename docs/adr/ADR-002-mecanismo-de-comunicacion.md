# ADR-002: Mecanismo de comunicación principal

## Estado

Propuesto

## Fecha

2026-11-21

## Responsable

SANCHEZ VERA DARWIN JOEL (Arquitecto)

## Contexto

Según ADR-001, el SGAC se divide en servicios por capacidad. En el esqueleto de E1, postulaciones consulta a elegibilidad si el estudiante cumple los requisitos académicos registrados en el SGA (RF-03): matrícula regular, nota de la asignatura y promedio.

Las interacciones previstas tienen necesidades distintas:

| Interacción | Requiere respuesta inmediata | Condición |
| --- | --- | --- |
| Postulaciones consulta a elegibilidad (RF-03) | Sí | Si el SGA no responde, la postulación queda en «Validación pendiente» (RNF-04) |
| El estudiante consulta el estado de su postulación (RF-05) | Sí | Percentil 95 inferior a 300 ms con 50 usuarios simultáneos (RNF-01) |
| Postulaciones avisa a notificaciones un cambio de estado (RF-05) | No | Puede entregarse después sin afectar a quien hizo el cambio |

## Opciones consideradas

### Opción A: REST sobre HTTP con JSON

- Ventajas: soporte en todos los lenguajes; se prueba con navegador, curl o Postman; contrato legible; se ajusta a consultas de solicitud y respuesta como RF-03 y RF-05.
- Desventajas: sincrónico; quien llama debe manejar el tiempo de espera y la revalidación (RNF-04); JSON ocupa más que un formato binario.

### Opción B: gRPC con Protocol Buffers

- Ventajas: contrato estricto en un archivo `.proto`; formato binario compacto; admite flujos.
- Desventajas: también sincrónico; requiere generar código y herramientas específicas para probarlo.

### Opción C: mensajería asincrónica con intermediario (RabbitMQ)

- Ventajas: si el consumidor está caído, el mensaje espera en la cola (RNF-04, RNF-11); adecuada para notificaciones.
- Desventajas: no entrega una respuesta inmediata para RF-03 y RF-05 sin montar petición y respuesta sobre colas; añade un componente que desplegar y vigilar.

### Criterios de comparación

| Criterio | Requisito |
| --- | --- |
| Respuesta inmediata en la consulta de elegibilidad y de estado | RF-03, RF-05, RNF-01 |
| Comportamiento si el SGA o elegibilidad no responden | RNF-04 |
| Actualización de un servicio sin redesplegar otro | RNF-11 |
| Desempeño medido por el equipo en PE-U1 | RNF-01, RNF-02 |

## Decisión tomada

Pendiente. Se decide con ADR-001 aceptado y las mediciones de PE-U1.

## Consecuencias

Pendientes de la decisión.

## Requisitos relacionados

RF-03, RF-05; RNF-01, RNF-02, RNF-04, RNF-11.

## Referencias

Pendientes de la decisión.
