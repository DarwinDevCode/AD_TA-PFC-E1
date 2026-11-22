# ADR-002: Mecanismo de comunicación principal entre servicios

- **Estado:** Pendiente de decisión
- **Fecha:** 2026-11-21
- **Requisitos relacionados:** RF-03, RF-05; RNF-01, RNF-02, RNF-04, RNF-11

## Contexto

Según ADR-001, el SGAC se divide en servicios por capacidad. En el esqueleto de E1, el servicio de postulaciones consulta al servicio de elegibilidad si el estudiante cumple los requisitos académicos registrados en el SGA (RF-03).

Las interacciones previstas tienen necesidades distintas:

| Interacción | Requiere respuesta inmediata | Condición |
| --- | --- | --- |
| Postulaciones consulta elegibilidad (RF-03) | Sí | Si elegibilidad no responde, la postulación se guarda igual (RNF-04) |
| Consulta del estado de la postulación (RF-05) | Sí | Tiempo de respuesta fijado en RNF-01 |
| Aviso de cambio de estado a notificaciones | No | Puede entregarse después sin afectar a quien hizo el cambio |

## Opciones consideradas

### A. REST sobre HTTP con JSON

- A favor: soporte en todos los lenguajes; se prueba con navegador, curl o Postman; contrato legible; se ajusta a consultas de solicitud y respuesta como RF-03 y RF-05.
- En contra: sincrónico; quien llama debe manejar tiempo de espera y reintentos (RNF-04); JSON ocupa más que un formato binario.

### B. gRPC con Protocol Buffers

- A favor: contrato estricto en un archivo `.proto`; formato binario compacto; admite flujos.
- En contra: también sincrónico; requiere generar código y herramientas específicas para probarlo.

### C. Mensajería asincrónica con intermediario (RabbitMQ)

- A favor: si el consumidor está caído, el mensaje espera en la cola (RNF-04, RNF-11); adecuada para notificaciones.
- En contra: no entrega una respuesta inmediata para RF-03 y RF-05 sin montar petición y respuesta sobre colas; añade un componente que desplegar y vigilar.

## Criterios de decisión

| Criterio | Requisito |
| --- | --- |
| Respuesta inmediata en la interacción del esqueleto | RF-03, RF-05, RNF-01 |
| Comportamiento si el otro servicio no responde | RNF-04 |
| Independencia entre servicios | RNF-11 |
| Desempeño medido por el equipo en PE-U1 | RNF-01, RNF-02 |

## Decisión

Pendiente. Se toma en la sesión de diseño 2, con ADR-001 ratificado y las mediciones de PE-U1.

## Consecuencias

Pendientes de la decisión.
