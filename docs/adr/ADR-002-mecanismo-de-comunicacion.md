# ADR-002: Mecanismo de comunicación principal

## Estado

Propuesto

## Fecha

2026-11-22

## Responsable

SANCHEZ VERA DARWIN JOEL (Arquitecto)

## Contexto

Según ADR-001, el SGAC se divide en servicios por capacidad. El diagrama de contenedores (C4 nivel 2) identifica 13 interacciones (I-01 a I-13) con dos necesidades distintas:

| Grupo | Interacciones | Necesidad |
| --- | --- | --- |
| Consultas y registros que el usuario espera ver resueltos | I-02 a I-07 | Respuesta inmediata. RF-03 registra el resultado de cada requisito con la fecha de consulta; RF-05 muestra el último estado registrado con un percentil 95 inferior a 300 ms para 50 usuarios simultáneos (RNF-01). |
| Avisos derivados de un cambio de estado | I-08 a I-13 | Entrega posterior sin bloquear a quien hizo el cambio (RF-05, RF-08, RF-11) y sin detener la recepción de postulaciones si notificaciones falla (RNF-03, RNF-11). |

El esqueleto de E1 implementa I-05: postulaciones (servicio B) consulta a elegibilidad (servicio A). Si el SGA no responde, la postulación debe quedar en «Validación pendiente» y revalidarse después (RNF-04). La aplicación web se ejecuta en Chrome, Firefox y Edge sin dependencias de pago (RNF-12).

### Mediciones de PE-U1

Las mediciones disponibles son las de la práctica PE-U1 del equipo CMSZ (Cedeño, Mendoza, Sánchez y Zambrano), en la que participó SANCHEZ VERA DARWIN JOEL. Los integrantes MUÑOZ VERA MELANIE MICHELLE y QUINTERO RICO LUIS DAVID no tienen mediciones de PE-U1 registradas en el repositorio.

Condiciones: sesión del 2026-11-22 01:16 UTC, una sola máquina (Windows 11, AMD Ryzen 7 7435HS, Python 3.14), interfaz local 127.0.0.1, respuesta eco, 5 corridas de 100 envíos por combinación (500 RTT cada una). Resultados recalculados a partir de los CSV de `data/protocolo/sesion_20261122T011620Z/` del repositorio de la práctica:

| Carga | Modo | RTT medio TCP (ms) | RTT medio gRPC (ms) | p95 gRPC (ms) | Rendimiento TCP (msg/s) | Rendimiento gRPC (msg/s) |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 100 B | Secuencial | 0,12 | 0,65 | 1,09 | 7960 | 826 |
| 100 B | Concurrente | 0,31 | 0,56 | 0,82 | 5809 | 2113 |
| 10 KiB | Secuencial | 0,21 | 0,79 | 1,80 | 4533 | 773 |
| 10 KiB | Concurrente | 0,57 | 0,91 | 2,09 | 3549 | 1565 |

Lectura para el SGAC: en la peor combinación, gRPC agregó 0,58 ms de RTT medio frente a TCP, y su p95 no superó 2,1 ms. Frente al umbral de 300 ms de RNF-01, el costo del protocolo no decide la elección. PE-U1 no midió REST ni mensajería; su latencia se medirá en el esqueleto.

Fuente: https://github.com/jcedenoi4/GA-SUM-02

## Opciones consideradas

### Opción A: REST sobre HTTP con JSON

- Ventajas: el navegador la consume sin intermediarios (RNF-12); el contrato es legible y se prueba con curl o Postman, lo que permite ejecutar los casos SA-01 a SA-11 tal como están escritos; códigos HTTP estándar para distinguir «no encontrado» (404) de «SGA no disponible» (503).
- Desventajas: sincrónica: quien llama debe fijar tiempo de espera y revalidación (RNF-04); JSON ocupa más que un formato binario; latencia no medida en PE-U1.

### Opción B: gRPC con Protocol Buffers

- Ventajas: contrato estricto en `.proto`; formato binario; medida en PE-U1 con p95 de 2,09 ms o menos.
- Desventajas: el navegador necesita un proxy gRPC-Web para usarla (I-02 a I-04); requiere generar código y herramientas específicas para probar; también es sincrónica.

### Opción C: mensajería asincrónica con intermediario (RabbitMQ)

- Ventajas: si el consumidor está caído, el mensaje espera en la cola (RNF-03, RNF-11); adecuada para avisos.
- Desventajas: no da respuesta inmediata a RF-03 y RF-05 sin montar petición y respuesta sobre colas; agrega un contenedor que desplegar y vigilar.

## Decisión tomada

1. **Mecanismo principal: REST sobre HTTP con JSON** para las interacciones sincrónicas I-02 a I-07. I-05 sigue el contrato `src/contrato/elegibilidad-v1.yaml`.
2. **Mensajería asincrónica con intermediario** para las interacciones I-08 a I-13. Se incorpora con notificaciones y seguimiento (E2 a E4); el esqueleto de E1 no la usa.

Se elige REST frente a gRPC porque I-02 a I-04 parten del navegador (RNF-12) y porque, según PE-U1, la diferencia de latencia entre protocolos es menor a 1 ms frente a un umbral de 300 ms (RNF-01). La mensajería no es el mecanismo principal porque RF-03 y RF-05 necesitan respuesta inmediata.

Para RNF-04, elegibilidad responde 503 si el SGA no contesta en 2 s. Postulaciones espera hasta 3 s; ante 503, error de conexión o tiempo agotado registra la postulación como «Enviada» con validación en «Validación pendiente» y repite la consulta cada 60 s hasta recibir 200 o 404.

Los servicios que publican eventos (I-08 a I-10) los guardan primero en su propia base de datos y los envían al intermediario después de confirmar la operación; si el intermediario no está disponible, el envío se repite y la operación original no se revierte.

## Consecuencias

- Positivas:
  - Un solo mecanismo para todas las consultas y para la aplicación web, verificable con herramientas comunes.
  - El contrato OpenAPI de I-05 es independiente del lenguaje: postulaciones está implementado en Python 3.12 con FastAPI y HTTPX, y elegibilidad puede implementarse con la tecnología que fije el Líder de Desarrollo.
  - Los avisos no bloquean la recepción de postulaciones y no se pierden si el intermediario falla.
- Negativas:
  - Postulaciones depende en línea de elegibilidad; la mitigan el tiempo de espera y la validación pendiente.
  - La latencia de REST debe medirse en el esqueleto para confirmar RNF-01.
  - El intermediario de mensajes y el registro de eventos pendientes agregan componentes a partir de E2.

## Requisitos relacionados

RF-03, RF-05, RF-08, RF-11; RNF-01, RNF-03, RNF-04, RNF-11, RNF-12.

## Referencias

1. Equipo CMSZ, «GA-SUM-02: comunicación entre procesos distribuidos con sockets TCP y gRPC (PE-U1)», repositorio GitHub, 2026. https://github.com/jcedenoi4/GA-SUM-02
2. Contrato de I-05: `src/contrato/elegibilidad-v1.yaml`.
