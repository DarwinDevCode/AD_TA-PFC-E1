
# Acta de entrevista — Levantamiento de requisitos

**Proyecto:** TA-PFC-E1 — Sistema de Gestión de Ayudantías de Cátedra (SGAC)  
**Fecha de entrevista:** 21-11-2026  
**Fecha de revisión del documento:** 22-11-2026  
**Medio:** Discord  
**Entrevistado:** KHRIZ ALEXANDER CORONEL GOMEZ  
**Cargo:** Ayudante de Cátedra  
**Participantes:** MUÑOZ VERA MELANIE MICHELLE y SANCHEZ VERA DARWIN JOEL  
**Responsable de documentación:** QUINTERO RICO LUIS DAVID

## 1. Objetivo

Recopilar información sobre el proceso de postulación y gestión de ayudantías de cátedra, sus dificultades y las necesidades que deben considerarse para el SGAC.

## 2. Síntesis de temas y necesidades

Los identificadores se relacionan con el guion de entrevista. Se presenta una síntesis temática para el análisis de requisitos, no una transcripción literal.

### P10. Volumen de postulaciones

Para dimensionar la plataforma se requiere conocer el número de postulaciones por convocatoria. El equipo considera **350 postulaciones** como escenario inicial de diseño, aún sin respaldo estadístico institucional.

### P12. Usuarios simultáneos

La demanda podría concentrarse cerca del cierre de postulaciones y de la publicación de resultados. Se plantean escenarios de prueba de **50 usuarios simultáneos** en consultas y **100 usuarios** en momentos de mayor actividad.

### P13. Tiempos de respuesta

La consulta del estado de postulación debe ser ágil. Se plantea como objetivo técnico inicial un **tiempo de respuesta p95 inferior a 300 ms**, bajo una carga de 50 usuarios simultáneos.

### P14. Disponibilidad

La disponibilidad es especialmente importante durante el período de inscripción. Se propone inicialmente un objetivo del **99 % durante cinco días de recepción de postulaciones**.

### P15. Consulta de información académica

Se contempla consultar en el SGA la matrícula, las calificaciones y el promedio del postulante para verificar su elegibilidad, mediante una integración de solo lectura. Su viabilidad requiere revisión técnica.

### P16. Fallos del SGA

Cuando el SGA no esté disponible, la comprobación automática de los requisitos académicos no podrá concluirse de inmediato. El procedimiento institucional de contingencia aún debe precisarse.

### P17. Manejo de postulaciones durante fallos del SGA

Se propone conservar las solicitudes válidas con el estado **«Validación pendiente»** y reintentar la consulta al restablecerse el SGA, evitando duplicaciones o nuevas postulaciones innecesarias.

### P21. Respaldos y recuperación

Para proteger los expedientes y las evidencias de ayudantía se proponen inicialmente **respaldos cada 24 horas** y **recuperación en un máximo de cuatro horas**, sujetos a evaluación técnica.

## 3. Relación con los requisitos no funcionales

| RNF | Referencia | Criterio técnico inicial |
| --- | --- | --- |
| RNF-01 | P12, P13 | 50 usuarios simultáneos; p95 inferior a 300 ms. |
| RNF-02 | P10, P12 | 350 postulaciones por convocatoria; pico de 100 usuarios. |
| RNF-03 | P14 | 99 % de disponibilidad durante cinco días de inscripción. |
| RNF-04 | P16, P17 | Conservar postulaciones en «Validación pendiente» y reintentar la verificación. |
| RNF-05 | P21 | Respaldo cada 24 horas y recuperación en un máximo de cuatro horas. |

## 4. Observaciones

Los valores de capacidad, rendimiento, disponibilidad y recuperación son **estimaciones y metas propuestas por el equipo**, no mediciones institucionales ni declaraciones textuales atribuidas al entrevistado.

Su adopción como requisitos definitivos requiere contraste con las respuestas de la entrevista y validación de los responsables académicos y técnicos.

**Revisión documental:** 22-11-2026.

## 5. Firma del entrevistado



________________________________________

**KHRIZ ALEXANDER CORONEL GOMEZ**

Firma del entrevistado
