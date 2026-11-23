# ADR-001: Estilo de arquitectura

## Estado

Propuesto

## Fecha

2026-11-21

## Responsable

SANCHEZ VERA DARWIN JOEL (Arquitecto)

## Contexto

El SGAC gestiona las ayudantías de cátedra de la UTEQ: convocatoria, postulación, evaluación por méritos y oposición, ejecución, seguimiento y certificación. Lo usan seis roles y depende de cuatro sistemas externos: el SGA, la mensajería institucional, un servicio de IA y la firma electrónica.

Las condiciones que influyen en el estilo de arquitectura son:

1. **Carga concentrada.** La inscripción dura 5 días calendario y el pico se produce el último día. El sistema debe admitir 350 postulaciones válidas por convocatoria y atender 100 usuarios simultáneos en ese pico (RNF-02). El resto del semestre la carga proviene del seguimiento y los informes.
2. **Disponibilidad en la inscripción.** La recepción de postulaciones debe estar disponible al menos el 99 % del tiempo durante los 5 días de inscripción (RNF-03).
3. **Dependencia del SGA.** La elegibilidad se valida en el SGA, que es externo y puede no responder. Las postulaciones recibidas durante una falla deben quedar en «Validación pendiente» (RNF-04), y el SGAC no realiza escrituras en el SGA (RNF-10).
4. **Cambio independiente.** Notificaciones, evaluación y seguimiento cambian por motivos distintos; actualizar un servicio no debe obligar a redesplegar otro (RNF-11).
5. **Alcance del periodo.** El equipo no tiene acceso al SGA real ni a la firma electrónica institucional. El SGA se representa con un servicio simulado de solo lectura; la IA y la firma electrónica quedan fuera de las entregas E1 a E4.

## Opciones consideradas

### Opción A: monolito

Una aplicación y una base de datos con todos los módulos.

- Ventajas: despliegue, pruebas y depuración más simples; sin latencia ni fallos de red internos.
- Desventajas: para atender el pico de inscripción se escala toda la aplicación (RNF-02); un fallo o un despliegue afecta a todos los módulos (RNF-03, RNF-11).

### Opción B: monolito modular

Una unidad desplegable dividida en módulos con límites claros: postulación, evaluación, ejecución, cierre y administración.

- Ventajas: organiza el código por dominio y conserva la simplicidad operativa del monolito.
- Desventajas: los módulos se despliegan y escalan juntos, por lo que no atiende RNF-02 ni RNF-11.

### Opción C: microservicios de grano fino

Un servicio por entidad u operación (convocatorias, documentos, méritos, oposición, ranking, sesiones, informes, certificados), cada uno con su base de datos.

- Ventajas: máxima independencia de despliegue y escalado.
- Desventajas: el número de servicios, contratos y bases de datos es difícil de operar y probar para un equipo de tres personas. La complejidad es el principal problema de diseño, monitoreo y pruebas de estos sistemas [2], y distribuir no mejora el desempeño por sí solo [1].

### Opción D: servicios por capacidad de negocio

Pocos servicios, uno por capacidad con carga o ritmo de cambio propio, cada uno dueño de sus datos:

| Servicio | Responsabilidad | Motivo de la separación |
| --- | --- | --- |
| Postulaciones | Convocatorias, postulaciones, revisión de documentos y estados (RF-01, RF-02, RF-04, RF-05) | Recibe el pico de inscripción (RNF-02, RNF-03) |
| Elegibilidad | Consulta de solo lectura al SGA (RF-03) | Aísla la dependencia externa (RNF-04, RNF-10) |
| Evaluación | Méritos, oposición, consolidación y resultados (RF-06 a RF-08) | Datos de selección; uso puntual por la comisión y la coordinación |
| Seguimiento | Sesiones, planificación semanal, informes y certificado (RF-09 a RF-12) | Carga durante el semestre y ritmo de cambio distinto |
| Notificaciones | Avisos de cambios de estado y resultados | Su retraso o falla no debe bloquear el resto (RNF-11) |

- Ventajas: cada servicio se escala y despliega por separado donde los requisitos lo piden; la falla del SGA queda contenida en elegibilidad; el número de piezas es manejable.
- Desventajas: comunicación por red, contratos que mantener, datos repartidos que exigen decidir su consistencia y más trabajo de despliegue y monitoreo.

## Decisión tomada

Se propone la opción D. El esqueleto de E1 implementa dos servicios: postulaciones, que consulta a elegibilidad (servicio A, con el SGA simulado). Evaluación, seguimiento y notificaciones se incorporan en E2 a E4. Dentro de cada servicio se aplica la organización modular de la opción B, con los principios de modularidad y ocultamiento de información que la literatura asocia al diseño de microservicios [3].

| Requisito | Cómo lo atiende la opción D | Por qué no basta la opción B |
| --- | --- | --- |
| RNF-02 | Solo se escala postulaciones durante la inscripción | Se escala toda la aplicación |
| RNF-03 | Un fallo en evaluación o seguimiento no detiene la recepción de postulaciones | Un fallo del proceso único detiene todo |
| RNF-04 | Si elegibilidad no obtiene respuesta del SGA, postulaciones conserva la postulación en «Validación pendiente» hasta su revalidación | La dependencia queda dentro del mismo proceso |
| RNF-10 | Elegibilidad es el único punto de contacto con el SGA y solo realiza lecturas | El límite es menos visible |
| RNF-11 | Cada servicio tiene su propio despliegue | No hay despliegue independiente |

La opción C se descarta por su costo operativo para el tamaño del equipo.

## Consecuencias

- Positivas:
  - Capacidad, disponibilidad, tolerancia a fallos e independencia de despliegue tienen un mecanismo concreto en la arquitectura.
  - La dependencia del SGA queda aislada y puede probarse interrumpiendo el SGA simulado.
- Negativas:
  - Aparecen fallos parciales y latencia entre servicios; cada llamada necesita tiempo de espera y manejo de errores.
  - Los datos quedan repartidos y hay que decidir, por dato, si se prioriza consistencia o disponibilidad.
  - Aumenta el trabajo de despliegue, configuración y pruebas de integración.
  - Los límites entre servicios pueden requerir ajustes al cerrar E2.

## Requisitos relacionados

RF-01 a RF-12; RNF-02, RNF-03, RNF-04, RNF-10, RNF-11.

## Referencias

1. G. Blinowski, A. Ojdowska y A. Przybyłek, «Monolithic vs. Microservice Architecture: A Performance and Scalability Evaluation», *IEEE Access*, vol. 10, pp. 20357–20374, 2022, doi: 10.1109/ACCESS.2022.3152803.
2. M. Waseem, P. Liang, M. Shahin, A. Di Salle y G. Márquez, «Design, monitoring, and testing of microservices systems: The practitioners' perspective», *Journal of Systems and Software*, vol. 182, art. 111061, 2021, doi: 10.1016/j.jss.2021.111061.
3. V. Velepucha y P. Flores, «A Survey on Microservices Architecture: Principles, Patterns and Migration Challenges», *IEEE Access*, vol. 11, pp. 88339–88358, 2023, doi: 10.1109/ACCESS.2023.3305687.
